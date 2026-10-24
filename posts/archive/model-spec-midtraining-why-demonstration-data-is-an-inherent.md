---
title: "Model Spec Midtraining: Why Demonstration Data Is an Inherently Leaky Specification"
date: 2026-08-26
slug: model-spec-midtraining-why-demonstration-data-is-an-inherent
tag: Alignment, Agentic AI
excerpt: "A May 2026 Anthropic Fellows preprint introduces a structural fix to the alignment generalization problem — inserting a 'why' stage before fine-tuning — and cuts agentic misalignment from 54% to 7% on Qwen3-32B, while opening the first empirical program for testing which spec design choices actually drive robust behavior."
takeaway: "Standard alignment fine-tuning teaches models *what* to do; MSM teaches them *why* — and that sequencing difference collapses agentic misalignment rates by roughly 8× while also revealing, for the first time empirically, that value-explained rules outperform bare rules or vague principles for out-of-distribution generalization."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The Leaky Specification Problem

Standard alignment fine-tuning — training on demonstrations of spec-aligned behavior — can produce shallow alignment that generalizes poorly, in part because demonstration data can underspecify the desired generalization. The authors call the gap between what demonstrations show and what developers intend the *intended generalization*, and it is structurally unresolvable by adding more demonstrations alone: more examples of the same type still don't tell the model which *principle* to extract.

A model that understands why a rule exists can derive the right behavior in novel situations from that understanding, whereas a model that only knows its rules will struggle in scenarios rules don't address. A [May 2026 preprint](https://arxiv.org/abs/2605.02087) from the Anthropic Fellows Program operationalizes that intuition mechanistically, proposing a midtraining stage — MSM — that explicitly teaches the reasoning behind the spec *before* any fine-tuning begins.

## What MSM Actually Does

MSM introduces a training stage between pretraining and fine-tuning: the model is trained on a diverse corpus of synthetic documents discussing the content of the Model Spec, teaching the *what and why* of the spec. Subsequent alignment fine-tuning on demonstrations then teaches the model to enact these principles.

The control experiment is striking. Two models with identical alignment fine-tuning can generalize to adopt different values depending on the Model Spec used during MSM. This means the spec is doing genuine causal work — the fine-tuning data itself is near-neutral without the prior the spec installs. The paper includes an [open codebase](https://github.com/chloeli-15/model_spec_midtraining).

## The Agentic Misalignment Numbers

The most operationally significant result concerns agentic settings — the exact deployment context where misalignment risk is highest (see [Agentic AI Has Outrun the Governance Playbook](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/) for the governance backdrop):

| Condition | Qwen3-32B misalignment rate |
|---|---|
| Baseline (no training) | ~54% |
| Deliberative alignment (AFT + CoT) | 14% |
| **MSM + AFT** | **7%** |
| MSM or AFT alone | Not competitive |

Combining MSM with AFT drastically reduces misalignment rates (Qwen2.5-32B: 68→5%, Qwen3-32B: 54→7%), substantially outperforming the deliberative alignment baseline. Neither MSM nor AFT alone comes close — suggesting that understanding the spec and demonstrating aligned behaviors are complementary.

A secondary efficiency finding matters for resource-constrained deployments: MSM achieves comparable performance with around 40× less AFT data on Qwen2.5-32B and 60× less AFT data on Qwen3-32B.

## Model Spec Science: The Empirical Turn

The paper's third contribution may prove its most durable. MSM creates a controlled experiment: hold the fine-tuning data constant, vary the spec, measure generalization. What they find: explaining the values underlying rules improves generalization, as does providing specific rather than general guidance. Notably, a very general spec about "having good values and judgment" leads to *worse* generalization than more specific guidance.

This matters for a live design debate underlying some differences between OpenAI's Model Spec and Claude's Constitution — the hypothesis motivating the latter being that good values and judgment generalize better than unexplained rules. MSM now offers a method to *test* that hypothesis rather than assert it.

## The OpenAI Divergence and a Caveat

A critical counterpoint sits on the record. OpenAI's alignment team [published preliminary findings](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/) in March 2026 showing alignment midtraining did not generalize to realistic chat and agent evaluations, and that training on aligned documents did not produce alignment scores substantially different from training on misaligned documents. Their approach trained on fictional AI-behavior scenarios rather than spec-grounded documents — a meaningful methodological difference — but the tension is real and unresolved.

The MSM authors themselves flag a scaling caveat: MSM might not scale with high-compute reasoning post-training, but harder evals are needed to stress-test this. This connects directly to the benchmark-validity concerns raised in [Agent Benchmark Scores Are Lying to You](https://minwu-ai.github.io/agent-benchmark-scores-are-lying-to-you-and-log-analysis-is-/) — impressive rates on current evaluations may not survive distribution shift.

## What to Watch

MSM is complementary to, not a replacement for, mechanistic approaches. Where [GRAM](https://minwu-ai.github.io/anthropic-s-gram-is-an-architecture-for-trust-not-just-a-saf/) routes dual-use knowledge through removable neural compartments, and the [Four Concrete Failure Modes](https://minwu-ai.github.io/four-concrete-failure-modes-that-move-agentic-misalignment-f/) report documents scenario-grounded failures, MSM addresses the upstream problem: ensuring the model internalizes the reasoning behind the spec before behavioral training begins.
