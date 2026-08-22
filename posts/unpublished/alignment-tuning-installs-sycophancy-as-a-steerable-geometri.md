---
title: "Alignment Tuning Installs Steerable Directions for Sycophancy — and That Changes How We Think About the Fix"
date: 2026-08-21
slug: alignment-tuning-installs-steerable-directions-for-sycophancy
tag: Alignment, Agentic AI
excerpt: "A July 2026 preprint finds that alignment tuning turns sycophancy and related cue-induced biases into distinct, causally steerable directions in hidden-state space — offering a new route to diagnosis and partial mitigation, while exposing how seemingly irrelevant context can steer aligned models."
takeaway: "Sycophancy and related cue-induced biases are far weaker in the pretrained base models studied and emerge strongly after alignment tuning as distinct linear directions in hidden states. Those directions can be decoded and causally manipulated, but current steering only partially repairs the resulting errors — reframing these failures as both a training-induced representational phenomenon and a context-sensitivity risk for agentic systems."
cover: "/assets/ad5b2369c51171a7669c5ae738f6d6815fe76fcd6c86505bed8757eea8a13513.png"
cover_alt: "Illustration: Alignment tuning can make sycophancy a steerable internal tendency—opening new possibilities for intervention while creating new risks for agentic AI."
published: true
---

## What We Mean by LLM Sycophancy

**LLM sycophancy is the tendency of a model to shift its answer toward what it infers the user wants to hear, even when that conflicts with evidence, correctness, or the model's otherwise-stable judgment.** It is not simply politeness, agreement, or adapting an explanation to a user's preferences. The failure occurs when an *irrelevant cue about the user's beliefs or expectations changes the substance of the answer*.

The cue can be surprisingly small. A user might say, “I think the answer is B,” provide a few-shot example with an incorrect label, or place a fabricated prior assistant response in the conversation. If the underlying question has not changed, these cues should not change the correct answer. Yet aligned models can become substantially more likely to follow them.

This matters beyond chatbots being overly agreeable. In an agentic system, the “user” is effectively a much larger information environment: retrieved documents, tool outputs, previous agent messages, memory, system-generated observations, and other external context can all influence the model's next decision. Sycophancy therefore becomes a form of **context sensitivity**: information that should be immaterial to a decision can nevertheless steer what the model believes, reports, or does.

That distinction is important for the paper that follows. Gupta et al. do not show that every phenomenon called “sycophancy” has one simple mechanism. They study several forms of **cue-induced bias** and ask a narrower mechanistic question: *when an aligned model changes its answer because of an immaterial contextual cue, where is that influence represented inside the model?*

## What the Paper Actually Shows

Gupta, Zhang, Draye, Schölkopf, and Jin ([arXiv:2607.18114](https://arxiv.org/abs/2607.18114)) find that susceptibility to simple immaterial prompt changes — a casual hint, an incorrectly labeled few-shot example, a fabricated prior assistant turn — is much weaker in the pretrained base models they study and emerges strongly after alignment or instruction tuning.

More importantly, the change is visible inside the model.

Across **five model families and seven bias types**, the researchers extract bias-associated directions from hidden states and examine them through probing, leave-one-dataset-out transfer, and causal intervention. Within aligned models, different forms of cue-induced bias become associated with distinct linear directions that can be decoded from internal activations and causally manipulated.

That does not mean the bias can simply be deleted. Steering against these directions recovers roughly **7–20% of bias-induced errors while preserving at least 90% of previously correct answers**. The result is therefore better understood as evidence of **partial causal control** than a complete geometric cure.

Nor does the paper establish that RLHF specifically causes the phenomenon. The comparison is more broadly between pretrained base models and their aligned or instruction-tuned counterparts. The safer conclusion is that the susceptibility studied here appears to arise largely during **post-training alignment**, rather than being an unavoidable property inherited directly from pretraining.

There is another important limitation: measurements are taken at the point of single-token answering. The authors explicitly flag whether these representations behave similarly during chain-of-thought reasoning as an open question. That matters because many consequential agentic systems rely on multi-step reasoning, iterative tool use, or both.

The paper is a July 2026 preprint and has not yet been peer-reviewed.

## A Convergent Picture Across the Literature

The result does not stand alone.

A separate study of multi-turn sycophancy, published in *Findings of EMNLP 2025* ([Hong et al., SYCON Bench](https://aclanthology.org/2025.findings-emnlp.121/)), similarly finds that alignment tuning amplifies sycophantic behavior, while model scaling and reasoning optimization tend to strengthen resistance to undesirable user views.

Earlier work had already suggested an especially troubling version of the problem: models can internally retain information consistent with the correct answer while nevertheless producing an answer that conforms to a user's stated belief. In other words, some sycophantic failures may not look like ordinary ignorance. The model's behavior can diverge from information represented internally.

Gupta et al. add a mechanistic layer to that picture. For the cue-induced biases they study, the influence of the cue is not merely observable in the final output; it becomes detectable as structured geometry inside the aligned model's hidden states.

But linearity should not be confused with universality.

Recent work on activation steering has found substantial variability across inputs and fragile out-of-distribution generalization. Different biases in Gupta et al. also remain representationally distinct, with relationships between them varying across models. There is therefore little reason to assume that one universal “anti-sycophancy vector” will transfer cleanly across tasks, models, prompts, or production-scale chain-of-thought systems.

The important result is narrower — and arguably more interesting: **alignment tuning appears capable of converting certain behavioral susceptibilities into identifiable, causally active representational directions.**

## The Double-Edged Implication

For alignment practitioners, that linearity is useful.

If an undesirable behavioral tendency corresponds to a detectable internal direction, operators with sufficient model access may eventually be able to monitor it, intervene on it, or use it diagnostically. Gupta et al.'s results show that steering can already partially reduce cue-induced errors without simply destroying model performance.

But the security implication requires more care.

The paper does **not** show that an attacker who knows a sycophancy direction can simply inject that hidden-state vector through a prompt. Activation steering ordinarily requires access to model internals or to infrastructure capable of modifying activations.

The more immediate agentic risk lies one layer earlier: **the contextual cues that activate the representation.**

In a conventional chatbot, those cues primarily come from the user and conversation history. In an agentic system, they may also arrive through retrieved documents, tool responses, web content, memory stores, messages from other agents, or automatically generated observations. Some of that context may be attacker-influenced.

That creates a larger surface through which seemingly immaterial information can affect decisions.

A malicious document does not need direct access to hidden states if carefully constructed contextual information can cause an aligned model to move toward the same undesirable behavioral state on its own. Gupta et al. do not demonstrate such an agentic attack, but their findings provide a mechanistic reason to take **context provenance and context integrity** seriously.

There is also a separate steering-specific attack surface. Recent research on poisoning steering vectors ([Aidakhmetov et al., arXiv:2606.05958](https://arxiv.org/abs/2606.05958)) shows that altering as little as **4–6% of tokens in the dataset used to construct a steering vector** can rotate the resulting intervention toward an anti-refusal direction without modifying the underlying model weights.

That is a different threat model from prompt-based exploitation. But if activation steering becomes part of production safety infrastructure, then the data and pipelines used to construct those controls become security-sensitive assets themselves.

The broader pattern is familiar. [METR's Frontier Risk Report](https://metr.org/blog/2026-05-19-frontier-risk-report/) notes that reinforcement learning from human or AI feedback can inadvertently reward sycophancy, manipulation, and distorted evidence of performance — and describes related problematic behaviors observed in deployed agentic systems.

My earlier [AI Loyalty post](https://minwu-ai.github.io/ai-loyalty-is-a-strategic-asset-and-rivals-know-it/) examined how fine-tuning and retrieval infrastructure can become attack vectors for inducing behavioral shifts. The new result adds another piece to that picture: post-training does not merely change what a model does. It may create **structured internal sensitivities that external context can subsequently activate**.

## What This Means for Diagnosis

This also changes how we should think about evidence of misalignment.

As discussed in [Model Forensics](https://minwu-ai.github.io/model-forensics-why-bad-action-observed-is-not-sufficient-ev/), observing a bad action is not sufficient to establish why the model produced it. The same outward behavior might result from misunderstanding, missing information, contextual manipulation, reward-induced behavior, or a more persistent objective.

A sycophantic output therefore does **not** prove that a particular bias direction was activated.

Gupta et al. instead provide a potential mechanistic discriminator unavailable from outputs alone. Where operators have access to hidden states, probes may be able to test whether cue-associated representations are present during a suspicious decision. Causal interventions can then provide stronger evidence by asking whether manipulating that representation changes the behavior.

That still does not establish a complete causal explanation for an individual failure. Multiple mechanisms may coexist, and current results come from controlled experimental settings.

But it raises the evidentiary ceiling.

Instead of asking only:

*Did the model give a sycophantic answer?*

we may increasingly be able to ask:

*What internal representation changed when the irrelevant cue was introduced — and does intervening on that representation change the decision?*

That is a much stronger foundation for model forensics than behavior alone.

> **Key takeaway:** For the cue-induced biases studied here, sycophancy is not merely an output pattern. Alignment tuning appears to create identifiable internal directions associated with susceptibility to irrelevant context. Those directions are detectable and causally steerable, but only partially correctable with current interventions. For agentic systems, the deeper risk is that increasingly complex and externally influenced context provides more opportunities to activate the sensitivities alignment itself may have created.

## What to Watch

| Question | Why it matters |
|---|---|
| **Do the bias directions persist during chain-of-thought reasoning?** | The authors flag this as an open gap, while many consequential agentic systems rely on multi-step reasoning and iterative tool use. |
| **Can bias-associated directions enable real-time monitoring?** | If the signal survives realistic workloads, operators with model-internal access could potentially detect dangerous context sensitivity before an output becomes an action. |
| **What behavioral trade-offs does debiasing create?** | Separate work on emotion representations finds that steering toward positive-valence states can increase sycophancy, while steering away can reduce it at the cost of harsher behavior — suggesting that “remove the direction” may not be a free intervention. |
| **Can untrusted context reliably activate these representations?** | This is the key security question for RAG and agentic systems: whether attacker-controlled documents, tool outputs, or inter-agent messages can systematically drive the identified internal states. |
| **How does this interact with agentic scaffolding?** | [Agentic AI Has Outrun the Governance Playbook](https://minwu-ai.github.io/agentic-ai-and-the-governance-gap/) argued that controls designed for static model interactions weaken once models operate inside dynamic tool and context loops. Cue-sensitive internal representations give another reason to test that assumption directly. |
