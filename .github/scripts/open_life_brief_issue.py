#!/usr/bin/env python3
"""
open_life_brief_issue.py — deliver the Saturday 'Life' briefs as a GitHub Issue,
so they arrive as a notification instead of sitting in a workflow log.

Unlike the daily pipeline, this never writes a post. The briefs are research
material — subjects, the surprise at their center, verified sources, and the one
question only you can answer. You write only if something grabs you.

Runs inside GitHub Actions. Standard library only. Expects:
  GH_TOKEN          - a token with issues:write (the workflow's GITHUB_TOKEN)
  GITHUB_REPOSITORY - "owner/repo" (provided by Actions)
  BRIEF_FILE        - path to the markdown written by `pipeline.py --life-briefs --out`
"""
import os
import json
import datetime
import urllib.request


def _open_issue(title, body):
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    payload = {
        "title": title,
        "body": body,
        # Assigning you triggers a GitHub email/mobile notification.
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
    today = datetime.date.today().isoformat()
    path = os.environ.get("BRIEF_FILE", "life_briefs.md")
    try:
        with open(path, encoding="utf-8") as f:
            body = f.read().strip()
    except OSError:
        print(f"No brief file at {path}; not opening an issue.")
        return
    if not body:
        print("Brief file is empty; not opening an issue.")
        return

    issue = _open_issue(f"\U0001F3D4️ Saturday reading — {today}", body)
    print(f"Opened Life brief issue #{issue['number']}: {issue['html_url']}")


if __name__ == "__main__":
    main()
