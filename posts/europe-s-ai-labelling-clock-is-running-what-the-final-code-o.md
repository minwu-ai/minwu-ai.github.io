---
title: "Europe's AI Labelling Clock Is Running: What the Final Code of Practice Means for Generative AI Governance"
date: 2026-06-16
slug: europe-s-ai-labelling-clock-is-running-what-the-final-code-o
tag: Regulation & Policy
excerpt: "The European Commission's June 10 Code of Practice on AI-generated content labelling sets the operational framework for Article 50 of the EU AI Act, which becomes enforceable law on August 2, 2026 — leaving enterprises fewer than 60 days to close compliance gaps."
published: false
---

The European Commission has published its final compliance playbook for AI-generated content transparency, and the statutory deadline behind it is not moving. The Commission published the final Code of Practice on marking and labelling of AI-generated content on June 10, 2026 — a voluntary instrument designed to help providers and deployers of generative AI systems meet the transparency obligations that will apply from 2 August 2026. Enterprises that have not yet mapped their generative AI deployments to these requirements have, at best, weeks to act.

## What the Code Actually Requires

The Code is structured around two distinct tiers in the AI supply chain.

The first section covers rules for marking and detecting AI content, applicable to **providers** of generative AI systems. The second section covers labelling deepfakes and certain AI-generated or manipulated text on matters of public interest, applicable to **deployers** of generative AI systems.

The underlying legal obligations — regardless of whether a company signs the Code — are concrete:

- Deepfakes and AI-generated or AI-manipulated text published on matters of public interest must be clearly labelled.
- Users must also be informed when they are interacting with an interactive AI system, such as a chatbot.
- Providers of AI systems that generate synthetic audio, image, video, or text must ensure that outputs are marked in a machine-readable format and detectable as AI-generated.

Three categories require labelling: deepfakes, AI-generated or manipulated text on matters of public interest, and interactive AI systems such as chatbots. The Commission also released standardized EU icons for labelling AI-generated content alongside the Code to reduce implementation friction for providers.

## Voluntary Code, Mandatory Law

The distinction between the Code and the law underneath it is critical for governance teams.

The transparency requirements under Article 50 are legal obligations even though adherence to the Code is voluntary. The Code was drafted by six independent experts through a process the Commission said involved more than 187 participants. It is currently being assessed by the Commission and the AI Board as to its adequacy to ensure compliance.

> **The practical implication:** Signing the Code provides a Commission-endorsed pathway to demonstrate compliance. Not signing it shifts the burden of proof entirely onto the organization to demonstrate an alternative mechanism — a harder position to defend under regulatory scrutiny.

On technical standards, C2PA is the Code's recommended pathway for machine-readable watermarking; adherence to C2PA creates a presumption of compliance. Alternative approaches are permissible if they achieve the same level of detectability, but in practice C2PA has emerged as the industry standard with broad tooling support.

## Penalty Exposure

The stakes are material. Non-compliance with Article 50 transparency obligations is subject to administrative fines of up to €15,000,000 or, if the offender is an undertaking, up to 3% of its total worldwide annual turnover for the preceding financial year, whichever is higher.

Provenance metadata that proves whether content is authentic will become both a compliance artifact and evidence — a point of direct relevance to model risk teams already managing documentation trails under frameworks analogous to SR 11-7.

Note one live legislative wrinkle: the AI Omnibus provisional agreement of May 2026 would grant generative AI systems already on the market before August 2, 2026 until December 2, 2026 to meet the machine-readable marking requirement under Article 50(2). That carve-out applies only to legacy systems and is not yet formally adopted; new deployments after August 2 carry no such buffer.

## What Governance Teams Should Do Now

| Action | Tier | Priority |
|---|---|---|
| Audit all GenAI content pipelines for labelling gaps | Deployers | Immediate |
| Evaluate C2PA watermarking integration | Providers | Immediate |
| Assess Code of Practice signatory status | Both | This month |
| Update AI system inventory / model risk register | Both | Before Aug 2 |
| Brief procurement on vendor transparency obligations | Deployers | Before Aug 2 |

Many organizations still see Article 50 as "just adding a label." In reality, it affects the entire chain: procurement, product development, marketing, communications, security, and data governance — covering watermarking, metadata, provenance, detectors, logging, and preventing removal of markings.

## A Reference Standard in the Making

Beyond EU borders, the Code's three-category labelling structure is already being watched by other jurisdictions building AI disclosure requirements. These rules aim to reduce the risk of misinformation, fraud, impersonation, and consumer deception by fostering trust in the information ecosystem — framing that resonates well beyond European legislative geography. For any enterprise with EU market exposure, August 2 is no longer a planning horizon. It is a deadline.

## Sources

- [European Commission — Code of Practice on Marking and Labelling of AI-Generated Content (June 10, 2026)](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content)
- [EU Digital Strategy — Code of Practice Policy Page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
- [EU AI Act Article 50 — Transparency Obligations (Official Text)](https://artificialintelligenceact.eu/article/50/)
- [EU AI Act Article 50 — Practical Guide](https://artificialintelligenceact.eu/transparency-rules-article-50/)
- [EU AI Act Article 99 — Penalties (Official Text)](https://artificialintelligenceact.eu/article/99/)
- [ComplexDiscovery — Europe's AI Labeling Rules Arrive with a Hard Deadline](https://complexdiscovery.com/europes-ai-labeling-rules-arrive-with-a-voluntary-code-and-a-hard-deadline/)
- [Lexology / Pearl Cohen — Article 50 Transparency Obligations Analysis](https://www.lexology.com/library/detail.aspx?g=90709492-5fd0-43ed-a7c3-e9962fa664ab)
- [EU AI Compass — Article 50 Code of Practice Guide](https://euaicompass.com/eu-ai-act-article-50-transparency-guide.html)
- [EU AI Act Guide — EU AI Icon and Watermarking Rules](https://euaiactguide.com/the-eu-ai-label-is-here-a-first-look-at-the-official-2026-transparency-icons-and-watermarking-rules/)
