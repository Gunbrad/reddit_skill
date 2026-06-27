---
name: reddit-search-occupancy
description: Use when Reddit topic directions must become long-tail search queries, SmartContent search occupancy runs, downloaded search maps/materials, mutually distinct selected directions, and generated topic cards.
---

# Reddit Search Occupancy

## Purpose

Convert approved topics into long-tail Reddit search directions, run the SmartContent search occupancy workflow, download all direction artifacts, select three non-overlapping successful directions, and generate topic cards for each selected direction.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/output-templates.md`
- `../../shared/smartcontent-api-contract.md`
- `../../shared/eval-loop.md`
- `../../evals/03-search-occupancy-eval.md`

## Inputs

- `01_product_brief/product_brief.md`
- `02_topic_plan/topic_plan.md`
- Valid `planner_session` cookie for SmartContent.
- Posts per query. Default: 10.
- Topic-card count per selected direction. Default: 12.

## Workflow

1. Generate exactly two long-tail search queries per approved topic unless the user specifies another count.
2. Save all queries to `03_search_occupancy/search_queries.md`.
3. Evaluate query quality before API calls. Revise weak queries first.
4. Authenticate with SmartContent.
5. Create or reuse the SmartContent project using the full product brief.
6. Create a search occupancy run with `posts_per_query` and the selected search directions.
7. Start `prepare-all`.
8. Poll until the run reaches a terminal state.
9. Inspect direction-level map status. Do not rely only on run-level success.
10. Download for every successful direction:
    - Search URL JSON and MD.
    - Raw posts MD.
    - Post Cards JSONL.
    - Search occupancy map JSON and MD.
11. Save each direction under `03_search_occupancy/directions/{direction_id}/`.
12. Select exactly three successful directions that are mutually distinct:
    - Different search intent.
    - Different community mix or audience.
    - Different narrative mechanism.
    - Different downstream post opportunity.
13. Generate 12 topic cards for each selected direction.
14. Download and save each selected direction's `topic_cards.md`.
15. Update `manifest.json` with `project_id`, `run_id`, selected directions, and artifact paths.
16. Run the paired eval and revise/rerun until it passes.

## Query Rules

Good queries:

- Are English, Reddit-search-friendly, and 4-10 meaningful terms.
- Contain the user pain, context, and category language.
- Avoid brand terms unless the topic is explicitly brand comparison or brand reputation.
- Avoid generic single-intent phrases like `best software`.
- Avoid duplicate intent across the two queries for one topic.
- Include community-native vocabulary when available.

Bad queries:

- Product slogans.
- Overly broad category names.
- Keyword stuffing.
- Queries that only match ads or SEO articles.
- Queries with unsupported claims.

## Direction Selection Rules

Pick three directions only after reading the maps. A direction is eligible when:

- Direction-level status is success.
- Map MD and JSON exist.
- Source posts are relevant to the product's messaging territory.
- Subreddit distribution is not entirely off-market.
- Title/content patterns are reusable.
- The direction does not substantially duplicate another selected direction.

If fewer than three eligible directions exist, revise queries and rerun before generating topic cards.

## Output Contract

Save:

- `03_search_occupancy/search_queries.md`
- `03_search_occupancy/directions/{direction_id}/search_urls.json`
- `03_search_occupancy/directions/{direction_id}/search_urls.md`
- `03_search_occupancy/directions/{direction_id}/raw_posts.md`
- `03_search_occupancy/directions/{direction_id}/post_cards.jsonl`
- `03_search_occupancy/directions/{direction_id}/search_occupancy_map.json`
- `03_search_occupancy/directions/{direction_id}/search_occupancy_map.md`
- `03_search_occupancy/directions/{direction_id}/topic_cards.md`
- `eval_reports/03_search_occupancy_eval.md`

## Handoff

Hand off:

- Product brief path.
- Topic plan path.
- Search query document.
- Three selected direction IDs.
- Topic card MD paths.
- Direction-level issues and dropped directions.
