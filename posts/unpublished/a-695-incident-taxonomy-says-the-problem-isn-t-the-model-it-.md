---
title: "What 695 AI Incidents Reveal About Human Control"
date: 2026-11-11
slug: what-695-ai-incidents-reveal-about-human-control
tag: Agentic AI, AI Governance
excerpt: "A Carnegie Mellon preprint identifies 12 ways human–agent interactions break down and asks what people can see, stop, and undo when agents act on their behalf."
takeaway: "All 12 interaction failure modes appeared in both low- and high-autonomy incidents. How they played out varied with how much work the agent completed between points of human involvement."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 🔍 The new evidence

An AI agent can make the same kind of mistake whether it answers one question at a time or carries out a series of actions on its own. What changes is what a person can do about it. In [When AI Agents Act on Our Behalf](https://arxiv.org/abs/2611.00291), an October 30 preprint, Carnegie Mellon researchers Canwen Wang, Qing Xiao, Haiyi Zhu, and Hong Shen analyzed 695 documented incidents from the AI, Algorithmic, and Automation Incident and Controversy repository (AIAAIC) and the AI Incident Database (AIID). They identified 12 ways human–agent interactions break down, and found examples of every mode at both low and high autonomy.

On October 2, this site covered Mohamed Aly Bouke’s [Competing-Hazards systematization](https://minwu-ai.github.io/a-competing-hazards-model-finally-gives-loss-of-control-a-sh/), which audited 22 incident reports and 102 evaluations to build a shared vocabulary for loss of control. Bouke tracks how an agent’s attempts end, including whether it stops safely or acts outside its approved scope. Wang and colleagues ask what people could understand, observe, control, or repair as the interaction unfolded.

## ⚙️ How the taxonomy is built

The authors adapted [Amershi et al.’s guidelines for human–AI interaction](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/). They folded the guidelines’ initial stage into *During Interaction* because questions about the agent’s role, capabilities, and sources can recur while it works. They retained *When Wrong* and *Over Time*.

- **During Interaction.** Boundary violation was the most frequently coded mode (261/695). The agent exceeded what the user understood they had delegated. Unclear provenance (224/695) covered uncertainty about where information came from or whether anyone had checked it. Unclear agent role (88/695) covered uncertainty about whether the user was interacting with AI or what role it was playing.
- **When Wrong.** In 152 incidents, an error went undetected until it affected later actions or other people. In 42, an attempted stop, override, escalation, or handoff failed to restore human control.
- **Over Time.** Failures included changes in the agent’s behavior that built up across interactions, delegated authority carrying over into new contexts, and unhealthy emotional or cognitive dependency.

An incident could receive more than one label. The [counts in Figure 2](https://arxiv.org/html/2611.00291v1#S4) describe the documented cases. The repositories supply no denominator for estimating how frequently each mode occurs in deployment.

## 🧱 Where safeguards can fall short

The authors classified 453 incidents as low autonomy, where a person was involved in each contribution, and 242 as high autonomy, where the agent did some work independently between points of human involvement. Consider an undetected error. At lower autonomy, a person might act on a plausible but incorrect output. At higher autonomy, the agent can carry an error into later steps before the person sees an intermediate result.

This is a distinction about deployment design. An approval checkpoint can give users time to intervene before a consequential action. Its value depends on what they can see at that point, what they can change, and whether they can still stop the action. The [qualitative comparison](https://arxiv.org/html/2611.00291v1#S3.SS3) shows how those opportunities differed across reported incidents. Measuring the effect of a checkpoint would require a separate study.

The earlier [Competing-Hazards audit](https://arxiv.org/abs/2609.38411) found that the environment allowed an out-of-scope effect in 20 of its 22 incident reports. In a separate [Cyera audit](https://www.cyera.com/research/agent-inflicted-damage-inside-the-real-world-failures-of-enterprise-ai-systems), 188 of 344 enterprise-relevant cases from September 2023 through May 2026 involved direct harm without an attacker. Both findings put the conditions under which an agent can act at the center of the investigation.

## 🧭 Where this leaves practitioners

The authors call for controls that let people keep an agent working while retaining the ability to constrain its scope, pause or redirect it, and recover when an action goes wrong. For a feature that can make purchases, that means asking what the user can see before the order is placed, whether they can stop it in time, and what recourse they have afterward.

The [paper’s critique of incident records and benchmarks](https://arxiv.org/html/2611.00291v1#S5.SS3) follows from those questions. The repositories often leave out whether the user had a checkpoint or could undo an action. The benchmarks discussed in the paper seldom exercise the user’s ability to intervene or recover. A team evaluating the purchase feature could give a user an order that goes beyond the original request and see whether they can spot the change, stop the purchase, or reverse it. That exercise tests what the deployment actually lets a person do when the agent gets something wrong.
