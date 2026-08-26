---
title: "The 2025 AI Agent Index: Accountability Infrastructure for Agentic AI Barely Exists"
date: 2026-08-26
slug: the-2025-ai-agent-index-accountability-infrastructure-for-ag
tag: Agentic AI, AI Governance
excerpt: "A peer-reviewed census of 30 deployed AI agents finds that most safety-related fields are simply blank — making this the first empirical baseline for a governance gap that was previously only described conceptually."
takeaway: "Of 240 safety-related fields across 30 deployed agents, 135 contain no public information — and of the 13 agents operating at frontier autonomy levels, only 4 disclose any agentic safety evaluations. The disclosure gap is not hypothetical; it is now measured."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 📊 What the Numbers Actually Say

The headline statistic is blunt. Most safety-related fields — 135 out of 240 — have no public information available. 25 out of 30 AI agents do not disclose internal safety results, while 23 out of 30 provide no data from third-party testing. The autonomy/disclosure inversion is particularly stark: of the 13 agents exhibiting frontier levels of autonomy, only 4 disclose any agentic safety evaluations. The lead researcher characterized this directly as "a weaker form of safety washing" — developers are "much more forthcoming about the capabilities of their AI agent" than its risks.

## Which Agent Categories Are Most Opaque

The Index reveals a clear gradient by agent type, with autonomy and opacity moving in lockstep:

| Agent Category | Safety Fields Missing | Typical Autonomy Level |
|---|---|---|
| Browser agents | 64% | Level 4–5 |
| Enterprise agents | 63% | Level 3–5 (deployed) |
| Chat agents | 43% | Level 1–3 |

The enterprise split is especially consequential: a system that looks supervised at design time may be largely autonomous by the time it reaches production. On identity and web conduct, only 7 out of 30 agents publish stable User-Agent strings and IP ranges for verification, while 6 explicitly use Chrome-like UA strings and residential IP contexts, mimicking human web traffic. Only 6 agents explicitly stated their crawler bots respect robots.txt; 16 provided no clear statement at all.

## The Ecosystem Concentration Risk

One underappreciated finding: outside of Chinese AI agents, almost all agents depend on just a few foundation models — GPT, Claude, Gemini — creating potential single points of failure where "a pricing change, service outage, or safety regression in one model could cascade across hundreds of AI agents." That concentration also creates a structural opportunity: safety improvements pushed at the foundation model layer can propagate broadly. The Index quietly identifies both the systemic risk and its own remedy.

## The FMTI Parallel — and Where It Diverges

The closest precedent is the [Foundation Model Transparency Index](https://crfm.stanford.edu/fmti/December-2025) from Stanford CRFM. When the FMTI launched in 2023, developers publicly disclosed very limited information, averaging 37 out of 100. Competitive pressure drove improvement — but companies score worse in the most recent edition, with the mean falling 17 points year-over-year. The agent transparency picture looks like 2023 FMTI all over again, but with higher stakes: foundation models predict, agents act.

The structural difference matters. The FMTI assesses a single developer's practices. The Agent Index confronts a distributed accountability problem: the architecture creates accountability diffusion where no single entity bears clear responsibility, and regulators risk false assurance from model-only documentation.

## What This Means for Practitioners

The [2025 AI Agent Index](https://arxiv.org/abs/2602.17753), published at [ACM FAccT 2026](https://dl.acm.org/doi/10.1145/3805689.3806728) by researchers from Cambridge, MIT, Stanford, Harvard Law, and Hebrew University, provides the empirical baseline that the [governance gap analysis](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/) described conceptually. It also tightens the stakes raised by the [GPT-5.6 Sol system card analysis](https://minwu-ai.github.io/gpt-5-6-sol-system-card-agentic-ai-tradeoff/) — if even frontier agents with published system cards document the autonomy/control trade-off imperfectly, the 26 agents without system cards are flying blind by comparison.

For developers, the Index identifies concrete gaps — agent-specific system cards, sandboxing documentation, and web conduct policies. For procurement and model-risk teams, this is a vendor due-diligence checklist in disguise.

> **My read:** The FMTI showed that structured public disclosure indexes *do* move developer behavior. The Agent Index has now done the same for the agentic layer. The question is whether regulatory pressure — the EU AI Act's Article 50 obligations, Illinois's [mandatory audit law](https://minwu-ai.github.io/illinois-sb-315-closes-the-audit-gap-the-first-mandatory-ind/) — arrives fast enough to accelerate that process before a high-profile agentic incident forces the conversation instead.

**What to watch:** Whether FAccT publication and the Cambridge/MIT imprimatur generate the same feedback-loop dynamic the FMTI did — developers quietly updating disclosures to improve their Index annotations within 12 months.
