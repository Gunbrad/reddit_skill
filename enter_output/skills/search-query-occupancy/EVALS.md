# EVALS — Search Queries + Directions + Topic Cards (Stage 3)

Three sub-gates: (A) queries before running the API, (B) directions after maps,
(C) Topic Cards after generation. **Blocking** must pass at each gate.

## Gate A — Query quality (before API run). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| A1 | Long-tail, not broad | ✅ | Each query is a multi-word intent phrase mapping to a real scenario/pain; reject single broad keywords ("AI app builder") |
| A2 | Candidates then one chosen | ✅ | Each 选题 lists `queries_per_topic` (default 3) distinct candidates and marks exactly ONE chosen query |
| A3 | One direction per 选题 | ✅ | top `topic_count` 选题 (default 6) → ≤6 directions, each uniquely tied to a 选题 (recorded in topic_to_direction) |
| A4 | Derived from 选题, not invented | ✅ | Each query traces to its 选题's pain/narrative; no off-topic queries |
| A5 | Chosen beats the rest | ⬜ | search_queries.md notes why the chosen candidate wins on search-occupancy intent |
| A6 | 长尾理由 recorded | ⬜ | search_queries.md notes why each chosen query is long-tail |

## Gate B — Direction sanity (after maps). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| B1 | Only success directions proceed | ✅ | Cards generated only for directions with `status: success` and `map_md/map_json: true` |
| B2 | No 选题 silently dropped | ✅ | Every top-`topic_count` 选题 has a successful direction, or its direction was re-run/replaced (logged) |
| B3 | Map quality usable | ⬜ | Each map has a populated 社区分布 + 标题规律 (not empty/degenerate) |
| B4 | Coverage breadth | ⬜ | The directions span distinct pains (a natural result of distinct 选题) |

## Gate C — Topic Cards (after generation). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| C1 | Card count matches config | ✅ | `run_config.topic_card_count` cards per successful direction (default 12); no fixed total — depends on direction count |
| C2 | Each card has required fields | ✅ | title_direction, content_form, post_format, expression_mechanism, brand_exposure_method, target_subreddit present |
| C3 | Brand exposure not an ad | ⬜ | brand_exposure_method surfaces product naturally, tied to a verified capability |
| C4 | Cards within a direction are varied | ⬜ | Not near-duplicates; varied content forms / angles |

## Failure → action

- Gate A fail → rewrite/re-pick queries before calling the API (saves a 10-min run).
- Gate B fail → re-run or replace any direction whose map failed; don't drop its 选题.
- Gate C fail → regenerate cards (overwrite:true) with a sharper supplemental_context.
- Record all three gate verdicts + run_id in `run_meta.json`/`run_manifest.md`.

## Reviewer prompt (optional subagent)

"Read search_queries.md and the maps. (A) Does each 选题 list 3 candidate queries and pick the
best one, each genuinely long-tail intent (not a broad keyword), with ≤6 directions one per
选题? (B) Did any 选题 get silently dropped because its direction failed? (C) Are there
`topic_card_count` varied cards per direction with all required fields and non-ad brand
exposure? List every violation."
