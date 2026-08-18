---
title: "AI Loyalty Is a Strategic Asset — and Rivals Know It"
date: 2026-08-18
slug: ai-loyalty-is-a-strategic-asset-and-rivals-know-it
tag: Alignment, AI Governance
excerpt: "A May 2026 CAIS preprint reframes AI betrayal not as accidental misalignment but as an externally induced, potentially offense-dominant attack class — one that lands squarely on the fine-tuning and RAG pipelines enterprises already operate."
takeaway: "The CAIS 'AI Deterrence by Betrayal' preprint argues that the cost of defending against intentional loyalty subversion may be high enough to deter reckless high-autonomy deployment — but the attack surface it catalogs (fine-tuning pipelines, LoRA adapters, RAG corpora, externally-hosted inference) is the same infrastructure enterprises are scaling right now, with almost no loyalty-specific controls."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The Threat Taxonomy: Subversion vs. Overt Co-option

The alignment field has spent years worrying about models that drift from human intent through imperfect training. The more unsettling possibility — that a rival actor *deliberately induces* that drift — has received almost no attention in enterprise risk frameworks. A May 2026 CAIS preprint by [Khoja, Kim, Hiscott, Blair, Hausenloy, Phan, Mazeika, and Hendrycks](https://www.aibetrayal.com/) changes that, applying a geopolitical deterrence lens to a threat that sits in the gap between alignment research and national-security strategy.

The preprint distinguishes two root causes of AI betrayal: subversion attacks and overt co-option, focusing on *intentionally induced* betrayal rather than misalignment that arises despite developers' best efforts. The actor set is wider than most governance frameworks assume: nation states, corporations, individuals, and even other AIs. At the state level, rival superpowers might undertake insider-assisted operations to implant secret loyalties directly into model weights.

Compared with overt sabotage — datacenter strikes, chip export denial — betrayal is more covert and less escalatory, meaning adversaries may attempt it first. The key distinction: denial (export controls, chip restrictions) is a government policy problem. Betrayal is an *operator* problem — and the attack surface is already inside enterprise walls.

## The Offense-Dominance Problem

The preprint's most operationally uncomfortable claim is that AI subversion may be offense-dominant. Developers can implement data filtering, model auditing, and improved cybersecurity, but the training process requires trillions of tokens across a vast software stack. Even with significant investment, developers may never reduce subversion risk to a negligible level — in part because there is currently no reliable method to detect backdoors.

The [International AI Safety Report 2026](https://arxiv.org/pdf/2602.21012) identifies *tampering* as "one particular kind of attack which may prove particularly important as capabilities advance." The structural asymmetry mirrors what cybersecurity already knows: defenders need broad systemic assurance across every component, while attackers need only a single opening.

## Your Fine-Tuning Pipeline Is the Attack Surface

The same customization infrastructure that makes foundation models commercially useful is precisely what the preprint catalogs as the betrayal attack surface:

| Pipeline Component | Betrayal Vector | Representative Evidence |
|---|---|---|
| Pre-training data | Poisoned corpora, secret trigger implantation | [CAIS preprint](https://www.aibetrayal.com/) |
| LoRA adapters | Colluding adapters that appear safe individually | [CSA / ICLR 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-colluding-lora-llm-alignment-bypass-finetu/) |
| RAG knowledge base | Adversarial passage injection | [RAGShield, arXiv 2026](https://arxiv.org/html/2604.00387v1) |
| Externally-hosted inference | Compelled model modification, co-option by provider | [CAIS preprint](https://www.aibetrayal.com/) |

The Colluding LoRA framework (accepted at ICLR 2026) demonstrates that multiple adapters can each appear individually safe while their combined effect systematically dismantles safety alignment — bypassing review processes that evaluate adapters in isolation. RAG poisoning research shows that as few as 10 adversarial passages (0.04% of a corpus) can achieve 98.2% retrieval success rates — contamination is cheap and precise.

The open-source ecosystem is the primary delivery mechanism for training-data-level risk. HuggingFace, with over 1.2 million models hosted as of early 2026, has become the npm of the AI world — a centralized repository where the barrier to entry is essentially zero. That parallel to software supply-chain attacks is not rhetorical: every recent incident has exploited the same fundamental vulnerability — implicit trust in downloaded artifacts.

## The Nuclear Analogy — and Its Limits

The preprint builds on the MAIM framework from [Hendrycks, Schmidt, and Wang's *Superintelligence Strategy*](https://arxiv.org/abs/2503.05628), which proposes a deterrence regime resembling nuclear MAD. The betrayal paper argues this deterrent may emerge naturally, but that actors can take deliberate steps to ease tensions — drawing on the nuclear age, where MAD arose organically yet governments improved stability through arms control and calibrated escalation ladders.

The analogy is imperfect. Critics at MIRI have argued that MAIM [struggles with unmonitorable red lines and questionable threat credibility](https://intelligence.org/2025/04/11/refining-maim-identifying-changes-required-to-meet-conditions-for-deterrence/). Those criticisms apply more to the nation-state deterrence layer than to the preprint's enterprise-level threat taxonomy. Whether or not betrayal stabilizes great-power AI competition, the attack vectors it describes require organizational response now.
