---
title: "NVIDIA & ServiceNow Launch 'Project Arc': A Governed Autonomous Desktop Agent Built for Enterprise Risk Realities"
date: 2026-06-16
slug: nvidia-servicenow-launch-project-arc-a-governed-autonomous-d
tag: News
excerpt: "Unveiled at Knowledge 2026 in Las Vegas, Project Arc pairs NVIDIA's OpenShell sandboxed runtime with ServiceNow's AI Control Tower to deliver the first production-grade autonomous desktop agent where every action is policy-enforced, logged, and auditable from day one."
published: false
---

## The Announcement

ServiceNow and NVIDIA introduced Project Arc at ServiceNow's Knowledge 2026 conference in Las Vegas — an enterprise autonomous desktop agent designed to complete complex, multistep work across enterprise tools and systems without requiring pre-built workflows. The launch was a centrepiece of what became an unusually substantive conference for governance-minded practitioners: NVIDIA founder and CEO Jensen Huang joined ServiceNow chairman and CEO Bill McDermott during the opening keynote to discuss the next phase of enterprise AI.

Project Arc is an enterprise autonomous desktop agent that thinks, writes code, executes, and adapts when things don't go as expected, completing complex multi-step work across enterprise tools and systems without requiring pre-built workflows. Critically for risk and governance teams, the architecture is not a capable agent with compliance bolted on afterward — the controls are load-bearing from the start.

## The Technical Stack: OpenShell + AI Control Tower

The governance architecture rests on two interlocking components. Every action the agent takes runs inside NVIDIA OpenShell, a sandboxed runtime environment that adds policy-based management so that autonomous activity stays contained, auditable, and enterprise safe.

OpenShell, which shipped at GTC 2026 in March alongside the broader NVIDIA Agent Toolkit, is purpose-built for agentic workloads. It is an open-source runtime that wraps autonomous agents in policy-governed sandboxes using kernel-level security primitives, so agents can run shell commands and call external tools without touching the host system. The policy model is granular: OpenShell allows per-binary control, restricting which executables the agent can invoke; per-endpoint control, limiting network traffic to specific IP addresses or domains; and per-method control, governing specific API calls or shell functions. Crucially, the agent starts with zero permissions and only gets access to what policy explicitly allows — nothing more.

The second layer is ServiceNow's AI Control Tower. ServiceNow AI Control Tower governs the actions the agent takes, setting policies, monitoring behavior, and logging files read, commands executed, and APIs called — resulting in an autonomous desktop agent that enterprise security leaders can fully audit and approve with confidence.

Unlike standalone AI agents, Project Arc connects natively to the ServiceNow AI Platform through ServiceNow Action Fabric to bring governance, auditability and workflow intelligence to every action the autonomous desktop agent takes. The agent connects to ServiceNow's Action Fabric, which gives it access to company workflows, systems, and operational history, and it can be accessed through a desktop app, enterprise collaboration tools, or email.

The practical implication for an IT administrator is illustrative: an IT administrator could ask the agent to diagnose a system issue, pull relevant logs, cross-reference them against known incidents in ServiceNow, and draft a remediation plan — all in a single autonomous workflow.

## Governance Extends to the Data Centre

Project Arc is not the only governance-forward announcement from the partnership. The companies are also extending ServiceNow's AI Control Tower into NVIDIA's Enterprise AI Factory infrastructure and launching open benchmarking tools for enterprise AI agents. ServiceNow AI Control Tower is now included in the NVIDIA Enterprise AI Factory validated design, extending enterprise governance to large-scale model workloads.

On benchmarking, ServiceNow and NVIDIA are advancing NOWAI-Bench, an open benchmarking suite comprising two frameworks: EnterpriseOps-Gym, a multi-step agentic evaluation framework spanning IT service management, customer service, and HR workflows, and EVA-Bench, a voice agent evaluation framework designed for enterprise settings. Both benchmarks are generally available as open-source releases, and NVIDIA is integrating both into NeMo Gym to make them reusable and accessible for automated model evaluation across the industry. NOWAI-Bench includes EnterpriseOps-Gym, one of the industry's most challenging enterprise agent benchmarks, where Nemotron 3 Super currently ranks No. 1 among open-source models.

## A Maturing Market Signal

The broader significance of Project Arc is what it signals about where the enterprise AI market now sits. The dominant signal from Knowledge 2026 was the movement from AI as an assistance layer to AI as part of the enterprise execution layer. The first wave of enterprise AI largely focused on helping individuals move faster — employees could summarize information, draft content, search knowledge, or complete isolated tasks with less manual effort. Those capabilities created useful gains, but they left the larger operating model mostly intact.

AI now sits closer to workflows, approvals, service delivery, employee interactions, and cross-functional coordination. This elevation of AI from assistant to actor is precisely what makes governance infrastructure non-negotiable rather than optional. ServiceNow is making a specific claim: frontier AI models are becoming commodities, and the durable scarce resource is not intelligence but governed execution.

ServiceNow used Knowledge 2026 to claim where it wants to sit in the enterprise AI stack. The company is no longer positioning itself only as a workflow platform with AI features. It is pitching itself as the governance and action layer for enterprise agents, identities, connected assets, and workflows. The presence of NVIDIA CEO Jensen Huang on the keynote stage, where he described ServiceNow as "destined to be the best platform, the operating system of enterprise AI agents," signals how seriously the broader ecosystem is treating this positioning.

## Availability and What to Watch

Project Arc is currently available as an early preview, while the AI Control Tower integration with NVIDIA Enterprise AI Factory is generally available. ServiceNow is building on and contributing to OpenShell to advance a common foundation for secure, enterprise-grade agent execution.

For risk, compliance, and applied-AI practitioners evaluating agentic deployments, three questions will determine whether Project Arc delivers on its governance promise at scale: whether the OpenShell policy engine is expressive enough to encode organization-specific access controls without creating operational overhead; whether AI Control Tower audit logs integrate with existing SIEM and GRC toolchains; and whether the early-preview limitation meaningfully constrains production rollout timelines for regulated industries. The architecture is sound in principle — the proof will be in the audits.
