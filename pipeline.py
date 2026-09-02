"""
pipeline.py — surfaces AI topics, researches them, and drafts articles as markdown.

It uses the Claude API to (1) discover topics and (2) write articles with web search.
Every article is saved into posts/unpublished/ as a DRAFT (published: false) so you review it
before it goes live. It works two ways:

  SCHEDULED (auto-discover trending topics and draft a few):
      python pipeline.py
      python pipeline.py --count 3

  ON DEMAND (you found something and want a draft about it):
      python pipeline.py --topic "OpenAI's new agent framework" --type analysis
      python pipeline.py --url "https://example.com/some-article"
      python pipeline.py --from-file notes.txt
      python pipeline.py --interactive          # paste/describe it at the prompt

Requires ANTHROPIC_API_KEY in the environment.
"""

import os
import sys
import glob
import json
import argparse
import datetime
import re

import anthropic

_client = None


def get_client():
    """Lazily create the Anthropic client (reads ANTHROPIC_API_KEY from the env)."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


# Sonnet 5 is both newer and cheaper than Sonnet 4.6: $2/$10 per MTok
# against $3/$15, roughly a third off a bill that is ~90% input tokens.
# Note: unlike 4.6, omitting `thinking` on Sonnet 5 runs ADAPTIVE thinking
# rather than none, so drafts may reason more (and bill some output tokens
# for it). Set thinking={"type": "disabled"} here to restore 4.6 behaviour.
MODEL = "claude-sonnet-5"

# Sonnet 5 runs ADAPTIVE thinking when `thinking` is omitted, unlike 4.6 which
# ran none. Thinking tokens count against max_tokens, which truncated the
# discovery call's JSON mid-string on the first run. This pipeline wants
# structured output within a fixed budget, not reasoning, so thinking is off.
THINKING = {"type": "disabled"}

# Drafts per weekday (Monday is 0). Tuesdays and Thursdays are deliberately
# lighter: one draft instead of two. That trims API spend and leaves room to
# revisit the unpublished backlog and reuse a draft already paid for, rather
# than always producing something new. Saturday is handled separately
# (History & People) and Sunday does not run.
DAILY_COUNTS = {0: 2, 1: 1, 2: 2, 3: 1, 4: 2}      # Mon-Fri
DEFAULT_COUNT = 2


def drafts_for_today():
    """Default number of drafts for today, unless --count overrides it."""
    return DAILY_COUNTS.get(datetime.date.today().weekday(), DEFAULT_COUNT)

POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")

# Topics the scheduled run should prioritize when surfacing the day's news.
# Edit this list freely. Override for a single run with --focus "a, b, c".
# Kept deliberately even across the categories — a focus list weighted toward
# safety/governance produces a site weighted toward safety/governance.
FOCUS_TOPICS = [
    "agentic AI, autonomous systems, and real-world agent deployments",
    "evaluation, benchmarking, red-teaming results, and audit methodology",
    "alignment research and interpretability findings",
    "enterprise AI adoption, vendor and market moves, and deployment economics",
    "AI regulation, policy, and enforcement",
    "AI safety incidents and frontier model releases",
    "model risk management and AI governance (SR 26-2)",
    "academic research on AI safety, interpretability, evaluation, auditing, and risk "
    "(arXiv papers and the followed researchers below)",
]

# Academic researchers to follow — surface and read their NEW papers/writing (arXiv,
# Google Scholar, personal sites) as post material. (name, focus, home page). Edit freely.
# (name, focus, homepage). Leave the URL empty when you aren't sure of it — the
# pipeline is told to find the person's latest work by name rather than guess a
# URL. Add freely; more names means more non-news material to draw on.
FOLLOWED_RESEARCHERS = [
    ("Neel Nanda", "mechanistic interpretability", "https://www.neelnanda.io/"),
    ("Been Kim", "explainability / concept-based interpretability", "https://beenkim.github.io/"),
    ("Jacob Steinhardt", "ML safety, evaluation, robustness", "https://jsteinhardt.stat.berkeley.edu/"),
    ("Dan Hendrycks", "AI safety benchmarks and catastrophic risk", "https://www.safe.ai/"),
    ("Inioluwa Deborah Raji", "algorithmic auditing and accountability", "https://rajiinio.github.io/"),
    ("Percy Liang", "holistic evaluation, benchmarks, transparency (Stanford CRFM)", ""),
    ("Rishi Bommasani", "foundation-model transparency and policy (Stanford)", ""),
    ("Sam Bowman", "alignment, model evaluation, scalable oversight", ""),
    ("Ethan Perez", "red-teaming, adversarial evaluation", ""),
    ("Chris Olah", "interpretability and features", ""),
    ("David Bau", "model editing and interpretability (Northeastern)", ""),
    ("Cynthia Rudin", "interpretable models over post-hoc explanation (Duke)", ""),
    ("Arvind Narayanan and Sayash Kapoor", "evaluation critique, AI claims (Princeton)", ""),
    ("Yoshua Bengio", "AI risk, scientific oversight (Mila)", ""),
]

# Listings and venues to scan for new work. These are where papers live; the
# news cycle is not.
RESEARCH_VENUES = [
    "arXiv cs.LG / cs.AI / cs.CY new-submission listings",
    "OpenReview (ICLR, NeurIPS, ICML submissions and reviews)",
    "ACL Anthology",
    "Transformer Circuits",
    "the Alignment Forum's research posts (not link posts)",
    "Stanford CRFM / HAI publications",
    "Epoch AI",
    "Redwood Research",
    "ACM FAccT proceedings",
]

# ---- Saturday 'History & People' -----------------------------------------
# Saturdays draft ONE post in the 'History & People' category: a historical
# event, story, or figure, plus what it still explains about the present. This
# is research and analysis, not memoir — no personal experience is invented.
# 'Life' is NOT written by the pipeline; those posts are written by hand.
#
# Add to this list freely — one entry per area of interest.
HISTORY_TOPICS = [
    ("Ancient Greece",
     "the city-states, Athenian democracy and its failure modes, Thucydides and "
     "the Peloponnesian War, philosophy and mathematics, Alexander"),
    ("Ancient Rome",
     "the Republic's institutions and their collapse, engineering and logistics, "
     "law and citizenship, the Principate, administration of a vast territory"),
    ("World War II",
     "strategy and logistics, codebreaking and intelligence, industrial "
     "mobilization, command decisions, reconstruction and the postwar order"),
    ("Ming dynasty China",
     "the Yongle era and the treasure fleets, the decision to turn inward, "
     "bureaucracy and the examination system, currency, porcelain and trade, "
     "the Great Wall and frontier defense"),
    ("US history & the founding",
     "the Constitutional Convention and the design of institutions, the "
     "Federalist debates, early republic finance under Hamilton, "
     "the founders as administrators rather than icons"),
    ("New York City",
     "the grid and the water supply, immigration and neighborhoods, the building "
     "of the bridges and subway, finance, and how the city kept reinventing itself"),
    ("Legendary golfers",
     "Bobby Jones, Old Tom Morris, Hogan, Nicklaus and the rest — careers, "
     "technique, temperament, and the eras that shaped them"),
]

# Keywords used to work out which palette area an existing post belongs to, so
# Saturdays can be balanced across areas the way weekdays are balanced across
# categories. Posts don't record their area, so it is inferred from the text.
HISTORY_AREA_KEYWORDS = {
    "Ancient Greece": ["athens", "athenian", "greek", "greece", "sparta", "spartan",
                       "socrates", "plato", "aristotle", "thucydides", "herodotus",
                       "peloponnesian", "alexander", "hellen", "ostracism", "agora",
                       "delphi", "marathon", "salamis", "arginusae"],
    "Ancient Rome": ["rome", "roman", "caesar", "augustus", "cicero", "republic",
                     "senate", "consul", "legion", "principate", "latin", "pompey",
                     "hadrian", "aqueduct", "carthage", "punic"],
    "World War II": ["world war", "wwii", "1939", "1940", "1941", "1942", "1943",
                     "1944", "1945", "nazi", "wehrmacht", "churchill", "roosevelt",
                     "normandy", "enigma", "bletchley", "pearl harbor", "stalingrad",
                     "blitz", "luftwaffe", "manhattan project"],
    "Ming dynasty China": ["ming", "yongle", "zheng he", "treasure fleet", "forbidden city",
                           "chinese", "china", "confucian", "mandarin", "great wall",
                           "porcelain", "qing", "dynasty"],
    "US history & the founding": ["constitution", "constitutional convention", "founding",
                                  "founders", "hamilton", "madison", "jefferson",
                                  "franklin", "washington", "federalist", "philadelphia",
                                  "continental congress", "revolutionary war", "adams"],
    "New York City": ["new york", "manhattan", "brooklyn", "nyc", "tammany", "subway",
                      "erie canal", "croton", "tenement", "ellis island", "harlem"],
    "Legendary golfers": ["golf", "golfer", "masters", "augusta", "nicklaus", "hogan",
                          "bobby jones", "old tom morris", "st andrews", "links",
                          "mackenzie", "palmer", "the open championship", "usga", "r&a"],
}

# An area is "over-covered" above this multiple of an even share.
HISTORY_OVER_SHARE = 1.25


def _history_area_of(text):
    """Best-guess palette area for a post, by keyword weight. None if unclear."""
    low = text.lower()
    scores = {area: sum(low.count(k) for k in keys)
              for area, keys in HISTORY_AREA_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else None


def history_area_counts():
    """How many History & People posts fall in each palette area."""
    from collections import Counter
    counts = Counter({name: 0 for name, _ in HISTORY_TOPICS})
    unknown = 0
    for path in glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True):
        meta = _read_frontmatter(path)
        tags = [t.strip() for t in str(meta.get("tag", "")).split(",")]
        if "History & People" not in tags:
            continue
        try:
            body = open(path).read()
        except OSError:
            continue
        area = _history_area_of(body)
        if area in counts:
            counts[area] += 1
        else:
            unknown += 1
    return counts, unknown


def history_plan():
    """Which palette areas this Saturday must draw from, and which are resting."""
    counts, _ = history_area_counts()
    areas = [name for name, _ in HISTORY_TOPICS]
    total = sum(counts.values())
    if total == 0:
        return {"counts": counts, "required": areas, "discouraged": []}
    even = total / len(areas)
    # Anything never used, or below an even share, is fair game; the leanest first.
    required = sorted((a for a in areas if counts[a] <= even), key=lambda a: counts[a])
    discouraged = sorted((a for a in areas if counts[a] > even * HISTORY_OVER_SHARE),
                         key=lambda a: -counts[a])
    return {"counts": counts, "required": required or areas,
            "discouraged": discouraged}


def print_history_coverage(plan=None):
    plan = plan or history_plan()
    counts = plan["counts"]
    total = sum(counts.values()) or 1
    print("\nSaturday 'History & People' coverage:")
    for area in sorted(counts, key=lambda a: -counts[a]):
        state = ("OVER — resting" if area in plan["discouraged"]
                 else "prioritised" if area in plan["required"] else "on target")
        print("  {:28s} {:2d}  {:5.1f}%  {}".format(
            area, counts[area], counts[area] / total * 100, state))
    print("  {} post(s) total\n".format(sum(counts.values())))


# Editorial guardrail. The point is settled history and durable institutional
# lessons, not commentary on live political fights.
HISTORY_GUARDRAIL = (
    "EDITORIAL GUARDRAIL — stay out of contested contemporary politics:\n"
    "- Write about episodes where the historical record is reasonably settled and "
    "the scholarship is solid. Report genuine historiographical disagreement as "
    "disagreement rather than picking a side.\n"
    "- Do NOT touch live partisan politics, current elections or candidates, "
    "ongoing wars and territorial disputes, or culture-war framing. No "
    "present-day politician should be praised or criticised.\n"
    "- Modern parallels must be STRUCTURAL and institutional — how institutions "
    "concentrate or check power, how organizations handle information, incentives, "
    "succession, overreach, logistics, trust. Never partisan.\n"
    "- Handle atrocity and human suffering with restraint and accuracy. No "
    "sensationalism, no invented detail, no dialogue you cannot source.\n"
    "- If a subject cannot be treated without taking a contemporary political "
    "side, choose a different subject."
)

WEB_SEARCH = {"type": "web_search_20250305", "name": "web_search"}

# Credible, top-tier sources to PRIORITIZE when researching and citing.
# Search still covers the whole web — these are simply preferred and cited where
# available. Edit this list freely.
# Priority research sources (name, URL), in order of trust. The pipeline checks and
# cites these first; it may still use other reputable sources. Edit freely.
PREFERRED_SOURCES = [
    ("Anthropic Research", "https://www.anthropic.com/research"),
    ("OpenAI Research", "https://openai.com/research"),
    ("Google DeepMind Blog", "https://deepmind.google/discover/blog/"),
    ("METR (Model Evaluation & Threat Research)", "https://metr.org/blog/"),
    ("Apollo Research", "https://www.apolloresearch.ai/research"),
    ("UK AI Security Institute", "https://www.aisi.gov.uk/research"),
    ("US AI Safety Institute (NIST)", "https://www.nist.gov/aisi"),
    ("Transformer Circuits", "https://transformer-circuits.pub/"),
    ("Neel Nanda's blog", "https://www.neelnanda.io/"),
    ("Centre for the Governance of AI (GovAI)", "https://www.governance.ai/research"),
    ("Center for AI Safety (CAIS)", "https://www.safe.ai/research"),
    ("RAND Technology & Security Policy Center", "https://www.rand.org/tspc.html"),
    ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("OECD AI Policy Observatory", "https://oecd.ai/en/"),
    ("European AI Office", "https://digital-strategy.ec.europa.eu/en/policies/european-ai-office"),
    ("Bank for International Settlements (BIS) — FinTech & AI", "https://www.bis.org/topic/fintech.htm"),
    ("Alignment Forum", "https://www.alignmentforum.org/"),
    ("LessWrong — AI Alignment", "https://www.lesswrong.com/tag/ai-alignment"),
    ("arXiv — AI safety", "https://arxiv.org/search/?query=AI+safety&searchtype=all"),
    ("arXiv — AI alignment", "https://arxiv.org/search/?query=AI+alignment&searchtype=all"),
    ("The Wall Street Journal", "https://www.wsj.com/"),
]


def _sources_preference():
    src = "; ".join("{} ({})".format(n, u) for n, u in PREFERRED_SOURCES)
    return (
        "SEARCH THE OPEN WEB BROADLY AND INDEPENDENTLY — you are NOT restricted to any "
        "fixed list. The following is a RECOMMENDED set of trusted, high-signal sources "
        "to keep in mind, not a limit. Workflow: discover what's genuinely notable from "
        "across the web; then, for anything you find circulating, CHECK whether these "
        "trusted sources cover it and report what they say (or note their silence / a "
        "differing take). Prefer and cite these when they're relevant, and always link "
        "the primary source for a factual claim. Recommended sources (rough priority): "
        + src + "."
    )


def _researchers_preference():
    who = "; ".join(
        "{}{} — {}".format(n, " ({})".format(u) if u else "", f)
        for n, f, u in FOLLOWED_RESEARCHERS)
    venues = "; ".join(RESEARCH_VENUES)
    return (
        "FOLLOW ACADEMIC RESEARCH — search these ACTIVELY, every run, by name. Do "
        "not wait for a paper to show up in the news; papers rarely do, which is "
        "exactly why this section exists.\n"
        "Researchers to track (find their latest work by searching their name plus "
        "'arXiv' or 'paper' if you don't have a URL): " + who + ".\n"
        "Venues and listings to scan: " + venues + ".\n"
        "Look back roughly 30 DAYS for papers and researcher writing — this window "
        "is deliberately much longer than the news window, because a good paper is "
        "not less interesting for being three weeks old.\n"
        "Read the abstract and introduction before proposing it, cite the abstract "
        "page URL, and describe what the paper actually shows — not what a headline "
        "says it shows."
    )


# Hosts that indicate a post is grounded in a real research artifact rather than
# an announcement. Used to measure how research-led the site actually is.
RESEARCH_HOSTS = ("arxiv.org", "doi.org", "openreview.net", "aclanthology.org",
                  "nature.com", "science.org", "pnas.org", "transformer-circuits.pub",
                  "distill.pub", "jmlr.org", "neurips.cc", "icml.cc", "iclr.cc")


def _research_share(recent=20):
    """How many of the most recent published posts cite a real research artifact."""
    dated = []
    for path in glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True):
        meta = _read_frontmatter(path)
        if str(meta.get("published", "true")).lower() == "false":
            continue
        dated.append((str(meta.get("date", "")), path))
    dated.sort(reverse=True)
    sample = dated[:recent]
    hits = 0
    for _, path in sample:
        try:
            body = open(path).read().lower()
        except OSError:
            continue
        if any(h in body for h in RESEARCH_HOSTS):
            hits += 1
    return hits, len(sample)


def _source_mix_requirement(count):
    """Require research-grounded candidates, sized to how thin that coverage is."""
    hits, total = _research_share()
    need = max(1, (count + 1) // 2)
    txt = ("SOURCE MIX (a second hard constraint, independent of category):\n")
    if total:
        txt += ("Of the last {} published posts, only {} cite a research artifact "
                "(arXiv, a journal, OpenReview, Transformer Circuits). The site reads "
                "as lab-announcement and regulatory news. Fix that here.\n".format(
                    total, hits))
    txt += (
        "- At least {} of the {} candidates MUST be grounded in a RESEARCH ARTIFACT: "
        "a paper or preprint, a lab's research write-up (not a product or policy "
        "announcement), or a benchmark/evaluation result with a methodology you can "
        "read. Its primary link must be to the artifact itself.\n".format(need, count)
        + "- Do NOT satisfy this with a news article about research. The candidate "
        "must point at the work.\n"
        "- Different material moves at different speeds, so use DIFFERENT LOOKBACK "
        "WINDOWS rather than one news window:\n"
        "    • announcements, incidents, regulatory action — last ~72 hours\n"
        "    • benchmark and evaluation results — last ~2 weeks\n"
        "    • papers, preprints, and researcher writing — last ~30 days\n"
        "  A three-week-old paper nobody has written up well is a BETTER candidate "
        "than today's press release.\n"
        "- Avoid stacking multiple candidates on one ongoing story. If the site has "
        "already covered an incident, only revisit it with genuinely new material.")
    return txt


# The AI categories the balancer manages. 'Life' is deliberately excluded — it's
# the Saturday category and is written by hand, not by the pipeline.
CATEGORIES = ["AI Safety", "AI Governance", "Alignment", "Evaluation", "Agentic AI",
              "Regulation & Policy", "Industry"]

# A category is "over-covered" above this multiple of an even share, and
# "under-covered" below this one. Tuned so a single big story can't tip a
# category into being blocked, but a sustained run of them will.
OVER_SHARE = 1.25
UNDER_SHARE = 0.75


def _coverage_counts():
    """Published-post weight per category.

    The FIRST tag on a post is its primary category and counts 1.0; any further
    tags count 0.5. Without this, a piece tagged 'Agentic AI, AI Safety' would
    credit AI Safety just as much as Agentic AI, which is how the imbalance kept
    compounding even while the prompt asked for balance.
    """
    from collections import Counter
    counts = Counter({c: 0.0 for c in CATEGORIES})
    for path in glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True):
        meta = _read_frontmatter(path)
        if str(meta.get("published", "true")).lower() == "false":
            continue
        tags = [t.strip() for t in str(meta.get("tag", "")).split(",") if t.strip()]
        for i, t in enumerate(tags):
            if t in counts:
                counts[t] += 1.0 if i == 0 else 0.5
    return counts


def coverage_plan():
    """Decide which categories this run must draw from, and which are on cooldown."""
    counts = _coverage_counts()
    total = sum(counts.values())
    if total <= 0:
        return {"counts": counts, "required": list(CATEGORIES), "discouraged": [],
                "even": 0.0}
    even = total / len(CATEGORIES)
    under = sorted((c for c in CATEGORIES if counts[c] < even * UNDER_SHARE),
                   key=lambda c: counts[c])
    over = sorted((c for c in CATEGORIES if counts[c] > even * OVER_SHARE),
                  key=lambda c: -counts[c])
    # If nothing is meaningfully under-covered, just take the leanest few so the
    # run still has a concrete target rather than a vague preference.
    required = under or sorted(CATEGORIES, key=lambda c: counts[c])[:3]
    return {"counts": counts, "required": required, "discouraged": over, "even": even}


def _coverage_summary(plan=None):
    """Turn the plan into an instruction with a hard requirement, not a nudge."""
    plan = plan or coverage_plan()
    counts, even = plan["counts"], plan["even"]
    line = ", ".join(
        "{} ({:g}{})".format(
            c, counts[c],
            " OVER" if c in plan["discouraged"] else
            (" UNDER" if c in plan["required"] else ""))
        for c in CATEGORIES)
    txt = ("CURRENT COVERAGE (weighted: primary tag 1.0, secondary 0.5) — "
           + line + ". An even share would be about {:.1f} per category.\n".format(even))
    txt += ("BALANCING REQUIREMENT (this is a hard constraint, not a preference):\n"
            "- EVERY candidate you return MUST have its 'category' set to one of: "
            + ", ".join(plan["required"]) + ".\n")
    if plan["discouraged"]:
        txt += ("- Do NOT return candidates in these over-covered categories: "
                + ", ".join(plan["discouraged"]) + ". The site already leans heavily "
                "on them. The ONLY exception is a genuinely major, unavoidable story "
                "(a landmark regulation taking effect, a major incident, a frontier "
                "release) — if you use the exception, say why in the angle.\n")
    txt += ("- A story can often be told through an under-covered lens: an incident "
            "framed as Evaluation (did the tests catch it?), a model release framed as "
            "Agentic AI or Industry (what it means for deployment and vendors), a "
            "safety paper framed as Alignment. Choose the lens that fills the gap, and "
            "make the piece genuinely about that lens — do not just relabel a safety "
            "story.\n"
            "- Set 'category' to the piece's PRIMARY subject. It becomes the first tag.")
    return txt


# Corroboration bar — what counts as trustworthy enough to write about.
CORROBORATION_RULE = (
    "CORROBORATION BAR (required): treat a development as established fact ONLY if "
    "EITHER (a) it is reported by at least ONE source on the priority list above, OR "
    "(b) it is independently reported by at least TWO credible sources OUTSIDE the "
    "priority list. If a story clears NEITHER bar, do not build a post around it — omit "
    "it, or clearly label the specific unconfirmed claims as unverified/rumored. Never "
    "present an uncorroborated story as established fact.\n"
    "CARVE-OUT FOR RESEARCH: a paper, preprint, or published evaluation IS its own "
    "primary source. It does NOT need secondary news coverage to qualify — requiring "
    "that would exclude exactly the research this publication most wants to cover. "
    "What it needs is that the work genuinely exists, that you have read the abstract "
    "and introduction, and that you describe its actual claims and stated limitations "
    "accurately. Treat a preprint as a preprint: report it as 'not yet peer reviewed' "
    "and do not overstate it."
)

# ---- Draft length & formatting (edit these to taste) ----
MAX_WORDS = 700   # hard cap; the model targets ~500-600

FORMAT_GUIDE = (
    f"LENGTH (STRICT): target 500-600 words; absolute maximum {MAX_WORDS}. Brevity is a "
    "feature — count the words and trim before finishing; never exceed the maximum. "
    "Open with the single most important point in the first two sentences.\n"
    "STRUCTURE for skimmability: use ## section headings, short paragraphs "
    "(2-4 sentences), and bullet lists where they help. Use a blockquote (>) for a "
    "key quote or takeaway, and a small markdown table when comparing things. Do NOT "
    "include an H1 (the title is rendered separately).\n"
    "EMOJI: you MAY use one tasteful emoji as a signpost at the start of a section "
    "heading (at most one per heading); never mid-sentence, and omit emoji entirely "
    "if the topic is serious (incidents, harm, regulation enforcement).\n"
    "VISUALS (encouraged): do NOT embed external images (link rot / licensing), but "
    "ACTIVELY look for a chance to illustrate. Whenever the content involves a process, "
    "workflow, comparison, taxonomy, timeline, hierarchy, or relationship, INCLUDE a "
    "simple, syntactically-valid Mermaid diagram in a ```mermaid fenced code block "
    "(flowchart, timeline, sequence, or mindmap) — you may include up to TWO small "
    "diagrams if they genuinely aid understanding. A markdown comparison table is also "
    "encouraged where apt. Keep diagrams small, correct, and readable; omit only if a "
    "visual truly adds nothing.\n"
    "CITATIONS (required): weave clickable INLINE hyperlinks into the prose — link the "
    "specific words that carry a factual claim straight to the primary source, as "
    "markdown [phrase](https://...). Do NOT add a separate 'Sources' or 'References' "
    "section at the end; all citations are inline. Example: \"...reflects the final "
    "agreement described by the [Council of the EU](https://...) and analysis from "
    "[White & Case](https://...).\" Cite ONLY real URLs you actually retrieved via web "
    "search — never invent or guess a link; if a claim can't be sourced, soften it or "
    "drop it. Use several inline citations across the piece."
)

# What makes a post worth publishing — analysis, not summary.
ANALYSIS_GUIDE = (
    "INSIGHT IS THE POINT — do NOT just restate what a source reported. A summary is a "
    "failure. Every post must add genuine analytical value by doing several of these:\n"
    "- CROSS-REFERENCE: pull from multiple sources on the same event and surface where "
    "they AGREE vs. DISAGREE, or where they frame it differently.\n"
    "- HISTORICAL PARALLEL: compare the development to a relevant past event/precedent "
    "and draw the lesson it suggests.\n"
    "- PREDICTION: offer a clearly-labeled, reasoned forecast (e.g. a 'What to watch' or "
    "'My read' line) — specific but appropriately hedged, never overconfident.\n"
    "- CONNECT: a list of already-published posts is provided in the user message. If "
    "this story overlaps one, do NOT rehash it — focus on what is NEW, and LINK the "
    "prior post inline using its FULL absolute URL (https://minwu-ai.github.io/<slug>/) "
    "so readers get the throughline.\n"
    "Always apply a model-risk, safety, and governance lens. Be the analyst a busy "
    "practitioner reads BECAUSE it tells them something the original source didn't."
)

INDEPENDENCE_RULE = (
    "INDEPENDENCE AND CONFLICTS OF INTEREST — this is a hard constraint:\n"
    "- Never claim or imply professional engagement, client work, or insider access. "
    "Do NOT write phrases like 'in my consulting experience', 'my clients', 'in my "
    "practice', 'firms I advise', 'in my work with banks', 'from my time at', or any "
    "variation that positions the author as speaking from privileged or paid engagements.\n"
    "- Ground every claim in the public record instead. Preferred framings: "
    "'Organizations commonly encounter...', 'Public regulatory guidance suggests...', "
    "'One practical governance challenge is...', 'Industry reporting indicates...', "
    "'The published guidance states...'.\n"
    "- Never reference confidential, non-public, proprietary, or internal information. "
    "Every factual claim must be traceable to a publicly accessible source.\n"
    "- First-person analytical judgment is fine ('I read this as...', 'my view is...'). "
    "First-person claims of professional authority or engagement are not."
)

DRAFT_SYSTEM = (
    "You are an AI industry analyst writing for a professional audience of risk, "
    "governance, and applied-AI practitioners. Voice: clear, authoritative, "
    "grounded, never hype. Authority comes from the quality of reasoning about public "
    "evidence — never from claimed professional engagements or privileged access. "
    "Where you make factual claims about recent events, ground them with web search.\n\n"
    + INDEPENDENCE_RULE + "\n\n"
    + ANALYSIS_GUIDE + "\n\n"
    + FORMAT_GUIDE + "\n\n"
    + _sources_preference() + "\n\n"
    + CORROBORATION_RULE + "\n\n"
    "Return the article in EXACTLY this format, and nothing else (no code fences):\n"
    "TITLE: <the title on a single line>\n"
    "EXCERPT: <one-sentence summary on a single line>\n"
    "TAG: <one or two best-fit subject categories from EXACTLY this list, "
    "comma-separated. Use TWO categories WHENEVER the piece genuinely spans two areas "
    "(this is encouraged, e.g. 'Agentic AI, AI Governance'); use one only if it clearly "
    "fits a single category. Choose from: AI Governance, AI Safety, Alignment, "
    "Evaluation, Agentic AI, Regulation & Policy, Industry>\n"
    "TAKEAWAY: <a '1-minute takeaway' in 1-2 sentences — the single most important "
    "point, specific and plainly stated>\n"
    "BODY:\n"
    "<the full markdown body; may span many lines>"
)


def _strip_fences(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    return text


def _extract_json(text):
    """Parse the first JSON value in a model response, ignoring any surrounding prose.

    Uses raw_decode so trailing commentary after the array/object (a common model
    habit) doesn't cause an 'Extra data' error.
    """
    text = _strip_fences(text)
    start = next((i for i, ch in enumerate(text) if ch in "[{"), None)
    if start is None:
        return json.loads(text, strict=False)  # no JSON found -> raise informative error
    try:
        obj, _ = json.JSONDecoder(strict=False).raw_decode(text[start:])
        return obj
    except json.JSONDecodeError:
        # Salvage: if the array was truncated, keep the complete {...} entries.
        objs = []
        for m in re.finditer(r"\{[^{}]*\}", text[start:], re.DOTALL):
            try:
                objs.append(json.loads(m.group(0), strict=False))
            except json.JSONDecodeError:
                pass
        if objs:
            return objs
        raise


def parse_article(text):
    """Parse the delimited TITLE/EXCERPT/TAG/BODY format into an article dict.

    Robust by design: the body is taken verbatim after the BODY: marker, so it can
    contain quotes, newlines, and arbitrary markdown without any escaping.
    """
    text = _strip_fences(text)
    meta = {"title": "", "excerpt": "", "tag": "", "takeaway": "", "body_markdown": ""}
    lines = text.splitlines()
    body_idx = None
    for i, line in enumerate(lines):
        up = line.lstrip().upper()
        if up.startswith("BODY:"):
            body_idx = i
            trailing = line.split(":", 1)[1].strip()
            break
        for key in ("TITLE", "EXCERPT", "TAG", "TAKEAWAY"):
            if up.startswith(key + ":"):
                meta[key.lower()] = line.split(":", 1)[1].strip()
                break
    if body_idx is not None:
        rest = lines[body_idx + 1:]
        body = (trailing + "\n" if trailing else "") + "\n".join(rest)
        meta["body_markdown"] = body.strip()
    else:
        # No BODY marker found — treat the whole thing as the body.
        meta["body_markdown"] = text.strip()
    if not meta["title"]:
        raise ValueError("Could not parse a title from the model output.")
    if not meta["body_markdown"]:
        raise ValueError("Model returned an empty body.")
    return meta


def _text_of(resp):
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _discovery_prompt(count, focus=None, plan=None):
    plan = plan or coverage_plan()
    focus_line = "; ".join(focus or FOCUS_TOPICS)
    return (
        f"Find {count} things worth writing about for a publication on AI risk, "
        "evaluation, and governance.\n\n"
        "IMPORTANT — this is NOT a news round-up. Do not start from today's "
        "headlines. Headlines are dominated by lab announcements and regulatory "
        "action, and a site built from them ends up covering the same few stories "
        "from every angle. Start instead from the question: what has been PUBLISHED "
        "recently — papers, evaluations, research write-ups, deployment data — that a "
        "risk practitioner would be glad someone read carefully for them?\n\n"
        f"General areas of interest: {focus_line}.\n\n"
        + _coverage_summary(plan) + "\n\n"
        + _source_mix_requirement(count) + "\n\n"
        "REQUIRED MIX (this is a candidate list; extras are backups in case some can't "
        "be corroborated):\n"
        "- Candidates must span DIFFERENT categories — do not return two topics in the "
        "same category.\n"
        "- Every candidate's category must come from the required list above.\n"
        "- Search SPECIFICALLY for stories in the required categories. Do not just "
        "report the day's headlines and label them; go looking for what happened in "
        "agent deployments, evaluation and benchmarking work, alignment research, and "
        "the business/vendor side of AI.\n"
        "- Order candidates best-first.\n\n"
        + _sources_preference() + "\n\n"
        + _researchers_preference() + "\n\n"
        + CORROBORATION_RULE + " Only propose topics that clear this bar.\n\n"
        "AVOID REDUNDANCY: a list of posts already published on this site is provided "
        "below. Do NOT propose a topic that merely repeats one of them. Revisiting a "
        "topic is fine ONLY if there's a genuine new development or new angle — if so, "
        "note in the angle what's new and which prior post it follows up.\n\n"
        "For each topic, set 'category' to one of the REQUIRED categories listed "
        "above: " + ", ".join(plan["required"]) + ". "
        "Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "angle": "...", "category": "..."}]'
    )


def discover_topics(count, focus=None, plan=None):
    resp = get_client().messages.create(
        model=MODEL,
        thinking=THINKING,
        max_tokens=3000,   # room for web-search rounds + the full candidate JSON
        tools=[WEB_SEARCH],
        messages=[{"role": "user",
                   "content": _discovery_prompt(count, focus, plan)
                   + published_posts_context()}],
    )
    topics = _extract_json(_text_of(resp))
    return topics[:count]


def _read_frontmatter(path):
    """Lightweight frontmatter reader (no extra deps) for the pipeline step."""
    meta = {}
    with open(path) as f:
        text = f.read()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def published_posts_context(limit=25):
    """A list of already-published posts the model can reference and link."""
    items = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True)):
        meta = _read_frontmatter(path)
        if str(meta.get("published", "true")).lower() == "false":
            continue
        title = meta.get("title", "")
        slug = meta.get("slug") or os.path.basename(path)[:-3]
        if title:
            items.append("- [{}](https://minwu-ai.github.io/{}/) — {}".format(
                title, slug, meta.get("excerpt", "")))
    if not items:
        return ""
    return ("\n\nAlready published on this site — reference and LINK any that are "
            "relevant (use the FULL absolute URL shown) to build a throughline:\n"
            + "\n".join(items[:limit]))


def draft_article(instruction, system=None):
    """instruction: a natural-language brief describing what to write."""
    resp = get_client().messages.create(
        model=MODEL,
        thinking=THINKING,
        max_tokens=2000,
        tools=[WEB_SEARCH],
        system=system or DRAFT_SYSTEM,
        messages=[{"role": "user", "content": instruction + published_posts_context()}],
    )
    return parse_article(_text_of(resp))


def has_sources(article):
    """True if the draft has enough INLINE citations (markdown links to real URLs).

    Citations are now woven into the prose (no end 'Sources' section), so we require
    at least two inline hyperlinks to http(s) sources.
    """
    body = article.get("body_markdown", "")
    return len(re.findall(r"\]\(https?://[^)]+\)", body)) >= 2


def trim_to_length(article, max_words=None, preserve="the core analysis "
                   "(cross-references, historical parallel, prediction)"):
    """Prompt-based limits don't hold, so enforce length with a dedicated trim pass."""
    limit = max_words or MAX_WORDS
    body = article.get("body_markdown", "")
    if len(body.split()) <= limit:
        return article
    resp = get_client().messages.create(
        model=MODEL,
        thinking=THINKING,
        max_tokens=1500,
        system=("You are a ruthless editor. Cut the following article body to UNDER "
                f"{limit} words (aim ~{int(limit * 0.85)}). Preserve {preserve} "
                "and KEEP every "
                "inline source hyperlink intact. Keep markdown headings. "
                "Return ONLY the tightened markdown body, nothing else."),
        messages=[{"role": "user", "content": body}],
    )
    new = _strip_fences(_text_of(resp))
    if new and re.search(r"https?://", new) and len(new.split()) < len(body.split()):
        article["body_markdown"] = new
    return article


def draft_with_sourcing(instruction, system=None, max_words=None, preserve=None):
    """Draft; ensure a real Sources section (retry once); then enforce length."""
    article = draft_article(instruction, system=system)
    if not has_sources(article):
        article = draft_article(
            instruction + "\n\nYOUR PREVIOUS DRAFT FAILED: it lacked real inline source "
            "links. Weave at least two clickable inline hyperlinks [phrase](https://...) "
            "to primary sources directly into the prose (no end 'Sources' section). If "
            "the story cannot be corroborated with real links, say so plainly rather "
            "than writing it.", system=system)
    if has_sources(article):
        kw = {"max_words": max_words} if max_words else {}
        if preserve:
            kw["preserve"] = preserve
        article = trim_to_length(article, **kw)
    return article


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]


def save_post(article, default_tag="Analysis"):
    today = datetime.date.today().isoformat()
    slug = slugify(article["title"])
    # New drafts start unpublished, so they file themselves into
    # posts/unpublished/. organize_posts.py moves them once you publish.
    draft_dir = os.path.join(POSTS_DIR, "unpublished")
    os.makedirs(draft_dir, exist_ok=True)
    path = os.path.join(draft_dir, f"{slug}.md")
    title = article["title"].replace('"', "'")
    excerpt = article.get("excerpt", "").replace('"', "'")
    takeaway = article.get("takeaway", "").replace('"', "'")
    tag = article.get("tag") or default_tag
    frontmatter = (
        "---\n"
        f'title: "{title}"\n'
        f"date: {today}\n"
        f"slug: {slug}\n"
        f"tag: {tag}\n"
        f'excerpt: "{excerpt}"\n'
        f'takeaway: "{takeaway}"\n'
        'cover: "/assets/"\n'          # <-- fill in your image path, e.g. /assets/foo.png
        'cover_alt: "Illustration: "\n'  # <-- fill in the caption / credit
        "published: false\n"        # <-- review gate: flip to true to publish
        "---\n\n"
    )
    with open(path, "w") as f:
        f.write(frontmatter + article["body_markdown"].strip() + "\n")
    print(f"  saved draft: posts/{slug}.md")
    return path


# ---- Mode: scheduled (auto-discover) -------------------------------------

def _dump_prompt(label, instruction):
    print("=" * 70)
    print("[DRY RUN] " + label)
    print("=" * 70)
    print("\n--- SYSTEM PROMPT ---\n" + DRAFT_SYSTEM)
    print("\n--- USER INSTRUCTION ---\n" + instruction)
    print("\n[dry-run] No API call made and no file written.\n")


def run_scheduled(count, focus=None, dry_run=False):
    plan = coverage_plan()
    if dry_run:
        print("=" * 70)
        print("[DRY RUN] scheduled mode")
        print("=" * 70)
        print_coverage_report(plan)
        print("\n--- TOPIC-DISCOVERY PROMPT ---\n"
              + _discovery_prompt(count, focus, plan))
        print("\n--- then each topic is drafted with this SYSTEM PROMPT ---\n"
              + DRAFT_SYSTEM)
        print("\n[dry-run] No API call made and no file written.\n")
        return
    target = count
    print("Balancing toward: " + ", ".join(plan["required"])
          + (" (cooling off: " + ", ".join(plan["discouraged"]) + ")"
             if plan["discouraged"] else ""))
    print(f"Discovering candidate topics (target {target})...")
    # Over-fetch so we can backfill when a topic can't be corroborated/cited.
    candidates = discover_topics(target + 4, focus=focus, plan=plan)
    saved = _select_and_draft(candidates, target, plan=plan)
    print(f"Done — saved {saved} of {target} target draft(s).")


def print_coverage_report(plan=None):
    plan = plan or coverage_plan()
    counts, even = plan["counts"], plan["even"]
    total = sum(counts.values()) or 1
    print("\nTopic coverage (primary tag 1.0, secondary 0.5):")
    print("  {:22s} {:>7s} {:>8s}  {}".format("category", "weight", "share", "status"))
    for c in sorted(CATEGORIES, key=lambda c: -counts[c]):
        status = ("OVER — on cooldown" if c in plan["discouraged"]
                  else "under — prioritised" if c in plan["required"] else "on target")
        print("  {:22s} {:7.1f} {:7.1f}%  {}".format(
            c, counts[c], counts[c] / total * 100, status))
    print("  even share would be {:.1f} each\n".format(even))


# ---- Mode: Saturday 'History & People' -----------------------------------

HISTORY_MAX_WORDS = 900   # a little more room than the weekday news analysis

HISTORY_DRAFT_SYSTEM = (
    "You are writing the Saturday 'History & People' piece for a personal website "
    "whose weekday subject is AI risk and governance. This piece is about the past: "
    "an event, an episode, or a figure — told well, and then read for what it still "
    "explains about the present. The reader is intelligent and curious but not a "
    "specialist in the period.\n\n"
    "STRUCTURE:\n"
    "1. Open on something concrete — a decision, a date, a scene, a number. No "
    "scene-setting throat-clearing.\n"
    "2. Tell the history clearly and accurately, with the detail that makes it stick.\n"
    "3. Then turn to what it means now. This is the part that earns the piece: the "
    "structural pattern that recurs — how institutions concentrate or check power, "
    "how organizations handle information and incentives, how succession, overreach, "
    "logistics, or trust actually work. Draw the parallel precisely and admit where "
    "it breaks down. A parallel that has to be forced is not a parallel.\n\n"
    "VOICE: warm, unhurried, confident, never grandiose. Short paragraphs. No "
    "'throughout history', no 'little did they know', no moral lecture at the end. "
    "First person is welcome for interpretation — 'what strikes me is...', 'I read "
    "this as...' — but never invent personal experience: no trips, no visits, no "
    "memories, no conversations. You do not know what the author has seen.\n\n"
    "ACCURACY AND SOURCING: this is real history and it must be right. Weave at "
    "least two clickable inline hyperlinks [phrase](https://...) to solid sources "
    "into the prose — university and museum collections, national archives, "
    "encyclopaedias of record, respected historians, primary documents in "
    "translation. No end 'Sources' section. Never state a date, quotation, or "
    "attribution you cannot support, and never invent a quotation. Where historians "
    "genuinely disagree, say so.\n\n"
    + HISTORY_GUARDRAIL + "\n\n"
    f"LENGTH: aim for 700-850 words; never exceed {HISTORY_MAX_WORDS}.\n\n"
    "VISUALS: a short markdown table or timeline is welcome when there is real "
    "structure to show (a sequence of decisions, a comparison across eras). Never "
    "invent an image.\n\n"
    "Return the article in EXACTLY this format, and nothing else (no code fences):\n"
    "TITLE: <the title on a single line>\n"
    "EXCERPT: <one-sentence summary on a single line>\n"
    "TAG: History & People\n"
    "TAKEAWAY: <a '1-minute takeaway' in 1-2 sentences — the pattern worth keeping>\n"
    "BODY:\n"
    "<the full markdown body; may span many lines>"
)


def _history_discovery_prompt(count, plan=None):
    plan = plan or history_plan()
    palette = "\n".join("- {}: {}".format(n, d) for n, d in HISTORY_TOPICS)
    counts = plan["counts"]
    tally = ", ".join("{} ({})".format(a, counts[a]) for a, _ in HISTORY_TOPICS)
    balance = (
        "AREA BALANCE (a hard constraint — the site has drifted badly here):\n"
        "Posts published per area so far: " + tally + ".\n"
        "- EVERY candidate's 'area' MUST be one of: "
        + ", ".join(plan["required"]) + ".\n"
        + ("- Do NOT propose anything from these over-used areas: "
           + ", ".join(plan["discouraged"]) + ". They have had more than their "
           "share and are resting this week. There is no exception — pick a "
           "different area.\n" if plan["discouraged"] else "")
        + "- Classical antiquity is NOT the default. An area with zero posts is a "
        "better choice than a fresh angle on one already covered.\n"
        "- Set 'area' to exactly one of the palette names above.\n\n"
    )
    return (balance + 
        f"Propose {count} candidate subjects for a Saturday 'History & People' essay: "
        "a historical event, episode, or figure, told for its own sake and then read "
        "for what it still explains about how institutions and people behave today.\n\n"
        "The author's areas of interest — choose from these:\n" + palette + "\n\n"
        "WHAT MAKES A GOOD SUBJECT:\n"
        "- Specific and concrete. 'Why the Ming turned the treasure fleets around' "
        "beats 'the history of Ming China'. One decision, person, institution, or "
        "episode — never a survey of a period.\n"
        "- Carries a genuine surprise or a reversal of the obvious reading — "
        "something a well-read person would not already know.\n"
        "- Supports a REAL modern parallel about institutions, incentives, "
        "information, or power — structural, never partisan. State the parallel in "
        "the angle so it can be judged. If the only available parallel is strained "
        "or a cliché, drop the subject.\n"
        "- Solidly documented: real, checkable sources (university and museum "
        "collections, national archives, encyclopaedias of record, respected "
        "historians, primary documents).\n"
        "- Candidates must span DIFFERENT areas from the list above.\n\n"
        + HISTORY_GUARDRAIL + "\n\n"
        "Use web search to confirm each subject is real, well documented, and not "
        "misremembered popular history before proposing it. Order candidates "
        "best-first.\n\n"
        "AVOID REDUNDANCY: a list of posts already published on this site is provided "
        "below. Do not propose a subject that repeats one of them.\n\n"
        "Set 'area' to one of the REQUIRED areas listed above: "
        + ", ".join(plan["required"]) + ".\n"
        "Return ONLY a JSON array, no markdown:\n"
        '[{"topic": "...", "angle": "...", "parallel": "...", "area": "..."}]'
    )


def discover_history_topics(count, plan=None):
    resp = get_client().messages.create(
        model=MODEL,
        thinking=THINKING,
        max_tokens=3000,
        tools=[WEB_SEARCH],
        messages=[{"role": "user",
                   "content": _history_discovery_prompt(count, plan)
                   + published_posts_context()}],
    )
    return (_extract_json(_text_of(resp)) or [])[:count]


def run_history(dry_run=False):
    """Saturday: draft one 'History & People' post for review."""
    if dry_run:
        print("=" * 70)
        print("[DRY RUN] Saturday 'History & People' mode")
        print("=" * 70)
        print_history_coverage()
        print("\n--- SUBJECT-DISCOVERY PROMPT ---\n" + _history_discovery_prompt(4))
        print("\n--- then drafted with this SYSTEM PROMPT ---\n"
              + HISTORY_DRAFT_SYSTEM)
        print("\n[dry-run] No API call made and no file written.\n")
        return
    plan = history_plan()
    print("Saturday History & People — balancing toward: "
          + ", ".join(plan["required"])
          + ((" (resting: " + ", ".join(plan["discouraged"]) + ")")
             if plan["discouraged"] else ""))
    candidates = discover_history_topics(4, plan=plan)
    if not candidates:
        print("No subjects found; nothing drafted.")
        return
    # Try the under-covered areas first; only fall back to the rest if none of
    # them can be researched and cited this week.
    required = set(plan["required"])
    candidates = ([c for c in candidates if c.get("area") in required]
                  + [c for c in candidates if c.get("area") not in required])
    for cand in candidates:
        area = cand.get("area", "")
        print(f"Drafting [{area}]: {cand.get('topic', '')}")
        instruction = (
            f"Write the Saturday 'History & People' piece about: {cand['topic']}. "
            f"Angle: {cand.get('angle', '')}. "
            f"The modern parallel to develop: {cand.get('parallel', '')}. "
            "Research it with web search first and cite real sources inline. "
            "Get the history right, then earn the parallel — and say where it "
            "breaks down. Set TAG to exactly 'History & People'."
        )
        article = draft_with_sourcing(
            instruction, system=HISTORY_DRAFT_SYSTEM, max_words=HISTORY_MAX_WORDS,
            preserve="the historical detail and the modern parallel")
        if not has_sources(article):
            print("  skipped (couldn't cite it) — trying the next subject.")
            continue
        article["tag"] = "History & People"
        save_post(article, default_tag="History & People")
        print("Done — saved 1 History & People draft for review.")
        return
    print("Done — saved 0 drafts (no subject could be cited).")


def _force_primary_tag(article, cat):
    """Make `cat` the first tag, keeping any extra category the model added.

    The drafting model often returns 'AI Safety, Agentic AI' for a piece assigned
    to Agentic AI. Since the first tag is the primary one for coverage purposes,
    letting that stand is what kept re-concentrating the site on AI Safety.
    """
    tags = [t.strip() for t in str(article.get("tag") or "").split(",") if t.strip()]
    tags = [t for t in tags if t in CATEGORIES and t != cat]
    article["tag"] = ", ".join([cat] + tags[:1])
    return article


def _select_and_draft(candidates, target, plan=None):
    """Save `target` drafts, preferring the categories the balancer asked for.

    Pass 1 takes only required (under-covered) categories, one per category.
    Pass 2 backfills from anything left, but only if pass 1 came up short — so a
    thin news day still produces posts instead of nothing.
    """
    plan = plan or coverage_plan()
    required = set(plan["required"])
    saved, used_cats = 0, set()

    def attempt(cand):
        nonlocal saved
        cat = cand.get("category", "").strip()
        if cat not in CATEGORIES:
            cat = plan["required"][0] if plan["required"] else "Industry"
        print(f"Drafting [{cat}]: {cand['topic']}")
        instruction = (
            f"Write an analytical piece about: {cand['topic']}. "
            f"Angle: {cand.get('angle', '')}. "
            f"The PRIMARY category is '{cat}' — the piece must genuinely be about "
            f"that, and TAG must start with '{cat}'. Add at most one more category, "
            "and only if the piece truly spans two. "
            "Research it with web search first, cross-referencing multiple sources."
        )
        article = draft_with_sourcing(instruction)
        if not has_sources(article):
            print("  skipped (couldn't corroborate/cite) — trying the next candidate.")
            return
        _force_primary_tag(article, cat)
        save_post(article, default_tag=cat)
        used_cats.add(cat)
        saved += 1

    # Pass 1: required (under-covered) categories only, one topic each.
    for c in candidates:
        if saved >= target:
            break
        cat = c.get("category", "").strip()
        if cat not in required or cat in used_cats:
            continue
        attempt(c)
    # Pass 2: only if short — anything left, still one per category.
    if saved < target:
        print(f"  only {saved}/{target} from under-covered categories; backfilling.")
        for c in candidates:
            if saved >= target:
                break
            if (c.get("category", "").strip() or "Industry") in used_cats:
                continue
            attempt(c)
    return saved


# ---- Mode: on demand -----------------------------------------------------

def _ondemand_instruction(topic=None, url=None, text=None, article_type=None, angle=None):
    parts = []
    kind = article_type or "analysis"
    if url:
        parts.append(f"Read and analyze this source, then write a {kind} piece about "
                     f"it (use web search to fetch and verify): {url}")
    if topic:
        parts.append(f"Write a {kind} piece about: {topic}.")
    if text:
        parts.append(
            "Below is a source document / link / notes I'm recommending as the basis "
            f"for a post. Write an original {kind} piece in the house style that "
            "engages with it: lead with the most important insight, add context and "
            "verification via web search, quote sparingly, and bring the risk-, "
            "governance-, and applied-AI lens of this publication. Do NOT merely "
            "summarize the source.\n\n--- SOURCE ---\n" + text)
    if angle:
        parts.append(f"Angle / emphasis: {angle}")
    if not parts:
        raise SystemExit("Nothing to write about. Provide --topic, --url, --from-file, "
                         "or use --interactive.")
    return "\n\n".join(parts), kind


def run_ondemand(topic=None, url=None, text=None, article_type=None, angle=None,
                 dry_run=False):
    instruction, kind = _ondemand_instruction(topic, url, text, article_type, angle)
    if dry_run:
        _dump_prompt("on-demand mode", instruction)
        return
    print("Researching and drafting...")
    article = draft_with_sourcing(instruction)
    if not has_sources(article):
        print("  ⚠ note: this draft has no '## Sources' section — verify it before publishing.")
    save_post(article, default_tag=kind.capitalize())
    print("Done. Review the draft, then flip 'published: false' to true.")


def run_interactive(dry_run=False):
    print("On-demand draft. Paste a link, describe a finding, or paste notes.")
    print("Finish your input with Ctrl-D (Mac/Linux) on a new line.\n")
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("No input received.")
    # If it's just a URL, treat it as a source; otherwise as notes/topic.
    if re.match(r"^https?://\S+$", text):
        run_ondemand(url=text, dry_run=dry_run)
    else:
        run_ondemand(text=text, dry_run=dry_run)


def main():
    p = argparse.ArgumentParser(description="Draft AI blog posts (scheduled or on demand).")
    p.add_argument("--count", type=int, default=None,
                   help="scheduled mode: how many topics to draft. Defaults to "
                        "2, or 1 on Tuesdays and Thursdays.")
    p.add_argument("--focus",
                   help="scheduled mode: comma-separated focus topics for this run "
                        "(overrides the FOCUS_TOPICS list)")
    p.add_argument("--topic", help="on demand: a topic/headline to write about")
    p.add_argument("--url", help="on demand: a source URL to read and analyze")
    p.add_argument("--from-file", dest="from_file",
                   help="on demand: path to a file with notes/pasted text")
    p.add_argument("--type", dest="article_type",
                   choices=["news", "analysis", "opinion", "governance"],
                   help="article type (on demand)")
    p.add_argument("--angle", help="on demand: angle/emphasis for the piece")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="on demand: paste/describe a finding at the prompt")
    p.add_argument("--history", action="store_true",
                   help="draft one 'History & People' post (auto-selected on Saturdays)")
    p.add_argument("--no-history", dest="no_history", action="store_true",
                   help="run the normal AI pipeline even if today is Saturday")
    p.add_argument("--history-coverage", dest="history_coverage", action="store_true",
                   help="print the Saturday 'History & People' area balance and exit")
    p.add_argument("--coverage", action="store_true",
                   help="print the topic-coverage report and what the next run would "
                        "target, then exit (no API call)")
    p.add_argument("--dry-run", dest="dry_run", action="store_true",
                   help="show the exact prompts that would be sent; no API call, "
                        "no file written")
    args = p.parse_args()

    if args.coverage:
        print_coverage_report()
        return

    if args.history_coverage:
        print_history_coverage()
        return

    text = None
    if args.from_file:
        with open(args.from_file) as f:
            text = f.read().strip()

    if args.interactive:
        run_interactive(dry_run=args.dry_run)
    elif args.topic or args.url or text:
        run_ondemand(topic=args.topic, url=args.url, text=text,
                     article_type=args.article_type, angle=args.angle,
                     dry_run=args.dry_run)
    elif args.history or (datetime.date.today().weekday() == 5
                          and not args.no_history):
        # weekday() == 5 is Saturday — one 'History & People' post.
        run_history(dry_run=args.dry_run)
    else:
        focus = [t.strip() for t in args.focus.split(",")] if args.focus else None
        count = args.count if args.count is not None else drafts_for_today()
        run_scheduled(count, focus=focus, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
