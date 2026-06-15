"""
build_site.py — turns markdown in posts/ (and pages/) into a finished website in public/

Run it with:  python build_site.py

Articles live in posts/ as markdown files; standalone pages (e.g. About) live in
pages/. This reads them, wraps them in templates/base.html, and writes ready-to-serve
HTML into public/. Posts with "published: false" are skipped (the review gate).
"""

import os
import re
import shutil
import datetime
from pathlib import Path

import markdown
import frontmatter
from jinja2 import Template

# ----------------------------------------------------------------------
# EDIT THESE — your site's basic info
# ----------------------------------------------------------------------
SITE_NAME = "Min Wu"
SITE_NAME_HTML = 'Min<span> Wu</span>'   # the <span> part shows in the accent color
AUTHOR = "Min Wu"
SITE_DESCRIPTION = "Analysis and commentary on AI, model risk, and governance."
SITE_URL = "https://minwu-ai.github.io"
# ----------------------------------------------------------------------

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
PAGES_DIR = ROOT / "pages"
PUBLIC_DIR = ROOT / "public"
TEMPLATE = Template((ROOT / "templates" / "base.html").read_text())

md = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])


def render_page(page_title, page_description, inner_html,
                nav_active="", canonical_path="/", og_type="website"):
    return TEMPLATE.render(
        page_title=page_title,
        page_description=page_description,
        site_name=SITE_NAME,
        site_name_html=SITE_NAME_HTML,
        site_url=SITE_URL,
        author=AUTHOR,
        year=datetime.date.today().year,
        content=inner_html,
        nav_active=nav_active,
        canonical_path=canonical_path,
        og_type=og_type,
    )


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def load_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        post = frontmatter.load(path)
        # Review gate: posts with "published: false" are hidden until you approve.
        # (Posts with no "published" field are treated as published.)
        if post.get("published", True) is False:
            continue
        title = post.get("title", path.stem)
        date_str = str(post.get("date", datetime.date.today().isoformat()))[:10]
        try:
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            date = datetime.date.today()
        slug = post.get("slug", path.stem)
        excerpt = post.get("excerpt", "")
        tag = post.get("tag", "")
        md.reset()
        body_html = md.convert(post.content)
        posts.append({
            "title": title, "date": date, "date_str": date.strftime("%b %d, %Y"),
            "slug": slug, "excerpt": excerpt, "tag": tag,
            "tag_slug": slugify(tag) if tag else "", "body_html": body_html,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def post_list_html(posts):
    items = ['<ul class="post-list">']
    for p in posts:
        tag_html = ('<a class="tag" href="/topics/{ts}/">{t}</a>'.format(ts=p["tag_slug"], t=p["tag"])
                    if p["tag"] else "")
        items.append(
            '<li class="post-item">'
            '<div class="date">{date}</div>'
            '<h2><a href="/{slug}/">{title}</a></h2>'
            '<p>{excerpt}</p>{tag}'
            '</li>'.format(date=p["date_str"], slug=p["slug"],
                           title=p["title"], excerpt=p["excerpt"], tag=tag_html)
        )
    items.append("</ul>")
    return "\n".join(items)


def build():
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir()

    posts = load_posts()

    # ---- Home page (hero + latest posts) ----
    if posts:
        listing = post_list_html(posts)
    else:
        listing = '<p class="lede">No posts published yet — drafts are awaiting review.</p>'
    home = (
        '<section class="hero">'
        '<div class="eyebrow">Min Wu</div>'
        '<h1>{name}</h1>'
        '<p class="lede">{desc}</p>'
        '</section>'
        '<div class="eyebrow">Latest writing</div>'
        '{listing}'
    ).format(name=SITE_NAME, desc=SITE_DESCRIPTION, listing=listing)
    (PUBLIC_DIR / "index.html").write_text(
        render_page(SITE_NAME, SITE_DESCRIPTION, home,
                    nav_active="home", canonical_path="/")
    )

    # ---- Individual post pages ----
    for p in posts:
        tag_link = ('<a class="tag" href="/topics/{ts}/">{t}</a>'.format(ts=p["tag_slug"], t=p["tag"])
                    if p["tag"] else "general")
        inner = (
            '<a class="back" href="/">← All posts</a>'
            '<article class="post">'
            '<div class="meta">{date} · {tag}</div>'
            '<h1>{title}</h1>{body}'
            '<div class="post-footer">Written by {author}. Filed under {tag_link}.</div>'
            '</article>'
        ).format(date=p["date_str"], tag=p["tag"] or "Article",
                 title=p["title"], body=p["body_html"], author=AUTHOR,
                 tag_link=tag_link)
        post_dir = PUBLIC_DIR / p["slug"]
        post_dir.mkdir(exist_ok=True)
        (post_dir / "index.html").write_text(
            render_page("{} — {}".format(p["title"], SITE_NAME),
                        p["excerpt"] or SITE_DESCRIPTION, inner,
                        canonical_path="/{}/".format(p["slug"]), og_type="article")
        )

    # ---- Topics: index + one page per tag ----
    build_topics(posts)

    # ---- About page (from pages/about.md if present) ----
    build_about()

    # ---- RSS feed ----
    build_rss(posts)

    # ---- 404 ----
    nf = ('<div class="eyebrow">404</div><h1 class="page">Page not found</h1>'
          '<p class="lede">That page doesn\'t exist. <a href="/">Back to home</a>.</p>')
    (PUBLIC_DIR / "404.html").write_text(
        render_page("Not found — " + SITE_NAME, "Page not found", nf,
                    canonical_path="/404.html"))

    print("Built {} published posts into public/".format(len(posts)))


def build_topics(posts):
    tags = {}
    for p in posts:
        if not p["tag"]:
            continue
        tags.setdefault(p["tag_slug"], {"name": p["tag"], "posts": []})
        tags[p["tag_slug"]]["posts"].append(p)

    # Topics index
    cards = ['<div class="eyebrow">Browse</div>',
             '<h1 class="page">Topics</h1>',
             '<p class="lede">Writing grouped by theme.</p>']
    if tags:
        cards.append('<ul class="topic-grid">')
        for ts, data in sorted(tags.items(), key=lambda kv: kv[1]["name"].lower()):
            n = len(data["posts"])
            cards.append(
                '<li class="topic-card"><a href="/topics/{ts}/">{name}</a>'
                '<span class="count">{n} post{s}</span></li>'.format(
                    ts=ts, name=data["name"], n=n, s="" if n == 1 else "s"))
        cards.append('</ul>')
    else:
        cards.append('<p>No topics yet.</p>')
    topics_dir = PUBLIC_DIR / "topics"
    topics_dir.mkdir(exist_ok=True)
    (topics_dir / "index.html").write_text(
        render_page("Topics — " + SITE_NAME, "Browse writing by topic",
                    "\n".join(cards), nav_active="topics", canonical_path="/topics/"))

    # Per-tag pages
    for ts, data in tags.items():
        n = len(data["posts"])
        inner = (
            '<a class="back" href="/topics/">← All topics</a>'
            '<div class="eyebrow">Topic</div>'
            '<h1 class="page">{name}</h1>'
            '<p class="lede">{n} post{s} on {name}.</p>{listing}'
        ).format(name=data["name"], n=n, s="" if n == 1 else "s",
                 listing=post_list_html(data["posts"]))
        d = topics_dir / ts
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(
            render_page("{} — {}".format(data["name"], SITE_NAME),
                        "Posts on " + data["name"], inner,
                        nav_active="topics", canonical_path="/topics/{}/".format(ts)))


def build_about():
    about_md = PAGES_DIR / "about.md"
    if about_md.exists():
        page = frontmatter.load(about_md)
        title = page.get("title", "About")
        md.reset()
        body = md.convert(page.content)
    else:
        title = "About"
        body = "<p>{}</p>".format(SITE_DESCRIPTION)
    inner = ('<div class="eyebrow">About</div>'
             '<h1 class="page">{title}</h1>'
             '<div class="prose">{body}</div>').format(title=title, body=body)
    d = PUBLIC_DIR / "about"
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(
        render_page("About — " + SITE_NAME, "About " + AUTHOR, inner,
                    nav_active="about", canonical_path="/about/"))


def build_rss(posts):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    entries = []
    for p in posts[:20]:
        pub = datetime.datetime.combine(p["date"], datetime.time()).strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        entries.append(
            "<item><title>{title}</title>"
            "<link>{url}/{slug}/</link>"
            "<guid>{url}/{slug}/</guid>"
            "<pubDate>{pub}</pubDate>"
            "<description>{desc}</description></item>".format(
                title=p["title"], url=SITE_URL, slug=p["slug"],
                pub=pub, desc=p["excerpt"])
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        "<title>{name}</title><link>{url}</link>"
        "<description>{desc}</description><lastBuildDate>{now}</lastBuildDate>"
        "{items}</channel></rss>"
    ).format(name=SITE_NAME, url=SITE_URL, desc=SITE_DESCRIPTION,
             now=now, items="".join(entries))
    (PUBLIC_DIR / "feed.xml").write_text(rss)


if __name__ == "__main__":
    build()
