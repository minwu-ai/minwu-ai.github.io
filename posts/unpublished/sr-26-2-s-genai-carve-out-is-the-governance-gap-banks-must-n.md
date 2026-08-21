---
title: "SR 26-2's GenAI Carve-Out Is the Governance Gap Banks Must Now Fill Themselves"
date: 2026-08-21
slug: sr-26-2-s-genai-carve-out-is-the-governance-gap-banks-must-n
tag: Industry, AI Governance
excerpt: "The first overhaul of U.S. bank model risk management in fifteen years explicitly places generative and agentic AI outside its scope — and a July 2026 Citigroup-affiliated preprint is the first research artifact to propose a systematic, workflow-mapped control framework in response."
takeaway: "SR 26-2's GenAI carve-out transfers the entire governance design burden to individual institutions, with no regulatory template; the Mao, Lin, Kang, Wang preprint (arXiv:2607.04103) is the first practitioner-authored attempt to fill that void with a capability-pattern-to-workflow control map — making it essential reading for bank risk and compliance teams who cannot afford to wait for follow-on guidance."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The Carve-Out Is a Transfer, Not an Exemption

The most consequential sentence in SR 26-2 is buried in a footnote: "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance." That single exclusion means the April 17, 2026 joint issuance by the Federal Reserve, OCC, and FDIC — the first overhaul of model risk management in fifteen years — leaves banks with no regulatory template for the AI systems they are deploying most aggressively.

The carve-out didn't shrink the governance problem; it expanded it. Responsibility shifts onto enterprise risk frameworks that don't exist yet at most banks. When an agentic system invokes a traditional model, that underlying model remains fully in scope — creating a layered accountability problem where the orchestrating layer is ungoverned and the governed layer sits downstream of it.

The historical parallel is instructive. SR 11-7's 2011 issuance left vendor models in a similar gray zone until examiners clarified expectations through supervisory pressure rather than formal guidance. Banks that waited were caught flat-footed. The same dynamic is already visible: examiners are asking every bank, regardless of size, how they govern the AI systems the rule doesn't cover.

## What the Citigroup Preprint Actually Proposes

[Mao, Lin, Kang, and Wang (arXiv:2607.04103)](https://arxiv.org/abs/2607.04103) — researchers affiliated with Citigroup and Florida State University — is the first preprint to attempt a systematic answer. *Not yet peer-reviewed; treat as a practitioner working paper.* The authors' core observation is precise: although generative AI may not directly estimate credit risk or make underwriting decisions, its outputs can materially affect the surrounding control environment through monitoring interpretation, policy analysis, or adverse-action language drafting.

The paper organizes potential uses around five capability patterns — knowledge synthesis, content generation, analytical assistance, interaction, and workflow orchestration — and maps them to major financial workflows. The control logic follows: risk calibration is attached to what a GenAI output *does to a regulated decision*, not whether the model itself meets the SR 26-2 definition of a "model." That reframing is the paper's primary analytical contribution.

The traceability and review controls the paper proposes respond directly to what the [Wolters Kluwer US Banking AI Risk and Governance Index](https://www.wolterskluwer.com/en/news/wolters-kluwer-survey-highlights-ai-governance-and-other-ongoing-needs-for-banking-institutions) found in June 2026: a survey of 230 banking professionals found that 72% identified kill-switch protocols or regulatory reporting of AI failures as their least-prepared area — "not esoteric capabilities — the minimum viable requirements for managing an AI incident in a regulated environment."

## Where Sources Agree — and Where They Differ

There is broad consensus that the carve-out is not a governance holiday. Multiple commentators — from [Domino.ai](https://domino.ai/blog/what-changes-with-sr-26-2) to [Matrix IFS](https://www.matrix-ifs.com/blog/sr-26-02-model-risk-management/) — converge on the view that institutions must identify which other frameworks apply and build controls accordingly.

The disagreement is about *method*. Vendor-facing commentary defaults to NIST AI RMF 1.0 and ISO/IEC 42001 as bridge frameworks. The Citigroup preprint takes a different path: rather than mapping GenAI to a general risk taxonomy, it anchors controls to specific financial *workflow outputs* — adverse-action notices, monitoring conclusions, policy interpretations — where a flawed GenAI contribution is already legally consequential. That workflow-first logic is more defensible under examination precisely because it mirrors how SR 11-7's materiality tests worked.

| Approach | Anchor | Examiner-Readiness |
|---|---|---|
| NIST AI RMF bridge | General risk functions (Govern, Map, Measure, Manage) | Framework-complete; light on banking-specific evidence |
| ISO/IEC 42001 overlay | Management system certification | Process-complete; not calibrated to supervisory expectations |
| Workflow-output mapping (arXiv:2607.04103) | Specific regulated decision touchpoints | Use-case-specific; requires per-workflow documentation |

## What to Watch

The preprint's workflow-output framing will likely influence how forward-looking MRM teams structure their GenAI inventories — not because regulators endorse it, but because it produces exactly the kind of use-case-specific documentation that exam-ready governance requires. The paper's limitation is scope: five capability patterns cover the landscape at a high level, and proposed controls will need institution-specific calibration before they translate into exam evidence.

The broader governance gap connects to a pattern this publication has tracked: [agentic AI has already outrun the governance playbook](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/) in enterprise settings, and SR 26-2's carve-out makes that gap structurally explicit in U.S. banking regulation for the first time. Survey respondents identified lending and underwriting workflows (33%) and collections and recovery (30%) as the functions where agentic AI poses the greatest risk without sufficient human-in-the-loop controls — precisely where GenAI output errors carry the highest regulatory consequence.
