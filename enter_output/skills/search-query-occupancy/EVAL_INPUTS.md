# Eval Inputs - search-query-occupancy

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/search-query-occupancy/EVALS.md`
3. `repo:enter_output/skills/search-query-occupancy/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/search-query-occupancy/HANDOFF_SCHEMA.json`

### Business input files

- `run:03_search/search_queries.md`
- `run:03_search/run_meta.json`
- `run:03_search/occupancy_heat_evidence.json`
- `run:03_search/maps/{direction_id}.md`
- `run:03_search/maps/{direction_id}.json`
- `run:03_search/topic_cards/{direction_id}.json`
- `run:02_topics/handoff_packet.json`
- `run:02_topics/topics.md`
- `run:global/product_fact_index.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Artifact under review.
3. Minimal fact / brand context.
4. Stage-specific upstream context.

### Allowed extra reads

- None by default.

### Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless passed in retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps unless explicitly produced by current run and listed above.
- Stage 4, Stage 5, Stage 6, or Stage 7 artifacts.
