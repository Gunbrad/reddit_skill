# Eval Report: Search Occupancy

- Artifact: `03_search_occupancy/search_queries.md`
- Evaluated At: 2026-06-27T01:08:00+08:00
- Result: PASS
- Score: 94/100

## Hard Gates

| Gate | Result | Evidence | Required Fix |
| --- | --- | --- | --- |
| Query count | PASS | Three source topics x two queries = six directions. | None. |
| Query quality | PASS | Queries are English, long-tail, non-brand, and intent-based. | None. |
| API proof | PASS | Login succeeded with user credentials; SmartContent run `20260627_002723_search` completed. | None. |
| Direction-level success | PASS | `search_occupancy_map_summary` reports all six directions with `status=success`, `map_md=true`, `map_json=true`. | None. |
| Three distinct directions | PASS | Selected `direction_002`, `direction_003`, `direction_006`; `001` overlaps `002`, `004` is thin, `005` overlaps `006`. | None. |
| Topic cards generated | PASS | 12 Topic Cards downloaded for each selected direction. | None. |

## Weighted Rubric

| Criterion | Weight | Score | Evidence | Required Fix |
| --- | ---: | ---: | --- | --- |
| Query specificity | 15 | 14 | Queries contain roles/data isolation, code export/handoff, and prompt drift/codebase maintenance contexts. | None. |
| Query diversity | 15 | 14 | Six directions cover three distinct search-intent families. | None. |
| Search-result relevance | 15 | 13 | Selected directions returned usable Reddit maps with relevant subreddits and source cards. | None. |
| Map usability | 15 | 14 | Direction maps and raw post assets were downloaded locally for all six directions. | None. |
| Direction selection logic | 20 | 19 | Selected directions are mutually distinct and aligned with Topic Plan. | None. |
| Artifact completeness | 10 | 10 | Query doc, run config, run status/meta, direction maps, URLs, raw posts, post cards, and topic cards are saved. | None. |
| Failure handling | 10 | 10 | Initial cookie failure was handled by verified login; thin/overlapping directions were dropped. | None. |

## Revision Log

- Attempt 1: Query set passed local checks but API was blocked by missing/invalid auth.
- Attempt 2: Auth succeeded via login; SmartContent run completed; direction artifacts and topic cards were downloaded.

## Handoff Notes

- Preserved facts: use only verified Enter Pro / Enter Cloud / Enter Code capabilities from `01_product_brief/product_brief.md`.
- Blockers: none for downstream card selection.
- Next-step inputs: selected direction topic cards under `03_search_occupancy/directions/{direction_id}/topic_cards.md`.

