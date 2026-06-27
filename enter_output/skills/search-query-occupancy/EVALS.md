# EVALS — Search Queries + Directions + Topic Cards (Stage 3)

Three sub-gates: (A) queries before running the API, (B) chosen directions after maps,
(C) Topic Cards after generation. **Blocking** must pass at each gate.

## Gate A — Query quality (before API run). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| A1 | Long-tail, not broad | ✅ | Each query is a multi-word intent phrase mapping to a real scenario/pain; reject single broad keywords ("AI app builder") |
| A2 | 2 queries per 选题 | ✅ | Each 选题 yields exactly 2 queries with distinct angles |
| A3 | Derived from 选题, not invented | ✅ | Each query traces to a 选题's pain/narrative; no off-topic queries |
| A4 | Semantic alignment | ⬜ | Query words match how a real user would search at that stage |
| A5 | 长尾理由 recorded | ⬜ | search_queries.md notes why each query is long-tail |

## Gate B — Direction selection (after maps). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| B1 | Only success directions | ✅ | Chosen directions have `status: success` and `map_md/map_json: true` (NOT just run succeeded) |
| B2 | Exactly 3, mutually exclusive | ✅ | 3 directions whose maps cover non-overlapping subreddits/title-patterns/semantics |
| B3 | Coverage breadth | ⬜ | The 3 together span distinct pains, not 3 flavors of one |
| B4 | Map quality usable | ⬜ | Each chosen map has a populated 社区分布 + 标题规律 (not empty/degenerate) |

Mutual-exclusivity check: compare each pair's `subreddit_distribution`,
`common_title_structures`, and `high_frequency_semantic_phrases`. If two directions share
most subreddits AND title structures, they overlap → pick a different pair.

## Gate C — Topic Cards (after generation). Threshold: all blocking pass.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| C1 | 12 cards per chosen direction | ✅ | 36 total across 3 directions |
| C2 | Each card has required fields | ✅ | title_direction, content_form, post_format, expression_mechanism, brand_exposure_method, target_subreddit present |
| C3 | Brand exposure not an ad | ⬜ | brand_exposure_method surfaces product naturally, tied to a verified capability |
| C4 | Cards within a direction are varied | ⬜ | Not 12 near-duplicates; varied content forms / angles |

## Failure → action

- Gate A fail → rewrite queries before calling the API (saves a 10-min run).
- Gate B fail → re-pick from success directions; if <3 succeeded, re-run weak directions.
- Gate C fail → regenerate cards (overwrite:true) with a sharper supplemental_context.
- Record all three gate verdicts + run_id in `run_meta.json`/`run_manifest.md`.

## Reviewer prompt (optional subagent)

"Read search_queries.md and the 3 chosen maps. (A) Is each query genuinely long-tail
intent, not a broad keyword? (B) Do any two chosen directions share most subreddits AND
title structures (i.e. they overlap)? (C) Are there 12 varied cards per direction with all
required fields and non-ad brand exposure? List every violation."
