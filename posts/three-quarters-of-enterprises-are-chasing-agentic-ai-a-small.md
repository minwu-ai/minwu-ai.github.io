---
title: "Three-Quarters of Enterprises Are Chasing Agentic AI. A Small Minority Are Catching It."
date: 2026-06-25
slug: three-quarters-of-enterprises-are-chasing-agentic-ai-a-small
tag: Agentic AI
excerpt: "Forrester's State of Agentic AI, 2026 and ISACA's 2026 AI Pulse Poll together deliver the most candid enterprise readiness snapshot yet — and the gap between claimed adoption and actual production scale is damning."
takeaway: "The core problem is not model capability — it is that enterprises are deploying autonomous systems faster than they can instrument, govern, or audit them, and the NIST AI RMF, however well-intentioned, cannot close that gap alone because a policy document cannot control a tool-invoking agent at runtime."
published: false
---

## 📊 What the Data Actually Shows

Three-quarters of enterprise leaders tell Forrester they are adopting agentic AI, yet only a small minority have it running in meaningful production. Meanwhile, 90% of organizations believe employees are using AI, but only 22% say AI ROI has met or exceeded expectations, according to ISACA's 2026 AI Pulse Poll of more than 3,400 digital trust professionals. Near-universal usage plus near-universal ROI disappointment is not a technology problem. It is an operationalization problem.

| Metric | Forrester (State of Agentic AI, 2026) | ISACA (2026 AI Pulse Poll) |
|---|---|---|
| Adoption claimed | 75% of enterprise leaders | 90% say employees use AI |
| Production at scale | Small minority | Only 22% met/beat ROI |
| Governance readiness | Agentic sprawl in >50% | Only 38% have comprehensive AI policies |
| Incident response | — | 56% don't know how fast they could halt an AI system |

One of the most common answers in the ISACA survey was some version of "I don't know" — including from audit, risk, and governance professionals whose roles depend on visibility into organizational controls. That is not a neutral finding; it is a material control deficiency hiding in plain sight.

## The Three Blockers Forrester Names

Forrester is unusually direct about why the gap persists. ROI uncertainty traps enterprise ambition in pilot mode; governance gaps drive agentic sprawl, with more than half of enterprises reporting sprawl even after adopting the NIST AI RMF; and platform confusion freezes commitment while teams argue over SaaS agents, SI-built systems, or custom builds.

Underneath all of it sits the "trust tax": every autonomous action must be logged and defensible to an auditor, and right now that cost is too high.

## The NIST RMF Finding Deserves a Separate Read

The foundational NIST AI RMF 1.0 was developed before agentic architectures emerged as a mainstream deployment pattern. As this site has tracked since [Agentic AI Has Outrun the Governance Playbook](/agentic-ai-and-the-governance-gap/): model risk frameworks were built to govern systems that predict, not systems that act. You cannot govern a proliferating agent population with quarterly reviews. You govern it with instrumentation that runs while the agent does, with identity and policy enforced as code. Forrester's finding that sprawl persists even among NIST AI RMF adopters confirms this: framework adoption and control-plane implementation are two entirely different things.

This maps directly to what [Microsoft's Agentic AI Red Team](/microsoft-s-agentic-ai-red-team-draws-a-line-in-the-sand-sev/) and [DeepMind's AI Control Roadmap](/deepmind-s-ai-control-roadmap-from-trust-the-model-to-contai/) have separately surfaced — autonomous agents with tool access and escalating privileges require runtime enforcement, not documentation.

> "The gap we see isn't about models or ambition — it's about orchestration, control, and trust." — Brian Hopkins, VP & Principal Analyst, Forrester

## The Incident Response Gap Is Underappreciated

56% of ISACA respondents are unsure how long it would take to halt an AI system due to a security incident. Only 36% say humans approve most AI-generated actions before execution. 67% of executives believe their company has already suffered a data leak due to unapproved AI tools, while 35% admit they couldn't immediately pull the plug on a rogue agent. The kill-switch question is not rhetorical.

## What to Watch

The historical parallel is early cloud adoption circa 2013–2015: enterprises deployed fast, governance lagged, and Shadow IT incidents forced a correction that took years. The difference with agentic AI is that agents act — they do not merely store. The blast radius of an ungoverned agent is larger and faster than an ungoverned S3 bucket.

Forrester predicts enterprises will delay 25% of AI spend into 2027, as only 15% of AI decision-makers reported an EBITDA lift in the past 12 months. That deceleration is CFOs demanding defensible numbers before the next deployment wave.

**My read:** Enterprises that build the control plane *before* scaling agents — runtime observability, agent identity registries, policy-as-code, and tested kill-switch procedures — will compress the trust tax and convert pilots into production faster. Those that do not will manage the incident Forrester predicted, not the ROI.

---

## Sources

- [Forrester: The State of Agentic AI in 2026 (blog summary)](https://www.forrester.com/blogs/the-state-of-agentic-ai-in-2026-companies-are-chasing-few-are-catching/)
- [ISACA: 2026 AI Pulse Poll](https://www.isaca.org/resources/ai-pulse-poll)
- [ISACA: AI Pulse Poll Reveals Rampant Uncertainty on Enterprise Landscape](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2026/ai-pulse-poll-reveals-rampant-uncertainty-)
