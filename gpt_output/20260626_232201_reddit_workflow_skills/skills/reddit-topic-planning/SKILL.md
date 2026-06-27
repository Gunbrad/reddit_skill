---
name: reddit-topic-planning
description: Use when a factual product brief exists and Codex must create Reddit topic directions, narrative angles, materials, brand exposure rules, selection rationale, local topic plan, and a Feishu document for client review.
---

# Reddit Topic Planning

## Purpose

Turn the product brief into Reddit-native topic directions. A good topic is not a slogan; it is a believable discussion, teardown, question, story, comparison, or troubleshooting angle that can earn attention while preserving product facts.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/output-templates.md`
- `../../shared/eval-loop.md`
- `../../evals/02-topic-planning-eval.md`

## Inputs

- `01_product_brief/product_brief.md`
- Client priorities or campaign goals.
- Desired number of topics. If absent, create 6-10 topics.
- Brand exposure preference: no mention, soft mention, explicit disclosure, comparison, or product-led.

## Workflow

1. Load the product brief and fact bank.
2. Identify topic territories from:
   - User pain.
   - Product differentiators.
   - Competitor gaps.
   - Reddit search intent.
   - Materials the client can actually provide.
3. Draft topics with mutually distinct purposes. Avoid producing many versions of the same angle.
4. For each topic, define:
   - Content type.
   - Narrative.
   - Materials or research needed.
   - Brand exposure method.
   - Target communities.
   - Search intent.
   - Why this direction is worth pursuing.
   - Product facts to preserve.
   - Risk and compliance notes.
5. Create local artifact `02_topic_plan/topic_plan.md`.
6. Create a Feishu cloud document containing the topic plan using the available Feishu document capability or `lark-cli`.
7. Save the Feishu title, URL, and token in `manifest.json`.
8. Run the paired eval and revise until it passes.

## Feishu Handoff Rules

- The Feishu document must contain the same topics as the local Markdown.
- The local Markdown remains the source of record.
- If Feishu creation fails, keep the local Markdown, mark the Feishu handoff as blocked in the eval report, and do not pretend a document exists.

## Output Contract

Save:

- `02_topic_plan/topic_plan.md`
- `eval_reports/02_topic_planning_eval.md`
- Updated `manifest.json`

Each topic must include:

- `Content Type`
- `Narrative`
- `Materials / Research Needed`
- `Brand Exposure`
- `Target Communities`
- `Search Intent`
- `Why This Direction`
- `Product Facts To Preserve`
- `Risk / Compliance Notes`

## Topic Design Rules

- Start from a user situation, not a product feature.
- Make the topic discussable even if the brand mention is removed.
- Avoid "best tool", fake review, fake revenue, and unsupported benchmark framing.
- Prefer trade-offs, questions, post-mortems, teardown, setup walkthrough, or comparison language.
- Include only materials the client can provide or that can be ethically created.
- Make brand exposure natural: first-person usage, disclosed comparison, tool-stack mention, or late-stage solution note.

## Handoff

Hand off:

- Topic plan path.
- Feishu topic doc URL/token.
- Eval report path.
- Topics approved for search query generation.
- Topics rejected or needing client confirmation.
