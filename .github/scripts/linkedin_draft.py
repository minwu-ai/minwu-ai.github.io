#!/usr/bin/env python3
"""
linkedin_draft.py — whenever a post goes live (published: true) that wasn't live
last time this ran, draft a short (<250 word) LinkedIn post for it and open a
GitHub Issue so you can review, edit, and post it yourself. Never posts to
LinkedIn directly.

The draft pulls in: the post's own excerpt, up to two external source links
found in the body, a short bullet summary of the first table if the post has
one (LinkedIn doesn't render markdown tables), a pointer to the full piece if
it has a mermaid diagram instead, and a note if this post links back to an
earlier post that already got a LinkedIn draft (so you can reference that
earlier LinkedIn post).

Runs inside GitHub Actions. Uses only the standard library plus python-frontmatter.
Expects:
  GH_TOKEN          - a token with issues:write (the workflow's GITHUB_TOKEN)
  GITHUB_REPOSITORY - "owner/repo" (provided by Actions)
  GITHUB_SERVER_URL - e.g. https://github.com (provided by Actions)
"""
import os
import re
import json
import urllib.request
from pathlib import Path

import frontmatter

SITE_URL = "https://minwu-ai.github.io"
POSTS_DIR = Path("posts")
STATE_PATH = Path(".github/state/linkedin_drafted_slugs.json")


def live_posts():
    """Mirrors build_site.py's publish gate: archive is always excluded, and a
    missing `published` field defaults to published."""
    posts = {}
    for path in sorted(POSTS_DIR.rglob("*.md")):
        if path.parent.name == "archive":
            continue
        post = frontmatter.load(path)
        if post.get("published", True) is False:
            continue
        slug = post.get("slug", path.stem)
        cover = str(post.get("cover", "")).strip()
        posts[slug] = {
            "title": post.get("title", path.stem),
            "excerpt": post.get("excerpt", ""),
            "tag": post.get("tag", ""),
            "date": str(post.get("date", ""))[:10],
            "cover": "" if cover in ("/assets/", "/assets") or cover.endswith("/") else cover,
            "body": post.content,
        }
    return posts


def hashtags(raw_tag, limit=3):
    values = raw_tag if isinstance(raw_tag, list) else str(raw_tag).split(",")
    tags = []
    for v in values:
        clean = re.sub(r"[^A-Za-z0-9]", "", str(v))
        if clean and clean not in tags:
            tags.append(clean)
    return " ".join(f"#{t}" for t in tags[:limit])


def external_links(body, limit=2):
    """First distinct non-site markdown links in reading order -- usually the
    primary sources (the paper, the lab's post, etc.)."""
    links = []
    for _, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body):
        if SITE_URL in url or url in links:
            continue
        links.append(url)
        if len(links) >= limit:
            break
    return links


def internal_links(body):
    """Slugs this post links to on this site, in reading order -- used to spot
    when a new post builds on one already drafted for LinkedIn."""
    slugs = []
    for s in re.findall(r"https?://minwu-ai\.github\.io/([a-z0-9-]+)/", body):
        if s not in slugs:
            slugs.append(s)
    return slugs


def table_bullets(body, max_rows=3):
    """Convert the first 2-column markdown table into short bullets -- LinkedIn
    doesn't render tables, so this keeps the structured content legible."""
    lines = body.splitlines()
    row_re = re.compile(r"^\s*\|.+\|\s*$")
    sep_re = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
    for i, line in enumerate(lines):
        if row_re.match(line) and i + 1 < len(lines) and sep_re.match(lines[i + 1]):
            rows = []
            for row_line in lines[i + 2:]:
                if not row_re.match(row_line):
                    break
                cells = [c.strip().strip("*") for c in row_line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0]:
                    rows.append((cells[0], cells[1]))
                if len(rows) >= max_rows:
                    break
            if rows:
                return [f"• {k}: {v}" for k, v in rows]
    return []


def draft_text(slug, post):
    lines = [post["title"].strip(), "", post["excerpt"].strip()]

    bullets = table_bullets(post["body"])
    if bullets:
        lines += [""] + bullets
    elif "```mermaid" in post["body"]:
        lines += ["", "\U0001F4CA Full visual breakdown in the piece."]

    lines += ["", f"Full piece: {SITE_URL}/{slug}/"]

    sources = external_links(post["body"])
    if sources:
        label = "Source" if len(sources) == 1 else "Sources"
        lines += [f"{label}: " + " | ".join(sources)]

    tags = hashtags(post["tag"])
    if tags:
        lines += ["", tags]

    return "\n".join(lines)


def open_issue(title, body):
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    payload = {
        "title": title,
        "body": body,
        "assignees": [os.environ.get("REVIEW_ASSIGNEE", "minw0607")],
    }
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues",
        data=json.dumps(payload).encode(), method="POST",
    )
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def load_state():
    state = json.loads(STATE_PATH.read_text())
    # Back-compat: the original state file was a bare list of slugs.
    if isinstance(state, list):
        state = {slug: {} for slug in state}
    return state


def main():
    current = live_posts()
    current_slugs = set(current)

    if not STATE_PATH.exists():
        # First run: seed state with everything already live so we don't open a
        # backlog of issues for posts that were published long before this existed.
        seed = {slug: {"date": current[slug]["date"]} for slug in current_slugs}
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(seed, indent=2, sort_keys=True) + "\n")
        print(f"Seeded state with {len(seed)} already-live posts; no issues opened.")
        return

    state = load_state()
    new_slugs = sorted(current_slugs - set(state), key=lambda s: current[s]["date"])

    if not new_slugs:
        print("No newly published posts since last run.")
        return

    for slug in new_slugs:
        post = current[slug]
        related_issue_url = None
        for ref_slug in internal_links(post["body"]):
            if state.get(ref_slug, {}).get("issue_url"):
                related_issue_url = state[ref_slug]["issue_url"]
                break

        text = draft_text(slug, post)
        word_count = len(text.split())
        title = post["title"]
        issue_title = f"\U0001F517 LinkedIn draft — {title[:80]}"
        notes = []
        if post["cover"]:
            notes.append(f"\U0001F4CE Suggested image to attach: {SITE_URL}{post['cover']}")
        if related_issue_url:
            notes.append(
                f"\U0001F517 This post links back to an earlier one you already drafted "
                f"for LinkedIn: {related_issue_url} — consider referencing that post "
                "if it still fits."
            )
        notes_md = ("\n" + "\n".join(notes) + "\n") if notes else ""
        body_md = (
            f"**Post:** [{title}]({SITE_URL}/{slug}/)\n\n"
            f"Draft below ({word_count} words) — edit as needed, then post it to LinkedIn "
            "yourself. Close this issue once you're done with it (posted or skipped)."
            f"{notes_md}\n"
            "---\n\n"
            f"{text}\n\n"
            "---\n"
        )
        issue = open_issue(issue_title, body_md)
        print(f"Opened #{issue['number']}: {issue['html_url']} ({word_count} words)")
        state[slug] = {"date": post["date"], "issue_url": issue["html_url"]}

    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
