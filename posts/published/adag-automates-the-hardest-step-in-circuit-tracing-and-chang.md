---
title: "ADAG Automates the Hardest Step in Circuit Tracing — and Changes What Interpretability Can Promise"
date: 2026-08-20
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

Consider a simple question:

> **What is the capital of the state containing Dallas?**

A capable model answers:

> **Austin.**

From ordinary evaluation, all we observe is:

**Prompt → LLM → Austin**

The model might even explain:

> Dallas is in Texas, and the capital of Texas is Austin.

That sounds like a perfectly sensible chain of reasoning. But it is still generated text. It does not establish that the model internally performed the computation:

**Dallas → Texas → Austin**

The model's explanation of its reasoning and the mechanism that actually produced its answer are not necessarily the same thing.

This distinction is at the heart of **mechanistic interpretability**: the attempt to reverse-engineer a learned neural network into human-understandable representations, components, and computational pathways.

Using the Dallas example, we can separate four increasingly ambitious questions:

| Level | Question | Dallas Example |
|---|---|---|
| **Behavior** | What did the model do? | It answered "Austin." |
| **Representation** | What information exists internally? | Internal activity contains representations related to Dallas, Texas, states, or capitals. |
| **Mechanism** | How did those representations interact? | Dallas-related representations contribute to Texas/state representations, which ultimately promote "Austin." |
| **Intervention** | Do those components actually matter? | Suppressing or amplifying a component changes the probability of producing "Austin." |

Most conventional AI evaluation operates primarily at the first level. Mechanistic interpretability is trying to reach the others.

## What Is an "Internal Feature"?

This raises an immediate question: when interpretability researchers say that a model contains a **feature** associated with something like Texas, what exactly do they mean?

The simplest mental model would be to imagine that somewhere inside the LLM there is:

> Neuron 172 = "Dallas"  
> Neuron 846 = "Texas"  
> Neuron 991 = "Austin"

Real neural networks are generally not organized that neatly.

A concept can be **distributed across many neurons**, while an individual neuron can participate in representing several seemingly unrelated concepts. Interpretability researchers commonly discuss these problems in terms of **distributed representation, polysemanticity, and superposition**.

A useful analogy is an audio recording.

Imagine several instruments — violin, piano, drums — recorded through thousands of microphones. Each microphone captures a different mixture of the instruments. There may be no single "violin microphone."

Yet by analyzing all of those recordings together, it may still be possible to recover an underlying **violin signal**.

In this analogy:

**individual neurons are like the microphones; an internal feature is more like the recovered violin signal.**

Mathematically, the model's activation at some point can be represented as a high-dimensional vector:

$$
\mathbf{x}=(x_1,x_2,\ldots,x_d)
$$

Rather than requiring one coordinate \(x_{417}\) to mean "Texas," researchers can look for a direction or pattern \(\mathbf{v}\) such that

$$
\mathbf{v}^{T}\mathbf{x}
$$

becomes large when the model is processing information associated with Texas.

That direction is a candidate **feature**: a detectable internal representation associated with some learned pattern, concept, relationship, or computational property.

Not every feature will correspond to a concept humans can conveniently name. And the word *feature* itself is used somewhat differently across interpretability methods. Sparse autoencoders, for example, attempt to decompose dense neural activations into a larger dictionary of relatively sparse features. ADAG's attribution graphs, by contrast, operate on MLP neurons and then organize related neurons into higher-level **supernodes**.

The distinction matters. A neuron, an SAE feature, and an ADAG supernode are not interchangeable objects.

But they are part of a broader progression in mechanistic interpretability:

**neurons / activations → features and representations → circuits → behavior**

Finding something that looks like a "Texas" representation is therefore only the beginning.

The harder question is:

> **How does the model use it?**

## From Features to Circuits: How Did "Dallas" Become "Austin"?

Suppose interpretability analysis finds internal activity associated with Dallas and Texas.

That is evidence about **representation**. It tells us that information related to those concepts appears to exist inside the model.

It still does not tell us how the answer was produced.

To understand the mechanism, researchers want to know whether those internal components participate in something resembling:

**"Dallas" input**  
↓  
**Dallas / Texas-related representations**  
↓  
**state / capital relationship representations**  
↓  
**Austin-related output contributions**  
↓  
**"Austin"**

That is the ambition of **circuit tracing**.

Rather than asking only which internal components activate, circuit tracing attempts to reconstruct relationships among components that contribute to a particular model output.

The analogy to reverse-engineering software is useful.

Behavioral evaluation is like running an unknown executable:

> Give it an input → observe the output.

Feature-level interpretability is like discovering meaningful variables or data structures inside the program.

Circuit tracing aims for something more ambitious:

> **recover enough of the internal computation to understand how those components interact to produce the output.**

Modern interpretability research has made meaningful progress toward this goal. Researchers have identified interpretable internal features, localized behaviors to model components, and changed outputs through targeted interventions. Sparse autoencoders and related dictionary-learning methods have made it easier to extract potentially meaningful representations from otherwise dense neural activations.

Anthropic made the next challenge explicit in its work on [mapping the internal features of Claude](https://www.anthropic.com/research/mapping-mind-language-model): discovering representations tells us something about what information exists inside a model, but understanding how the model *uses* those representations requires studying the circuits connecting them.

And this creates another problem.

Once researchers extract an attribution graph containing potentially hundreds or thousands of internal components, **someone has to figure out what all of those components mean**.

That is where ADAG enters.

## The Human Bottleneck in Circuit Tracing

Submitted April 8, 2026 by Arora, Wu, Steinhardt, and Schwettmann of Stanford and Transluce, [ADAG: Automatically Describing Attribution Graphs](https://arxiv.org/abs/2604.07615) introduces a fully automated pipeline for organizing and describing attribution graphs.

Prior circuit-tracing work relied heavily on researchers manually inspecting activation examples and attribution patterns, grouping related components, and deciding what those groups appeared to represent. The ADAG authors characterize this researcher-driven interpretation as a major obstacle to scaling circuit analysis across many prompts and increasingly complex models.

Think again about the Dallas example.

It is one thing for software to produce a huge graph of neurons and attribution relationships associated with the answer "Austin."

It is another thing for a researcher to look through that graph and conclude:

> **These neurons appear related to Dallas and Texas. These others appear involved in state-capital relationships. This group contributes toward Austin.**

Doing that manually does not scale well.

ADAG therefore attacks a different bottleneck from simply computing the attribution graph:

> **How do you turn a large collection of internal components and relationships into something humans can understand without manually interpreting them one by one?**

Its answer is to automate much of that interpretation layer.

This does not mean that ADAG "solves interpretability." More precisely, it automates one of the most stubborn human bottlenecks in circuit tracing: turning large attribution graphs into semantically organized, human-readable **candidate mechanisms**.

## How ADAG Works

ADAG's pipeline has four broad stages:

1. **Circuit tracing** identifies internal components and attribution relationships relevant to a particular model output.
2. **Attribution profiles** characterize each component according to the inputs contributing to its activation and its contribution toward candidate output logits.
3. **Automatic clustering** groups related components into higher-level "supernodes."
4. **Automatic description** generates natural-language interpretations of those supernodes.

The attribution profile is particularly important.

Traditional approaches might inspect examples that strongly activate a component and conclude, for example, that it has something to do with "Texas." But observing what activates something reveals only part of its functional role.

ADAG instead examines both directions:

**What contributes to this component?**

and

**What output logits does this component contribute toward?**

A clustering algorithm then groups neurons with similar attribution profiles. An explainer language model proposes descriptions for those groups, while a simulator language model evaluates how well candidate descriptions predict held-out attribution patterns.

On manually defined supernodes in the state-capitals setting, automated descriptions perform approximately as well as human descriptions on input attribution and substantially better under the paper's output-contribution metric.

That result should be interpreted carefully. Both human and machine descriptions are evaluated through the paper's simulator framework, and the automated procedure selects among multiple candidate descriptions. The experiment therefore demonstrates strong performance under ADAG's autointerpretability metric; it is not independent proof that the generated descriptions are mechanistically correct.

## What ADAG Can Actually Do

The paper provides two especially useful demonstrations.

### Recovering a Known Circuit

ADAG revisits the same kind of multi-hop state-capitals task we have been using as our running example.

This matters because earlier human-led work gives the authors something against which an automated pipeline can be compared. ADAG recovers qualitatively similar functional structure without requiring researchers to manually interpret every component.

A later independent pipeline from Patel et al., [LLMs Can Annotate Attribution Graphs](https://arxiv.org/abs/2608.02632), reaches a related result: automatically generated supernodes achieve interpretability comparable to human-generated ones under automated evaluation, while recovering the intermediate-hop supernode in 97 of 100 prompts.

The convergence is useful evidence that **automating the organization and description of attribution graphs is becoming technically viable**.

It does not establish that either pipeline has recovered the complete ground-truth mechanism.

### From "Why Austin?" to "Why Did the Jailbreak Work?"

Now the safety significance becomes clearer.

Instead of asking:

> **Why did the model answer Austin?**

ask:

> **Why did an aligned model provide harmful medical advice after a jailbreak?**

ADAG applies its pipeline to a harmful-medical-advice jailbreak against Llama 3.1 8B Instruct. It analyzes more than 150 semantically related prompt variants and groups relevant internal neurons into 20 supernodes.

The researchers then go beyond simply labeling them.

They **intervene** on selected clusters — suppressing or amplifying their activations — and measure whether jailbreak success changes.

Some interventions produce large effects. Negatively steering one cluster associated with safety-oriented behavior substantially increases attack success, while positively steering another jailbreak-associated cluster produces a similarly large increase.

This provides stronger evidence than merely observing that a cluster activates during jailbreaks.

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

That gives us another useful hierarchy:

**Correlation:** this component activates during the behavior.

**Interpretation:** this component appears to represent something meaningful.

**Circuit evidence:** this component participates in an attribution pathway associated with the behavior.

**Intervention:** changing this component changes the behavior.

Each step gives us stronger evidence about what may actually be happening inside the model.

## What Interpretability Can — and Cannot — Tell Us Today

ADAG arrives at an important moment for mechanistic interpretability.

The field has moved considerably beyond treating large language models as completely opaque black boxes. Researchers can now recover meaningful internal representations, identify computational motifs, construct candidate circuits, and sometimes intervene on those components to alter model behavior.

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

And that may be the most important lesson from the paper:

> **Automating our ability to describe what appears to happen inside an LLM is not the same as automating our ability to know that we truly understand it.**
