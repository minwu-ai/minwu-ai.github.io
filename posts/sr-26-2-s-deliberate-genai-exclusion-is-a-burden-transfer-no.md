---
title: "SR 26-2's Deliberate GenAI Exclusion Is a Burden Transfer, Not a Reprieve"
date: 2026-06-26
slug: sr-26-2-s-deliberate-genai-exclusion-is-a-burden-transfer-no
tag: AI Safety
excerpt: "By explicitly placing generative and agentic AI outside its scope, SR 26-2 doesn't shrink the governance problem — it relocates it entirely onto institutions, with no prescribed floor and an examiner who may read the same footnote very differently."
takeaway: "SR 26-2 names generative and agentic AI as 'novel and rapidly evolving' and declines to govern them — but regulators retain full authority to cite unsafe or unsound practices, meaning institutions that treat the exclusion as permission to do less are building governance for a regulatory environment that no longer exists."
published: false
---

## What SR 26-2 Actually Says (and Doesn't)

SR 26-2 was issued jointly by the Federal Reserve, OCC, and FDIC on April 17, 2026, superseding SR 11-7, which had governed model risk management for fifteen years. The biggest operational shift: annual revalidation is out, and risk-based oversight tied to model materiality is in.

The exclusion of GenAI and agentic AI is precise — but narrower than it looks:

| Category | SR 26-2 Status |
|---|---|
| Traditional statistical / quantitative models | Fully in scope |
| Non-generative, non-agentic ML (credit, fraud, BSA/AML) | Fully in scope |
| Generative AI (LLMs, diffusion models) | Explicitly excluded |
| Agentic AI systems | Explicitly excluded |

For most institutions, the bulk of their AI/ML footprint remains governed by the revised guidance. The open question sits only with the newest generative and agentic systems — which is exactly where the institution, not the regulator, now sets the standard.

## The "GenAI Gap" Is Structural, Not Temporary

By carving out GenAI and agentic AI, SR 26-2 didn't shrink the governance problem — it expanded it, pushing responsibility onto enterprise risk frameworks that don't exist yet at most banks.

> "The agencies modernized the baseline and were deliberate about not extending it to generative and agentic AI. That is a reasonable call given how fast the technology is moving, but it does not reduce the risk these systems carry. It relocates the burden." — Kevin Oden, Kevin D. Oden & Associates

The hidden danger is pipeline contamination. Consider a chain many institutions already operate: a generative AI tool parses a borrower's financial statements, that output feeds a credit model, the credit model produces a risk rating, and that rating informs the CECL reserve. The GenAI link is formally out of scope; the credit model downstream is not. SR 26-2 draws a legal line that the data does not honor.

## The Non-Binding Trap

The guidance explicitly states it "does not set forth enforceable standards or prescriptive requirements" — language deliberately broader than SR 11-7's framing. Practitioners should not mistake it for leniency.

The exclusion is not a reprieve from governance — it is a statement that the technology is moving too fast for a fixed framework, and an instruction to build governance anyway. Institutions that treat the carve-out as permission to do less will find that an examiner reading the same footnote reached a different conclusion.

This parallels the pre-crisis SR 11-7 period: that guidance was also non-binding, yet for years it was enforced as de facto binding, with deviations triggering Matters Requiring Attention and driving ratings downgrades. Expect the same trajectory once the forthcoming RFI crystallizes into guidance.

## The Signal in the OCC Press Release

The OCC release notes that "the agencies plan to issue in the near future a request for information that addresses model risk management generally and considers, in particular, banks' use of AI, including generative AI and agentic AI." That RFI is the real governance clock — not SR 26-2's current exclusion.

This mirrors how Basel II handled operational risk: acknowledge complexity, defer prescriptive rules, solicit industry input, then codify expectations once practice matures. The window between the carve-out and the RFI is not a vacation; it is the period during which the industry writes the exam question for itself.

## What Practitioners Should Do Now

- **Build the parallel governance track now.** Banks that build robust frameworks for agentic AI before a formal rulebook exists will shorten the distance between experimentation and production deployment; those that wait will accept elevated risk.
- **Treat the RFI as your filing deadline.** When agencies solicit comments on GenAI MRM, institutions without documented governance programs will have nothing defensible to say.
- **Map GenAI-to-model pipelines explicitly.** Large language models often act as orchestrators feeding inputs into traditional statistical models. The exclusion ends where those interactions begin.

**My read:** The RFI arrives within 12 months, likely mid-to-late 2027. Institutions that treated SR 26-2's exclusion as breathing room will face a compressed remediation window — precisely the dynamic that made SR 11-7 so punishing in its early enforcement years.

## Sources

- [SR 26-2 — Federal Reserve Board (April 17, 2026)](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm)
- [SR 26-2 Full Attachment PDF — Federal Reserve](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf)
- [What Changes with SR 26-2 — Domino Data Lab](https://domino.ai/blog/what-changes-with-sr-26-2)
- [SR 26-2: Model Risk Management Guidance Explained — Domino Data Lab](https://domino.ai/data-science-dictionary/sr-26-2)
