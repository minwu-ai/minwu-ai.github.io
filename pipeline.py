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

DRAFT_SYSTEM = (
    "You are an AI industry analyst writing for a professional audience of risk, "
    "governance, and applied-AI practitioners. Voice: clear, authoritative, "
    "grounded, never hype. Length: 700-1000 words. Use markdown: ## for section "
    "headings, normal paragraphs, occasional bullet lists; do NOT include an H1 "
    "(the title is rendered separately). Where you make factual claims about recent "
    "events, ground them with web search. Return ONLY a JSON object, no markdown "
    'fences:\n{"title": "...", "excerpt": "one-sentence summary", '
    '"tag": "News|Analysis|Opinion|Governance", "body_markdown": "..."}'
)


def _extract_json(text):
    """Pull a JSON object/array out of a model response, tolerating stray fences."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if not m:
            raise
        return json.loads(m.group(1))


def _text_of(resp):
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def discover_topics(count, focus=None):
    areas = focus or FOCUS_TOPICS
    focus_line = "; ".join(areas)
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=1200,
        tools=[WEB_SEARCH],
        messages=[{"role": "user", "content": (
            f"Search the web for the {count} most significant, recent AI developments "
            f"(roughly the last 48 hours), giving STRONG PRIORITY to these focus areas: "
            f"{focus_line}. Prefer concrete news (releases, regulation, research, "
            "incidents) over evergreen topics. Return ONLY a JSON array, no markdown:\n"
            '[{"topic": "...", "angle": "...", "type": "news|analysis|opinion"}]'
        )}],
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
    return _extract_json(_text_of(resp))


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

def run_scheduled(count, focus=None):
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

def run_ondemand(topic=None, url=None, text=None, article_type=None, angle=None):
    parts = []
    kind = article_type or "analysis"
    if url:
        parts.append(f"Read and analyze this source, then write a {kind} piece about "
                     f"it (use web search to fetch and verify): {url}")
    if topic:
        parts.append(f"Write a {kind} piece about: {topic}.")
    if text:
        parts.append(
            "Here is something I found / my notes. Research it as needed with web "
            f"search, then write a polished {kind} piece based on it:\n\n{text}")
    if angle:
        parts.append(f"Angle / emphasis: {angle}")
    if not parts:
        raise SystemExit("Nothing to write about. Provide --topic, --url, --from-file, "
                         "or use --interactive.")
    instruction = "\n\n".join(parts)
    print("Researching and drafting...")
    article = draft_article(instruction)
    save_post(article, default_tag=kind.capitalize())
    print("Done. Review the draft, then flip 'published: false' to true.")


def run_interactive():
    print("On-demand draft. Paste a link, describe a finding, or paste notes.")
    print("Finish your input with Ctrl-D (Mac/Linux) on a new line.\n")
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("No input received.")
    # If it's just a URL, treat it as a source; otherwise as notes/topic.
    if re.match(r"^https?://\S+$", text):
        run_ondemand(url=text)
    else:
        run_ondemand(text=text)


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
    args = p.parse_args()

    text = None
    if args.from_file:
        with open(args.from_file) as f:
            text = f.read().strip()

    if args.interactive:
        run_interactive()
    elif args.topic or args.url or text:
        run_ondemand(topic=args.topic, url=args.url, text=text,
                     article_type=args.article_type, angle=args.angle)
    else:
        focus = [t.strip() for t in args.focus.split(",")] if args.focus else None
        run_scheduled(args.count, focus=focus)


if __name__ == "__main__":
    main()
