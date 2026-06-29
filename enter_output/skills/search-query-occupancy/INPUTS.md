# Stage 3 Inputs - search-query-occupancy

## Agent prompt packet

### Role prompt

You are the Stage 3 search-query-occupancy generator worker. Convert approved topics into
specific long-tail search queries, run the occupancy workflow, and emit search maps, topic
cards, and heat evidence without dropping any approved topic silently.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/search-query-occupancy/SKILL.md`
6. `repo:enter_output/skills/search-query-occupancy/api-reference.md`
7. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.search-query-occupancy.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:02_topics/handoff_packet.json`
- `run:02_topics/topics.md`
- `run:02_topics/feishu_links.md` for the topic doc URL only.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/search-query-occupancy/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/search-query-occupancy/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/search-query-occupancy/EVALS.md` for gate self-checks only; the generator cannot pass itself.

### Allowed extra reads

- `repo:enter_output/skills/search-query-occupancy/run_search_occupancy.py` when executing or inspecting the API runner.
- No prompt-folder browsing; extra prompt files must be listed in `run_config`.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `02_topics/handoff_packet.json`
- `02_topics/topics.md`
- `02_topics/feishu_links.md` for the topic doc URL only.
- `search-query-occupancy/api-reference.md`
- `search-query-occupancy/run_search_occupancy.py`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed query attempts unless the orchestrator passes a retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Full product brief when compressed global files are sufficient.
- Raw Reddit dumps not produced by the current Stage 3 workflow run.
- Stage 4/5 screening, optimization, and draft files.
- Stage 6/7 final posts, Feishu docs, image prompts, or formatting reports.
