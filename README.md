# Min on AI — automated blog

A free, static personal website that publishes AI articles. New drafts are written
automatically by an AI pipeline, saved for your review, and published when you approve.

## How it works

```
pipeline.py   →  writes new articles into posts/ as DRAFTS (hidden)
   you         →  review a draft, change "published: false" to "true"
build_site.py →  turns posts/ into a finished website in public/
GitHub Pages  →  serves the website for free at your domain
```

There is no server to manage. GitHub builds and hosts the site for free.

## The three things only you can do

1. Create a GitHub repository and upload these files.
2. Get an Anthropic API key and add it to the repo (Settings → Secrets → Actions →
   new secret named `ANTHROPIC_API_KEY`).
3. Turn on GitHub Pages (Settings → Pages → Source: GitHub Actions).

That's it. After that:

- The pipeline runs on a schedule and adds drafts.
- You review drafts (flip `published: false` to `true`).
- Every push rebuilds and republishes the site automatically.

## Your daily routine

1. Open the newest file in `posts/`.
2. Read it. Edit anything you want.
3. Change `published: false` to `published: true`.
4. Save and push (or commit in GitHub's web editor).
5. The site updates itself within a minute.

## Editing site info

Open `build_site.py` and edit the block at the top (site name, your name,
description, domain).

## Running it yourself locally (optional)

```
pip install -r requirements.txt
python pipeline.py      # draft new articles
python build_site.py    # build the site into public/
```

Then open `public/index.html` in a browser to preview.
