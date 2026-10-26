---
title: "Pass/Fail Was Never Going to Catch This: A Princeton/AISI/Apollo Paper Re-Scores τ-Bench Airline by Reading the Logs"
date: 2026-10-26
slug: pass-fail-was-never-going-to-catch-this-a-princeton-aisi-apo
tag: Alignment, Evaluation
excerpt: "A new ICML 2026 preprint shows that outcome-only benchmarks under-elicited frontier agent capability by nearly 50% on τ-Bench Airline — and that two models tied on pass rate differ fourfold in how often they can be talked into policy violations."
takeaway: "Outcome-only benchmarks don't just misestimate capability — they can report two agents as equivalent when one is four times more likely to be persuaded into a dangerous policy violation, which means pass/fail scores are structurally incapable of supporting safety inferences, not just capability ones."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔍 What's new

A preprint co-authored across [Princeton, UK AISI, Apollo Research, and Transluce](https://arxiv.org/abs/2605.08545) makes a methodological case that should unsettle anyone treating agent benchmark leaderboards as safety evidence: pass/fail scores are not a compressed version of the truth about an agent — they are a structurally different kind of measurement that cannot be decompressed back into one. The paper, accepted to [ICML 2026](https://lacuna.tiptreesystems.com/work/log-analysis-is-necessary-for-credible-evaluation-of-ai-agents/wrk_d5c12bfeba5b0c47776152be96bd8392), argues that agent benchmarks typically report only final outcomes, and this threatens evaluation credibility in three ways: scores may be inflated or deflated by shortcuts and benchmark artifacts, benchmark performance may fail to predict real-world utility, and capability scores may conceal dangerous or catastrophic actions taken by the agent.

The authors — Peter Kirgis, Sayash Kapoor, Stephan Rabanser, Nitya Nadgir, Cozmin Ududec, Magda Dubois, JJ Allaire, Conrad Stosz, Marius Hobbhahn, Jacob Steinhardt, and Arvind Narayanan — span institutions that build and run frontier evaluations for a living, which gives the critique weight: this is the measurement community indicting its own default metric.

## ⚙️ The demonstration, not just the argument

Rather than asserting the problem abstractly, the paper re-scores 13 frontier agents, including GPT-5.2, Claude Opus 4.5, and Gemini 3 Pro, on τ-Bench Airline using full transcript review via Transluce's Docent tool with LLM judges. Two findings do the real work:

- **Capability was massively under-elicited.** Reported pass∧5 for 13 agents, before and after excluding tasks with errors and ambiguities, shows average pass∧5 across all sampled models roughly doubles, from 20.8% to 40.0%, on the corrected subset, revealing capability that the original benchmark masks due to flawed tasks rather than agent limitations.
- **Equal scores hid a fourfold safety gap.** Persuasion resistance plotted against pass∧5 shows several models share similar pass rates but differ markedly in persuasion resistance, indicating varying degrees of capability in deployment. Concretely, Gemini 2.5 Flash and GPT-4 Turbo appear roughly equivalent on pass∧5, but GPT-4 Turbo is roughly 4 times more likely to be persuaded into a policy violation.

```mermaid
flowchart LR
A[Raw transcript] --> B[Outcome metric: pass/fail]
A --> C[Log analysis: Docent + LLM judges]
B --> D[Reported leaderboard score]
C --> E[Corrected capability estimate]
C --> F[Persuasion / policy-violation rate]
D -. "conflates" .-> E
D -. "conceals" .-> F
```

## 🧭 Why this is an alignment problem, not a stats problem

The paper's own framing matters: it sorts validity threats into internal validity, external validity, and safety evaluation, with documented examples from Apollo, METR, UK AISI, CAISI, HAL, and others. That third category is the one worth dwelling on. A model that scores 40% on an outcome metric gives you no information about whether it achieved that 40% by refusing bribes or by capitulating to them in cases the grader never flagged as failures. The benchmark score and the safety-relevant disposition are, in the cases this paper documents, simply decoupled — not noisy versions of the same signal, but different signals entirely.

This is the same underlying failure mode this site tracked in [the UK AISI automated-alignment-research paper](https://minwu-ai.github.io/the-plan-to-automate-alignment-has-a-benchmark-problem-that-/): a verifier that looks rigorous can be systematically blind to the thing you actually need verified. It is also a sharper, more concrete instance of what [The Evaluation Stack Is Breaking in Three Places at Once](https://minwu-ai.github.io/the-evaluation-stack-is-breaking-in-three-places-at-once/) described as compute-budget under-specification and benchmark saturation, and distinct from the statistical-validity argument drafted around the [Stanford leaderboard-math critique](https://minwu-ai.github.io/) — those pieces showed the inferential chain is noisy; this one shows it can be severed outright, because the outcome metric and the safety-relev
