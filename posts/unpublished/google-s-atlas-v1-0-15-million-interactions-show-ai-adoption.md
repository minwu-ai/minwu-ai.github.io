---
title: "Google's ATLAS v1.0: 15 Million Interactions Show AI Adoption Is a Mile Wide and an Inch Deep"
date: 2026-09-01
slug: google-s-atlas-v1-0-15-million-interactions-show-ai-adoption
tag: Industry, AI Governance
excerpt: "Google's first large-scale behavioral study of Gemini usage finds observed AI activity across occupations representing 88% of US employment, but across only 21% of tasks in the median covered occupation — a 'broad but shallow' pattern that should reshape how enterprises measure adoption, ROI, and workforce exposure."
takeaway: "ATLAS v1.0's real lesson is not simply that AI adoption should go deeper. It is that adoption counts are becoming the wrong denominator: enterprises should measure where AI appears at the task level, how deeply it penetrates workflows, whether it assists or executes, and whether the resulting work actually improves."
cover: "/assets/"
cover_alt: "Illustration: "
published: false
---

## 📊 What ATLAS Actually Measured

ATLAS — the Activity, Task, Landscape, and Adoption Study — analyzes roughly 15 million de-identified interactions across the Gemini App, Google AI Mode, and the Gemini API, mapped to more than 800 occupations, 4,000 tasks, 300 household activities, 150 countries, and 140 languages. The dataset covers 14,653,926 interactions sampled between April 6 and April 19, 2026. Zanna Iscenko — AI & Economy Lead in Google's Chief Economist's Office — and Scott Strand are corresponding authors.

ATLAS insights are powered by Google DeepMind's Observation Clustering and Taxonomy Organisation (OCTO), which transforms unstructured LLM conversations into organized entities and maps work-related activity to O\*NET occupational and task taxonomies — also used by Anthropic's [Economic Index](https://arxiv.org/abs/2503.04761). The methodologies are different, but the shared taxonomy creates an unusually useful cross-vendor comparison point.

The distinction between **interactions and adoption** matters. ATLAS does not observe every task performed by a worker, nor does it measure whether the interaction ultimately produced useful work. It measures where AI-related activity appears in a very large sample of real-world interactions.

## 🌊 The Structural Finding: Broad But Shallow

The most important number in Google's [ATLAS v1.0](https://arxiv.org/abs/2608.00038) is not 15 million — it's 21.

Observed AI usage spans roughly 68% of detailed occupations, representing 88.4% of total US employment. But among occupations where ATLAS observes meaningful AI activity, the median occupation shows usage across only about **21% of its constituent tasks**. Only around 3% of occupations show observed AI activity across more than three-quarters of their tasks.

That produces an important distinction:

**AI has broad occupational reach without equivalent workflow depth.**

And where AI does appear, it is not predominantly replacing an entire task. Usage clusters around Partial Drafting and Generation, Review and Refinement, Ideation and Strategy, and Information Retrieval and Learning.

For non-routine cognitive work — which accounts for roughly 65% of observed work-related interactions despite representing only about 35% of professional tasks — end-to-end automation intent represents less than 10% of conversations.

But that headline hides an important boundary.

> **The <10% automation figure is not economy-wide.** ATLAS's classification shows end-to-end automation intent at roughly 27% for routine cognitive interactions, versus about 6.5% for non-routine cognitive work.

The distinction matters enormously for workforce risk. Codifiable, rules-based cognitive tasks already show materially more automation intent than complex non-routine work.

ATLAS therefore describes something more nuanced than either "AI is automating jobs" or "AI is merely assisting workers." **The execution mode depends heavily on the structure of the task.**

## 📐 Comparing ATLAS to Anthropic's Economic Index

Anthropic's Economic Index provides the closest large-scale comparison, but the numbers should not be treated as directly interchangeable.

| Dimension | Google ATLAS v1.0 | Anthropic Economic Index |
|---|---|---|
| Sample size | ~14.7M interactions | >4M conversations in early reports |
| Occupational breadth | ~68% of occupations show meaningful observed use | 36% showed use across ≥25% of tasks in original study |
| Task depth | Median covered occupation: ~21% | 49% reach ≥25% when observations are pooled across reports |
| Automation signal | <10% end-to-end automation intent in non-routine cognitive interactions | 43% automation classification in original Claude.ai study |
| Scope | Gemini App, AI Mode, API | Claude.ai + first-party API |

Anthropic originally found that 36% of occupations saw Claude used across at least a quarter of their tasks. Pooling observations across subsequent Economic Index reports raises that figure to 49%.

But Google's <10% automation number and Anthropic's 43% should **not** be read as evidence that Gemini is less automation-oriented than Claude. They use different automation taxonomies, populations, interfaces, and denominators.

Anthropic itself demonstrates why interface matters: its later Economic Index work finds substantially higher automation rates in first-party API usage than in Claude.ai. Agentic environments such as Claude Code have likewise shown much higher automation classifications than ordinary conversational use.

The directional convergence is therefore narrower but still important: **both datasets show broad AI diffusion combined with highly uneven depth and execution patterns.**

Both also share a critical limitation. They observe interactions, not the ultimate productive output the user is trying to achieve — and not whether AI actually made that output better.

## 💼 What This Means for Deployment Strategy

### AI adoption needs a better denominator

Enterprise AI programs still frequently report adoption through metrics such as licenses deployed, monthly active users, prompt volume, or percentage of employees using AI.

ATLAS shows why those numbers can be deeply misleading.

Imagine two organizations:

```text
Company A
80% of employees exposed → 20% of tasks touched → 5% delegated end-to-end

Company B
40% of employees exposed → 60% of tasks touched → 35% delegated end-to-end
```

A conventional adoption dashboard might conclude that Company A is further along.

Operationally, Company B may be undergoing the much larger transformation.

**The unit of AI adoption is increasingly the task, not the user.**

A more useful enterprise measurement stack is therefore:

```text
Occupational Breadth
        ↓
Task Penetration
        ↓
Execution Mode
Assist ↔ Automate
        ↓
Realized Outcome
```

That shift matters simultaneously for ROI, workforce planning, and governance.

### ROI depends on which tasks AI touches

Only 46% of AI initiatives launched in the prior year were assessed as on track to achieve positive ROI within 12 months, while 37% were considered operational and delivering business value.

ATLAS offers one structural explanation for why enterprise value may diffuse more slowly than adoption headlines imply. If AI reaches many workers but touches only selected tasks within their workflows, the economic impact depends not simply on penetration but on **which tasks are affected, how important and time-consuming they are, and whether AI actually improves their execution**.

A 21% task-penetration rate does not imply a 21% productivity impact. Automating one critical bottleneck may generate more value than assisting ten peripheral activities.

That is precisely why task-level measurement matters.

### Workforce exposure is not the same as displacement

ATLAS suggests higher-wage workers may automate routine cognitive activities while collaborating with AI on more complex non-routine work — a pattern Google notes could contribute to deeper wage inequality.

The immediate workforce signal is therefore not wholesale occupational displacement, but **uneven task transformation**: some activities are delegated, others augmented, and still others largely untouched.

But "shallow" should not be confused with a technological ceiling.

ATLAS is a two-week snapshot of usage in April 2026. More embedded and agentic interfaces can produce very different behavior, as Anthropic's API and Claude Code data already suggest.

**ATLAS describes today's adoption frontier, not the ultimate automation frontier.**

That distinction should matter to workforce-risk models.

## 🏢 What ATLAS Doesn't See

The dataset excludes Google Workspace, Google Translate, AI Overviews, Gemini for Google Cloud, and Gemini Enterprise.

That is not a minor sampling footnote.

It means ATLAS does not observe a major class of embedded enterprise workflows — precisely the environments where AI may be integrated directly into documents, software development, customer operations, analytics, and business processes.

Those environments could exhibit materially different task penetration and automation patterns.

So the 21% figure should not become another universal benchmark. It is a behavioral baseline for the surfaces ATLAS observes.

## 🔬 OCTO as a Measurement Template

The methodological contribution may ultimately outlast the headline statistics.

OCTO itself is Google's infrastructure and is not directly replicable by most enterprises. But the measurement architecture is:

```text
Interaction Logs
      ↓
Business Tasks
      ↓
Workflow Penetration
      ↓
Augmentation / Automation
      ↓
Outcomes
```

That creates an interesting connection to the [Agent Benchmark Scores Are Lying to You](https://minwu-ai.github.io/agent-benchmark-scores-are-lying-to-you-and-log-analysis-is-/) problem.

ATLAS analyzes interaction traces rather than agent execution traces, so the two are not technically identical. But the conceptual overlap is important: **both treat behavioral traces rather than benchmark scores or adoption counts as the unit of evidence.**

For agentic systems, the same measurement philosophy can extend further — from conversations into tool calls, intermediate actions, retries, permissions, state transitions, and environmental effects.

That suggests a broader enterprise measurement framework:

**Don't ask only who has access to AI. Measure what AI actually does inside the workflow.**

ATLAS v1.0 is one of the strongest large-scale behavioral baselines yet available for doing exactly that.

It does not show that AI will not automate jobs. Nor does it prove that shallow adoption explains disappointing enterprise ROI.

It shows something more immediately useful: **AI diffusion is occurring task by task, unevenly inside occupations, and predominantly through collaboration rather than end-to-end delegation — at least for now.**

For enterprises, that makes "How many people use AI?" increasingly the wrong question.

The better questions are: **Which tasks? How deeply? In what execution mode? And with what outcome?**
