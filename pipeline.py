"""
pipeline.py — finds topics, drafts articles, and saves them as markdown posts.

It uses the Claude API to (1) discover trending AI topics and (2) write articles.
Each finished article is saved into posts/ as a markdown file, ready for the site
builder to pick up. New posts are saved as DRAFTS (published: false) so you review
them before they go live.

Run it with:  python pipeline.py
"""

import os
import json
import datetime
import re

import anthropic

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
MODEL = "claude-sonnet-4-5"
POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")

HOW_MANY = 2   # how many articles to draft per run


def discover_topics():
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": (
            "Search for the most discussed AI topics from the last 48 hours. "
            "Focus on model releases, regulation, research, and enterprise AI. "
            "Return ONLY a JSON array, no markdown:\n"
            '[{"topic": "...", "angle": "...", "type": "news|analysis|opinion"}]'
        )}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    text = text.strip().strip("`")
    if text.startswith("json"):
        text = text[4:]
    return json.loads(text)


def draft_article(topic, angle, article_type):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2500,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        system=(
            "You are an AI industry analyst writing for a professional audience. "
            "Tone: clear, authoritative, accessible. Length: 600-900 words. "
            "Use markdown: ## for section headings, normal paragraphs, no H1 "
            "(the title is added separately). Return ONLY JSON, no markdown fences:\n"
            '{"title": "...", "excerpt": "one sentence", "body_markdown": "..."}'
        ),
        messages=[{"role": "user", "content":
                   f"Write a {article_type} piece about: {topic}. Angle: {angle}"}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    text = text.strip().strip("`")
    if text.startswith("json"):
        text = text[4:]
    return json.loads(text)


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]


def save_post(article, article_type):
    today = datetime.date.today().isoformat()
    slug = slugify(article["title"])
    path = os.path.join(POSTS_DIR, f"{slug}.md")
    body = article["body_markdown"].replace('"', '\\"')
    frontmatter = (
        "---\n"
        f'title: "{article["title"]}"\n'
        f"date: {today}\n"
        f"slug: {slug}\n"
        f"tag: {article_type.capitalize()}\n"
        f'excerpt: "{article["excerpt"]}"\n'
        "published: false\n"        # <-- review gate: flip to true to publish
        "---\n\n"
    )
    with open(path, "w") as f:
        f.write(frontmatter + article["body_markdown"] + "\n")
    print(f"  saved draft: posts/{slug}.md")


def run():
    print("Discovering topics...")
    topics = discover_topics()
    for t in topics[:HOW_MANY]:
        print(f"Drafting: {t['topic']}")
        article = draft_article(t["topic"], t["angle"], t["type"])
        save_post(article, t["type"])
    print("Done. Review the new drafts, then flip 'published: false' to true.")


if __name__ == "__main__":
    run()
