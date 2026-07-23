---
title: "Article 50 Goes Live in Days — and the Conformity Split Is Already Locked In"
date: 2026-07-23
slug: article-50-goes-live-in-days-and-the-conformity-split-is-alr
tag: Regulation & Policy
excerpt: "The European Commission's July 20 final guidelines on EU AI Act Article 50 arrive eleven days before the August 2 enforcement date, creating a durable asymmetry between Code of Practice signatories and everyone else — and exposing a technical gap in watermarking that neither document fully resolves."
takeaway: "Article 50 is the EU AI Act's first provision to carry real enforcement teeth, and the conformity divide between Code of Practice signatories and non-signatories is now fixed — with national market surveillance authorities free to act on August 2 regardless of whether harmonized watermarking standards exist."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

The EU AI Act's first major compliance stress test is not the high-risk provisions enterprises have been stress-modeling for years. It is Article 50 — and it is arriving Sunday, August 2, with enforcement authority intact and no grace period for the companies that missed last week's signatory window.

On July 20, the European Commission adopted the final version of its Guidelines on the implementation of the transparency obligations under Article 50 of the AI Act, less than two weeks before those obligations begin to apply. As covered in depth in [Europe's AI Labelling Clock](https://minwu-ai.github.io/europe-s-ai-labelling-clock-is-ticking-what-the-final-conten/) and [One Vote Left: Why August 2 Still Matters More Than the Omnibus](https://minwu-ai.github.io/council-vote-this-week-closes-the-legislative-loop-august-2-/), this date has been approaching for months. What is new is that the final guidance has arrived — and the Code of Practice signatory window has closed.

## What Article 50 Actually Requires

Providers of AI systems designed to interact directly with natural persons must inform those persons, before or at the start of each interaction, that they are communicating with an AI system. Separately, providers and deployers using AI to generate synthetic audio, image, video, or text must ensure the output carries machine-readable disclosure markers before distribution.

All Article 50 obligations — chatbot disclosure, deepfake labeling, AI-generated public-interest text labeling — apply from August 2 without exception. The transparency obligations were not postponed by the Digital Omnibus. A breach carries a fine of up to €15 million or 3% of total worldwide annual turnover, whichever is higher.

One clarification in the final text matters operationally: there is no retroactive labelling obligation, but the cut-off works differently by modality. Image, audio, and video deep fakes generated before August 2 do not need to be marked retroactively — the relevant date is the date of generation. For text publications on matters of public interest, the relevant date is the date of publication, so text generated before August 2 but published on or after that date must be labelled.

## The Conformity Split That Is Already Locked In

July 22, 2026 at 18:00 CEST was the deadline to submit a signatory form to the EU AI Office and appear on the initial list of Code of Practice signatories. Signing confers a presumption of regulatory conformity, reducing enforcement risk and evidentiary burden.

The Code is open not only to providers and deployers directly bound by Article 50, but also to actors not directly bound by them. Adherence is not a guarantee of compliance, but the Code is expected to serve as the main reference point for regulators' assessments, while non-signatories will need to demonstrate compliance through other means and may face greater scrutiny.

> Non-signatories are not in violation — but they now carry the full evidentiary burden of demonstrating compliance independently, to 27 separate national authorities, with no shared reference framework.

Article 50 enforcement is decentralized — national market surveillance authorities in each member state carry it, which means enforcement intensity will likely vary by country and the first test cases may come from the more active regulators rather than Brussels. A structural fragility compounds this: many member states failed to meet the August 2025 deadline to establish market surveillance authorities. As of the last update, only 9 member states had designated both market surveillance and notifying authorities, while 12 had pending proposals or partial designations, and 6 had yet to designate any competent authority. The enforcement map is uneven before the first case is filed.

## The Watermarking Gap the Guidelines Cannot Close

The guidelines explicitly acknowledge that technical standards for measuring compliance with the watermarking obligation are still being developed through the Code of Practice and EU standardization work. That is a significant admission eleven days before enforcement.

No single current technology fully meets all four statutory requirements — effectiveness, interoperability, robustness, and reliability. The C2PA content credentials standard can be stripped by a screenshot or social media re-upload. Imperceptible watermarks like Google's SynthID survive more processing but are not universally robust. The Code therefore mandates a layered approach combining metadata, watermarking, and logging — and explicitly sets requirements in advance of the industry benchmarks needed to measure them.

There is also a sovereignty wrinkle: Google's SynthID requires Google's detection API for verification. Under Article 50, detectability must not require a proprietary or third-party-controlled service. SynthID alone is insufficient for EU compliance unless paired with a C2PA layer or a detection API the operator controls.

## The Digital Omnibus Complication

On June 29, the Council of the EU gave its final green light to the Digital Omnibus on AI. The final act was signed on July 8, 2026, and the regulation is awaiting publication in the Official Journal of the European Union — a necessary step before it can enter into force. As of this writing, that publication has not occurred.

The amended dates do not bind until formal adoption and Official Journal publication. The practical consequence: the December 2, 2026 Article 50(2) transparency grace period for legacy systems is real in political terms but not yet legally operative. Companies banking on that relief for pre-existing systems are building on a text that is not yet law.

| Obligation | Effective Date | Notes |
|---|---|---|
| Chatbot / agent AI disclosure (Art. 50(1)) | August 2, 2026 | No relief; applies to all systems |
| Deepfake & public-interest text labelling (Art. 50(4)) | August 2, 2026 | Date of publication triggers label duty |
| Machine-readable marking, new systems (Art. 50(2)) | August 2, 2026 | No grace period for post-Aug 2 deployments |
| Machine-readable marking, legacy systems (Art. 50(2)) | December 2, 2026 | Contingent on Digital Omnibus OJ publication |

## What to Watch

The first Article 50 enforcement actions will reveal which national regulators move fastest and whether they target GPAI providers (where the AI Office has supervisory overlap) or deployers. The Code of Practice signatory list — published before August 2 — will function as a de facto compliance signal: major global AI providers signing first will effectively set the technical standard; once they agree on a specific watermarking or metadata approach, it will likely become the de facto market requirement.
