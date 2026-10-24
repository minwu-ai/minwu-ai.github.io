---
title: "Neurons Are the Feature Basis After All: What the Arora–Steinhardt–Schwettmann Circuit Paper Means for Interpretability Practice"
date: 2026-08-20
slug: neurons-are-the-feature-basis-after-all-what-the-arora-stein
tag: Alignment, Evaluation
excerpt: "A January 2026 ICML Spotlight paper shows MLP neurons are empirically as sparse a feature basis as SAE-learned features — a finding that could lower the bar for third-party model auditing by eliminating the need to train a separate sparse autoencoder."
takeaway: "Arora, Wu, Steinhardt, and Schwettmann's preprint (arXiv:2601.22594) shows that gradient-based circuit tracing directly on MLP neurons matches SAE-circuit quality, with circuits of roughly 100 neurons causally controlling model behavior — suggesting interpretability audits may not require the expensive, model-specific SAE training step that has been the field's dominant assumption."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔬 What the Paper Shows

The interpretability community has broadly turned to sparse autoencoders (SAEs) to decompose the neuron basis into more interpretable units of model computation. A January 2026 preprint — now an [ICML 2026 Spotlight](https://icml.cc/virtual/2026/poster/64312) — by Aryaman Arora, Zhengxuan Wu, Jacob Steinhardt, and Sarah Schwettmann pushes back: "not all neuron-based representations are uninterpretable." The authors empirically demonstrate that **MLP neurons are as sparse a feature basis as SAEs**, and use this to develop an end-to-end pipeline for circuit tracing on the MLP neuron basis using gradient-based attribution.

The empirical stakes are concrete. On a standard subject-verb agreement benchmark, roughly 10² MLP neurons is enough to control model behaviour — corroborated by a concurrent finding that 100–200 neurons can explain complete task behaviors. Crucially, the approach does not require loading SAEs into memory, making it tractable for large models. The [Transluce blog post](https://transluce.org/neuron-circuits) distills the upshot: the team introduces "a new approach to finding sparse circuits in the neuron basis, without relying on learned features."

## ⚖️ What This Runs Against

The SAE consensus is substantial. SAEs address polysemanticity by learning overcomplete, sparse latent representations that decompose dense activations into interpretable features; they have been used to identify monosemantic features, analyze activations across contexts, and support circuit investigations. A growing literature addresses SAE training variants, evaluation protocols, and architectural improvements.

But the SAE pipeline carries genuine friction. Training is computationally expensive and data-intensive, requiring one SAE per layer — repeated across dozens or hundreds of layers for deep models. SAEs also introduce approximation error: if the sparse codes are wrong, feature attribution is wrong regardless of reconstruction fidelity.

The auditing cost is not hypothetical. In a December 2025 interpretability auditing exercise, SAEs were not pursued by the blue team during the auditing game, as training them for each model would have taken significant time and effort. That omission mattered for the audit's conclusions.

## 🏛️ The Governance Connection

The timing matters. Illinois joins California and New York in imposing obligations on frontier model developers — including transparency reports and annual independent third-party safety audits conducted by qualified experts without financial conflicts of interest.

The Arora et al. result is relevant in a specific way. Third-party auditors typically lack access to developer SAE training infrastructure, and as the sandbagging audit literature shows, training SAEs per-model-under-audit is practically prohibitive. A gradient-based neuron circuit pipeline requiring no auxiliary training is a meaningfully lower-friction tool for external parties. This connects directly to the framework examined in [Illinois SB 315's audit mandate](https://minwu-ai.github.io/illinois-sb-315-closes-the-audit-gap-the-first-mandatory-ind/): the practical question is not whether audits are legally required but whether auditors have techniques independent of the developer's own interpretability infrastructure.

There is also a parallel to Anthropic's GRAM work, covered [here](https://minwu-ai.github.io/anthropic-s-gram-is-an-architecture-for-trust-not-just-a-saf/): both efforts point toward model internals inspectable via targeted, localized tools rather than whole-model retraining.

## What to Watch

The results so far rely on templatic paired data; real-world data is non-templatic, and for many behaviors we may lack hypotheses permitting paired data generation. How the method performs on naturalistic, open-ended behaviors — and on larger, proprietary models — remains open. The follow-on ADAG paper from the same group takes a step toward automation, and Steinhardt's Transluce lab has oriented its research program toward precisely this problem.

> **My read:** If the neuron-basis result holds at scale, the field's working assumption — that SAEs are the necessary entry point for circuit-level analysis — will need updating. For governance practitioners, the more immediate implication is procedural: an audit toolkit requiring no auxiliary model training reduces the informational asymmetry between developer and auditor, which is exactly what third-party evaluation frameworks are designed to correct.

| Approach | Training required | Approximation error | Memory overhead | Auditor-accessible |
|---|---|---|---|---|
| SAE circuits | Yes (per model, per layer) | Yes (reconstruction) | High | Low |
| Neuron-basis circuits (Arora et al.) | No | Minimal | Low | Higher |
