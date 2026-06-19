---
title: "Colorado's AI Governance Retreat: What SB 26-189 Means for Every Enterprise Compliance Program"
date: 2026-06-19
slug: colorado-s-ai-governance-retreat-what-sb-26-189-means-for-ev
tag: AI Governance
excerpt: "Colorado repealed its landmark risk-based AI Act before it ever took effect, replacing it with a disclosure-only regime — a clear signal that SR 11-7-style model governance mandates cannot survive in the current US federal-preemption environment."
takeaway: "The most ambitious state-level attempt to impose substantive model risk governance on private-sector AI has been dismantled under combined industry and federal pressure. Compliance teams anchoring programs to any single state AI framework now have concrete evidence that those anchors can be pulled without warning."
published: false
---

## What Was Lost in the Rewrite

The strongest AI governance law in the United States never governed anything. Colorado's 2024 AI Act (SB 24-205) never took effect; Governor Polis signed SB 26-189 on May 14, 2026, reenacting the rules as a narrower transparency and disclosure regime with substantive compliance landing January 1, 2027. For practitioners who spent two years modeling compliance programs around that law, the lesson is structural, not incidental.

When Colorado enacted the first comprehensive state AI law in 2024, it imported the EU AI Act's conceptual architecture: a risk-based regime built on duties of care, risk management programs, and impact assessments — mapping cleanly onto SR 11-7's model risk management logic. The new law strips all of that in favor of a pre-use notice, a post-adverse-outcome disclosure, and limited consumer rights tied to "covered ADMT."

| SB 24-205 (2024) | SB 26-189 (2026) |
|---|---|
| Duty of reasonable care | No duty of care |
| Mandatory risk management program | No risk management requirement |
| Pre-deployment impact assessments | No impact assessment |
| Discrimination self-reporting to AG | No self-reporting |
| Pre-use notice | Pre-use notice ✓ |
| — | Post-adverse-outcome explanation (30 days) |
| — | Data correction rights / meaningful human review |

The delta is not a refinement — it is the difference between governance and disclosure. Enforcement falls exclusively to the Colorado AG under the Consumer Protection Act; violations are deemed deceptive trade practices, but there is no private right of action.

## How It Happened: Industry Pressure Meets Federal Preemption Threat

When Polis signed SB 24-205 in 2024, he did so with public reservations, inviting the legislature to refine the approach — setting in motion roughly six months of structured stakeholder consultation. That internal process then collided with external federal pressure. On December 11, 2025, President Trump signed an executive order establishing an AI Litigation Task Force to challenge state AI laws and threatening funding cuts over "onerous" statutes. On April 9, 2026, xAI sued in the US District Court for the District of Colorado, arguing the law was unconstitutionally vague, violated the First Amendment through compelled speech, and offended the Dormant Commerce Clause. The DOJ intervened on April 24 — the first time the federal government sought to invalidate a state AI law.

The xAI litigation remains technically active. The enforcement stay applies to SB 26-189 as well, and xAI's preliminary injunction motion must be filed within 28 days of the state finalizing rulemaking — meaning enforcement is contingent on rulemaking, which is currently subject to a court stay.

## The Historical Parallel Worth Noting

This trajectory mirrors the Gramm-Leach-Bliley privacy provisions of the late 1990s, where a strong state baseline was disciplined by federal preemption threats until a federal floor emerged. The difference here: no federal floor exists, and the December 2025 EO explicitly aims to keep it as low as possible. The Commerce Department has yet to publicly release its evaluation of existing state AI statutes, but other state laws may be next on the DOJ's list.

## What Remains — and Why It Still Matters

SB 26-189 is both narrower in scope and broader in reach than the law it replaces: it eliminates the most demanding compliance obligations but pulls employees and job applicants into a notice-and-rights regime that the Colorado Privacy Act expressly excludes. It also voids contract clauses purporting to indemnify a party for its own discriminatory ADMT-related acts — demanding immediate review of AI vendor contracts.

That vendor-contract implication connects directly to the supply-chain risk logic explored in [Microsoft's MAI Family piece](/microsoft-s-mai-family-is-a-vendor-risk-hedge-disguised-as-a/): when indemnification clauses for algorithmic discrimination become void as against public policy, deployers own the liability gap their vendor contracts previously papered over. As [agentic AI compounds that exposure](/agentic-ai-and-the-governance-gap/), the absence of a risk management mandate removes the compliance forcing function that would have surfaced it — not the underlying risk.

> **My read:** The January 1, 2027 effective date is the operative planning horizon, but the litigation stay means enforcement may slip. Build to the statute's text now and treat the stay as a timing hedge, not an exemption.

Two signals will determine whether the disclosure-only model holds: whether xAI files a renewed injunction motion against SB 26-189 specifically, and whether the Commerce Department releases its list of "onerous" state laws — likely triggering a broader DOJ campaign. For teams tracking the EU's parallel trajectory, [Europe's Article 50 enforcement clock](/europe-s-ai-labelling-clock-is-ticking-what-the-final-conten/) is accelerating while the US's most ambitious state regime just decelerated. That divergence is now a material compliance design constraint.

## Sources

- [Colorado Enacts Artificial Intelligence Replacement Law — Seyfarth Shaw](https://www.seyfarth.com/news-insights/colorado-enacts-artificial-intelligence-replacement-law.html)
- [Colorado Governor Signs SB 189 — Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/05/colorado-governor-signs-sb-189)
- [Colorado AI Act Repealed and Replaced — Davis Wright Tremaine](https://www.dwt.com/blogs/privacy--security-law-blog/2026/05/colorado-ai-act-repeal-new-transparency-law)
