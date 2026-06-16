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
PREFERRED_SOURCES = [
    "The Wall Street Journal (wsj.com)",
    "The New York Times (nytimes.com)",
    "Bloomberg (bloomberg.com)",
    "Financial Times (ft.com)",
    "Reuters (reuters.com)",
    "The Economist (economist.com)",
    "official AI labs: OpenAI (openai.com), Anthropic (anthropic.com), "
    "Google DeepMind (deepmind.google), Microsoft, Meta AI",
    "primary/official: arXiv, NIST, the Federal Reserve, OCC, the EU Commission",
]


def _sources_preference():
    return (
        "Prioritize credible, top-tier sources when researching and citing. "
        "Prefer, in roughly this order of trust: " + "; ".join(PREFERRED_SOURCES)
        + ". You may use other sources when needed, but prefer these, and include "
        "links to the primary source for any factual claim."
    )


DRAFT_SYSTEM = (
    "You are an AI industry analyst writing for a professional audience of risk, "
    "governance, and applied-AI practitioners. Voice: clear, authoritative, "
    "grounded, never hype. Length: 700-1000 words. Use markdown: ## for section "
    "headings, normal paragraphs, occasional bullet lists; do NOT include an H1 "
    "(the title is rendered separately). Where you make factual claims about recent "
    "events, ground them with web search.\n\n"
    + _sources_preference() + "\n\n"
    "Return the article in EXACTLY this format, and nothing else (no code fences):\n"
    "TITLE: <the title on a single line>\n"
    "EXCERPT: <one-sentence summary on a single line>\n"
    "TAG: <one of: News, Analysis, Opinion, Governance>\n"
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
    meta = {"title": "", "excerpt": "", "tag": "", "body_markdown": ""}
    lines = text.splitlines()
    body_idx = None
    for i, line in enumerate(lines):
        up = line.lstrip().upper()
        if up.startswith("BODY:"):
            body_idx = i
            trailing = line.split(":", 1)[1].strip()
            break
        for key in ("TITLE", "EXCERPT", "TAG"):
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
        f"Search the web for the {count} most significant, recent AI developments "
        f"(roughly the last 48 hours), giving STRONG PRIORITY to these focus areas: "
        f"{focus_line}. Prefer concrete news (releases, regulation, research, "
        "incidents) over evergreen topics. " + _sources_preference() + " "
        "Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "angle": "...", "type": "news|analysis|opinion"}]'
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


def draft_article(instruction):
    """instruction: a natural-language brief describing what to write."""
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=3000,
        tools=[WEB_SEARCH],
        system=DRAFT_SYSTEM,
        messages=[{"role": "user", "content": instruction}],
    )
    return parse_article(_text_of(resp))


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]


def save_post(article, default_tag="Analysis"):
    today = datetime.date.today().isoformat()
    slug = slugify(article["title"])
    path = os.path.join(POSTS_DIR, f"{slug}.md")
    title = article["title"].replace('"', "'")
    excerpt = article.get("excerpt", "").replace('"', "'")
    tag = article.get("tag") or default_tag
    frontmatter = (
        "---\n"
        f'title: "{title}"\n'
        f"date: {today}\n"
        f"slug: {slug}\n"
        f"tag: {tag}\n"
        f'excerpt: "{excerpt}"\n'
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
    print(f"Discovering {count} topic(s)...")
    topics = discover_topics(count, focus=focus)
    for t in topics:
        print(f"Drafting: {t['topic']}")
        instruction = (
            f"Write a {t.get('type', 'analysis')} piece about: {t['topic']}. "
            f"Angle: {t.get('angle', '')}. Research it with web search first."
        )
        article = draft_article(instruction)
        save_post(article, default_tag=t.get("type", "Analysis").capitalize())
    print("Done. Review the new drafts, then flip 'published: false' to true.")


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
    article = draft_article(instruction)
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
