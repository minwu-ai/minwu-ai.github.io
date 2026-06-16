# Workflow — how the blog runs end to end

This is the operating manual for the site. It covers both ways posts get created
(automatic + manual), how review/publishing works, and the knobs you can tune.

---

## The big picture

```
            ┌─────────────────────────┐
 SCHEDULED  │  daily_pipeline.yml      │  weekdays ~8am ET (cron) or manual
 (auto)     │  → pipeline.py           │  → drafts topics in your FOCUS areas
            └───────────┬─────────────┘
                        │ commits drafts (published: false)
                        │ opens a GitHub Issue listing them  ──► you get notified
                        ▼
 MANUAL     ┌─────────────────────────┐
 (on        │  you run pipeline.py     │  --from-file / --interactive / --url
  demand)   │  with a document         │  → 1 draft in your house style
            └───────────┬─────────────┘
                        │
                        ▼
            ┌─────────────────────────┐
 REVIEW     │  posts/<slug>.md         │  read, edit, flip published: false→true
            └───────────┬─────────────┘
                        │ push
                        ▼
            ┌─────────────────────────┐
 PUBLISH    │  build_and_deploy.yml    │  builds + deploys to GitHub Pages
            │  → build_site.py         │  live at minwu-ai.github.io
            └─────────────────────────┘
```

**Nothing is ever published automatically.** Every draft is `published: false` until
you change it. The review gate is enforced in `build_site.py` (it skips unpublished
posts).

---

## 1. Scheduled (automatic) drafting

- **When:** weekdays at 12:00 UTC (~8am ET), via `cron` in
  `.github/workflows/daily_pipeline.yml`. Also runnable on demand from the Actions
  tab → "Run workflow."
- **What it does:** asks Claude (with live web search) for the day's most significant
  AI developments, **prioritizing your `FOCUS_TOPICS`** and **preferring your
  `PREFERRED_SOURCES`**, then drafts ~2 posts.
- **Output:** new files in `posts/` as `published: false`, committed by "Draft Bot."
- **Notification:** the workflow then opens a **GitHub Issue** ("📝 N new drafts to
  review …") with edit/view links for each draft.

To get pinged: on the repo, **Watch → All Activity** (or Custom → Issues).

## 2. Manual (on-demand) drafting — your recommendation process

You only supply the document; voice, length, structure, output format, and source
preferences are fixed in code, so you never retype instructions.

```bash
# paste an article you read (e.g. a WSJ piece) into a file, then:
python pipeline.py --from-file my-doc.txt

# or paste it inline:
python pipeline.py --interactive          # paste, then Ctrl-D

# or point at a public URL:
python pipeline.py --url "https://…"

# optional knobs:
python pipeline.py --from-file my-doc.txt --type governance --angle "impact on MRM"
```

A fed document becomes an **original analysis in the blog's risk/governance voice**
— it won't just summarize. Result: one draft in `posts/`, `published: false`.

> **Paywalled sources (WSJ, etc.):** web search can prefer and cite them but can't
> read full paywalled text, and credentialed scraping is out (ToS + public-repo
> security). For an article you've read as a subscriber, paste it via `--from-file`
> / `--interactive` — that's the supported path.

## 3. Review & publish

1. Open the new file in `posts/` (or use the link in the review Issue).
2. Read it. **Verify factual claims** — these are AI-drafted.
3. Edit as needed; change `published: false` → `published: true`.
4. Commit & push (or just edit in GitHub's web UI and commit).
5. `build_and_deploy.yml` rebuilds and deploys; live in ~a minute.

(Locally you can preview first: `python build_site.py` then open `public/`.)

---

## Tuning knobs (top of `pipeline.py`)

| Setting | Controls | Override per run |
|---|---|---|
| `FOCUS_TOPICS` | themes the scheduled run prioritizes | `--focus "a, b, c"` |
| `PREFERRED_SOURCES` | outlets to prefer & cite (search stays web-wide) | — |
| `DRAFT_SYSTEM` | house voice, length, structure, output format | — |
| `MODEL` | which Claude model drafts | — |
| `HOW_MANY` / `--count` | posts per scheduled run | `--count N` |

Site identity (name, author, description, URL) lives at the top of `build_site.py`.

## Dry run (preview the prompts without calling the API)

```bash
python pipeline.py --from-file my-doc.txt --type governance --dry-run
```

Prints the exact system prompt + instruction that *would* be sent, and the draft
filename that *would* be written — no API call, no tokens spent, no file created.

## Requirements / setup (already done)

- `ANTHROPIC_API_KEY` set as a repo Actions secret (for the scheduled run) and in
  your local env (for manual runs): `export ANTHROPIC_API_KEY=sk-…`.
- GitHub Pages enabled (Settings → Pages → Source: GitHub Actions).
- `pip install -r requirements.txt` for local use.
