# EVALS - Mechanism Variant Selection (Stage 4)

Run by a separate evaluator worker. The evaluator receives `mechanism_selection.md`,
`variant_history.json`, `applied_variants.json`, Stage 3 Topic Cards, this file, and schemas.

## Gate A - Coverage And API State

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| A1 | Every Topic Card processed | ✅ | Every `topic_id` in `03_topic_retrieval/topic_cards.json` has one generated batch |
| A2 | Variant count | ✅ | Each processed card has exactly 8 generated variants or a recorded API failure that blocks handoff |
| A3 | Apply endpoint called | ✅ | Every selected variant has `applied=true` and an active/applied variant id |
| A4 | API ids traceable | ⬜ | `project_id`, `run_id`, `round_id`, `topic_id`, `batch_id`, `variant_id` are recorded |

## Gate B - Selection Quality

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| B1 | Better than original | ✅ | Selected variant improves hook/comment engine/community fit or lowers ad risk versus original |
| B2 | Topic preserved | ✅ | Selected mechanism does not change the core title direction or source-card logic |
| B3 | Brand natural | ✅ | Brand exposure is natural, light, and tied to verified capability; no feature dump |
| B4 | No fabricated material | ✅ | If extra material is needed, required material is explicit; no fake screenshots/data/reviews implied |
| B5 | Rationale concrete | ⬜ | Selection rationale cites specific mechanism qualities, not "best one" |

## Failure -> action

- A1/A2/A3 fail -> complete missing generation/apply or stop with explicit blocker.
- B fail -> choose a safer/better variant or regenerate one batch for the affected card.

## Reviewer prompt (MANDATORY evaluator worker)

"Review Stage 4 mechanism selection. Did every Topic Card receive exactly 8 mechanism variants,
and was exactly one best variant applied? Does each selected mechanism improve Reddit-native
discussion potential while preserving the original topic and avoiding ad/AI flavor,
unverified claims, and fabricated materials? List each blocking violation by topic_id."
