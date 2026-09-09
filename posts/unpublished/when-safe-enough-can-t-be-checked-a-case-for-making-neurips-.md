---
title: "When 'Safe Enough' Can't Be Checked: A Case for Making NeurIPS Gatekeep Reproducibility"
date: 2026-09-09
slug: when-safe-enough-can-t-be-checked-a-case-for-making-neurips-
tag: Regulation & Policy, Evaluation
excerpt: "A May 2026 Oxford position paper argues that NeurIPS should treat unreproducible frontier AI safety claims as a methodology failure rather than a transparency nicety — and uses Anthropic's Claude Mythos Preview disclosure to show why even the best-case regime still falls short."
takeaway: "The paper's real contribution isn't a new safety framework — it's a proposed audit standard: publication venues should refuse to let 'we tested it and it's safe' count as evidence unless third parties can actually check the claim."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The core argument

A [position paper](https://arxiv.org/abs/2605.08192) submitted to arXiv in May 2026 by four Oxford-affiliated researchers — Varad Vishwarupe, Nigel Shadbolt, Marina Jirotka, and Ivan Flechais — makes a narrow but pointed claim: NeurIPS, the field's most influential publication venue, should require reproducibility standards specifically for papers making frontier AI safety claims, and should treat non-reproducibility not as a transparency preference but as an evaluation-methodology failure.

This is not a safety paper. It doesn't propose new red-teaming methods or argue for a particular threshold of dangerous capability. It is an audit-methodology paper wearing a policy hat, and that framing matters — it's aimed at reviewers and area chairs, not regulators.

The authors define frontier AI safety claims precisely: published assertions that a highly capable general-purpose model is below a threshold of concern, adequately mitigated, or suitable for release. Their complaint is that the artefacts needed to evaluate them are routinely withheld, producing an evidential inversion: the most consequential claims in AI safety are often the least reproducible.

## The evidence base: a sector going the wrong direction

The paper leans on Stanford's [2025 Foundation Model Transparency Index](https://crfm.stanford.edu/fmti/December-2025/index.html) (FMTI), and the numbers are unambiguous. The average transparency score across developers fell from 58 in 2024 to 40 in 2025 — a reversal, not a plateau. The FMTI's own authors are blunt about the trend: the average score out of 100 fell from 58 in 2024 to 40 in 2025 — companies are most opaque about their training data and training compute as well as the post-deployment usage and impact of their flagship models. While companies tend to disclose evaluations of model capabilities and risks, limited methodological transparency, third-party involvement, reproducibility, and reporting of train-test overlap pose challenges.

Most damning for the position paper's argument: Amazon, Google, Midjourney, Mistral, OpenAI and xAI do not score any indicators in the model information subdomain, such as the basic model information indicator. Six major developers, zero disclosure on the most basic descriptive facts about their own models.

| FMTI metric | 2024 | 2025 |
|---|---|---|
| Sector average score | 58/100 | 40/100 |
| Top scorer | — | IBM, 95/100 |
| Bottom scorers | — | xAI, Midjourney: 14/100 |
| Developers scoring zero on model information | — | 6 |

## The Mythos case study: best case, still broken

The paper's sharpest move is choosing Anthropic — usually treated as the industry's disclosure benchmark — as its illustrative failure case. Around the April 2026 release of Claude Mythos Preview, Anthropic published a [technical report](https://red.anthropic.com/2026/mythos-preview/), updated its Responsible Scaling Policy risk assessment, and both the [UK AI Security Institute](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities) and [CETaS at the Alan Turing Institute](https://cetas.turing.ac.uk/publications/claude-mythos-future-cybersecurity) ran independent evaluations. AISI reported that Mythos Preview was the first model it has tested to fully complete its 32-step "The Last Ones" enterprise-network attack range on three of ten attempts — a genuinely notable capability jump, reported with unusual candor about its own limits, since the results establish that Mythos can attack weakly-defended systems autonomously — not that it can breach hardened enterprise networks.

Yet the position paper's diagnosis is that even here — arguably the most cooperative disclosure regime currently observable — key risk-report sections remain redacted, capability evaluations rely substantially on internal methodology, and third-party reproducibility of the safety-relevant claims is still structurally unavailable. The point isn't that Anthropic behaved badly relative to peers; it's that "best in class" still lands well short of a standard any other empirical science would accept.

```mermaid
flowchart LR
    A[Frontier model release] --> B[Vendor technical report]
    A --> C[Vendor RSP/framework update]
    A --> D[Independent evaluator report<br/>AISI, CETaS]
    B --> E{
