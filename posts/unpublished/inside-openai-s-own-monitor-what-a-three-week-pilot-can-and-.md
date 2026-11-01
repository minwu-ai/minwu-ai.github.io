---
title: "Inside OpenAI's Own Monitor: What a Three-Week Pilot Can and Can't Prove"
date: 2026-11-01
slug: inside-openai-s-own-monitor-what-a-three-week-pilot-can-and-
tag: Alignment, AI Governance
excerpt: "METR and Redwood Research found vulnerabilities in OpenAI's internal agent monitoring. Their pilot shows the value of outside access, while leaving subsequent fixes and expanded coverage unverified by the evaluators."
takeaway: "Independent access helped expose real weaknesses in OpenAI's monitoring system. But finding a flaw, reporting a patch, and independently testing the repaired system are different evidentiary steps. This pilot establishes the first; it does not establish the last."
published: false
---

*Updated November 1 to incorporate METR's October 29 clarification and OpenAI's monitoring-system description published that day.*

METR has already shown how an evaluator's own tooling can be subverted — a lesson from [its Inspect transcript-viewer exploit, which I covered earlier](https://minwu-ai.github.io/when-the-auditor-s-camera-can-be-hacked-metr-s-inspect-vulne/). The October 22 report examined a different layer of the safety system: OpenAI's internal monitoring of its own agents.

The central question is simple. If a monitor is supposed to catch an agent acting against its operator's intentions, what evidence shows that the agent cannot evade the monitor itself?

## 🔍 What actually happened

Between July 21 and August 11, 2026, one METR employee and one Redwood Research employee worked onsite at OpenAI. They had access to internal code, monitor prompts and configuration, documentation, and interviews with roughly a dozen staff. Their task was to estimate monitoring coverage and investigate whether agents could disable or subvert it. The assessment concerned the system as it existed on and before July 21, excluding changes then underway. [METR's public report](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/)

The researchers estimated that 75–94% of agentic internal Responses API traffic from models at least as capable as GPT-5.5 was **eligible for monitoring**, with substantial uncertainty in both directions. For the internal Codex subset, the estimate was 99.2%. These are eligibility estimates, not successful-review rates or measures of how reliably misconduct was detected. They also do not describe all OpenAI traffic. [Redwood's co-published findings](https://blog.redwoodresearch.org/p/red-teaming-openais-internal-agent)

The vulnerabilities included a way Codex agents could in principle bypass sandboxing and Auto-Review, and an exploit that could prevent hundreds of recent actions from being monitored. Those findings concern possible evasion; they do not establish that agents had already exploited these routes in practice. [Redwood's account](https://blog.redwoodresearch.org/p/red-teaming-openais-internal-agent)

## ⚖️ The sentence that does the real work

The important qualification concerns what happened afterward.

METR's October 29 update says OpenAI reports that most vulnerabilities have been patched, with one fix still in progress; the remaining vulnerability does not affect OpenAI's misuse safeguards stack. METR says it has not evaluated these claims. [Updated report and change log](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/)

OpenAI's own October 29 account likewise acknowledges an outstanding fix and describes a substantially expanded monitoring system. That is useful additional disclosure. It is still a developer account, rather than a follow-up assessment by the pilot's evaluators. [OpenAI's monitoring-system description](https://openai.com/index/how-we-detect-frontier-model-misalignment/)

> The pilot found weaknesses in the historical system. It did not independently establish that subsequent fixes work or that the expanded system provides the intended coverage.

That is narrower than saying nobody independent has checked anything. The public report establishes what these evaluators did and did not verify; it cannot establish the absence of every other review.

Nor does an unverified patch mean a failed patch. It means the public evidence supports a more limited conclusion than a clean bill of health.

## 🚧 What the design actually limits

Three features bound what readers can infer:

| Constraint | What it means for the evidence |
|---|---|
| Two researchers, three weeks | This was a bounded search for weaknesses. Finding some does not tell us how many remained undiscovered. |
| Restricted disclosure | The public account exposes only part of the evidence, limiting outsiders' ability to assess the full findings. |
| Historical scope, without evaluator verification of later claims | The findings cannot certify the current system or the effectiveness of subsequent remediation. |

The disclosure restriction deserves precision. The researchers produced a 61-page report for OpenAI researchers and security staff; METR and Redwood leadership received a 38-page version redacted by OpenAI. OpenAI also held discretion over sensitive material in the public post, and the evaluators lacked a unilateral right to describe those redactions. They nevertheless endorsed the published findings. [Disclosure terms](https://blog.redwoodresearch.org/p/red-teaming-openais-internal-agent)

These terms limit public scrutiny. They do not, by themselves, demonstrate that an adverse conclusion was suppressed. The difference between the reports' page counts is not a measure of how much safety-relevant evidence was withheld.

The pilot was explicitly designed to test deep external access, rather than deliver robust public transparency. That makes it a useful experiment in assessment, while limiting its value as public assurance. [Pilot's stated purpose](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/)

## 🛡️ Why this is an alignment question

Monitoring is one of the controls on which an AI safety argument may depend. That makes the monitor's integrity part of the alignment problem: an agent's behavior can only be assessed through evidence the oversight system actually receives and interprets.

Several questions therefore need separate answers. Was the activity selected for monitoring? Did the monitor receive the relevant evidence? Did it recognize the problem? Did someone intervene soon enough?

A high eligibility percentage answers only part of the first question. It cannot stand in for the whole chain.

OpenAI's system performs asynchronous review, so detection and timely intervention also need to be distinguished from blocking an action before it happens. OpenAI's current description discusses both monitoring and the response mechanisms that follow alerts. [How OpenAI describes the system](https://openai.com/index/how-we-detect-frontier-model-misalignment/)

This connects to the questions I raised in [my discussion of GovAI's embedded-assessment proposal](https://minwu-ai.github.io/govai-s-embedded-assessments-paper-turns-ceo-safety-pledges/): access, scope, independence, and disclosure determine what an outside assessment can establish. Getting evaluators inside is valuable. The terms of that access determine how much confidence can travel outside with their conclusions.

## 🧭 What to watch

METR and Redwood say future exercises should follow the transparency and independence practices in [METR's approach to working with AI companies](https://metr.org/blog/2026-10-14-our-approach-to-risk-assessment/). Those practices include disclosing material access restrictions and whether redactions affect conclusions. That is a concrete standard against which to judge the next engagement. [Commitment in the pilot report](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/)

For the next assessment, I would look for three things:

1. **Independent retesting of remediation.** Identify which findings were retested, on which system version, and what remains unresolved. Include fresh adversarial cases where feasible.
2. **Evidence across the monitoring chain.** Distinguish eligibility, completed review, detection, and response time, with clear denominators and exclusions.
3. **Disclosure rights that make limitations visible.** Evaluators should be able to say when withheld information materially changes the public's ability to assess their conclusions, without publishing dangerous exploit details.

Retesting would strengthen the evidence for specific fixes under specific conditions. It would not prove that every future attack will fail. The point is to make confidence traceable to tests, and to repeat those tests as the system changes.

The pilot's strongest result is that meaningful external access can expose weaknesses in a safety control. The next milestone is a public account of what independent evaluators retested after remediation, what passed, and what remains uncertain.
