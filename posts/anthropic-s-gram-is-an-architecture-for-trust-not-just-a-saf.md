---
title: "Anthropic's GRAM Is an Architecture for Trust — Not Just a Safety Feature"
date: 2026-07-09
slug: anthropic-s-gram-is-an-architecture-for-trust-not-just-a-saf
tag: AI Safety
excerpt: "Gradient-Routed Auxiliary Modules isolate dual-use knowledge into removable neural compartments, pointing toward a future where AI capability tiers are governed by verified trust levels — with direct implications for vendor risk, export controls, and emerging AI governance."
takeaway: "GRAM introduces a fundamentally different way to think about AI safety: treating certain high-risk capabilities as removable infrastructure rather than relying solely on behavioral guardrails. If that approach ultimately scales, AI governance may evolve from choosing between models to governing which capabilities are present in a deployed system."
cover: "/assets/4A02872F-7960-4414-B1B3-511277E68BC5.png"
cover_alt: "Illustration: Can AI Modularize its Knowledge"
published: true
---

# 🔬 What GRAM Actually Does

Anthropic's most interesting research announcement of the year landed on July 8—the same day Reuters reported that the Trump administration had approved OpenAI's broad GPT-5.6 rollout following additional testing. While much of the attention focused on export controls and frontier model deployment, [Anthropic and AE Studio published GRAM](https://www.anthropic.com/research/off-switch-dual-use), a pretraining architecture asking a different question:

> What if dangerous knowledge could simply not exist in the version of the model a regulator or enterprise deploys?

Put differently, GRAM asks whether some AI capabilities can be **designed to be removable** rather than merely suppressed. Instead of trying to make a fully trained model *forget* dangerous knowledge—a notoriously difficult problem because knowledge becomes distributed across billions of parameters—it changes how that knowledge is learned in the first place.

The core insight is architectural, not behavioral. GRAM gives a model dedicated, removable compartments for each dual-use knowledge category—additional neurons integrated into every Transformer layer and organized into separate auxiliary modules. During pretraining, the model learns to route designated knowledge into those modules. When a module is deleted, the model behaves as though it had never learned that category. When enabled, the knowledge is fully available.

That makes GRAM fundamentally different from what is often called **post-training unlearning** or "de-training." Traditional unlearning attempts to remove knowledge after it has already diffused throughout a model's parameters. GRAM instead tries to **prevent certain categories of knowledge from becoming inseparable** by routing them into dedicated modules during pretraining. If successful, removing a capability becomes closer to removing a software component than retraining an entire foundation model.

That is the critical distinction from previous safety approaches. Refusal training and output classifiers sit on top of knowledge the model still possesses—and therefore remain vulnerable to jailbreaks. Whole-model access controls force organizations to choose between an entire model being available or unavailable. GRAM instead suggests that individual capabilities themselves could become configurable.

Anthropic's experiments also suggest an encouraging security property. According to the accompanying GitHub repository, removing a GRAM module proved substantially more resistant to recovery through adversarial fine-tuning than conventional post-hoc unlearning approaches.

# ⚠️ The Honest Limitations

This remains early-stage research. GRAM has not been demonstrated on production Claude models or other frontier-scale systems. The published experiments evaluated models up to 5 billion parameters—orders of magnitude smaller than today's largest foundation models.

There is also a deeper scientific question. Knowledge inside large language models is highly interconnected. Virology overlaps with biology, chemistry, medicine, and even general scientific reasoning. It remains an open research problem whether those capabilities can be isolated cleanly without degrading useful adjacent knowledge.

That uncertainty is precisely what makes GRAM interesting. For years, researchers have largely assumed that once knowledge is learned, it becomes inseparable from the rest of the model. GRAM challenges that assumption by asking whether certain capabilities can remain modular from the beginning. Whether that modularity survives frontier-scale training is still unknown.

# 📋 The Governance Signal Is the Story

What makes GRAM significant is not simply the research result—it is the model for AI governance that it implies.

| Safeguard layer | What it controls | Adversarial robustness |
|---|---|---|
| Refusal training | Model outputs | Low — jailbreakable |
| Output classifiers | Model outputs | Low — continual retuning required |
| Post-hoc unlearning | Existing weights (approximate) | Moderate — partially recoverable |
| GRAM modules | Dedicated architectural components | Higher — capability structurally removed |

If GRAM-class architectures eventually reach production, vendors could offer the same base model at multiple capability tiers: a virology module enabled for accredited biosecurity laboratories, disabled for general enterprise deployments, or additional cybersecurity capabilities available only to verified customers.

That would transform AI governance from a binary question of **which model** an organization is permitted to deploy into a more granular question of **which capabilities** are authorized, auditable, and appropriate for a particular user or environment.

This possibility maps naturally onto several emerging governance trends.

**Illinois SB 315**, signed into law on July 6, requires frontier AI developers to publish catastrophic-risk safety frameworks and obtain recurring independent third-party audits beginning in **2028**. An auditor assessing whether a high-risk capability has been structurally removed—supported by verifiable technical evidence rather than repeated jailbreak testing—would have a much more concrete assurance target. GRAM is still research, but it illustrates the kind of architectural evidence future governance frameworks may eventually be able to rely upon.

**Export controls** present another interesting thought experiment. Rather than treating an entire frontier model as export controlled, a future GRAM-like architecture could, in principle, allow specific regulated capabilities to be removed before deployment, accompanied by cryptographic or other verifiable attestations demonstrating what functionality is present. Whether policymakers would ultimately accept such an approach is a separate question, but it illustrates how architectural innovation could expand the policy toolkit beyond today's largely all-or-nothing model restrictions.

**Vendor risk management** also gains a new due-diligence question. Instead of asking only which foundation model a vendor uses, organizations may eventually ask which capability modules are present, which have been removed, and how those claims can be independently verified. That connects naturally to the model supply-chain questions raised in [Microsoft's MAI family analysis](https://minwu-ai.github.io/microsoft-s-mai-family-is-a-vendor-risk-hedge-disguised-as-a/) and the containment-oriented governance discussed in [DeepMind's AI Control Roadmap](https://minwu-ai.github.io/deepmind-s-ai-control-roadmap-from-trust-the-model-to-contai/).

# 💭 My Read

> GRAM does not solve AI safety—and it does not claim to. What it does is introduce a fundamentally different way to think about one of the field's hardest problems.

For years, the prevailing assumption has been that once a model learns dangerous knowledge, the challenge is preventing it from using that knowledge through behavioral controls. GRAM asks a different question:

> **What if some capabilities could be architected to remain removable from the beginning?**

That shift—from behavioral control toward architectural capability design—may ultimately prove more important than GRAM itself.

The closest historical analogy is export-controlled cryptography in the 1990s, where different cryptographic strengths were licensed for different jurisdictions and products encoded compliance directly into their architecture. GRAM points toward a similar possibility for AI capability governance.

Whether this particular implementation ultimately succeeds is almost secondary.

The more important contribution is demonstrating that **"de-training" does not necessarily have to mean making a model forget after training**. It may instead mean designing the training process so that certain categories of knowledge remain modular, removable, and verifiable from the outset.

**What to watch:** Whether future frontier model safety frameworks—including Anthropic's eventual compliance with Illinois SB 315—begin treating architectural capability isolation as a recognized mitigation alongside behavioral safeguards. If they do, GRAM may be remembered less as a single research paper than as the beginning of a new way to engineer trust into foundation models.
