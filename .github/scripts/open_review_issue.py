#!/usr/bin/env python3
"""
open_review_issue.py — after the daily pipeline commits new drafts, open a GitHub
Issue that lists them with direct edit/view links, so you get a notification and a
ready-to-act review checklist instead of having to dig through the repo.

Runs inside GitHub Actions. Uses only the standard library. Expects:
  GH_TOKEN          - a token with issues:write (the workflow's GITHUB_TOKEN)
  GITHUB_REPOSITORY - "owner/repo" (provided by Actions)
  GITHUB_SERVER_URL - e.g. https://github.com (provided by Actions)
"""
import os
import json
import datetime
import subprocess
import urllib.request


def added_drafts():
    """Markdown files under posts/ added in the most recent commit."""
    out = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r",
         "--diff-filter=A", "HEAD", "--", "posts/"],
        capture_output=True, text=True,
    ).stdout
    return [ln for ln in out.splitlines() if ln.endswith(".md")]


def title_of(path):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("title:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return os.path.basename(path)


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
    repo = os.environ["GITHUB_REPOSITORY"]
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    today = datetime.date.today().isoformat()

    # Empty-run mode: the pipeline saved no drafts — notify so it never goes silent.
    if os.environ.get("REVIEW_EMPTY") == "1":
        body = (
            "Today's pipeline ran but published **no new drafts** — it didn't find a "
            "topic it could corroborate against the trusted-source bar (≥1 priority "
            "source, or ≥2 outside sources). No action needed; this is the guardrail "
            "working. You can run it again from the "
            f"[Actions tab]({server}/{repo}/actions/workflows/daily_pipeline.yml) if "
            "you'd like to retry.")
        issue = _open_issue(f"ℹ️ No corroborated topics today — {today}", body)
        print(f"Opened empty-run notice #{issue['number']}: {issue['html_url']}")
        return

    drafts = added_drafts()
    if not drafts:
        print("No new drafts; not opening an issue.")
        return

    lines = [
        f"The daily pipeline drafted **{len(drafts)} new post(s)** for your review. "
        "They're hidden on the live site (`published: false`) until you approve.\n",
        "**To publish one:** open it, edit if needed, change `published: false` to "
        "`published: true`, and commit. The site rebuilds automatically.\n",
    ]
    for path in drafts:
        edit = f"{server}/{repo}/edit/main/{path}"
        view = f"{server}/{repo}/blob/main/{path}"
        lines.append(f"- [ ] **{title_of(path)}** — [edit]({edit}) · [view]({view}) · `{path}`")

    issue = _open_issue(
        f"\U0001F4DD {len(drafts)} new draft(s) to review — {today}", "\n".join(lines))
    print(f"Opened review issue #{issue['number']}: {issue['html_url']}")


if __name__ == "__main__":
    main()
