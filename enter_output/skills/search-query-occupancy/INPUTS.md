# Stage 3 Inputs - search-query-occupancy

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
