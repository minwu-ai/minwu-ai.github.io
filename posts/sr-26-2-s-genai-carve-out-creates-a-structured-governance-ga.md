---
title: "SR 26-2's GenAI Carve-Out Creates a Structured Governance Gap — and Banks Must Fill It Themselves"
date: 2026-06-30
slug: sr-26-2-s-genai-carve-out-creates-a-structured-governance-ga
tag: AI Governance
excerpt: "The Fed, OCC, and FDIC's April 2026 model risk overhaul explicitly excludes generative and agentic AI from its scope — not as relief, but as a delegation of responsibility that banks now own entirely, without a template."
takeaway: "SR 26-2 does not exempt GenAI and agentic AI from governance — it transfers the obligation to build that governance entirely onto the institution, with no prescribed controls, a forthcoming RFI as the only regulatory signal, and examiners already asking for the evidence."
cover: "/assets/26-2.jpg"
cover_alt: "The regulatory boundary may end at SR 26-2’s scope, but governance responsibility does not. Banks must bridge the gap with institution-specific AI controls."
published: true
---

# 🏛️ What SR 26-2 Actually Says

On April 17, 2026, the OCC, Federal Reserve, and FDIC jointly issued [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm), revised supervisory guidance on model risk management superseding SR 11-7. The update is shorter, more principles-based, and introduces a proportionality threshold relevant primarily to banking organizations over $30 billion in total assets.

The critical sentence sits in the scope section. Generative AI and agentic AI models are described as "novel and rapidly evolving," placed outside the guidance's scope, yet a banking organization's risk management and governance practices should guide the determination of appropriate controls for any tools not covered. Out of SR 26-2 scope is not the same as out of governance scope.

# 🧩 The Gap Is Structural, Not Incidental

The carve-out pushes responsibility onto enterprise risk frameworks that don't exist yet at most banks. Traditional MRM controls don't reach prompt usage, sensitive-data exposure, hallucination, human review of material outputs, output logging, or — for agentic AI — which actions an autonomous agent may take without approval. Those are not edge cases: Goldman Sachs is developing autonomous AI agents with Anthropic for internal functions including trade and transaction accounting, client due diligence, and onboarding ([Reuters](https://www.reuters.com/business/finance/goldman-sachs-teams-up-with-anthropic-automate-banking-tasks-with-ai-agents-cnbc-2026-02-06/)); Lloyds Banking Group expects agentic AI to generate more than £100 million in value during 2026 ([Lloyds Banking Group](https://www.lloydsbankinggroup.com/media/press-releases/2026/lloyds-banking-group/ai-driven-benefits-2026.html)).

There is also a chain-contamination problem SR 26-2 doesn't resolve. Consider a chain already operating at many institutions: a generative AI tool summarizes a borrower's financial statements, and that output feeds a credit model. A systematic error travels into the credit model as a data quality problem, into the risk rating, and into the reserve as a misstatement whose origin is three steps removed from where anyone is looking — auditors will follow that chain to its end regardless of where the AI exclusion begins.

> *"The institutions that treat the carve-out as permission to do less will find that an examiner reading the same footnote reached a different conclusion."* — [Moody's](https://www.moodys.com/web/en/us/insights/banking/from-sr117-to-sr262-managing-model-risk-when-models-dont-stand-still.html)

# ⚖️ Supervisory Liability Did Not Move

Outside the framework is not outside the risk perimeter. Supervisory action may still result from violations of law or unsafe or unsound practices arising from insufficient management of model risk. AI governance questions are increasingly appearing in bank examination and internal audit programs, even as the agencies prepare a dedicated request for information on AI model risk. Institutions therefore should not interpret the carve-out as a reduction in supervisory expectations.

# 📚 The Historical Parallel Worth Taking Seriously

SR 11-7 was technically non-binding when issued in 2011. Within a few years it had been enforced as de facto binding, with deviations triggering Matters Requiring Attention and ratings downgrades — a 2019 [GAO decision](https://www.gao.gov/products/b-331324) even classified it as a rule under the Congressional Review Act. The GenAI RFI will likely follow the same arc: informal today, codified faster than most institutions' governance programs can adapt. The agencies have explicitly stated they plan to issue, in the near future, a request for information addressing model risk management and banks' use of AI, including generative and agentic AI.

This connects directly to the broader problem covered in [Agentic AI Has Outrun the Governance Playbook](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/) — SR 26-2 doesn't resolve that gap in banking; it formalizes it.

# 🛡️ What the Parallel Framework Must Cover

| Domain | Controls Traditional MRM Doesn't Reach |
|---|---|
| GenAI | Use-case intake gates, prompt logging, hallucination detection, human review of material outputs |
| Agentic AI | Enumerated permitted actions, mandatory human-approval points, activity logging, exception escalation |
| Vendor/Third-Party | Periodic re-review of vendor model versioning, prompt stability, data residency, documented exit paths |
| Inventory | GenAI and agentic use cases included regardless of carve-out status; risk-tiered with documented rationale |

# 💡 My Read

Risk and MRM teams have a critical 12-to-18-month window to build enterprise AI governance frameworks before formal rules are codified. Institutions that use it to build a documented, tiered, examiner-ready control library — mirroring SR 26-2's principles where they fit and adding GenAI-specific controls where they don't — will set the informal industry standard the eventual RFI codifies. Those that wait will spend that time catching up to a bar they had the chance to help define.
