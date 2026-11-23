#!/usr/bin/env python3
"""
linkedin_draft.py — whenever a post goes live (published: true) that wasn't live
last time this ran, draft a short LinkedIn post for it and open a GitHub Issue so
you can review, edit, and post it yourself. Never posts to LinkedIn directly.

Runs inside GitHub Actions. Uses only the standard library plus python-frontmatter.
Expects:
  GH_TOKEN          - a token with issues:write (the workflow's GITHUB_TOKEN)
  GITHUB_REPOSITORY - "owner/repo" (provided by Actions)
  GITHUB_SERVER_URL - e.g. https://github.com (provided by Actions)
"""
import os
import re
import json
import datetime
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
        posts[slug] = {
            "title": post.get("title", path.stem),
            "excerpt": post.get("excerpt", ""),
            "takeaway": post.get("takeaway", ""),
            "tag": post.get("tag", ""),
            "date": str(post.get("date", ""))[:10],
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


def draft_text(slug, post):
    url = f"{SITE_URL}/{slug}/"
    parts = [post["title"].strip(), "", post["excerpt"].strip(), "", f"Read the full piece: {url}"]
    tags = hashtags(post["tag"])
    if tags:
        parts += ["", tags]
    return "\n".join(parts)


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


def main():
    current = live_posts()
    current_slugs = set(current)

    if not STATE_PATH.exists():
        # First run: seed state with everything already live so we don't open a
        # backlog of issues for posts that were published long before this existed.
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(sorted(current_slugs), indent=2) + "\n")
        print(f"Seeded state with {len(current_slugs)} already-live posts; no issues opened.")
        return

    previous_slugs = set(json.loads(STATE_PATH.read_text()))
    new_slugs = sorted(current_slugs - previous_slugs, key=lambda s: current[s]["date"])

    if not new_slugs:
        print("No newly published posts since last run.")
        return

    for slug in new_slugs:
        post = current[slug]
        text = draft_text(slug, post)
        title = post["title"]
        issue_title = f"\U0001F517 LinkedIn draft — {title[:80]}"
        body = (
            f"**Post:** [{title}]({SITE_URL}/{slug}/)\n\n"
            "Draft below — edit as needed, then post it to LinkedIn yourself. "
            "Close this issue once you're done with it (posted or skipped).\n\n"
            "---\n\n"
            f"{text}\n\n"
            "---\n"
        )
        issue = open_issue(issue_title, body)
        print(f"Opened #{issue['number']}: {issue['html_url']}")

    STATE_PATH.write_text(json.dumps(sorted(current_slugs), indent=2) + "\n")


if __name__ == "__main__":
    main()
