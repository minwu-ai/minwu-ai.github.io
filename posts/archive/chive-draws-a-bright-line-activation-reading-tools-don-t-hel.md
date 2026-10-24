---
title: "CHIVE Draws a Bright Line: Activation-Reading Tools Don't Help You Predict What a Model Will Do Next"
date: 2026-08-27
slug: chive-draws-a-bright-line-activation-reading-tools-don-t-hel
tag: Alignment, Evaluation
excerpt: "Anthropic's CHIVE pipeline delivers the first large-scale empirical evidence that sparse autoencoders, natural-language autoencoders, and activation oracles give agents zero detectable uplift when predicting how real, in-the-wild LLM behaviors respond to prompt edits — sharpening what 'good interpretability' must actually mean."
takeaway: "Current activation-reading interpretability tools — sparse autoencoders, natural-language autoencoders, and activation oracles — provide no measurable uplift over simply reading a conversation transcript when predicting whether a prompt edit will change model behavior in the wild. That null result, replicated across two target models and three predictor families, is the most quantified limit on today's interpretability stack yet published; training on CHIVE-generated counterfactual data offers the best current path around it."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔬 What CHIVE Actually Does

CHIVE is a novel agentic pipeline that identifies unexpected model behaviors in the wild and investigates them with counterfactual prompt edits. Given transcripts from any source, it discovers unexpected behaviors of a target model and investigates each one with counterfactual prompt edits; each investigation produces an open-ended explanation and the counterfactual experiments that support it, with measured outcomes that serve as evaluation labels.

The team ran investigation pipelines on five target models — Qwen3-8B, Qwen3-32B, Qwen3.5-397B-A17B, Gemma-3-27B-IT, and Llama-3.1-8B — and released all code, models, and datasets. That breadth matters: prior evaluations of interpretability tools have almost exclusively run on deliberately fine-tuned, quirk-carrying models, not on stock models behaving unexpectedly in natural deployment.

## The Null Result, Replicated

The experimental design is clean. Each predictor agent receives a transcript, a behavior, and one proposed counterfactual, and outputs the probability that the counterfactual would change the behavior; the transcript-only baseline sees just the transcript. Tool predictors can additionally make five read-only activation calls using one of three tools — activation oracles, natural-language autoencoders, or sparse autoencoders.

All three activation-reading tools, which provided uplift in prior auditing games on fine-tuned models, provide no uplift on CHIVE's evaluation. No predictor outperforms one that is simply shown the transcript with no access to interpretability tools. The no-uplift result replicates across predictor families — GPT-5.5 and Gemini-3.1-Pro as predictor agents produce the same pattern on the Gemma-3-27B-IT claims.

The paper is also candid about practical stakes: at Anthropic, interpretability tools like the ones studied here are frequently used in system card evaluations. That admission makes the null result consequential beyond academia.

## Why Auditing-Game Uplift Doesn't Transfer

The key structural tension CHIVE surfaces is the difference between *planted* behaviors and *emergent* ones. In prior auditing games, the target model is typically fine-tuned to carry a quirk — a hidden objective, an implanted behavior, or secret knowledge. Research suggests that fine-tuning modifies a small, interpretable subset of representations, which may make such models easier to audit than models where concerning behaviors emerge more diffusely.

Real deployment looks like the second case, not the first. CHIVE is the first evaluation that systematically tests interpretability tools against the latter — and the tools fail.

| Setting | Activation-tool uplift? | Behavior origin |
|---|---|---|
| Prior auditing games (fine-tuned quirks) | ✅ Yes | Narrow, deliberately implanted |
| CHIVE (in-the-wild transcripts) | ❌ None | Emergent, diffuse |

Recovering a sparse, plausible-looking decomposition is not the same as demonstrating that the decomposition is the one the model actually uses. CHIVE puts a number on that gap.

## 🛤 The Forward Path: Training on Counterfactual Outcomes

The secondary result is where the constructive signal lives. The team trains target models to predict, as a follow-up turn on their own transcript, whether a given prompt edit would change their behavior. Prior work of this kind trains and evaluates in hint settings — where a known cue is planted in the prompt — and reports only narrow generalization.

CHIVE-trained models break out of that band. Training generalizes to the hint setting, which was not targeted during training, and to held-out investigations from the pipeline, including ones built from out-of-distribution transcripts. There is also evidence that strong hint-setting results may overstate general performance: prior work found that a method performing well in the hint setting (+35pp) obtains much weaker results in a more general setting (+2pp). CHIVE's training route avoids that collapse.

Training to generate *open-ended explanations* is a weaker proposition: experiments with training models to generate open-ended explanations of their own behavior yielded weaker, mixed results. Prediction, not narration, is what generalizes.

## Alignment Framing: What This Demands of "Good Explanation"

The paper evaluates explanations through the lens of counterfactual simulatability: whether the explanation is useful for predicting model behaviors on related counterfactual inputs. That is precisely the right standard for alignment verification. An explanation that cannot generate accurate predictions about behavioral perturbations is, at best, a narrative — and narratives are insufficient for safety cases.

This connects directly to two threads this site has tracked. The [sycophancy directions paper](https://minwu-ai.github.io/alignment-tuning-installs-steerable-directions-for-sycophancy/) showed that alignment tuning installs causally steerable hidden-state directions — evidence that internal structure *corresponds to* behavior. CHIVE now shows that reading those structures doesn't yet let you *predict behavior changes* in realistic settings. The [model forensics piece](https://minwu-ai.github.io/model-forensics-why-bad-action) argued that post-hoc auditing requires predictive power to anchor safety cases; CHIVE quantifies exactly how far current tools fall short of that bar.
