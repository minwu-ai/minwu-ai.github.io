---
title: "GovAI's Embedded Assessments Paper Is the Blueprint CEO Promises Didn't Include"
date: 2026-10-02
slug: govai-s-embedded-assessments-paper-is-the-blueprint-ceo-prom
tag: Regulation & Policy, AI Governance
excerpt: "A September 2026 GovAI paper turns Anthropic's and OpenAI's vague 'embedded evaluator' pledges into a specific design — scope, cadence, and escalation rules modeled on nuclear and banking inspectors — exposing exactly how much the labs' commitments still leave undefined."
takeaway: "GovAI's paper doesn't announce a program — it specifies the seven design choices (scope, access, duration, disclosure, escalation) that will determine whether Anthropic's and OpenAI's embedded-evaluator pledges become real oversight or theater, and California is now studying whether to make a version of it mandatory."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## From pledge to blueprint

On September 21, 2026, the Centre for the Governance of AI published [Embedded Assessments for Frontier AI](https://www.governance.ai/research-paper/embedded-assessments-for-frontier-ai), a paper that does something the recent flurry of CEO announcements did not: it specifies what "embedded evaluators" should actually look like. The authors — Jacob Charnock, Sophie Williams, Zaheed Kara, Markus Anderljung, Alejandro Tlaie Boria, Stephen Casper, Anka Reuel, and Jonas Freund — recommend that frontier AI developers begin hosting embedded assessments now, covering at least three areas central to managing risks from internal AI use: internal agent monitoring, internal agent security controls and permissions, and model alignment, with continuous access and detailed public reports at least quarterly.

This matters because of what prompted it. On September 12, Anthropic CEO Dario Amodei published ["We Must Pace the Frontier,"](https://darioamodei.com/post/we-must-pace-the-frontier) proposing that each frontier AI company commits to giving ongoing, employee-like access to a team of embedded third-party evaluators, whose role is to verify adherence to safety practices and commitments, report incidents, and help assess the alignment of not just completed AI models but training pipelines and processes. OpenAI's Sam Altman matched the pledge within hours, writing that [OpenAI would do the same](https://www.unite.ai/altman-says-openai-will-match-anthropics-embedded-evaluator-pledge/) and would share more "soon." That "soon" is precisely the gap GovAI is trying to fill — a specification problem this site flagged when covering [Apollo Research's Auto-Mode audit](https://minwu-ai.github.io/apollo-research-s-auto-mode-audit-is-a-working-template-for-/) and [California's auditor registry](https://minwu-ai.github.io/california-s-new-ai-auditor-registry-is-real-infrastructure-/): external, pre-deployment red-teaming tells you about a model at a moment in time, not about the institution operating it continuously.

## Why the CEO pledges are thin

Industry coverage since Amodei's essay has converged on the same critique. [TechCrunch](https://techcrunch.com/2026/09/16/anthropic-and-openai-want-to-embed-safety-evaluators-will-they-really-be-independent/) framed it as a test of whether evaluators become watchdogs or window dressing. [CNBC](https://www.cnbc.com/2026/09/16/anthropic-open-ai-model-safety-risks.html) reported more bluntly that details released to date suggest the evaluators would have extraordinary access to frontier AI systems but limited formal authority over the companies developing them, and neither Anthropic's proposal nor OpenAI's framework gives outside evaluators independent authority to halt development or deployment. As of mid-September, OpenAI had not yet published operational details such as who the evaluators will be, what access they will receive, which systems will be reviewed, or how findings will affect development decisions.

GovAI's contribution is to convert that ambiguity into named design choices. The paper examines seven design questions about scope, information gathering, duration, timing, terms of engagement, disclosure, and escalation. That's the difference between a press-release commitment and an auditable standard — the same gap this site noted in [Agentic AI Has Outrun the Governance Playbook](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/): controls built for systems that predict don't automatically specify how you supervise systems that act continuously, inside an organization, with employee-level permissions.

## The institutional precedent is explicit

Amodei's essay itself drew the analogy GovAI formalizes: he explicitly cited embedded bank supervisors as a precedent, writing that his proposal "has precedent in the banking industry, which sometimes involves regulatory 'supervisors' embedded along with employees." The nuclear parallel is older and more tested — the NRC's [resident inspector program](https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/resident-inspectors-bg) has stationed on-site inspectors at the nation's nuclear power plants since the late 1970s, with each plant assigned at least two such inspectors whose work is at the core of the agency's reactor inspection program
