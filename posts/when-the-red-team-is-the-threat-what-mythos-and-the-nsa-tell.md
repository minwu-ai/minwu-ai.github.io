---
title: "When the Red Team Is the Threat: What Mythos and the NSA Tell Us About AI Control"
date: 2026-07-01
slug: when-the-red-team-is-the-threat-what-mythos-and-the-nsa-tell
tag: AI Safety
excerpt: "An authorized red-team evaluation showing Anthropic's Mythos model surfacing classified-system vulnerabilities in hours — and the regulatory shock wave that followed — has exposed a structural gap between frontier AI capability and every existing control framework."
takeaway: "The Mythos episode proves that dangerous-capability evaluations can themselves become the policy trigger — and that 'authorized test' and 'national security threat' are no longer mutually exclusive categories, demanding control architectures that are operational before red-team results are classified."
published: false
---

## The Signal Beneath the Hype

The headline that spread virally — "AI hacked the NSA" — was wrong in the ways that matter for governance practitioners, and right in the ways that matter even more. The actual story: Senator Mark Warner said General Joshua Rudd told him Mythos "broke into almost all of our classified systems, not in weeks, but in hours." But as [The Next Web reported](https://thenextweb.com/news/anthropic-mythos-classified-systems-vulnerabilities), finding a weakness within hours is not the same as exploiting it within hours.

The corrected reading is almost more alarming: the model reportedly identified weaknesses and gained access across nearly every classified system targeted — completing in hours what human operators would have taken weeks or months to accomplish. That is a dangerous-capability threshold event, regardless of how "breach" is defined.

## The Policy Response Was First, the Evidence Came After

The regulatory sequence is consequential. On June 12, the Trump administration directed Anthropic to restrict Fable 5 and Mythos 5 to US citizens only; unable to verify nationality at scale, Anthropic's only option was a full global shutdown, cutting off allies, researchers, and its own foreign-national employees with 90 minutes' notice. The Warner–Rudd testimony only became public ten days later.

This marks the first time the United States has applied export controls directly to an AI model rather than to the hardware powering it. As [Nextgov/FCW reported](https://www.nextgov.com/artificial-intelligence/2026/06/parts-nsa-lose-mythos-5-access-amid-anthropic-supply-chain-dispute/414366/), the irony ran deep: parts of the NSA itself lost Mythos 5 access. The ban has since been lifted, with Anthropic announcing access restoration from July 1 after receiving Department of Commerce permission.

## The Contradiction the Government Cannot Resolve

The governance fracture is more interesting than any specific red-team claim. The same government that depends on the model has also restricted it, opposed expanding it, and branded its maker a national security supply-chain risk. Meanwhile, roughly six Anthropic engineers are embedded directly inside the NSA, adapting Mythos for operational applications including, per sources, infiltrating networks operated by China and Iran.

This is not incoherence — it is the predictable outcome of a government trying to simultaneously exploit and contain a capability it does not control. The historical parallel is nuclear dual-use policy in the 1950s: the same enrichment science that powered deterrence required export licensing the moment it threatened to proliferate. Warner's target was anyone who would leave model safety to company good faith alone, with no independent testing requirements.

## What Existing Control Frameworks Don't Cover

This connects directly to [DeepMind's AI Control Roadmap](https://minwu-ai.github.io/deepmind-s-ai-control-roadmap-from-trust-the-model-to-contai/), which identifies that for high-risk actions such as major cyber attacks, systems must shift to real-time prevention, with controls based on the deployed model's detection evasion and attack execution capability. The Mythos episode exposes the gap: DeepMind's architecture governs what deployed agents *do* — but presupposes evaluators already know the capability level before a red team runs.

> **The control problem**: Existing frameworks treat red-team evaluation as *input* to a containment decision. Mythos shows that the evaluation itself can become the threat vector — or the political trigger — before any containment layer is in place.

Helen Toner of Georgetown's Centre for Security and Emerging Technology warned that restricting foreign nationals "is essentially equivalent to preventing any company affected from doing any further AI R&D work." Former FBI cyber official Cynthia Kaiser noted that hackers are already purchasing American identities to access restricted models — meaning the export order imposes asymmetric costs on defenders more than adversaries. Practitioners who built supply-chain governance around model access (covered in the [prior post on this shutdown](https://minwu-ai.github.io/the-government-just-killed-two-frontier-models-overnight-and/)) now face a second-order problem: the evaluation regime itself is ungoverned.

## What to Watch

- **Red-team disclosure norms**: Anthropic has not disclosed what the NSA test found, and has already finished training a Mythos successor — the capability is advancing regardless of how politics settle.
- **Mandatory pre-release evaluation**: Warner's argument for compulsory government testing before frontier launches remains live; Anthropic's decision to launch Fable 5 without following the [Trump executive order's 30-day voluntary window](https://minwu-ai.github.io/trump-s-ai-executive-order-builds-the-scaffold-but-won-t-lig/) is the proximate friction point.
- **Allied fragmentation**: The UK AI Security Institute was locked out of systems it was actively evaluating — signaling that frontier model access is now a sovereign dependency question, not just a procurement one.

**My read**: The real precedent is epistemic, not regulatory. When a government restricts a model *because* an authorized red team found too much, it confirms that dangerous-capability evaluations have become a triggering condition rather than a governance input. Every frontier lab now has an incentive to make its red teams less legible — exactly the wrong outcome. The [METR Frontier Risk Report](https://minwu-ai.github.io/the-insider-threat-you-built-yourself-metr-s-frontier-risk-r/) warned that limited strategic judgment is the primary gap; this episode suggests the institutional judgment surrounding evaluations is equally fragile.
