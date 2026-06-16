---
title: "EU AI Act: European Commission Publishes Final Code of Practice on AI-Generated Content Transparency"
date: 2026-06-16
slug: eu-ai-act-european-commission-publishes-final-code-of-practi
tag: Governance
excerpt: "The European Commission's June 10 publication of the final Code of Practice on marking and labelling of AI-generated content sets a hard operational clock for generative AI providers and deployers, with Article 50 transparency obligations becoming enforceable on August 2, 2026."
published: false
---

## A Regulatory Milestone Seven Weeks in the Making

The European Commission published the final Code of Practice on marking and labelling of AI-generated content on June 10 — a voluntary playbook arriving roughly seven weeks before the AI Act's transparency obligations begin applying on August 2, 2026. The publication caps a drafting process that began in earnest in late 2025: the code was drafted by six independent experts through a process the Commission said involved more than 187 participants, giving it a stakeholder legitimacy that purely top-down regulation rarely achieves.

The immediate operational fact for compliance teams is straightforward. Providers and deployers wishing to formally sign the code must download the signature form, complete it, and submit it by 22 July 2026 at 18:00 CEST via the EU AI Office email address. In principle, providers and deployers can sign the code at any time, including after 22 July 2026, simply by submitting the signature form. However, signing before the deadline aligns an organisation with the first published list of signatories — a reputational and procurement signal that should not be underestimated.

## What the Code Actually Requires

The technical core of the code sits squarely within the marking and detection obligations of Article 50(2). Providers of AI systems — including general-purpose AI systems — generating synthetic audio, image, video, or text content must ensure that the outputs are marked in a machine-readable format and detectable as artificially generated or manipulated.

The code operationalises this in a layered architecture. The guidance instructs AI providers to use two primary mechanisms for adding metadata: digitally-signed metadata (sub-measure 1.1.1) and imperceptible watermarking (sub-measure 1.1.2). An optional third mechanism — fingerprinting or logging — is also available, though it requires a registry database. Crucially, the code explicitly rejects the idea that a single technical solution could satisfy Article 50 in all cases, instead promoting a multilayered approach combining visible disclosures with invisible or machine-readable techniques, in order to improve resilience against removal or manipulation.

On the deployer side, the obligations are distinct. Section 2 of the code addresses the obligations of deployers of generative AI systems under Article 50(4), setting out commitments on the labelling of deepfakes and AI-generated or manipulated text published for the purpose of informing the public on matters of public interest, while also providing practical guidance on the design, placement, and presentation of labels, disclaimers, or icons. Annex I provides an optional EU icon in three variants that deployers can rely on to easily implement the labelling obligation in a consistent and effective manner.

Beyond technical measures, providers are expected to implement organisational safeguards, including internal frameworks for testing, monitoring, and periodically assessing the effectiveness of labelling solutions, as well as documentation demonstrating the robustness and limitations of the chosen measures.

## Scope: Broader Than Most Organisations Expect

One of the most consequential features of Article 50 is its horizontal reach. Transparency obligations are not limited to systems classified as "high-risk": they apply to any AI system used in the four situations the Article covers — meaning, in practice, Article 50 is relevant to every business that uses generative AI to produce content.

Article 50 may act as the compliance baseline for the AI economy. While it does not impose the heavy conformity assessments of "high-risk" AI or the stringent prohibitions of Article 5, its scope is significantly broader. Model providers who assume that mastering the GPAI obligations under Article 53 — safety, documentation, copyright — provides full coverage are likely mistaken. Some model providers might assume that if they master the Article 53 hurdles, they are in the clear. That can easily lead to overlooking the immense technical implications of the labelling obligation in Article 50(2).

The code also extends to a class of participants beyond direct AI system providers. Technology providers of marking and detection solutions — who develop tools, services, or infrastructure for the watermarking or detection of AI-generated content and place such tools on the EU market — may also sign the code.

## The "Voluntary-but-Not-Really" Dynamic

Legally, the code is voluntary. Strategically, for most organisations operating in the EU market, it is anything but. The final Code of Practice offers a significant legal benefit: the presumption of conformity. Companies that sign the code and implement its measures will be presumed to be compliant with the obligations under Article 50 — and in practice, this creates a strong gravitational pull.

If the code is approved by the Commission, signatories will be able to rely on it to demonstrate compliance. With respect to providers and deployers that adhere to the code, the Commission will focus its enforcement activities on monitoring their adherence to the code. That framing effectively bifurcates the enforcement landscape: signatories face a monitoring regime; non-signatories face an open-ended assessment of whether their bespoke implementations satisfy the statute.

The financial stakes are concrete. Non-compliance with transparency obligations for providers and deployers pursuant to Article 50 is subject to administrative fines of up to €15,000,000 or, if the offender is an undertaking, up to 3% of its total worldwide annual turnover for the preceding financial year, whichever is higher. Provenance metadata that proves whether content is authentic will become both a compliance artifact and evidence.

## Enterprise and Procurement Implications

The publication of the final code reshapes the enterprise AI procurement landscape in at least two directions.

First, contractual compliance flows downstream. For AI providers in particular, the code is increasingly shaping what enterprise customers will expect to see, and require contractually, from their technology partners. Risk and legal teams should be updating vendor agreements now to reflect Article 50 marking obligations, treating watermarking capability and signed metadata support as baseline procurement criteria rather than differentiating features.

Second, the code carries a competitive dimension on interoperability. As the code converges on interoperability standards and common iconography, organisations that have already embedded these into their products and workflows will find it easier to operate across the EU market without bespoke adaptation.

After publication of the code on June 10, the Commission and the AI Board will assess its adequacy. The Commission will complement the code with guidelines on the implementation of the transparency obligations for certain AI systems under Article 50 — guidelines to be published ahead of August 2, 2026.

## What Practitioners Should Do Now

For risk, governance, and applied-AI teams, the immediate priorities are clear:

- **Assess scope exposure.** Map every internal generative AI deployment — regardless of risk tier — against Article 50's four covered situations. Assume broader coverage than your legal team initially expects.
- **Audit technical architecture.** Providers should assess whether their systems support multi-layered marking and auditable detection; deployers should map their content workflows to identify where labelling obligations arise.
- **Decide on signature.** Evaluate whether formal sign-up before the July 22 deadline is achievable. The presumption of conformity and the focused (rather than open-ended) enforcement posture toward signatories make this a risk management decision, not merely a PR one.
- **Update vendor contracts.** Require compliance from AI vendors contractually, and ensure supply-chain agreements specify which party is responsible for embedding and preserving transparency metadata.
- **Preserve metadata in workflows.** Vendors embedding generative AI into their platforms will face provenance questions in the next procurement cycle, and discovery teams will need collection workflows that preserve, rather than strip, transparency metadata.

Compared to earlier drafts, the final code moves decisively away from high-level principles and open questions towards prescriptive, technically detailed commitments, narrowing discretion and signalling how regulators are likely to assess compliance in practice. The window for strategic preparation is narrow. August 2 is not a soft deadline.
