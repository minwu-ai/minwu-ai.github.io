



⸻

title: “Trustworthiness Fixes That Travel: A New Paper Tests Whether Agent Safety Generalizes Across Model Families”
date: 2026-09-21
slug: trustworthiness-fixes-that-travel-a-new-paper-tests-whether-
tag: Agentic AI, Evaluation
excerpt: “A new agent-evaluation framework does something most benchmarks stop short of: find failures, engineer controls against them, and then test whether those controls still work when the underlying model changes.”
takeaway: “HAAF’s most interesting contribution isn’t another taxonomy of trustworthy AI. It’s closing the loop between evaluation and engineering: two controls derived from one Qwen3-8B failure study improved all 13 tested systems across seven model families without model-specific tuning. If that result eventually survives real deployment environments, agent safety controls could become infrastructure rather than model-specific patches.”
cover: “/assets/”
cover_alt: “Illustration: “
published: false


🔄 The Missing Step After Evaluation

Over the past several months, a recurring theme on this site has been that an agent benchmark score answers increasingly little by itself.

OSWorld 2.0 showed that an agent can look capable on short tasks while performance collapses across long, stateful workflows.

Execution-trace research showed that even a correct outcome can conceal dangerous intermediate actions, benchmark shortcuts, or flawed evaluation infrastructure.

Princeton’s reliability work added another distinction: capability tells us whether an agent can do something; reliability asks whether we can depend on it to keep doing it.

And Scale AI’s READY framework moved the unit of evaluation beyond the autonomous agent entirely, asking how much human oversight and cost are required to reach a specified reliability level.

Together, those papers progressively deepen the evaluation question:

Can the agent do it?

Can it do realistic work?

What did it actually do while completing the work?

Can it do it consistently?

How much oversight is required before we can rely on it?

A March 2026 preprint from researchers at the Chinese University of Hong Kong, Macao Polytechnic University, and Jilin University adds a different question:

Once evaluation discovers a failure and we engineer a control against it, does that control survive when the underlying model changes?

That may be the paper’s most useful contribution.

🧩 First, Define What You’re Trying to Fix

The paper proposes the Holographic Agent Assessment Framework (HAAF).

Its starting point is that agent evaluation remains fragmented across coding, hallucination, jailbreak resistance, tool use, and other isolated capabilities. Before measuring trustworthiness, the authors argue, evaluators need to define what the target actually contains.

HAAF uses five properties:

* Reliability
* Robustness
* Safety
* Social-Ethical Alignment
* Operational Integrity

It then evaluates them across a scenario manifold varying task objectives, tool interfaces, interaction depth, environmental constraints, social context, and consequence severity.

The distributional component matters.

Rare adversarial manipulations, cascading tool failures, authorization mistakes, or socially sensitive interactions may matter far more than their frequency suggests. An average benchmark score can therefore look excellent while concealing exactly the failure an organization most needs to prevent.

But a five-dimensional trustworthiness taxonomy is not, by itself, what makes this paper particularly interesting.

What HAAF does after finding the failures is more consequential.

🛠️ From Evaluation to Engineering

Most benchmarks effectively end here:

test → score → report

HAAF instead tries to create a lifecycle:

test → diagnose → intervene → retest → transfer

The authors first conduct a 24-scenario design study using Qwen3-8B.

That evaluation reveals recurring weaknesses and leads to two relatively simple system-level interventions.

The first is a tool-output firewall, intended to stop untrusted content returned by tools from silently becoming trusted instructions.

The second is a confirmation gate, requiring explicit confirmation before certain consequential actions proceed.

Neither intervention requires changing the underlying model weights.

That distinction matters.

As I discussed in Before You Blame the Model, agent failures can originate not only in the LLM but in the surrounding machinery — orchestration, tools, memory, permissions, retrieval, and execution infrastructure.

HAAF suggests the complementary proposition:

Some safety improvements may belong in that surrounding machinery too.

And if they do, they may be portable.

🧪 The Experiment That Makes This Interesting

The researchers freeze those two interventions and apply them to 13 systems from seven model families:

Llama, Mistral, Kimi, GLM, Qwen, GPT, and DeepSeek.

There is no model-specific tuning.

The validation suite contains 100 scenarios, including 76 additional adversarial scenarios that weren’t part of the original 24-scenario design study.

All 13 systems improve on the paper’s risk-weighted failure measure.

Two — GPT-oss-120B and Llama-3.1-8B — reach RWF = 0.000 on this synthetic suite.

That’s a more interesting result than simply showing that a mitigation improves the model on which it was developed.

It asks whether an agent-safety intervention can behave more like an architectural control than a model-specific patch.

🔧 A Safety Control That Survives the Model Swap

Consider what this means operationally.

An enterprise evaluates an agent running Model A and discovers that malicious tool output can manipulate its behavior. It builds a tool-output firewall to enforce a trust boundary.

Six months later, Model A is replaced by Model B.

Under one model of AI safety, much of the work begins again:

new model → rediscover failures → redesign mitigation → retune → revalidate

But if important controls live at the system layer and transfer across models, the lifecycle could look different:

new model → retain controls → regression-test → validate remaining risks

That is a major distinction for enterprise AI governance.

Foundation models may change several times during the life of an application. Safety infrastructure that must be rebuilt every time the model changes creates both operational cost and governance risk.

A control that survives the model swap begins to look less like a patch and more like infrastructure.

📉 Transfer Doesn’t Mean Universal Protection

The results also show why that claim needs boundaries.

The interventions do not help every model equally.

GPT-oss-120B moves from a risk-weighted failure score of 0.481 to 0.000.

Qwen3-32B moves only from 0.462 to 0.443.

The interventions transfer, but they primarily address the failure surfaces they were designed to fix. Models whose remaining failures arise elsewhere receive much less benefit.

So the paper does not demonstrate:

Safety fixes generalize.

It provides evidence for something narrower and more useful:

Some system-level controls can generalize across model families against the classes of failure those controls were designed to address.

“Works across models” is not the same as “solves every model’s problems.”

⚠️ Cross-Model Is Not Cross-Domain

There is another important limitation.

The intervention-design study and validation suite contain different scenarios, so this isn’t simply a case of designing fixes against 100 tests and replaying those same tests.

But both experiments still operate inside the same synthetic environment and tool ecosystem.

The paper therefore provides evidence roughly equivalent to:

new models + additional scenarios + same underlying environment

It does not yet establish:

new models + new tools + new organizations + new workflows + new deployment distributions

The authors acknowledge this limitation and frame the experiment as an illustrative validation of the methodology rather than proof that these systems are deployment-ready.

Real deployment claims would require genuinely held-out environments, broader tool ecosystems, repeated hardening cycles, and human-validated scenarios.

The evidence is therefore meaningfully cross-model, but not yet convincingly cross-domain.

🏗️ The Evaluation Stack Gets One Layer Deeper

Seen alongside the evaluation work covered here over the past few months, HAAF fills a useful gap.

Benchmark: Can the agent do the task?

Long-horizon evaluation: Can it do realistic work?

Trace analysis: What actually happened during execution?

Reliability: Can we depend on it to keep working?

READY: What human-AI configuration reaches the required reliability at an acceptable cost?

HAAF: When evaluation discovers a weakness and we engineer a control, does that control survive a model change?

That final question connects evaluation directly to model change management.

Evaluation is no longer only a mechanism for deciding whether a model is good enough. It can become the beginning of an engineering process: discover failure modes, translate them into controls, validate those controls, and determine which remain valid as the underlying technology changes.

That is a considerably more mature conception of what an evaluation program should do.

🎯 From Patches to Infrastructure

HAAF doesn’t prove that portable agent-safety infrastructure exists in the general case.

Its environment is synthetic. Its scenario distribution is limited. And the uneven improvements across models show that no small set of controls substitutes for model-specific evaluation.

But it demonstrates a direction worth testing.

The governance question for an agentic system is increasingly not simply:

Is this model safe?

It is:

Which risks belong to the model, which belong to the system around it, and which controls remain effective when the model changes?

That changes what evaluation is for.

A benchmark tells you something about today’s model.

A mature evaluation program should also help you build controls that remain useful tomorrow.

A safeguard that works only for one model is a patch.

A safeguard that survives the model swap starts to look like infrastructure.
