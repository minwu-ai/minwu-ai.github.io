"""
pipeline.py — surfaces AI topics, researches them, and drafts articles as markdown.

It uses the Claude API to (1) discover topics and (2) write articles with web search.
Every article is saved into posts/ as a DRAFT (published: false) so you review it
before it goes live. It works two ways:

  SCHEDULED (auto-discover trending topics and draft a few):
      python pipeline.py
      python pipeline.py --count 3

  ON DEMAND (you found something and want a draft about it):
      python pipeline.py --topic "OpenAI's new agent framework" --type analysis
      python pipeline.py --url "https://example.com/some-article"
      python pipeline.py --from-file notes.txt
      python pipeline.py --interactive          # paste/describe it at the prompt

Requires ANTHROPIC_API_KEY in the environment.
"""

import os
import sys
import glob
import json
import argparse
import datetime
import re

import anthropic

_client = None


def get_client():
    """Lazily create the Anthropic client (reads ANTHROPIC_API_KEY from the env)."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


MODEL = "claude-sonnet-4-6"
POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")

# Topics the scheduled run should prioritize when surfacing the day's news.
# Edit this list freely. Override for a single run with --focus "a, b, c".
FOCUS_TOPICS = [
    "AI safety and alignment",
    "model risk management and AI governance (SR 11-7 / SR 26-2)",
    "agentic AI and autonomous systems",
    "AI regulation and policy",
    "enterprise AI adoption and risk",
    "notable frontier model releases",
]

WEB_SEARCH = {"type": "web_search_20250305", "name": "web_search"}

# Credible, top-tier sources to PRIORITIZE when researching and citing.
# Search still covers the whole web — these are simply preferred and cited where
# available. Edit this list freely.
# Priority research sources (name, URL), in order of trust. The pipeline checks and
# cites these first; it may still use other reputable sources. Edit freely.
PREFERRED_SOURCES = [
    ("Anthropic Research", "https://www.anthropic.com/research"),
    ("OpenAI Research", "https://openai.com/research"),
    ("Google DeepMind Blog", "https://deepmind.google/discover/blog/"),
    ("METR (Model Evaluation & Threat Research)", "https://metr.org/blog/"),
    ("Apollo Research", "https://www.apolloresearch.ai/research"),
    ("UK AI Security Institute", "https://www.aisi.gov.uk/research"),
    ("US AI Safety Institute (NIST)", "https://www.nist.gov/aisi"),
    ("Transformer Circuits", "https://transformer-circuits.pub/"),
    ("Neel Nanda's blog", "https://www.neelnanda.io/"),
    ("Centre for the Governance of AI (GovAI)", "https://www.governance.ai/research"),
    ("Center for AI Safety (CAIS)", "https://www.safe.ai/research"),
    ("RAND Technology & Security Policy Center", "https://www.rand.org/tspc.html"),
    ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("OECD AI Policy Observatory", "https://oecd.ai/en/"),
    ("European AI Office", "https://digital-strategy.ec.europa.eu/en/policies/european-ai-office"),
    ("Bank for International Settlements (BIS) — FinTech & AI", "https://www.bis.org/topic/fintech.htm"),
    ("Alignment Forum", "https://www.alignmentforum.org/"),
    ("LessWrong — AI Alignment", "https://www.lesswrong.com/tag/ai-alignment"),
    ("arXiv — AI safety", "https://arxiv.org/search/?query=AI+safety&searchtype=all"),
    ("arXiv — AI alignment", "https://arxiv.org/search/?query=AI+alignment&searchtype=all"),
    ("The Wall Street Journal", "https://www.wsj.com/"),
]


def _sources_preference():
    src = "; ".join("{} ({})".format(n, u) for n, u in PREFERRED_SOURCES)
    return (
        "SEARCH THE OPEN WEB BROADLY AND INDEPENDENTLY — you are NOT restricted to any "
        "fixed list. The following is a RECOMMENDED set of trusted, high-signal sources "
        "to keep in mind, not a limit. Workflow: discover what's genuinely notable from "
        "across the web; then, for anything you find circulating, CHECK whether these "
        "trusted sources cover it and report what they say (or note their silence / a "
        "differing take). Prefer and cite these when they're relevant, and always link "
        "the primary source for a factual claim. Recommended sources (rough priority): "
        + src + "."
    )


# Corroboration bar — what counts as trustworthy enough to write about.
CORROBORATION_RULE = (
    "CORROBORATION BAR (required): treat a development as established fact ONLY if "
    "EITHER (a) it is reported by at least ONE source on the priority list above, OR "
    "(b) it is independently reported by at least TWO credible sources OUTSIDE the "
    "priority list. If a story clears NEITHER bar, do not build a post around it — omit "
    "it, or clearly label the specific unconfirmed claims as unverified/rumored. Never "
    "present an uncorroborated story as established fact."
)

# ---- Draft length & formatting (edit these to taste) ----
MAX_WORDS = 700   # hard cap; the model targets ~500-600

FORMAT_GUIDE = (
    f"LENGTH (STRICT): target 500-600 words; absolute maximum {MAX_WORDS}. Brevity is a "
    "feature — count the words and trim before finishing; never exceed the maximum. "
    "Open with the single most important point in the first two sentences.\n"
    "STRUCTURE for skimmability: use ## section headings, short paragraphs "
    "(2-4 sentences), and bullet lists where they help. Use a blockquote (>) for a "
    "key quote or takeaway, and a small markdown table when comparing things. Do NOT "
    "include an H1 (the title is rendered separately).\n"
    "EMOJI: you MAY use one tasteful emoji as a signpost at the start of a section "
    "heading (at most one per heading); never mid-sentence, and omit emoji entirely "
    "if the topic is serious (incidents, harm, regulation enforcement).\n"
    "VISUALS: do NOT embed external images (link rot / licensing); rely on text "
    "formatting for visual structure. The author may add images during review.\n"
    "CITATIONS (required): support every factual claim with an inline markdown link "
    "to its primary source, and end the piece with a '## Sources' section listing the "
    "key references as markdown links (title + URL). Cite ONLY real URLs you actually "
    "retrieved via web search — never invent or guess a link. If you could not verify "
    "a claim with a real source, soften it or leave it out rather than fabricate a "
    "citation. The Sources section does not count toward the word limit."
)

# What makes a post worth publishing — analysis, not summary.
ANALYSIS_GUIDE = (
    "INSIGHT IS THE POINT — do NOT just restate what a source reported. A summary is a "
    "failure. Every post must add genuine analytical value by doing several of these:\n"
    "- CROSS-REFERENCE: pull from multiple sources on the same event and surface where "
    "they AGREE vs. DISAGREE, or where they frame it differently.\n"
    "- HISTORICAL PARALLEL: compare the development to a relevant past event/precedent "
    "and draw the lesson it suggests.\n"
    "- PREDICTION: offer a clearly-labeled, reasoned forecast (e.g. a 'What to watch' or "
    "'My read' line) — specific but appropriately hedged, never overconfident.\n"
    "- CONNECT: when relevant, reference and LINK to a prior post on this site (a list is "
    "provided in the user message) using its /slug/ path, to build a throughline.\n"
    "Always apply a model-risk, safety, and governance lens. Be the analyst a busy "
    "practitioner reads BECAUSE it tells them something the original source didn't."
)

DRAFT_SYSTEM = (
    "You are an AI industry analyst writing for a professional audience of risk, "
    "governance, and applied-AI practitioners. Voice: clear, authoritative, "
    "grounded, never hype. Where you make factual claims about recent events, ground "
    "them with web search.\n\n"
    + ANALYSIS_GUIDE + "\n\n"
    + FORMAT_GUIDE + "\n\n"
    + _sources_preference() + "\n\n"
    + CORROBORATION_RULE + "\n\n"
    "Return the article in EXACTLY this format, and nothing else (no code fences):\n"
    "TITLE: <the title on a single line>\n"
    "EXCERPT: <one-sentence summary on a single line>\n"
    "TAG: <the single best-fit subject category, chosen from EXACTLY this list: "
    "AI Governance, AI Safety, Alignment, Evaluation, Agentic AI, "
    "Regulation & Policy, Industry>\n"
    "TAKEAWAY: <a '1-minute takeaway' in 1-2 sentences — the single most important "
    "point, specific and plainly stated>\n"
    "BODY:\n"
    "<the full markdown body; may span many lines>"
)


def _strip_fences(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    return text


def _extract_json(text):
    """Pull a JSON object/array out of a model response, tolerating stray fences."""
    text = _strip_fences(text)
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if not m:
            raise
        return json.loads(m.group(1), strict=False)


def parse_article(text):
    """Parse the delimited TITLE/EXCERPT/TAG/BODY format into an article dict.

    Robust by design: the body is taken verbatim after the BODY: marker, so it can
    contain quotes, newlines, and arbitrary markdown without any escaping.
    """
    text = _strip_fences(text)
    meta = {"title": "", "excerpt": "", "tag": "", "takeaway": "", "body_markdown": ""}
    lines = text.splitlines()
    body_idx = None
    for i, line in enumerate(lines):
        up = line.lstrip().upper()
        if up.startswith("BODY:"):
            body_idx = i
            trailing = line.split(":", 1)[1].strip()
            break
        for key in ("TITLE", "EXCERPT", "TAG", "TAKEAWAY"):
            if up.startswith(key + ":"):
                meta[key.lower()] = line.split(":", 1)[1].strip()
                break
    if body_idx is not None:
        rest = lines[body_idx + 1:]
        body = (trailing + "\n" if trailing else "") + "\n".join(rest)
        meta["body_markdown"] = body.strip()
    else:
        # No BODY marker found — treat the whole thing as the body.
        meta["body_markdown"] = text.strip()
    if not meta["title"]:
        raise ValueError("Could not parse a title from the model output.")
    if not meta["body_markdown"]:
        raise ValueError("Model returned an empty body.")
    return meta


def _text_of(resp):
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _discovery_prompt(count, focus=None):
    focus_line = "; ".join(focus or FOCUS_TOPICS)
    return (
        f"Find the {count} most significant, recent AI developments (roughly the last "
        "48 hours) worth writing about. Prefer concrete news (releases, regulation, "
        "research, incidents) over evergreen topics. General areas of interest: "
        f"{focus_line}.\n\n"
        "REQUIRED MIX (this is a candidate list; extras are backups in case some can't "
        "be corroborated):\n"
        "- The FIRST TWO topics MUST each be squarely about AI SAFETY (e.g. alignment, "
        "dangerous capabilities, evaluations/red-teaming, oversight, control, security "
        "of AI systems, safety policy) — distinct stories.\n"
        "- The REMAINING topics should span DIFFERENT categories, whichever are most "
        "newsworthy: AI Governance, Alignment, Evaluation, Agentic AI, Regulation & "
        "Policy, Industry. Vary them. Order them best-first.\n\n"
        + _sources_preference() + "\n\n"
        + CORROBORATION_RULE + " Only propose topics that clear this bar.\n\n"
        "For each topic, set 'category' to the best-fit category name (the first topic's "
        "category is normally 'AI Safety'). Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "angle": "...", "category": "..."}]'
    )


def discover_topics(count, focus=None):
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=1200,
        tools=[WEB_SEARCH],
        messages=[{"role": "user", "content": _discovery_prompt(count, focus)}],
    )
    topics = _extract_json(_text_of(resp))
    return topics[:count]


def _read_frontmatter(path):
    """Lightweight frontmatter reader (no extra deps) for the pipeline step."""
    meta = {}
    with open(path) as f:
        text = f.read()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def published_posts_context(limit=25):
    """A list of already-published posts the model can reference and link."""
    items = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        meta = _read_frontmatter(path)
        if str(meta.get("published", "true")).lower() == "false":
            continue
        title = meta.get("title", "")
        slug = meta.get("slug") or os.path.basename(path)[:-3]
        if title:
            items.append("- [{}](/{}/) — {}".format(title, slug, meta.get("excerpt", "")))
    if not items:
        return ""
    return ("\n\nAlready published on this site — reference and LINK any that are "
            "relevant (use the /slug/ path) to build a throughline:\n"
            + "\n".join(items[:limit]))


def draft_article(instruction):
    """instruction: a natural-language brief describing what to write."""
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=2000,
        tools=[WEB_SEARCH],
        system=DRAFT_SYSTEM,
        messages=[{"role": "user", "content": instruction + published_posts_context()}],
    )
    return parse_article(_text_of(resp))


def has_sources(article):
    """True if the draft has a Sources section containing at least one URL.

    Lenient on purpose: accepts a '## Sources' heading OR a 'Sources:' label, and
    counts ANY http(s) URL after it — markdown links, bare URLs, or numbered refs.
    """
    body = article.get("body_markdown", "")
    m = re.search(r"(?:^|\n)\s*(?:#{1,6}\s*|\*{0,2})sources\b\*{0,2}\s*:?", body, re.IGNORECASE)
    if not m:
        return False
    return bool(re.search(r"https?://", body[m.end():]))


def trim_to_length(article):
    """Prompt-based limits don't hold, so enforce length with a dedicated trim pass."""
    body = article.get("body_markdown", "")
    if len(body.split()) <= MAX_WORDS:
        return article
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=1500,
        system=("You are a ruthless editor. Cut the following article body to UNDER "
                f"{MAX_WORDS} words (aim ~600). Preserve the core analysis "
                "(cross-references, historical parallel, prediction) and KEEP the "
                "'## Sources' section with ALL its links intact. Keep markdown headings. "
                "Return ONLY the tightened markdown body, nothing else."),
        messages=[{"role": "user", "content": body}],
    )
    new = _strip_fences(_text_of(resp))
    if new and re.search(r"https?://", new) and len(new.split()) < len(body.split()):
        article["body_markdown"] = new
    return article


def draft_with_sourcing(instruction):
    """Draft; ensure a real Sources section (retry once); then enforce length."""
    article = draft_article(instruction)
    if not has_sources(article):
        article = draft_article(
            instruction + "\n\nYOUR PREVIOUS DRAFT FAILED: it had no proper '## Sources' "
            "section with real links. Either ground this in real, citable sources that "
            "meet the corroboration bar and include a '## Sources' list of working links, "
            "or — if the story cannot be corroborated — say so plainly rather than writing it.")
    if has_sources(article):
        article = trim_to_length(article)
    return article


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]


def save_post(article, default_tag="Analysis"):
    today = datetime.date.today().isoformat()
    slug = slugify(article["title"])
    path = os.path.join(POSTS_DIR, f"{slug}.md")
    title = article["title"].replace('"', "'")
    excerpt = article.get("excerpt", "").replace('"', "'")
    takeaway = article.get("takeaway", "").replace('"', "'")
    tag = article.get("tag") or default_tag
    frontmatter = (
        "---\n"
        f'title: "{title}"\n'
        f"date: {today}\n"
        f"slug: {slug}\n"
        f"tag: {tag}\n"
        f'excerpt: "{excerpt}"\n'
        f'takeaway: "{takeaway}"\n'
        "published: false\n"        # <-- review gate: flip to true to publish
        "---\n\n"
    )
    with open(path, "w") as f:
        f.write(frontmatter + article["body_markdown"].strip() + "\n")
    print(f"  saved draft: posts/{slug}.md")
    return path


# ---- Mode: scheduled (auto-discover) -------------------------------------

def _dump_prompt(label, instruction):
    print("=" * 70)
    print("[DRY RUN] " + label)
    print("=" * 70)
    print("\n--- SYSTEM PROMPT ---\n" + DRAFT_SYSTEM)
    print("\n--- USER INSTRUCTION ---\n" + instruction)
    print("\n[dry-run] No API call made and no file written.\n")


def run_scheduled(count, focus=None, dry_run=False):
    if dry_run:
        print("=" * 70)
        print("[DRY RUN] scheduled mode")
        print("=" * 70)
        print("\n--- TOPIC-DISCOVERY PROMPT ---\n" + _discovery_prompt(count, focus))
        print("\n--- then each topic is drafted with this SYSTEM PROMPT ---\n"
              + DRAFT_SYSTEM)
        print("\n[dry-run] No API call made and no file written.\n")
        return
    target = count
    print(f"Discovering candidate topics (target {target})...")
    # Over-fetch so we can backfill when a topic can't be corroborated/cited.
    candidates = discover_topics(target + 4, focus=focus)
    saved = 0
    for t in candidates:
        if saved >= target:
            break
        print(f"Drafting: {t['topic']}")
        cat = t.get("category", "").strip()
        instruction = (
            f"Write an analytical piece about: {t['topic']}. "
            f"Angle: {t.get('angle', '')}. "
            + (f"This belongs in the '{cat}' category; set TAG accordingly. " if cat else "")
            + "Research it with web search first, cross-referencing multiple sources."
        )
        article = draft_with_sourcing(instruction)
        if not has_sources(article):
            print("  skipped (couldn't corroborate/cite) — trying the next candidate.")
            continue
        save_post(article, default_tag=cat or "Industry")
        saved += 1
    print(f"Done — saved {saved} of {target} target draft(s).")


# ---- Mode: on demand -----------------------------------------------------

def _ondemand_instruction(topic=None, url=None, text=None, article_type=None, angle=None):
    parts = []
    kind = article_type or "analysis"
    if url:
        parts.append(f"Read and analyze this source, then write a {kind} piece about "
                     f"it (use web search to fetch and verify): {url}")
    if topic:
        parts.append(f"Write a {kind} piece about: {topic}.")
    if text:
        parts.append(
            "Below is a source document / link / notes I'm recommending as the basis "
            f"for a post. Write an original {kind} piece in the house style that "
            "engages with it: lead with the most important insight, add context and "
            "verification via web search, quote sparingly, and bring the risk-, "
            "governance-, and applied-AI lens of this publication. Do NOT merely "
            "summarize the source.\n\n--- SOURCE ---\n" + text)
    if angle:
        parts.append(f"Angle / emphasis: {angle}")
    if not parts:
        raise SystemExit("Nothing to write about. Provide --topic, --url, --from-file, "
                         "or use --interactive.")
    return "\n\n".join(parts), kind


def run_ondemand(topic=None, url=None, text=None, article_type=None, angle=None,
                 dry_run=False):
    instruction, kind = _ondemand_instruction(topic, url, text, article_type, angle)
    if dry_run:
        _dump_prompt("on-demand mode", instruction)
        return
    print("Researching and drafting...")
    article = draft_with_sourcing(instruction)
    if not has_sources(article):
        print("  ⚠ note: this draft has no '## Sources' section — verify it before publishing.")
    save_post(article, default_tag=kind.capitalize())
    print("Done. Review the draft, then flip 'published: false' to true.")


def run_interactive(dry_run=False):
    print("On-demand draft. Paste a link, describe a finding, or paste notes.")
    print("Finish your input with Ctrl-D (Mac/Linux) on a new line.\n")
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("No input received.")
    # If it's just a URL, treat it as a source; otherwise as notes/topic.
    if re.match(r"^https?://\S+$", text):
        run_ondemand(url=text, dry_run=dry_run)
    else:
        run_ondemand(text=text, dry_run=dry_run)


def main():
    p = argparse.ArgumentParser(description="Draft AI blog posts (scheduled or on demand).")
    p.add_argument("--count", type=int, default=2,
                   help="scheduled mode: how many topics to draft (default 2)")
    p.add_argument("--focus",
                   help="scheduled mode: comma-separated focus topics for this run "
                        "(overrides the FOCUS_TOPICS list)")
    p.add_argument("--topic", help="on demand: a topic/headline to write about")
    p.add_argument("--url", help="on demand: a source URL to read and analyze")
    p.add_argument("--from-file", dest="from_file",
                   help="on demand: path to a file with notes/pasted text")
    p.add_argument("--type", dest="article_type",
                   choices=["news", "analysis", "opinion", "governance"],
                   help="article type (on demand)")
    p.add_argument("--angle", help="on demand: angle/emphasis for the piece")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="on demand: paste/describe a finding at the prompt")
    p.add_argument("--dry-run", dest="dry_run", action="store_true",
                   help="show the exact prompts that would be sent; no API call, "
                        "no file written")
    args = p.parse_args()

    text = None
    if args.from_file:
        with open(args.from_file) as f:
            text = f.read().strip()

    if args.interactive:
        run_interactive(dry_run=args.dry_run)
    elif args.topic or args.url or text:
        run_ondemand(topic=args.topic, url=args.url, text=text,
                     article_type=args.article_type, angle=args.angle,
                     dry_run=args.dry_run)
    else:
        focus = [t.strip() for t in args.focus.split(",")] if args.focus else None
        run_scheduled(args.count, focus=focus, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
