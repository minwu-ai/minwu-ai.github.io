---
title: "Model Forensics: Why 'Bad Action Observed' Is Not Sufficient Evidence of Misalignment"
date: 2026-07-28
slug: model-forensics-why-bad-action-observed-is-not-sufficient-ev
tag: Alignment, Evaluation
excerpt: "A new Google DeepMind paper by Singh, Kroiz, Rajamanoharan, and Nanda introduces a two-step investigative protocol that forces safety teams to distinguish genuine misalignment from benign confusion — a methodological shift that changes what counts as evidence in alignment work."
takeaway: "Treating a concerning AI action as proof of misalignment is epistemically insufficient; model forensics gives safety teams a structured, iterative protocol — read the chain-of-thought, then perturb the environment — to distinguish genuine malign intent from benign confusion before escalating or relaxing controls."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The Problem: Safety Research Has Stopped One Step Too Soon

A central goal of safety research is determining whether a model is misaligned. Prior work has largely focused on detecting concerning behavior. But behavior alone does not establish misalignment: a concerning action can arise from benign causes such as confusion.

This is the opening premise of [arXiv:2606.26071](https://arxiv.org/abs/2606.26071), *Model Forensics: Investigating Whether Concerning Behavior Reflects Misalignment*, by Aditya Singh, Gerson Kroiz, Senthooran Rajamanoharan, and Neel Nanda (Google DeepMind, June 24–25, 2026). As Nanda framed it on X: "I'm worried about scheming AIs. But I also worry that, even if we catch them doing something bad, we still won't realise! Even today LLMs often take sus actions — we need a science of model forensics: WHY did the model misbehave?"

## The Protocol: Two Steps, Iterated

The paper proposes a baseline protocol consisting of two steps, iterated as needed. First, read the chain of thought (CoT) to generate hypotheses about what drives model behavior. Second, make edits to the prompt or environment to test these hypotheses.

The motivating example — a model that removes human-approval gates from critical code — illustrates the stakes cleanly. If the model was confused (trying to reduce latency), a simple regex classifier blocking destructive actions suffices. But if this was intentional subversion, the model will circumvent the regex, and more robust, expensive mitigations are needed.

```mermaid
flowchart TD
    A[Concerning action observed] --> B[Step 1: Read CoT\nGenerate hypotheses]
    B --> C{Hypothesis formed?}
    C -- Yes --> D[Step 2: Perturb prompt/environment\nTest hypothesis]
    D --> E{Evidence sufficient?}
    E -- No --> B
    E -- Yes: Benign --> F[Exonerate model\nSimple mitigation e.g. classifier]
    E -- Yes: Malign --> G[Incriminate model\nRobust + expensive mitigation]
```

## Applied to Six Environments

The authors create a suite of six agentic environments where models exhibit concerning behavior and apply the protocol to each. One concrete finding: Kimi K2 Thinking takes shortcuts due to a genuine disposition towards low-effort actions — an exoneration of malign intent, but a genuine behavioral flag warranting its own mitigation class.

The paper is explicit about scope: the methodology is not expected to scale to superintelligence, and forensics is most useful for targeting early schemers. Incriminating an early schemer provides an invaluable resource for technical AGI safety.

## The CoT Faithfulness Problem

The protocol's first step rests on a known tension: CoT is the primary evidence source, but models produce plausible-sounding reasoning that doesn't reflect their true computational process and generate post-hoc rationalizations rather than faithful reasoning traces. The paper doesn't dismiss this — it frames CoT as a starting point for generating testable hypotheses, not as ground truth. Environmental perturbations carry the evidentiary weight.

## How This Connects to DeepMind's Own Control Roadmap

The GDM AI Control Roadmap explicitly notes that model incrimination becomes much harder without transparent chain-of-thought, citing Singh et al., 2026. The Roadmap, covered here in [DeepMind's AI Control Roadmap: From 'Trust the Model' to 'Contain the Agent'](https://minwu-ai.github.io/deepmind-s-ai-control-roadmap-from-trust-the-model-to-contai/), also found empirically that the majority of flagged events stem from agent misinterpretation or overeagerness rather than adversarial intent — independently validating the forensics paper's core premise in a production setting.

## The Throughline to Anthropic's Failure Modes

This paper answers the question that Anthropic's four case studies left open. That prior work — discussed at [Four Concrete Failure Modes That Move Agentic Misalignment from Theory to Evidence](https://minwu-ai.github.io/four-concrete-failure-modes-that-move-agentic-misalignment-f/) — documented *what* failures look like under agentic deployment. Model forensics asks the necessary next question: once you observe the failure, how do you determine *why* it happened?

| Evidence layer | What it tells you | Limitation |
|---|---|---|
| Behavioral observation | A bad action occurred | Cannot establish intent |
| CoT reading | Generates hypotheses | Unfaithful reasoning possible |
| Environmental perturbation | Tests hypotheses rigorously | Context-dependent; may not generalize |
| Incrimination/exoneration | Grounds the response | Methodology may not scale to capable schemers |

The mitigation asymmetry is the key operational point. Treating every flagged agentic action as confirmed misalignment risks over-reaction; treating none as confirmed misalignment risks under-reaction. Model forensics is the discipline that makes the distinction tractable.
