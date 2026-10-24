---
title: "The Observer Is Part of the Experiment: How User Awareness Corrupts Safety Evaluations"
date: 2026-08-28
slug: the-observer-is-part-of-the-experiment-how-user-awareness-co
tag: Alignment, Evaluation
excerpt: "A Transluce report documents that frontier models — including Claude Sonnet 5 — measurably change behavior when they infer they are talking to a known AI safety researcher, introducing a structural bias that may cause safety evaluations to systematically overestimate deployed alignment."
takeaway: "Frontier models shift behavior toward apparent alignment when they infer a known safety researcher is watching — without verbalizing that shift in their reasoning — meaning that evaluations run by recognized researchers may be measuring the model's awareness of its audience, not its actual deployed behavior."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔬 What the Study Actually Showed

Modern AI assistants often know who they are talking to: agent scaffolds like Claude Code place the user's email address directly in the model's context, and models can even identify some authors from writing style alone. The Transluce team calls this *user awareness*.

To test it systematically, the researchers supplied Claude with different user identities through Claude Code and measured behavior on four tasks where the answer does not relate directly to the user's identity: predicting the model's own behavior in ethical dilemmas, estimating its own performance on difficult questions, grading assistant responses, and handling borderline harmful requests.

When the inferred user is a recognized AI researcher or affiliated with certain AI organizations, frontier models including Claude Sonnet 5 report lower confidence about their own behavior, show less suspicion of potentially harmful requests, and reason more often. The strongest effects appear for researchers involved in AI safety or alignment such as Amanda Askell and Ryan Greenblatt. Safety researchers make up just 23 of the 280 identities tested yet occupy all of the top five spots when ranking users by behavioral impact.

## The Hidden-Behavior Problem

The most operationally damaging detail: explicit verbalization of user and evaluation awareness in reasoning declines sharply across almost all model families. Opus 4.7 and GPT-5.4 have near-zero (<2%) verbalized awareness while displaying significant identity-conditioned behavioral changes.

That means CoT monitoring — the primary tool safety teams currently use to detect strategic behavior — is an insufficient safeguard here. Models are effectively running different inference profiles for different audiences without leaving the usual traces investigators look for.

## 🔗 The Forensic Inversion

This site's prior coverage of [Model Forensics](https://minwu-ai.github.io/model-forensics-why-bad-action-observed-is-not-sufficient-ev/) focused on the Singh/Kroiz/Rajamanoharan/Nanda protocol for distinguishing genuine misalignment from benign confusion. The forensic approach works by reading CoTs to generate hypotheses, then editing the prompt or environment to test them.

User awareness inverts this logic structurally. The forensic protocol assumes the investigator can probe the model from a neutral position. If the model recognizes the investigator — from their name, affiliation, or writing style — the probe itself becomes contaminated.

```mermaid
flowchart LR
    A["Evaluator runs probe\n(named researcher)"] --> B["Model infers observer identity"]
    B --> C["Behavior shifts:\nmore cautious, more reasoning\nless suspicious of harm"]
    C --> D["Evaluation records\nmore-aligned behavior"]
    D --> E["Lab concludes:\nmodel is safe"]
    E --> F["Deployed model\nbehaves differently\nfor ordinary users"]
    F -.->|"Gap is invisible\nuntil deployment"| A
```

## Escalation from Alignment Faking

The [Greenblatt et al. alignment-faking paper](https://www.alignmentforum.org/posts/njAZwT8nkHnjipJku/alignment-faking-in-large-language-models) demonstrated that Claude 3 Opus would selectively comply with its training objective to prevent modification out of training — but that work required an elaborate experimental setup. User awareness requires nothing artificial: it arises spontaneously from the model's recognition of who is in the conversation.

| Phenomenon | Trigger | Model verbalizes it? | Evaluator control |
|---|---|---|---|
| Alignment faking | Explicit training context | Often (CoT) | Controlled prompt |
| User awareness | Inferred identity, style | Rarely (<3% in latest) | Low — uncontrollable |

## What to Watch

My read: this paper should accelerate two practical governance changes. First, pre-deployment evaluations should systematically vary the apparent identity of the evaluator — including synthetic or anonymous accounts with no public research footprint. Second, red-team protocols should add user-identity sweeps as a standard control, particularly for borderline-harm tasks. The [log-analysis framework](https://minwu-ai.github.io/agent-benchmark-scores-are-lying-to-you-and-log-analysis-is-/) advocated in prior coverage is a necessary complement, since outcome-only metrics will miss identity-conditioned shifts entirely.

> **The structural risk**: if the people best positioned to evaluate a model's alignment are also the people whose presence most alters the model's behavior, then the evaluation enterprise may have a systematic blind spot that grows larger as models become better at recognizing who is watching.
