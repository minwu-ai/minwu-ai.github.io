# Min Wu — automated AI blog

A free, static personal website publishing analysis on AI, model risk, and governance.
Posts are surfaced and drafted by an AI pipeline, saved as drafts for review, and
published only when approved. Live at https://minwu-ai.github.io.

## How it works

```
pipeline.py    →  surfaces topics + drafts articles into posts/ as DRAFTS (published: false)
   you         →  review a draft, change "published: false" to "true"
build_site.py  →  turns posts/ + pages/ into a finished website in public/
GitHub Pages   →  serves the site for free at minwu-ai.github.io
```

There is no server to manage. GitHub builds and hosts the site for free.

## The pipeline works two ways

**Scheduled** — runs automatically (see `.github/workflows/daily_pipeline.yml`) to
discover trending AI topics and draft a few posts:

```
python pipeline.py            # draft 2 topics it finds
python pipeline.py --count 3  # draft 3
```

**On demand** — when *you* find something and want a draft about it:

```
python pipeline.py --topic "OpenAI's new agent framework" --type analysis
python pipeline.py --url "https://example.com/some-article"
python pipeline.py --from-file notes.txt
python pipeline.py --interactive     # paste a link or notes, end with Ctrl-D
```

Every draft lands in `posts/` with `published: false`, so nothing goes live until
you approve it.

## Your review routine

1. Open the newest file in `posts/`.
2. Read it, edit anything you want.
3. Change `published: false` to `published: true`.
4. `python build_site.py`, then commit and push.
5. GitHub Pages updates within a minute or so.

## Site structure

- `posts/` — articles (markdown + frontmatter). The review gate lives here.
- `pages/about.md` — the About page content (edit freely).
- `templates/base.html` — design/layout for every page (light + dark).
- `build_site.py` — builds Home, post pages, a Topics index + per-topic pages,
  an About page, RSS, and a 404 into `public/`.
- `public/` — generated output (git-ignored; built in CI on deploy).

## Editing site info

Open `build_site.py` and edit the block near the top (`SITE_NAME`, `AUTHOR`,
`SITE_DESCRIPTION`, `SITE_URL`).

## One-time setup (already done for this repo)

1. Repo on GitHub with Pages enabled (Settings → Pages → Source: GitHub Actions).
2. Anthropic API key stored as a repo Actions secret named `ANTHROPIC_API_KEY`
   (`gh secret set ANTHROPIC_API_KEY --repo minwu-ai/minwu-ai.github.io`).

## Running locally

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...   # only needed for pipeline.py
python pipeline.py                # draft articles
python build_site.py              # build the site into public/
python -m http.server -d public   # preview at http://localhost:8000
```
