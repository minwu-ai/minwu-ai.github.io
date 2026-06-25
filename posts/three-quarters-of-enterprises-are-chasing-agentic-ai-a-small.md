---
title: "Three-Quarters of Enterprises Are Chasing Agentic AI. Few Have Built the Control Plane"
date: 2026-06-24
slug: three-quarters-of-enterprises-are-chasing-agentic-ai-a-small
tag: Agentic AI
excerpt: "Forrester's State of Agentic AI, 2026 and ISACA's 2026 AI Pulse Poll together provide one of the clearest snapshots yet of enterprise AI readiness—and the gap between adoption and operational maturity remains striking."
takeaway: "The evidence suggests the primary bottleneck is no longer model capability but enterprise operationalization. Organizations are deploying autonomous systems faster than they can instrument, govern, and monitor them, making runtime controls increasingly important alongside traditional governance frameworks."
published: true
---

## 📊 What the Data Actually Shows

Forrester reports that three-quarters of enterprise leaders are adopting agentic AI, yet only a small minority have deployed it in meaningful production beyond isolated pilots or "agentish" chatbots. Meanwhile, ISACA's 2026 AI Pulse Poll found that 90% of organizations believe employees are already using AI, but only 22% say AI has met or exceeded ROI expectations.

Taken together, the surveys point to the same conclusion: enterprise AI adoption is accelerating much faster than enterprise operational readiness.

| Metric | Forrester (State of Agentic AI, 2026) | ISACA (2026 AI Pulse Poll) |
|---|---|---|
| Adoption | 75% of enterprise leaders report adopting agentic AI | 90% believe employees are using AI |
| Production maturity | Only a small minority have meaningful production deployments | Only 22% report AI meeting or exceeding ROI expectations |
| Governance | Governance gaps contribute to agentic sprawl | 38% report comprehensive AI policies |
| Operational readiness | Trust and orchestration remain key barriers | 56% do not know how quickly they could halt an AI system after a security incident |

Perhaps the most striking result from the ISACA survey is how often respondents answered, "I don't know"—including on questions related to incident response and operational control. For organizations deploying increasingly autonomous systems, that uncertainty itself is an important governance signal.

---

## 🚧 Why Production Scale Remains Elusive

Forrester identifies three recurring obstacles preventing enterprises from moving beyond pilots.

First, uncertain ROI keeps many organizations trapped in experimentation rather than broad deployment.

Second, governance has not kept pace with autonomous, tool-using agents. As agents become capable of executing workflows across multiple systems, traditional governance processes become harder to apply consistently.

Third, platform fragmentation leaves organizations debating whether to adopt SaaS agents, build custom agents, or rely on systems integrators before establishing a scalable operating model.

Underlying all three challenges is what Forrester describes as the **"trust tax"**—the operational overhead required to make every autonomous action observable, explainable, and defensible.

---

## 🛡️ Governance Frameworks Need a Runtime Companion

None of this diminishes the value of frameworks such as the NIST AI Risk Management Framework. They provide an essential foundation for identifying, measuring, and managing AI risk.

However, agentic systems introduce a different operational challenge.

Traditional model governance was developed primarily for systems that generate predictions or recommendations. Autonomous agents continuously plan, invoke tools, access external systems, and make decisions throughout execution. Those behaviors require controls that operate while the system is running—not solely during design reviews or periodic governance assessments.

The emerging pattern across industry is increasingly clear:

> Policies define expectations.
>
> Runtime control planes enforce them.

This aligns closely with themes emerging from [Microsoft's recent work on agentic AI security and red teaming](/microsoft-s-agentic-ai-red-team-draws-a-line-in-the-sand-sev/), 
as well as [DeepMind's AI Control Roadmap](/deepmind-s-ai-control-roadmap-from-trust-the-model-to-contai/). As AI systems gain greater autonomy, governance increasingly depends on continuous observability, identity, policy enforcement, and execution logging—not documentation alone.

---

## 🚨 The Incident Response Gap Deserves More Attention

ISACA's findings suggest many organizations are not yet operationally prepared for AI incidents.

More than half of respondents (56%) said they do not know how quickly they could halt an AI system following a security incident. Only about one-third believed they could stop a system within an hour.

That finding may be more important than any adoption statistic.

As organizations begin deploying long-running agents capable of interacting with enterprise systems, knowing how to safely pause, isolate, or terminate those agents becomes a fundamental operational capability—not simply an IT process.

---

## 🔭 What to Watch

The historical parallel is early cloud adoption circa 2013–2015: enterprises deployed fast, governance lagged, and Shadow IT incidents forced a correction that took years. 
The difference with agentic AI is that agents act—they do not merely store. The blast radius of an ungoverned agent is larger and faster than an ungoverned S3 bucket.

Separately, in its **2026 Technology Predictions**, Forrester forecasts that enterprises will defer **25% of planned AI spending into 2027**, noting that only **15% of AI decision-makers reported an EBITDA lift** over the previous 12 months. That suggests many CFOs are beginning to demand measurable business outcomes—not simply more AI deployments—before approving the next wave of investment.

**My read:** Enterprises that build the **AI control plane** before scaling agents—runtime observability, agent identity registries, policy-as-code, and tested kill-switch procedures—will compress the trust tax and convert pilots into production faster. Those that do not are more likely to spend the next few years managing operational failures instead of realizing ROI.


---

## Sources

- [Forrester: The State of Agentic AI in 2026 – Companies Are Chasing, Few Are Catching](https://www.forrester.com/blogs/the-state-of-agentic-ai-in-2026-companies-are-chasing-few-are-catching/)
- [Forrester: Predictions 2026 – AI Moves From Hype To Hard Hat Work](https://www.forrester.com/blogs/predictions-2026-ai-moves-from-hype-to-hard-hat-work/)
- [ISACA: 2026 AI Pulse Poll](https://www.isaca.org/resources/ai-pulse-poll)
- [ISACA: AI Pulse Poll Reveals Rampant Uncertainty on Enterprise Landscape](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2026/ai-pulse-poll-reveals-rampant-uncertainty-on-enterprise-landscape)
