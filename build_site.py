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
SITE_DESCRIPTION = "Analysis and commentary on Frontier AI safety, alignment, evaluation, and governance."
SITE_URL = "https://minwu-ai.github.io"

# Small kicker shown above your name on the home page (was a duplicate "Min Wu").
HOME_EYEBROW = "Home"
# Epigraph under the home lede: (quote, attribution). Set HOME_QUOTE = None to hide.
HOME_QUOTE = (
    "Uncertainty is the only certainty there is, and knowing how to live with "
    "insecurity is the only security.",
    "John Allen Paulos",
)

# Contact / social links shown in the footer (all pages) and the home hero.
SOCIAL_LINKS = {
    "LinkedIn": "https://www.linkedin.com/in/wumin2021/",
    "GitHub": "https://github.com/minw0607",
    "Email": "mailto:min.wu.2020@gmail.com",
}

# Curated topics shown on the Topics page (in this order), even when empty.
# A post joins a topic when its `tag` matches the topic name. Edit freely.
TOPICS = [
    ("AI Governance", "Frameworks, model risk, and accountability for AI systems."),
    ("AI Safety", "Keeping increasingly capable systems controllable and secure."),
    ("Alignment", "Making AI systems pursue what we actually intend."),
    ("Evaluation", "Measuring capability, safety, and reliability of models."),
    ("Agentic AI", "Systems that take actions, not just generate text."),
    ("Regulation & Policy", "Laws, standards, and the politics shaping AI."),
    ("Industry", "Model releases, labs, and the business of AI."),
    ("Life", "Notes and photos from outside the work."),
]

# Projects shown on the Projects page. Each links to its repo. Edit freely.
# (name, short description, repo URL). The shared avatar is assets/axiom-avatar.svg.
PROJECT_AVATAR = "/assets/axiom-avatar.svg"
PROJECTS = [
    ("Regulus",
     "AI governance standards lookup powered by RAG and knowledge graphs — retrieves "
     "applicable risks and cross-referenced guidance across NIST AI RMF, SR 26-2, the "
     "EU AI Act, and more.",
     "https://github.com/minw0607/Regulus"),
    ("LLM Red Teaming",
     "A modular toolkit for red teaming LLMs — adversarial attacks, jailbreak "
     "evaluation (JailbreakBench), and prompt injection, with pluggable targets and "
     "automated judges. Built for AI safety practitioners.",
     "https://github.com/minw0607/llm_red_teaming"),
    ("GenAI Capability Bench",
     "A modular benchmark suite evaluating GenAI across accuracy, truthfulness, "
     "instruction following, reasoning, RAG, tool use, and agentic task completion.",
     "https://github.com/minw0607/genai_capability_bench"),
    ("Multi-Agent OTel Eval",
     "Enterprise-grade GenAI observability and evaluation using OpenTelemetry "
     "conventions, with multi-agent orchestration tested on the Mind2Web benchmark.",
     "https://github.com/minw0607/multi_agent_otel_eval"),
    ("RAG Eval Framework",
     "Provider-agnostic RAG evaluation benchmarked on HotpotQA — 13 metrics, "
     "multi-prompt comparison, failure diagnosis, and an auto-generated audit report.",
     "https://github.com/minw0607/rag_eval_framework"),
    ("Geometric Knowledge Network",
     "A lightweight geometric knowledge network that augments vector RAG with "
     "document-grounded graph structure, hybrid retrieval, and evaluation.",
     "https://github.com/minw0607/geometric_knowledge_network"),
    ("ML Validation Framework",
     "Interactive ML model validation — explainability, weak spots, robustness, and "
     "fairness — widget-driven, no-code demo.",
     "https://github.com/minw0607/ml_validation_framework"),
]
# ----------------------------------------------------------------------

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
PAGES_DIR = ROOT / "pages"
ASSETS_DIR = ROOT / "assets"
PUBLIC_DIR = ROOT / "public"
TEMPLATE = Template((ROOT / "templates" / "base.html").read_text())

md = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])


def render_page(page_title, page_description, inner_html,
                nav_active="", canonical_path="/", og_type="website", wide=False):
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
        wide=wide,
        social_html=social_links_html(),
    )


# Social / contact icons (inline SVG, fill=currentColor).
_SOCIAL_ICONS = {
    "LinkedIn": '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>',
    "GitHub": '<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222 0 1.606-.014 2.898-.014 3.293 0 .322.216.694.825.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>',
    "Email": '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>',
}


def social_links_html(extra_class=""):
    cls = ("social-row " + extra_class).strip()
    items = []
    for name, url in SOCIAL_LINKS.items():
        ext = "" if url.startswith("mailto:") else ' target="_blank" rel="noopener"'
        items.append(
            '<a href="{url}"{ext} aria-label="{name}" title="{name}">'
            '<svg viewBox="0 0 24 24" aria-hidden="true">{icon}</svg></a>'.format(
                url=url, ext=ext, name=name, icon=_SOCIAL_ICONS[name]))
    return '<div class="{cls}">{items}</div>'.format(cls=cls, items="".join(items))


# Small "copy link / share" control (wired up by JS in the template).
SHARE_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
              '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>'
              '<polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>')


def share_button(url, label="Copy link", icon_only=False):
    cls = "share-btn icon-only" if icon_only else "share-btn"
    text = "" if icon_only else '<span>{}</span>'.format(label)
    aria = "Share or copy link"
    return ('<button class="{cls}" type="button" data-share-url="{url}" '
            'aria-label="{aria}" title="{aria}">{icon}{text}</button>').format(
                cls=cls, url=url, aria=aria, icon=SHARE_ICON, text=text)


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
        takeaway = post.get("takeaway", "")
        md.reset()
        body_html = md.convert(post.content)
        posts.append({
            "title": title, "date": date, "date_str": date.strftime("%b %d, %Y"),
            "slug": slug, "excerpt": excerpt, "tag": tag, "takeaway": takeaway,
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
    quote_html = ""
    if HOME_QUOTE:
        quote_html = (
            '<figure class="epigraph"><blockquote>“{q}”</blockquote>'
            '<figcaption>— {a}</figcaption></figure>'
        ).format(q=HOME_QUOTE[0], a=HOME_QUOTE[1])
    home = (
        '<section class="hero">'
        '<div class="eyebrow">{eyebrow}</div>'
        '<h1>{name}</h1>'
        '<p class="lede">{desc}</p>'
        '{quote}'
        '{social}'
        '</section>'
        '<div class="eyebrow">Latest writing</div>'
        '{listing}'
    ).format(eyebrow=HOME_EYEBROW, name=SITE_NAME, desc=SITE_DESCRIPTION,
             quote=quote_html, social=social_links_html("hero-social"), listing=listing)
    (PUBLIC_DIR / "index.html").write_text(
        render_page(SITE_NAME, SITE_DESCRIPTION, home,
                    nav_active="home", canonical_path="/", wide=True)
    )

    # ---- Individual post pages ----
    for p in posts:
        tag_link = ('<a class="tag" href="/topics/{ts}/">{t}</a>'.format(ts=p["tag_slug"], t=p["tag"])
                    if p["tag"] else "general")
        post_url = "{}/{}/".format(SITE_URL, p["slug"])
        takeaway_html = ""
        if p["takeaway"]:
            takeaway_html = (
                '<div class="takeaway"><span class="takeaway-label">1-minute takeaway</span>'
                '<p>{}</p></div>').format(p["takeaway"])
        inner = (
            '<a class="back" href="/">← All posts</a>'
            '<article class="post">'
            '<div class="meta">{date} · {tag}</div>'
            '<h1>{title}</h1>{takeaway}{body}'
            '<div class="post-footer"><span>Written by {author}. Filed under {tag_link}.</span>'
            '{share}</div>'
            '</article>'
        ).format(date=p["date_str"], tag=p["tag"] or "Article",
                 title=p["title"], takeaway=takeaway_html, body=p["body_html"],
                 author=AUTHOR, tag_link=tag_link, share=share_button(post_url))
        post_dir = PUBLIC_DIR / p["slug"]
        post_dir.mkdir(exist_ok=True)
        (post_dir / "index.html").write_text(
            render_page("{} — {}".format(p["title"], SITE_NAME),
                        p["excerpt"] or SITE_DESCRIPTION, inner,
                        canonical_path="/{}/".format(p["slug"]), og_type="article")
        )

    # ---- Topics: index + one page per tag ----
    build_topics(posts)

    # ---- Projects page ----
    build_projects()

    # ---- About page (from pages/about.md if present) ----
    build_about()

    # ---- RSS feed ----
    build_rss(posts)

    # ---- Static assets (images, etc.) copied through to /assets ----
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, PUBLIC_DIR / "assets")

    # ---- 404 ----
    nf = ('<div class="eyebrow">404</div><h1 class="page">Page not found</h1>'
          '<p class="lede">That page doesn\'t exist. <a href="/">Back to home</a>.</p>')
    (PUBLIC_DIR / "404.html").write_text(
        render_page("Not found — " + SITE_NAME, "Page not found", nf,
                    canonical_path="/404.html"))

    print("Built {} published posts into public/".format(len(posts)))


def build_topics(posts):
    # Group published posts by their tag (matched to a curated topic name).
    by_name = {}
    for p in posts:
        if p["tag"]:
            by_name.setdefault(p["tag"], []).append(p)

    topics_dir = PUBLIC_DIR / "topics"
    topics_dir.mkdir(exist_ok=True)

    # Topics index — every curated topic appears, even with zero posts.
    cards = ['<div class="eyebrow">Browse</div>',
             '<h1 class="page">Topics</h1>',
             '<p class="lede">Writing grouped by theme.</p>',
             '<ul class="topic-grid">']
    for name, desc in TOPICS:
        ts = slugify(name)
        items = by_name.get(name, [])
        n = len(items)
        count = "{} post{}".format(n, "" if n == 1 else "s") if n else "Coming soon"
        cards.append(
            '<li class="topic-card"><a href="/topics/{ts}/">'
            '<span class="topic-name">{name}</span>'
            '<span class="desc">{desc}</span>'
            '<span class="count">{count}</span></a></li>'.format(
                ts=ts, name=name, desc=desc, count=count))
    cards.append('</ul>')
    (topics_dir / "index.html").write_text(
        render_page("Topics — " + SITE_NAME, "Browse writing by topic",
                    "\n".join(cards), nav_active="topics", canonical_path="/topics/",
                    wide=True))

    # One page per curated topic.
    for name, desc in TOPICS:
        ts = slugify(name)
        items = by_name.get(name, [])
        n = len(items)
        if items:
            body = '<p class="lede">{n} post{s} on {name}.</p>{listing}'.format(
                n=n, s="" if n == 1 else "s", name=name,
                listing=post_list_html(items))
        else:
            body = ('<p class="lede">{desc}</p>'
                    '<p>No posts here yet — check back soon.</p>').format(desc=desc)
        inner = (
            '<a class="back" href="/topics/">← All topics</a>'
            '<div class="eyebrow">Topic</div>'
            '<h1 class="page">{name}</h1>{body}'
        ).format(name=name, body=body)
        d = topics_dir / ts
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(
            render_page("{} — {}".format(name, SITE_NAME),
                        desc, inner,
                        nav_active="topics", canonical_path="/topics/{}/".format(ts)))


def build_projects():
    head = (
        '<div class="page-head">'
        '<div class="page-head-text">'
        '<div class="eyebrow">Building</div>'
        '<h1 class="page">Projects</h1>'
        '<p class="lede">Open-source tools I build around AI safety, evaluation, and '
        'governance. Each links to its repository.</p>'
        '</div>'
        '<img class="page-logo" src="{avatar}" alt="Axiom" width="120" height="120">'
        '</div>'
    ).format(avatar=PROJECT_AVATAR)
    cards = [head, '<ul class="project-grid">']
    for name, desc, url in PROJECTS:
        cards.append(
            '<li class="project-card">'
            '<a class="card-link" href="{url}" target="_blank" rel="noopener">'
            '<div class="project-body"><span class="project-name">{name} '
            '<span class="project-arrow">↗</span></span>'
            '<span class="project-desc">{desc}</span></div></a>'
            '{share}'
            '</li>'.format(url=url, name=name, desc=desc,
                           share=share_button(url, icon_only=True)))
    cards.append('</ul>')
    d = PUBLIC_DIR / "projects"
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(
        render_page("Projects — " + SITE_NAME,
                    "Open-source AI safety, evaluation, and governance tools by " + AUTHOR,
                    "\n".join(cards), nav_active="projects", canonical_path="/projects/",
                    wide=True))


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
