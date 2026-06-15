"""
build_site.py — turns markdown files in posts/ into a finished website in public/

Run it with:  python build_site.py
Your articles live in posts/ as markdown files. This reads them, wraps them in
the design template, and writes ready-to-serve HTML into public/.
"""

import os
import shutil
import datetime
from pathlib import Path

import markdown
import frontmatter
from jinja2 import Template

# ----------------------------------------------------------------------
# EDIT THESE — your site's basic info
# ----------------------------------------------------------------------
SITE_NAME = "Min on AI"
SITE_NAME_HTML = 'Min<span> / AI</span>'   # the <span> part shows in the accent color
AUTHOR = "Min Wu"
SITE_DESCRIPTION = "Analysis and commentary on AI, model risk, and governance."
SITE_URL = "https://example.com"   # change to your real domain once you have one
# ----------------------------------------------------------------------

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
PUBLIC_DIR = ROOT / "public"
TEMPLATE = Template((ROOT / "templates" / "base.html").read_text())

md = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])


def render_page(page_title, page_description, inner_html):
    return TEMPLATE.render(
        page_title=page_title,
        page_description=page_description,
        site_name=SITE_NAME,
        site_name_html=SITE_NAME_HTML,
        author=AUTHOR,
        year=datetime.date.today().year,
        content=inner_html,
    )


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
            "slug": slug, "excerpt": excerpt, "tag": tag, "body_html": body_html,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build():
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir()

    posts = load_posts()

    # ---- Home page ----
    items = ['<div class="eyebrow">Latest</div>',
             '<h1 class="page">{}</h1>'.format(SITE_NAME),
             '<p class="lede">{}</p>'.format(SITE_DESCRIPTION),
             '<ul class="post-list">']
    for p in posts:
        tag_html = '<div class="tag">{}</div>'.format(p["tag"]) if p["tag"] else ""
        items.append(
            '<li class="post-item">'
            '<div class="date">{date}</div>'
            '<h2><a href="/{slug}/">{title}</a></h2>'
            '<p>{excerpt}</p>{tag}'
            '</li>'.format(date=p["date_str"], slug=p["slug"],
                           title=p["title"], excerpt=p["excerpt"], tag=tag_html)
        )
    items.append("</ul>")
    (PUBLIC_DIR / "index.html").write_text(
        render_page(SITE_NAME, SITE_DESCRIPTION, "\n".join(items))
    )

    # ---- Individual post pages ----
    for p in posts:
        tag_html = '<span class="tag">{}</span>'.format(p["tag"]) if p["tag"] else ""
        inner = (
            '<a class="back" href="/">← All posts</a>'
            '<article class="post">'
            '<div class="meta">{date} · {tag}</div>'
            '<h1>{title}</h1>{body}'
            '</article>'
        ).format(date=p["date_str"], tag=p["tag"] or "Article",
                 title=p["title"], body=p["body_html"])
        post_dir = PUBLIC_DIR / p["slug"]
        post_dir.mkdir(exist_ok=True)
        (post_dir / "index.html").write_text(
            render_page("{} — {}".format(p["title"], SITE_NAME),
                        p["excerpt"] or SITE_DESCRIPTION, inner)
        )

    # ---- RSS feed ----
    build_rss(posts)

    # ---- CNAME for custom domain (GitHub Pages reads this) ----
    # Uncomment and set your domain once you have one:
    # (PUBLIC_DIR / "CNAME").write_text("yourdomain.com")

    print("Built {} posts into public/".format(len(posts)))


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
