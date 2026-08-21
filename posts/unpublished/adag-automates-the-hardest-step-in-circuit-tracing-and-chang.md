---
title: "ADAG Automates the Hardest Step in Circuit Tracing — and Changes What Interpretability Can Promise"
date: 2026-08-19
slug: adag-automates-the-hardest-step-in-circuit-tracing-and-chang
tag: Interpretability, Evaluation
excerpt: "A Stanford/Transluce preprint automates one of the most stubborn human bottlenecks in circuit tracing: turning attribution graphs into semantically organized, human-readable candidate mechanisms. The result points toward interpretability at much greater scale — while sharpening the question of what such automated explanations actually prove."
takeaway: "ADAG demonstrates an automated pipeline for organizing and describing attribution graphs, recovering known circuits and identifying steerable feature clusters associated with a jailbreak in Llama 3.1 8B. But its autointerpretability scores validate how well descriptions capture measured attribution profiles, not whether those graphs constitute complete or uniquely faithful accounts of the model's underlying computation."
cover: "/assets/c4f974a06fc0151d836bbb546ff1b538b82dbc621f356c154748a6b260a52640.png"
cover_alt: "Illustration: an automated system opening the black box of a language model and tracing an internal computational pathway, while part of the mechanism remains obscured."
published: true
---

## 🔬 What Does It Mean to "Interpret" an LLM?

We routinely evaluate large language models from the outside. Give a model a prompt, observe its response, and score whether the answer is correct, safe, grounded, or useful.

That tells us **what the model did**. It does not necessarily tell us **how the model produced it**.

Even asking the model to explain itself does not solve this problem. A language model can generate a perfectly plausible account of why it gave an answer without that account faithfully describing the computation that occurred inside the network. The explanation is another model output.

This distinction is at the heart of **mechanistic interpretability**: an effort to reverse-engineer learned neural networks into human-understandable representations, components, and computational pathways.

A useful hierarchy is:

| Level | Question | Example |
|---|---|---|
| **Behavior** | What did the model do? | It answered "Austin." |
| **Representation** | What information exists internally? | Internal features encode concepts related to Dallas or Texas. |
| **Mechanism** | How did those representations interact to produce the answer? | Dallas-related representations contribute to Texas-related representations, which ultimately promote "Austin." |
| **Intervention** | Does changing those internal components change the behavior? | Suppressing or amplifying a component changes the probability of the answer. |

Modern interpretability research has made meaningful progress across these levels. Researchers have identified interpretable internal features, localized behaviors to model components, and altered outputs through targeted interventions. Sparse autoencoders and related dictionary-learning methods, for example, attempt to decompose dense neural activations into more interpretable features — an important response to **superposition** and **polysemanticity**, where concepts need not map cleanly onto individual neurons.

But finding a feature is not the same as understanding a mechanism.

Anthropic made this distinction explicit in its work on [mapping the internal features of Claude](https://www.anthropic.com/research/mapping-mind-language-model): discovering representations tells us something about what information exists inside a model, but understanding how the model *uses* those representations requires tracing the circuits connecting them.

That is the problem that attribution graphs — and now ADAG — attempt to address.

## From "Dallas" to "Austin": What Circuit Tracing Is Actually Trying to Do

Consider a deceptively simple question:

> **What is the capital of the state containing Dallas?**

A capable model answers:

> **Austin.**

From ordinary evaluation, all we observe is:

**Prompt → LLM → Austin**

The model might even explain:

> Dallas is in Texas, and the capital of Texas is Austin.

But that generated explanation does not establish that the model internally computed:

**Dallas → Texas → Austin**

Mechanistic interpretability asks whether something resembling that computation can actually be recovered from inside the network.

Prior circuit-tracing work has studied precisely this kind of multi-hop state-capitals task. Instead of treating the model as a single black box, attribution methods attempt to identify internal features contributing to the answer and relationships among them.

Conceptually, the recovered computation might resemble:

**"Dallas" input**  
↓  
**Dallas / Texas-related features**  
↓  
**state / capital relationship features**  
↓  
**Austin-related output features**  
↓  
**"Austin"**

This is the ambition of **circuit tracing**: not merely identifying a neuron that activates when the model sees "Dallas," but reconstructing a candidate pathway through which internal representations contribute to the final output.

The analogy to reverse-engineering software is useful. Behavioral evaluation is like running an unknown executable and testing its outputs. Mechanistic interpretability is an attempt to recover something closer to the program's internal logic.

The problem is that these graphs quickly become too large and messy for humans to interpret manually.

That is where ADAG enters.

## The Human Bottleneck in Circuit Tracing

Submitted April 8, 2026 by Arora, Wu, Steinhardt, and Schwettmann of Stanford and Transluce, [ADAG: Automatically Describing Attribution Graphs](https://arxiv.org/abs/2604.07615) introduces a fully automated pipeline for organizing and describing attribution graphs.

Prior circuit-tracing work relied heavily on researchers manually inspecting activation examples and attribution patterns, grouping related features, and deciding what those groups appeared to represent. The ADAG authors characterize this researcher-driven interpretation as a major obstacle to scaling circuit analysis across many prompts and increasingly complex models.

ADAG therefore attacks a different bottleneck from simply computing an attribution graph:

**How do you turn thousands of internal features and relationships into something a human can understand without manually annotating them one by one?**

Its answer is to automate much of that interpretation layer.

This does not mean that ADAG "solves interpretability." It automates one of the most stubborn human bottlenecks in circuit tracing: turning large attribution graphs into semantically organized, human-readable **candidate mechanisms**.

## How ADAG Works

ADAG's pipeline has four broad stages:

1. **Circuit tracing** identifies internal features and attribution relationships relevant to a particular model output.
2. **Attribution profiles** characterize each feature according to the inputs contributing to its activation and its contribution toward candidate output logits.
3. **Automatic clustering** groups related features into higher-level "supernodes."
4. **Automatic description** generates natural-language interpretations of those supernodes.

The attribution profile is particularly important.

Traditional approaches might inspect the inputs that maximally activate a feature and conclude, for example, that it represents "Texas." But this can reveal only part of its functional role.

ADAG instead examines both directions:

**What contributes to this feature?**  
and  
**What output logits does this feature contribute toward?**

A clustering algorithm then groups features with similar attribution profiles. An explainer language model proposes descriptions for those groups, while a simulator language model evaluates how well candidate descriptions predict held-out attribution patterns.

On manually defined supernodes in the state-capitals setting, automated descriptions perform approximately as well as human descriptions on input attribution and substantially better under the paper's output-contribution metric.

That result should be interpreted carefully. Both human and machine descriptions are evaluated through the paper's simulator framework, and the automated procedure selects among multiple candidate descriptions. The experiment therefore demonstrates strong performance under ADAG's autointerpretability metric; it is not independent proof that the generated descriptions are mechanistically correct.

## What ADAG Can Actually Do

The paper provides two especially useful demonstrations.

### Recovering a Known Circuit

ADAG revisits the multi-hop state-capitals task.

This matters because earlier human-led work gives the authors something against which an automated pipeline can be compared. ADAG recovers qualitatively similar functional structure without requiring researchers to manually interpret every feature.

A later independent pipeline from Patel et al., [LLMs Can Annotate Attribution Graphs](https://arxiv.org/abs/2608.02632), reaches a related result: automatically generated supernodes achieve interpretability comparable to human-generated ones under automated evaluation, while recovering the intermediate-hop supernode in 97 of 100 prompts.

The convergence is useful evidence that **automating the organization and description of attribution graphs is becoming technically viable**.

It does not establish that either pipeline has recovered the complete ground-truth mechanism.

### From "Why Austin?" to "Why Did the Jailbreak Work?"

The state-capitals example makes ADAG intuitive. Its safety significance becomes clearer when the same idea is applied to harmful behavior.

Instead of asking:

> **Why did the model answer Austin?**

ask:

> **Why did an aligned model provide harmful medical advice after a jailbreak?**

ADAG applies its pipeline to a harmful-medical-advice jailbreak against Llama 3.1 8B Instruct. It analyzes more than 150 semantically related prompt variants and groups relevant internal neurons into 20 supernodes.

The researchers then go beyond simply labeling them.

They **intervene** on selected clusters — suppressing or amplifying their activations — and measure whether the probability of successful jailbreak behavior changes.

Some interventions produce large changes. Negatively steering one cluster associated with safety-oriented behavior raises attack success substantially; positively steering another jailbreak-associated cluster produces a similarly large increase.

This provides stronger evidence than simply observing that a cluster activates during jailbreaks.

Conceptually, researchers are trying to move from:

**Jailbreak prompt → harmful answer**

toward something closer to:

**Jailbreak prompt**  
↓  
**internal attack-context representations**  
↓  
**safety / refusal-related computation**  
↓  
**compliance-related computation**  
↓  
**harmful answer**

The paper does not prove that this simplified chain is the model's complete mechanism. But interventions showing that particular internal clusters materially affect jailbreak success provide evidence that those components are functionally involved in the behavior.

That distinction matters.

Finding correlation is interesting.

Finding a human-readable internal structure is more interesting.

**Changing the structure and changing the behavior is stronger evidence still.**

## What Interpretability Can — and Cannot — Tell Us Today

ADAG arrives at an important moment for mechanistic interpretability.

The field has moved considerably beyond treating large language models as completely opaque black boxes. Researchers can now recover meaningful internal features, identify computational motifs, construct candidate circuits, and sometimes intervene on those components to alter model behavior.

But that is very different from possessing a source-code-level understanding of an LLM.

Several fundamental problems remain.

**Coverage.** An attribution graph may capture important components without capturing every component responsible for a behavior.

**Faithfulness.** A simplified graph or natural-language description may be useful without being a uniquely faithful representation of the computation performed by the original network.

**Granularity.** Human concepts such as "Texas," "refusal," or "harmful compliance" may be convenient descriptions without necessarily corresponding cleanly to the computational units the model actually uses.

**Superposition.** Information can be distributed and overlapping rather than neatly localized in individual neurons or features.

**Scalability.** A technique that works on selected prompts and behaviors still has to scale to billions of parameters, long contexts, diverse behaviors, and eventually agentic systems acting across extended trajectories.

**Validation.** Perhaps most importantly, a plausible-looking circuit can become persuasive before we have established that it is complete or faithful.

A reasonable description of the field today is therefore:

> **We have moved from "LLMs are completely opaque" toward "we can recover meaningful pieces of their internal representations and computations." We have not reached "we can reliably reconstruct what an LLM is doing internally."**

ADAG potentially accelerates that transition by removing a major human scaling constraint.

It does not eliminate the epistemic gap.

## The Critical Distinction: Description Is Not Faithfulness

This is where ADAG's own evaluation methodology deserves careful interpretation.

Its simulator scores test whether a natural-language description can predict measured attribution patterns. A high score therefore provides evidence that a description captures regularities in the attribution profile.

But there are two separate questions:

> **Does the description accurately summarize the attribution graph?**

and

> **Does the attribution graph faithfully and completely represent the model's underlying causal computation?**

ADAG directly advances the first problem.

It does not, by itself, resolve the second.

That distinction becomes especially important once the entire process is automated. A pipeline can potentially produce thousands of coherent, convincing circuit descriptions. Automation therefore removes one scalability bottleneck while potentially making it easier to produce mechanistic claims faster than those claims can be independently validated.

This is not an argument against automated interpretability. It is an argument for keeping **interpretability evidence and mechanistic proof conceptually separate**.

A related dual-use concern follows naturally from the jailbreak experiment. If automated circuit analysis can identify internal clusters that control safety-relevant behavior, the same capability could plausibly help an attacker locate and manipulate those clusters. Better internal visibility can strengthen both defense and intervention.

## ⚖️ The Governance Read

| Claim | What ADAG Supports | What It Doesn't Establish |
|---|---|---|
| **"We found internal components involved in behavior X."** | Automated MLP-neuron circuit tracing, clustering, and description | Completeness or uniqueness of the recovered mechanism |
| **"We identified components affecting jailbreak behavior."** | Interventions on selected clusters materially change jailbreak success | A complete jailbreak mechanism or generalization to other models and attacks |
| **"The automated description is meaningful."** | Simulator evaluation tests whether descriptions predict measured attribution profiles | Independent mechanistic faithfulness of the underlying graph |
| **"Our safety argument is grounded in circuit analysis."** | Mechanistic evidence can supplement behavioral evaluation at greater scale | Circuit analysis alone constitutes proof that a system is safe |

This is the governance significance of ADAG.

Most AI assurance today observes systems predominantly from the outside: benchmark performance, red-team results, hallucination rates, jailbreak success, policy compliance, or agent behavior.

Mechanistic interpretability offers something fundamentally different:

**evidence from inside the model.**

If mature, that could eventually give auditors evidence not only that a model behaved safely during testing, but about the internal mechanisms associated with that behavior.

ADAG makes this prospect more scalable by automating a previously labor-intensive interpretation layer. That helps close a gap relevant to [model forensics and evidentiary standards](https://minwu-ai.github.io/model-forensics-why-bad-action-observed-is-not-sufficient-ev/): observing an outcome is not always enough to establish why it occurred.

But internal evidence creates its own evidentiary problem.

A circuit labeled **"safety refusal"** is not automatically a verified safety mechanism simply because an automated pipeline produced a coherent description for it. The stronger the interpretability tooling becomes, the more important it will be to distinguish:

**observed behavior → identified representation → candidate mechanism → causally validated mechanism → sufficiently complete safety evidence**

ADAG meaningfully advances us along that chain.

It does not collapse the chain into one step.

And that may be the most important lesson from the paper: **automating our ability to describe what appears to happen inside an LLM is not the same as automating our ability to know that we truly understand it.**
