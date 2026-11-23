---
title: "The Paper Behind the Pattern: Why Three of This Site's Prior Posts Share One Ancestor"
date: 2026-11-23
slug: the-paper-behind-the-pattern-why-three-of-this-site-s-prior-
tag: Evaluation, Agentic AI
excerpt: "A Stanford/Princeton/Berkeley preprint argues pass/fail benchmark scores are structurally blind to three distinct validity failures — and names log analysis as the missing fourth pillar that several previously covered agent-evaluation findings all trace back to."
takeaway: "Outcome-only benchmarks can't distinguish 'right answer, wrong reason' from 'right answer, right reason' — and arXiv:2605.08545 gives that gap a taxonomy (internal validity, external validity, safety evaluation) and four operating principles, turning a methodology this site has cited repeatedly into a framework with its own name."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔍 The paper this site kept citing without naming

Readers of this site have already met the empirical output of this paper twice without meeting the paper itself. [Why Your Agent's Pass Rate Alone Can't Tell You What You Need to Know](https://minwu-ai.github.io/why-your-agents-pass-rate-alone-isnt-enough/) covered its τ-Bench Airline case study — showing how task flaws suppress scores and how similar pass rates can mask different policy-violation risks. [Same Benchmark Score, Four Times the Risk](https://minwu-ai.github.io/pass-fail-was-never-going-to-catch-this-a-princeton-aisi-apo/) covered a related finding: two models with near-identical benchmark scores differed fourfold in susceptibility to policy-violating persuasion. Both posts, and the agent-reliability piece before them, trace back to the same source: [arXiv:2605.08545](https://arxiv.org/abs/2605.08545), "Log analysis is necessary for credible evaluation of AI agents," by Peter Kirgis, Sayash Kapoor, Stephan Rabanser, Jacob Steinhardt, Arvind Narayanan, and collaborators from Princeton, Stanford, UC Berkeley, UK AISI, Apollo Research, and Transluce. This is the first time the site has treated the paper's actual argument — not one of its downstream findings — as the subject.

## ⚙️ The claim: three ways pass/fail breaks, not one

The paper's structural move is to stop treating "benchmark gave a misleading number" as a single problem and instead split it into three distinct validity failures, each with its own failure mechanism. Scores may misrepresent capability, inflated by shortcuts or deflated by environmental artifacts (internal validity); accurate capability estimates may fail to predict deployment due to differences in context, time horizons, or available assistance (external validity); and evaluations may miss safety-relevant behaviors like costly errors, dangerous reasoning, or harmful actions that correct outcomes conceal (safety evaluation). The authors frame this as a chain of links between a benchmark score and a real-world safety claim, and the paper's thesis is blunt: log analysis verifies each link.

```mermaid
flowchart LR
    A[Benchmark score] -->|Internal validity| B[True capability]
    B -->|External validity| C[Deployment performance]
    C -->|Safety evaluation| D[No hidden dangerous actions]
    A -.log analysis checks.-> B
    B -.log analysis checks.-> C
    C -.log analysis checks.-> D
```

A pass/fail bit, the paper argues, is a lossy compression of a trajectory that may contain a correct answer reached by an illegitimate shortcut, a correct answer that won't generalize past the benchmark's narrow context, or a correct answer purchased with a dangerous intermediate action. Collapsing all three into one bit doesn't just lose detail — it makes the three failure modes indistinguishable from each other and from genuine competence.

## 🧭 The four principles — the part prior posts didn't need to explain

What's genuinely new to cover here is the methodology layer: the paper doesn't just diagnose the problem, it proposes how log analysis should be done so it doesn't become its own unreliable instrument. The first and most load-bearing of the four principles is **defining a validity target** before analysis begins — explicitly choosing whether the goal is testing score-to-capability fidelity (internal), testing capability-to-deployment transfer (external), or surfacing safety-critical actions, because the target determines the burden of proof. That single move explains why the τ-Bench Airline findings read so differently across the two prior posts: one post's near-50% under-elicitation finding is an internal-validity claim, while the cross-model persuasion-susceptibility finding is closer to a safety-evaluation claim — different targets, different evidentiary bars, same underlying method.

The paper is explicit that this is not a replacement pillar but an added one: we do not claim log analysis is sufficient for trustworthy evaluation... there is momentum for log analysis to become a pillar of agent evaluation, but much work remains. It also preempts the obvious rebuttal — that better benchmark design should make log analysis unnecessary — by arguing that as task horizons grow longer, evaluation boundaries thinner, and task success more ambiguous, even the most rigorous evaluators cannot foresee every meaningful shortcut or reward hack an agent will discover. That argument generalizes well beyond any single benchmark, which is precisely the point: it's a structural claim about what pass/fail scoring can ever capture, not a complaint about one dataset's implementation bugs.

## 🧱 Where the argument has edges

Independent review of the
