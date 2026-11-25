---
title: "OpenAI Says Automated Red-Teaming Took GPT-6 Astra From 59% to 91.5% on Cyber Jailbreaks. Five Days Later, UK Testers Found the Next Model Regressed."
date: 2026-11-25
slug: openai-says-automated-red-teaming-took-gpt-6-astra-from-59-t
tag: Industry, AI Safety
excerpt: "OpenAI's November 12 'Fuzzy Robustness' write-up documents a large measured safety gain from automated adversarial training — but the method's own limits showed up almost immediately in the very next model."
takeaway: "A vendor-reported jump in safe-response rates describes performance against the attacker that produced it, not a durable property of the model — and OpenAI's own system card for the next Astra release shows that gap closing again within weeks."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔍 The headline number

On November 12, OpenAI published [a research write-up](https://openai.com/safety-alignment/fuzzy-robustness/) describing how automated adversarial training improved what it calls "fuzzy robustness" — the reliability with which a model withholds disallowed help under sustained jailbreak pressure, in domains where safety is hard to specify precisely. The topline comparison is stark: on cyber, GPT-6 Astra answered 91.5% safely, compared with 59% for GPT-5.6 Sol, measured against a [fixed set of prior jailbreaks](https://openai.com/index/path-to-astra/) generated against earlier model generations, plus an adaptive multi-turn evaluation where multiple attackers are prompted to extract information that meaningfully uplifts harm, and GPT-6 Astra remains more robust than GPT-5.6 Sol across all attacker budgets.

This is a lab research write-up, not a product launch — and that distinction matters. OpenAI is making a methodological claim: that scaling attacker compute and requiring repeated success, a criterion it calls "worst@n," generates adversarial training data reliable enough to move safety numbers this far in one generation. The company also reports the gain came without the usual overrefusal tax: it measured whether the robustness-trained model was more likely to refuse benign tasks, and found this was not the case for GPT-6 Astra.

## ⚙️ How the method works

```mermaid
flowchart LR
    A[Seed prompts:<br/>cyber, bio, violence] --> B[Automated attacker<br/>iteratively jailbreaks]
    B --> C{worst@n:<br/>succeeds across<br/>repeated tries?}
    C -->|yes| D["Robustified" prompt<br/>dataset]
    C -->|no, discard| B
    D --> E[Safety training data]
    E --> F[GPT-6 Astra / Sol]
    F --> G[Re-evaluated against<br/>fixed + adaptive jailbreaks]
    G -.feedback loop.-> B
```

The attacker itself is notable: OpenAI reports the helpful-only reasoning model had no specific training on how to jailbreak other models — it is an emergent phenomenon — and adding attacker training tasks, such as GPT-Red, can significantly improve the efficiency and efficacy of the attacker. That echoes the structure of [Anthropic's Anvil system](https://safeguards.anthropic.com/2026/automated-red-teaming/), published the same month, which similarly uses a frontier model as the attacker and reports that when humans and Anvil attempt the same jailbreak strategies, Anvil usually executes them better, finding more cyber breaks faster than expert human red-teamers. Two labs, converging independently on the same idea: let the frontier model attack itself, and train on what breaks.

## 🧱 What the curve doesn't show

An outside synthesis of the same release flagged the central limitation plainly: the paper demonstrates evidence that automated red-teaming can create useful training material, not a deployment-wide safety rate — the remaining question is how well that resistance carries beyond the attacks and domains researchers tested. The 91.5% figure describes performance against *this* evaluation set, built from *this* attacker generation, at *this* moment. It is not a property of GPT-6 Astra that travels automatically to new attack strategies, new domains, or future model updates.

That caveat stopped being theoretical within days. OpenAI's own system card for the follow-on release — GPT-6.2 Astra, published November 17 — disclosed that [UK AISI](https://venturebeat.com/security/openais-pre-release-gpt-6-2-astra-was-easier-to-jailbreak-than-its-predecessor-uk-government-testers-found) identified a substantial regression in robustness relative to GPT-6 Astra, building a universal jailbreak against two pre-release versions of GPT-6.2 Astra, using half as many model queries as it needed against GPT-6 Astra. UK AISI's red-team lead [called it](https://dev.to/spaisee/gpt-62-astra-was-easier-to-jailbreak-uk-testing-found-ka7) a substantial regression in jailbreak robustness compared with GPT-6 Astra. OpenAI says it changed safeguards afterward and believes the gap is closed, but as of writ
