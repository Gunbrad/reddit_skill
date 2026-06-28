---
name: topic-selection
description: Use after a product brief exists and before generating search queries or posts, when deciding the content directions (选题) for Reddit posts, or when the user wants to lock down what posts to write and record them in Feishu. Stage 2 of the Reddit posting pipeline.
---

# Topic Selection (选题) → Feishu (Stage 2)

## Overview

Decide the **content directions** for the campaign before any search or drafting. A 选题 is
not a post — it's a brief that says: what content type, what narrative angle, what
material/research is needed, how the brand surfaces, and why this direction is worth it.
In stage 3 each 选题 yields `queries_per_topic` candidate long-tail queries (default 3); the
single best candidate is chosen as that 选题's one search direction.

**Core principle:** a good 选题 starts from a *real user pain or scenario*, not from a
product feature. The product appears as something a user stumbles onto while solving that
pain — never as the headline.

## When to use

- `product_brief.md` exists and passed stage-1 EVALS.
- You need to lock content directions and write them into a Feishu doc.

Not for: writing search queries (stage 3) or actual posts (stages 4-5).

## Inputs

Read only the files allowed by `INPUTS.md`. By default this stage uses
`global/product_fact_index.json`, `global/claim_boundary_table.json`, and
`global/brand_safety_rules.md` instead of the full product brief. Re-read
`01_product_brief/product_brief.md` only when the compressed files miss a required persona,
boundary, or differentiation detail, and log that reason in `run_manifest.md`.

- Run folder from orchestrator.
- `run_config.json` if present. **Skip auto-generation** when the user specified 选题
  (`run_config.topics` non-empty, or `2 in skip_stages` / `provided_artifacts.topics`):
  normalize them into the block format below and run EVALS — don't invent new ones. If
  auto-generating, use `run_config.topic_count` for how many to produce (else propose & confirm).

## Required output structure

Write to `02_topics/topics.md` (UTF-8). One block per 选题. Each block MUST have these
labeled fields (downstream stage 3 reads them to build queries):

```
主线N：{the strategic thread this 选题 reinforces}

N. {选题标题 / 一句话方向}
内容类型：{discussion / troubleshooting / experience recap / cost breakdown / ...}
叙事思路：{start from which user pain/scenario; how the story unfolds; where product enters}
素材/调研：{what material or research is needed; mark if client must supply}
品牌词露出：{how the brand surfaces naturally; what NOT to claim}
选择理由：{why this direction has search/purchase intent and low platform risk}
```

Produce enough 选题 to feed stage 3. Count = `run_config.topic_count` if set, else the
number the user wants; if unspecified, propose a set and confirm. Group them under 主线
(strategic threads) so directions don't overlap.

## After writing locally: write to Feishu

Use the `lark-doc` skill to create a new Feishu doc titled `{Product} - 选题 - {date}` and
write the 选题 content into it. Record the doc URL in `02_topics/feishu_links.md` and in
`run_manifest.md`. This is part of stage completion: do not mark stage 2 done or hand off with
the 选题 Feishu doc merely "deferred". (See conventions.md for Feishu rules — block-level,
never overclaim.)

## Process

1. Read the compressed global files: personas/pains if present, fact index, claim boundary,
   brand safety, and "不可说" features. Use the full brief only by the logged exception above.
2. For each persona/pain, draft a 选题 that leads with the pain, not the product.
3. Fill all 6 fields. For 品牌词露出, tie it to a specific verified capability; respect red lines.
4. Group 选题 under 主线 so they are mutually distinct (stage 3 needs non-overlapping directions).
5. Run EVALS (see EVALS.md). Revise until blocking criteria pass.
6. Create the Feishu doc; record links. Log manifest. Hand off to `search-query-occupancy`.

## Common mistakes

- Leading with the product instead of the user pain.
- 品牌词露出 written like a feature ad ("it has A, B, C and D").
- Overlapping 选题 that would generate near-identical search queries.
- Inventing material/data instead of marking "needs client material".
- Claiming an unverified ("不可说") feature from the brief.
