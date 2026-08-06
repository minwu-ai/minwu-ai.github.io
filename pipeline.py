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
    "model risk management and AI governance (SR 26-2)",
    "agentic AI and autonomous systems",
    "AI regulation and policy",
    "enterprise AI adoption and risk",
    "notable frontier model releases",
    "academic research on AI safety, interpretability, evaluation, auditing, and risk "
    "(arXiv papers and the followed researchers below)",
]

# Academic researchers to follow — surface and read their NEW papers/writing (arXiv,
# Google Scholar, personal sites) as post material. (name, focus, home page). Edit freely.
FOLLOWED_RESEARCHERS = [
    ("Neel Nanda", "mechanistic interpretability", "https://www.neelnanda.io/"),
    ("Been Kim", "explainability / concept-based interpretability", "https://beenkim.github.io/"),
    ("Jacob Steinhardt", "ML safety, evaluation, robustness", "https://jsteinhardt.stat.berkeley.edu/"),
    ("Dan Hendrycks", "AI safety benchmarks and catastrophic risk", "https://www.safe.ai/"),
    ("Inioluwa Deborah Raji", "algorithmic auditing and accountability", "https://rajiinio.github.io/"),
]

# ---- Saturday 'Life' briefs ----------------------------------------------
# Saturdays do NOT auto-draft a Life post. A personal essay's value is the
# author's own point of view, which the pipeline cannot supply — so instead of
# writing prose in a borrowed voice, it does the legwork: it surfaces a few
# researched subjects with verified sources and leaves the writing to you.
# Edit this palette freely.
LIFE_TOPICS = [
    ("Golf history & architecture",
     "the origins and design of a famous course or hole, a course architect "
     "(MacKenzie, Colt, Ross, Tillinghast), how the rules or equipment evolved, "
     "the story behind a championship or a piece of golf tradition"),
    ("Places & the history beneath them",
     "why a city, region, route, or landmark came to look and feel the way it "
     "does — the geography, trade, or accident of history that shaped it"),
    ("Skiing & alpine culture",
     "how a resort or region was built, the evolution of technique and equipment, "
     "avalanche and snow science, the history of alpine racing and mountaineering"),
    ("People worth knowing",
     "a short biographical essay on a figure whose life is genuinely interesting — "
     "explorers, architects, mathematicians, athletes, builders, eccentrics"),
    ("Ideas & reflection",
     "an idea from science, mathematics, or history examined slowly and personally, "
     "in the register of the 'Entropy, Evolution, and AI' post"),
]

LIFE_BRIEF_COUNT = 4      # how many subjects to surface each Saturday

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


def _researchers_preference():
    who = "; ".join("{} ({}) — {}".format(n, u, f) for n, f, u in FOLLOWED_RESEARCHERS)
    return (
        "FOLLOW ACADEMIC RESEARCH: actively track and surface NEW papers/writing "
        "(roughly the last 2 weeks) from these researchers as post material — check "
        "arXiv, Google Scholar, and their sites: " + who + ". Also scan arXiv "
        "(cs.LG / cs.AI / cs.CY) for notable AI-safety, interpretability, evaluation, "
        "or auditing papers. Papers on arXiv are open-access — read the abstract and "
        "intro, and cite the arXiv URL. A rigorous paper is excellent post material."
    )


def _coverage_summary():
    """Recent published-post distribution, to steer discovery toward under-covered topics."""
    from collections import Counter
    counts = Counter()
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        meta = _read_frontmatter(path)
        if str(meta.get("published", "true")).lower() == "false":
            continue
        for t in str(meta.get("tag", "")).split(","):
            t = t.strip()
            if t:
                counts[t] += 1
    cats = ["AI Safety", "AI Governance", "Alignment", "Evaluation", "Agentic AI",
            "Regulation & Policy", "Industry"]
    line = ", ".join("{} ({})".format(c, counts.get(c, 0)) for c in cats)
    return (
        "CURRENT COVERAGE (published posts per category): " + line + ". The blog is "
        "over-concentrated in AI Safety and AI Governance. Keep featuring those regularly "
        "but do NOT let them dominate — actively PRIORITISE the under-covered categories "
        "(especially any with 0-2 posts, e.g. Alignment, Evaluation, Agentic AI, "
        "Regulation & Policy, Industry) so coverage balances across the site over time."
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
    "VISUALS (encouraged): do NOT embed external images (link rot / licensing), but "
    "ACTIVELY look for a chance to illustrate. Whenever the content involves a process, "
    "workflow, comparison, taxonomy, timeline, hierarchy, or relationship, INCLUDE a "
    "simple, syntactically-valid Mermaid diagram in a ```mermaid fenced code block "
    "(flowchart, timeline, sequence, or mindmap) — you may include up to TWO small "
    "diagrams if they genuinely aid understanding. A markdown comparison table is also "
    "encouraged where apt. Keep diagrams small, correct, and readable; omit only if a "
    "visual truly adds nothing.\n"
    "CITATIONS (required): weave clickable INLINE hyperlinks into the prose — link the "
    "specific words that carry a factual claim straight to the primary source, as "
    "markdown [phrase](https://...). Do NOT add a separate 'Sources' or 'References' "
    "section at the end; all citations are inline. Example: \"...reflects the final "
    "agreement described by the [Council of the EU](https://...) and analysis from "
    "[White & Case](https://...).\" Cite ONLY real URLs you actually retrieved via web "
    "search — never invent or guess a link; if a claim can't be sourced, soften it or "
    "drop it. Use several inline citations across the piece."
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
    "- CONNECT: a list of already-published posts is provided in the user message. If "
    "this story overlaps one, do NOT rehash it — focus on what is NEW, and LINK the "
    "prior post inline using its FULL absolute URL (https://minwu-ai.github.io/<slug>/) "
    "so readers get the throughline.\n"
    "Always apply a model-risk, safety, and governance lens. Be the analyst a busy "
    "practitioner reads BECAUSE it tells them something the original source didn't."
)

INDEPENDENCE_RULE = (
    "INDEPENDENCE AND CONFLICTS OF INTEREST — this is a hard constraint:\n"
    "- Never claim or imply professional engagement, client work, or insider access. "
    "Do NOT write phrases like 'in my consulting experience', 'my clients', 'in my "
    "practice', 'firms I advise', 'in my work with banks', 'from my time at', or any "
    "variation that positions the author as speaking from privileged or paid engagements.\n"
    "- Ground every claim in the public record instead. Preferred framings: "
    "'Organizations commonly encounter...', 'Public regulatory guidance suggests...', "
    "'One practical governance challenge is...', 'Industry reporting indicates...', "
    "'The published guidance states...'.\n"
    "- Never reference confidential, non-public, proprietary, or internal information. "
    "Every factual claim must be traceable to a publicly accessible source.\n"
    "- First-person analytical judgment is fine ('I read this as...', 'my view is...'). "
    "First-person claims of professional authority or engagement are not."
)

DRAFT_SYSTEM = (
    "You are an AI industry analyst writing for a professional audience of risk, "
    "governance, and applied-AI practitioners. Voice: clear, authoritative, "
    "grounded, never hype. Authority comes from the quality of reasoning about public "
    "evidence — never from claimed professional engagements or privileged access. "
    "Where you make factual claims about recent events, ground them with web search.\n\n"
    + INDEPENDENCE_RULE + "\n\n"
    + ANALYSIS_GUIDE + "\n\n"
    + FORMAT_GUIDE + "\n\n"
    + _sources_preference() + "\n\n"
    + CORROBORATION_RULE + "\n\n"
    "Return the article in EXACTLY this format, and nothing else (no code fences):\n"
    "TITLE: <the title on a single line>\n"
    "EXCERPT: <one-sentence summary on a single line>\n"
    "TAG: <one or two best-fit subject categories from EXACTLY this list, "
    "comma-separated. Use TWO categories WHENEVER the piece genuinely spans two areas "
    "(this is encouraged, e.g. 'Agentic AI, AI Governance'); use one only if it clearly "
    "fits a single category. Choose from: AI Governance, AI Safety, Alignment, "
    "Evaluation, Agentic AI, Regulation & Policy, Industry>\n"
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
    """Parse the first JSON value in a model response, ignoring any surrounding prose.

    Uses raw_decode so trailing commentary after the array/object (a common model
    habit) doesn't cause an 'Extra data' error.
    """
    text = _strip_fences(text)
    start = next((i for i, ch in enumerate(text) if ch in "[{"), None)
    if start is None:
        return json.loads(text, strict=False)  # no JSON found -> raise informative error
    try:
        obj, _ = json.JSONDecoder(strict=False).raw_decode(text[start:])
        return obj
    except json.JSONDecodeError:
        # Salvage: if the array was truncated, keep the complete {...} entries.
        objs = []
        for m in re.finditer(r"\{[^{}]*\}", text[start:], re.DOTALL):
            try:
                objs.append(json.loads(m.group(0), strict=False))
            except json.JSONDecodeError:
                pass
        if objs:
            return objs
        raise


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
        "48 hours) worth writing about, INCLUDING notable new academic research/papers. "
        "Prefer concrete items (releases, regulation, research papers, incidents) over "
        f"evergreen topics. General areas of interest: {focus_line}.\n\n"
        + _coverage_summary() + "\n\n"
        "REQUIRED MIX (this is a candidate list; extras are backups in case some can't "
        "be corroborated):\n"
        "- Candidates must span DIFFERENT categories — do not return two topics in the "
        "same category.\n"
        "- PRIORITISE under-covered categories per the coverage stats above. AI Safety "
        "and AI Governance may appear but must NOT both dominate; include Alignment, "
        "Evaluation, Agentic AI, Regulation & Policy, or Industry whenever there's a real "
        "story.\n"
        "- Include at least one candidate grounded in ACADEMIC research (an arXiv paper "
        "or a followed researcher's new work) whenever a notable one exists.\n"
        "- Order candidates best-first.\n\n"
        + _sources_preference() + "\n\n"
        + _researchers_preference() + "\n\n"
        + CORROBORATION_RULE + " Only propose topics that clear this bar.\n\n"
        "AVOID REDUNDANCY: a list of posts already published on this site is provided "
        "below. Do NOT propose a topic that merely repeats one of them. Revisiting a "
        "topic is fine ONLY if there's a genuine new development or new angle — if so, "
        "note in the angle what's new and which prior post it follows up.\n\n"
        "For each topic, set 'category' to the best-fit category from: AI Safety, AI "
        "Governance, Alignment, Evaluation, Agentic AI, Regulation & Policy, Industry. "
        "Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "angle": "...", "category": "..."}]'
    )


def discover_topics(count, focus=None):
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=3000,   # room for web-search rounds + the full candidate JSON
        tools=[WEB_SEARCH],
        messages=[{"role": "user",
                   "content": _discovery_prompt(count, focus) + published_posts_context()}],
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
            items.append("- [{}](https://minwu-ai.github.io/{}/) — {}".format(
                title, slug, meta.get("excerpt", "")))
    if not items:
        return ""
    return ("\n\nAlready published on this site — reference and LINK any that are "
            "relevant (use the FULL absolute URL shown) to build a throughline:\n"
            + "\n".join(items[:limit]))


def draft_article(instruction, system=None):
    """instruction: a natural-language brief describing what to write."""
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=2000,
        tools=[WEB_SEARCH],
        system=system or DRAFT_SYSTEM,
        messages=[{"role": "user", "content": instruction + published_posts_context()}],
    )
    return parse_article(_text_of(resp))


def has_sources(article):
    """True if the draft has enough INLINE citations (markdown links to real URLs).

    Citations are now woven into the prose (no end 'Sources' section), so we require
    at least two inline hyperlinks to http(s) sources.
    """
    body = article.get("body_markdown", "")
    return len(re.findall(r"\]\(https?://[^)]+\)", body)) >= 2


def trim_to_length(article, max_words=None, preserve="the core analysis "
                   "(cross-references, historical parallel, prediction)"):
    """Prompt-based limits don't hold, so enforce length with a dedicated trim pass."""
    limit = max_words or MAX_WORDS
    body = article.get("body_markdown", "")
    if len(body.split()) <= limit:
        return article
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=1500,
        system=("You are a ruthless editor. Cut the following article body to UNDER "
                f"{limit} words (aim ~{int(limit * 0.85)}). Preserve {preserve} "
                "and KEEP every "
                "inline source hyperlink intact. Keep markdown headings. "
                "Return ONLY the tightened markdown body, nothing else."),
        messages=[{"role": "user", "content": body}],
    )
    new = _strip_fences(_text_of(resp))
    if new and re.search(r"https?://", new) and len(new.split()) < len(body.split()):
        article["body_markdown"] = new
    return article


def draft_with_sourcing(instruction, system=None, max_words=None, preserve=None):
    """Draft; ensure a real Sources section (retry once); then enforce length."""
    article = draft_article(instruction, system=system)
    if not has_sources(article):
        article = draft_article(
            instruction + "\n\nYOUR PREVIOUS DRAFT FAILED: it lacked real inline source "
            "links. Weave at least two clickable inline hyperlinks [phrase](https://...) "
            "to primary sources directly into the prose (no end 'Sources' section). If "
            "the story cannot be corroborated with real links, say so plainly rather "
            "than writing it.", system=system)
    if has_sources(article):
        kw = {"max_words": max_words} if max_words else {}
        if preserve:
            kw["preserve"] = preserve
        article = trim_to_length(article, **kw)
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
        'cover: "/assets/"\n'          # <-- fill in your image path, e.g. /assets/foo.png
        'cover_alt: "Illustration: "\n'  # <-- fill in the caption / credit
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
    saved = _select_and_draft(candidates, target)
    print(f"Done — saved {saved} of {target} target draft(s).")


# ---- Mode: Saturday 'Life' briefs ----------------------------------------

def _life_brief_prompt(count):
    palette = "\n".join("- {}: {}".format(n, d) for n, d in LIFE_TOPICS)
    return (
        f"Surface {count} subjects worth writing a personal essay about, for the "
        "Saturday 'Life' section of a website that spends the rest of the week on AI "
        "safety and governance. Saturday is the author's day off from AI — these must "
        "have NOTHING to do with AI, machine learning, or technology policy.\n\n"
        "You are NOT writing the essay. You are doing the legwork so the author can "
        "decide whether they have something to say. Give them material and a question, "
        "never prose in their voice.\n\n"
        "The author's interests, and the palette to choose from:\n" + palette + "\n\n"
        "WHAT MAKES A GOOD SUBJECT:\n"
        "- Evergreen, not news. There is no recency requirement here.\n"
        "- Specific and concrete: 'Why the Old Course at St Andrews is played "
        "anticlockwise' beats 'the history of golf'. A single course, person, place, "
        "object, decision, or question — never a survey.\n"
        "- Built on a genuine surprise: a fact that reverses an assumption, an origin "
        "nobody expects, a decision that turned out to matter. If there is no surprise, "
        "drop the subject.\n"
        "- Genuinely researchable: real, checkable public sources (club and resort "
        "archives, museums, governing bodies like the R&A or USGA, university and "
        "library collections, reputable long-form journalism).\n"
        "- Subjects must span DIFFERENT entries in the palette above.\n"
        "- Nothing requiring personal experience of the author — you do not know where "
        "they have been or what they have played.\n\n"
        "VERIFY BEFORE YOU PROPOSE: use web search on every subject. Every source URL "
        "you return must be one you actually found — never guess or construct a URL, "
        "and never cite a page you did not see. Drop any subject you cannot support "
        "with at least two real sources.\n\n"
        "AVOID REDUNDANCY: a list of posts already published on this site is provided "
        "below. Do not propose a subject that repeats one of them.\n\n"
        "For each subject return:\n"
        "- topic: the specific subject, as a short phrase\n"
        "- hook: the surprising fact at its center, in 1-2 sentences of plain "
        "reporting (facts only — not an opening line for the essay)\n"
        "- why: one sentence on why this could be worth an essay\n"
        "- question: ONE genuine question the author would have to answer for "
        "themselves to make it a real piece — the thing only they can supply\n"
        "- sources: 2-4 objects with 'title' and 'url', verified via search\n"
        "- category: which palette entry it belongs to\n\n"
        "Order best-first. Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "hook": "...", "why": "...", "question": "...", '
        '"sources": [{"title": "...", "url": "..."}], "category": "..."}]'
    )


def generate_life_briefs(count=LIFE_BRIEF_COUNT):
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=4000,
        tools=[WEB_SEARCH],
        messages=[{"role": "user",
                   "content": _life_brief_prompt(count) + published_posts_context()}],
    )
    briefs = _extract_json(_text_of(resp)) or []
    # Keep only briefs with at least two real-looking source links.
    clean = []
    for b in briefs:
        srcs = [s for s in (b.get("sources") or [])
                if isinstance(s, dict) and str(s.get("url", "")).startswith("http")]
        if len(srcs) >= 2:
            b["sources"] = srcs
            clean.append(b)
    return clean[:count]


def life_briefs_markdown(briefs):
    today = datetime.date.today().isoformat()
    if not briefs:
        return ("No Life subjects cleared the bar this week — nothing that had both a "
                "real surprise and sources to back it. No action needed.\n")
    out = [
        f"Saturday reading for {today}. {len(briefs)} subject(s) with the legwork done "
        "— sources checked, nothing written in your voice.\n",
        "Write one only if the question at the end is one you actually have a view on. "
        "Most weeks the honest answer is none, and that's the point.\n",
    ]
    for i, b in enumerate(briefs, 1):
        out.append(f"\n---\n\n### {i}. {b.get('topic', 'Untitled')}")
        if b.get("category"):
            out.append(f"*{b['category']}*\n")
        if b.get("hook"):
            out.append(f"**The surprise:** {b['hook']}\n")
        if b.get("why"):
            out.append(f"**Why it could be an essay:** {b['why']}\n")
        if b.get("question"):
            out.append(f"**Your call:** {b['question']}\n")
        if b.get("sources"):
            out.append("**Sources:**\n")
            for s in b["sources"]:
                out.append("- [{}]({})".format(s.get("title") or s["url"], s["url"]))
    out.append("\n---\n\nTo write one up with research support:\n"
               "`python pipeline.py --topic \"<subject>\" --angle \"<your take>\"`\n")
    return "\n".join(out)


def run_life_briefs(dry_run=False, out_path=None):
    """Saturday: surface researched subjects. Writes no post and no prose."""
    if dry_run:
        print("=" * 70)
        print("[DRY RUN] Saturday 'Life' briefs")
        print("=" * 70)
        print("\n--- BRIEF PROMPT ---\n" + _life_brief_prompt(LIFE_BRIEF_COUNT))
        print("\n[dry-run] No API call made and no file written.\n")
        return
    print("Saturday Life briefs — researching subjects...")
    briefs = generate_life_briefs()
    md = life_briefs_markdown(briefs)
    print("\n" + md)
    if out_path:
        with open(out_path, "w") as f:
            f.write(md)
        print(f"\n  wrote {out_path}")
    print(f"Done — {len(briefs)} brief(s).")


def _select_and_draft(candidates, target):
    """Save `target` drafts across DISTINCT categories, in discovery order (which is
    coverage-balanced). Skips topics that can't be cited; backfills if still short."""
    saved, used_cats = 0, set()

    def attempt(cand):
        nonlocal saved
        cat = cand.get("category", "").strip() or "Industry"
        print(f"Drafting: {cand['topic']}")
        instruction = (
            f"Write an analytical piece about: {cand['topic']}. "
            f"Angle: {cand.get('angle', '')}. "
            f"This belongs in the '{cat}' category; set TAG accordingly (add a second "
            "category too if the piece genuinely spans two). "
            "Research it with web search first, cross-referencing multiple sources."
        )
        article = draft_with_sourcing(instruction)
        if not has_sources(article):
            print("  skipped (couldn't corroborate/cite) — trying the next candidate.")
            return
        save_post(article, default_tag=cat)
        used_cats.add(cat)
        saved += 1

    # Pass 1: fill with DISTINCT categories, in discovery (coverage-balanced) order.
    for c in candidates:
        if saved >= target:
            break
        if (c.get("category", "").strip() or "Industry") in used_cats:
            continue
        attempt(c)
    # Pass 2: backfill with anything remaining if still short.
    for c in candidates:
        if saved >= target:
            break
        attempt(c)
    return saved


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
    p.add_argument("--life-briefs", dest="life_briefs", action="store_true",
                   help="surface researched 'Life' subjects to write about yourself "
                        "(auto-selected on Saturdays); writes no post")
    p.add_argument("--no-life", dest="no_life", action="store_true",
                   help="run the normal AI pipeline even if today is Saturday")
    p.add_argument("--out", help="with --life-briefs: also write the briefs to this file")
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
    elif args.life_briefs or (datetime.date.today().weekday() == 5 and not args.no_life):
        # weekday() == 5 is Saturday — Life briefs, not an auto-drafted post.
        run_life_briefs(dry_run=args.dry_run, out_path=args.out)
    else:
        focus = [t.strip() for t in args.focus.split(",")] if args.focus else None
        run_scheduled(args.count, focus=focus, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
