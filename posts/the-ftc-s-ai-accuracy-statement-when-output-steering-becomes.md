---
title: "The FTC's AI Accuracy Statement: When Output Steering Becomes Deception — and a Federal Shot Across State AI Laws"
date: 2026-07-10
slug: the-ftc-s-ai-accuracy-statement-when-output-steering-becomes
tag: Regulation & Policy
excerpt: "The FTC's proposed policy statement reframes AI model alignment and safety guardrails as a potential consumer-deception problem under Section 5 — and simultaneously fires a preemption warning at state AI laws, most explicitly Colorado's, creating a structural compliance trap for every enterprise deploying AI."
takeaway: "The FTC's July 1 proposed statement on AI accuracy puts enterprises in a genuine double bind: state AI laws may require output modifications that the FTC now characterizes as deceptive — and the preemption question will not be resolved before Colorado's revised AI Act takes effect in August."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🎯 The Core Deception Theory

The proposed statement describes how AI companies that distort outputs to achieve undisclosed ideological objectives could be deceiving consumers under Section 5 of the FTC Act. The mechanism is the standard three-part deception framework: AI companies have made explicit and implicit representations that their systems produce the most accurate, faithful output possible — and because consumers accept AI outputs without independent fact-checking more than 90% of the time, there is a reasonable expectation that systems aren't secretly pursuing undisclosed objectives.

This differs from earlier FTC AI initiatives focused on deceptive *claims about capabilities* — the statement looks at whether systems are *designed* to pursue undisclosed objectives. That's a meaningful doctrinal shift: the FTC is now looking inside the model, not just at the marketing.

The FTC distinguishes intentional output steering from hallucinations, stating that inaccuracies from technological limitations generally don't raise the same concerns. The line: design choice versus technical constraint. Guardrails reflecting deliberate value-loading — equity objectives, harm mitigation, politically sensitive topic avoidance — sit in the former bucket unless disclosed.

## The Guardrail Trap

This collides directly with mainstream AI safety practice. Post-training tuning that model providers treat as a safety obligation could be read as undisclosed manipulation of the product consumers thought they were buying — putting virtually every RLHF-era alignment technique into a gray zone.

The FTC's safe harbor is narrow: disclosures must be sufficiently prominent to alter consumer expectations and cannot be buried in terms of service. For enterprises deploying third-party models, this raises an immediate vendor-risk question: do your upstream providers' disclosures actually reach your end users?

> **The analytical point most coverage misses:** The FTC is not prohibiting output steering. It is requiring that steering be *disclosed at the level of consumer impact* — a standard almost no current product UI meets.

## The Preemption Shot

The statement was issued pursuant to Executive Order 14365 (December 11, 2025), directing the FTC to address how state laws requiring alterations to AI outputs can conflict with federal law. The statement singles out Colorado's Artificial Intelligence Act as a law that may pressure AI companies to suppress accuracy to avoid disparate impact liability, concluding it is impliedly preempted to the extent it conflicts with Section 5. This directly targets the revised Colorado law covered in our earlier analysis of [Colorado's AI Governance Retreat](https://minwu-ai.github.io/colorado-s-ai-governance-retreat-what-sb-26-189-means-for-ev/) — and the FTC's position is that even the narrowed SB 26-189 creates the same conflict.

The preemption theory is legally contested. The FTC Act neither explicitly preempts state law nor occupies the entire field of consumer protection regulation. To preempt state authority over AI, the FTC would need to issue a formal rule complying with the Administrative Procedure Act and its own heightened rulemaking procedures. A policy statement will not suffice.

| Dimension | FTC Position | Critical Response |
|---|---|---|
| Preemption basis | Implied conflict preemption via Section 5 | FTC Act has no express preemption clause; courts presume against it |
| Instrument | Proposed policy statement | Courts require formal APA rulemaking for preemptive effect |
| Target | Colorado AI Act (disparate impact duty) | Colorado's August 1 effective date arrives before any court ruling |
| Safe harbor | Clear and conspicuous disclosure | No product UI standard defined |

The preemption position is the farthest-reaching aspect of the proposal — its logic extends to many other contexts and could produce unintended consequences if adopted in reverse by a more aggressively pro-regulatory administration.

## Compliance Reality Right Now

If you are subject to state AI laws, especially Colorado's revised Act, there is real tension: state law may push toward output adjustments that the FTC says could be deceptive unless prominently disclosed. Document your compliance choices and consider whether transparent disclosure can satisfy both regimes.

For financial institutions, the double-bind is acute. The FTC notes the statement may be particularly significant for institutions deploying AI in fraud detection, underwriting, and compliance — compounding the unresolved governance gap documented in our [SR 26-2 analysis](https://minwu-ai.github.io/sr-26-2-s-genai-carve-out-creates-a-structured-governance-ga/).

## What to Watch

The comment period closes July 31, 2026 — the same week Colorado's revised Act nears effectiveness. **My read:** the preemption theory won't survive its first serious court challenge without formal rulemaking, but the deception theory is durable and immediately actionable. Treat the disclosure standard — not the preemption gambit — as the operative compliance pressure. Map every intentional output constraint in your deployed models, trace whether disclosure reaches end users, and file comments if the definition of "adequate disclosure" matters to your product stack.
