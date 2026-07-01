---
name: community-card-draft-generation
description: Use after mechanism variants are applied, when choosing TopN Topic Cards, writing per-card supplemental contexts that copy the original topic direction and add suitable notes, selecting draft length, creating SmartContent draft jobs, and handing drafts to native rewrite. Stage 5 of the subreddit build workflow.
---

# Community Card Draft Generation (Stage 5)

## Overview

Rank applied Topic Cards, choose TopN, write a per-card `supplemental_context`, choose length,
create the SmartContent draft job, wait for completion, and save drafts for native rewrite.

**Core principle:** the supplemental context is the bridge between the chosen Topic Card and
the final post. It must copy the original topic direction, then add targeted instructions that
fit that card's mechanism, source posts, subreddit, brand boundary, and risk profile.

## Inputs

- Stage 4 handoff with applied mechanisms.
- Stage 3 Topic Cards and reference post cards.
- `run_config.top_n` or user-selected TopN.
- `run_config.draft_length` or `run_config.draft_length_multiplier`.
- Global fact and brand files.

## Required Output

Write to `05_optimized_cards/`:

- `optimization.md` - ranking, TopN, supplemental contexts, length choices, draft job ids.
- `draft_jobs_receipt.json` - job id, status, requested ids, completed ids, errors.
- `drafts_md/{post_id}.md` - one markdown file per generated draft.
- `handoff_packet.json` - per-post viral intent and preservation requirements for Stage 6a.

## Supplemental Context Format

Each selected card's note must contain:

1. `原选题方向（复制自选题卡，供参考，不必逐字一致，但不要偏移该方向）：...`
2. `机制选择：...` summarizing the applied mechanism and why it was selected.
3. `写作补充：...` with concrete scene, emotional trigger, and comment engine.
4. `品牌露出边界：...` with verified claims only and light mention.
5. `风险与素材：...` including required placeholders and no-fabrication rule.

## Length Map

| UI | multiplier |
|---|:---:|
| 更短 | 0.3 |
| 稍短 | 0.5 |
| 默认 | 1 |
| 稍长 | 1.8 |
| 更长 | 2.5 |

Use the user value when provided. If not provided, prefer 稍短/默认 unless the chosen card truly
needs a detailed walkthrough.

## Process

1. Load applied cards, reference post cards, content maps, fact index, and brand rules.
2. Rank all applied cards by production safety and viral potential.
3. Select TopN with diversity across subreddits, content forms, and hooks.
4. Write supplemental context for every selected card using the required format.
5. Create one draft job with selected topic ids and `topic_supplemental_contexts`, or split jobs
   only if the API requires it.
6. Poll draft job until completed/failed/deadline. Save each draft.
7. Build `handoff_packet.json` with `viral_intent`, `topic_anchor`, selected mechanism, length,
   allowed/forbidden claim ids, and draft paths.

## Common Mistakes

- Writing generic supplemental notes like "make it viral".
- Forgetting to copy the original topic direction into the note.
- Choosing only the safest cards instead of TopN with breakout potential.
- Maxing length without a reason.
- Handing drafts to native rewrite without structured viral intent.
