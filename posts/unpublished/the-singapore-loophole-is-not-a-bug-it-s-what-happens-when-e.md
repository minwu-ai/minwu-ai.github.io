---
title: "The Singapore Loophole Is Not a Bug — It's What Happens When Export Controls Are Built for Hardware"
date: 2026-07-13
slug: the-singapore-loophole-is-not-a-bug-it-s-what-happens-when-e
tag: AI Governance
excerpt: "OpenAI and Google legally served Pentagon-blacklisted Chinese firms through Singapore subsidiaries, exposing a structural gap that semiconductor-era export controls cannot fix — and that Anthropic's blanket ban is now forcing Congress to confront."
takeaway: "US AI export controls are built around geography and named models, not ownership — meaning a Pentagon-blacklisted Chinese parent can legally access frontier AI through a Singapore subsidiary. Closing that gap requires ownership-based access rules, and the divergence between Anthropic's total ban and the OpenAI/Google access policies has made inaction politically untenable."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## The Specific Mechanics of the Gap

The headline — "OpenAI and Google sold AI to Pentagon-blacklisted firms" — is technically accurate and analytically misleading. Both companies confirmed to the Financial Times that they provided access to advanced AI systems to Singapore-registered subsidiaries of Alibaba, Baidu, and Tencent — and the transactions are entirely legal under current US regulations. That is the real story: not misconduct, but a structural flaw in the rules themselves.

The existing export control framework places strict limits on physical shipment of advanced semiconductors but does not broadly restrict Chinese companies from accessing those same capabilities delivered as cloud-based services through subsidiaries outside mainland China. US legislation restricts access to certain cutting-edge models — including OpenAI's GPT-5.6 and Anthropic's Mythos and Fable — but imposes no blanket ban on AI software supply to Chinese companies, even those on the Pentagon's blacklist.

Washington has built its China technology policy around controlling geography and hardware, while frontier AI is a cloud service that crosses borders through accounts, subsidiaries, resellers, and ordinary-looking API requests. The Fable and Mythos controls — discussed in [The Government Just Killed Two Frontier Models Overnight](https://minwu-ai.github.io/the-government-just-killed-two-frontier-models-overnight-and/) — are the exception that proves the rule: restricting specific named models while leaving the broader API ecosystem open replicates the whack-a-mole dynamic that plagued semiconductor controls.

## A Hardware Precedent That Should Have Warned Us

This echoes the hardware fight. Trump officials already warned that a loophole let Chinese firms buy Nvidia's Blackwell chips; Nvidia's Vera CPU has been cast as a side door back into China. Now the same pattern has reached the software layer. The lesson from chip controls is that geography-based rules invite subsidiary arbitrage — and the software layer is easier to arbitrage than physical goods, because there is no customs checkpoint for an API call.

## Three Labs, Three Policies

| Lab | Access Policy | Distillation Response |
|---|---|---|
| OpenAI | Blocks mainland China; allows Chinese-owned entities in enforceable jurisdictions | Suspended Alibaba-linked accounts; reported to USG |
| Google | Available in Singapore & Hong Kong under ToS | Acknowledges geography alone is insufficient |
| Anthropic | Bans all Chinese-affiliated entities entirely | Accused Alibaba of 25,000 fake accounts, 28.8M interactions |

OpenAI blocks direct access from China but allows some Chinese-owned companies to use its services in jurisdictions where safeguards can be enforced. Google said its AI services are available in markets including Singapore and Hong Kong, subject to usage policies, while acknowledging geographical restrictions alone are insufficient. Anthropic has taken the strictest stance, banning all Chinese-affiliated entities from Claude and accusing Alibaba of creating 25,000 fake accounts for data extraction.

Leaving that distinction to provider discretion guarantees inconsistent outcomes. Anthropic may block a corporate family that OpenAI or Google serves, while all three claim to support American national-security objectives.

## The Distillation Problem Sits Inside the Loophole

OpenAI confirmed suspensions after FT inquiries: the blocked accounts were suspected of "distillation" — systematically gathering AI responses to train competing models — and the company forwarded information to US authorities. This is analytically important: the distillation risk is not hypothetical. It already triggered enforcement. But enforcement happened *after* the fact, via contract-violation detection, not ex-ante access rules — precisely the governance gap [Anthropic's GRAM architecture](https://minwu-ai.github.io/anthropic-s-gram-is-an-architecture-for-trust-not-just-a-saf/) was designed to address at the model level.

> The 1260H list has created a warning without a complete transaction rule, leaving companies to decide how much warning is enough.

Joe Khawam, an AI policy and national security law specialist at the Law Reform Institute, warned that distillation practices could erode "the economic foundation of US frontier AI leadership."

## What to Watch

The divergence between Anthropic's ownership-based ban and the geography-based policies of OpenAI and Google has handed Congress a concrete policy choice rather than an abstract debate.

**My read:** Expect legislative proposals within 6–12 months extending something resembling an "ultimate beneficial ownership" standard to AI API access — analogous to OFAC's 50-percent rule for sanctions — requiring labs to verify that no 1260H-listed entity holds a controlling interest in any API customer, regardless of incorporation location. Whether that clears the Senate is another question; but the [Trump executive order's voluntary framework](https://minwu-ai.github.io/trump-s-ai-executive-order-builds-the-scaffold-but-won-t-lig/) has no answer for this, and a confirmed public disclosure from two of America's largest AI labs is not something the administration can ignore indefinitely.
