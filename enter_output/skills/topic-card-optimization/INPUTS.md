# Stage 5 Inputs - topic-card-optimization

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `04_screen/handoff_packet.json`
- `04_screen/passed_cards.json`
- `04_screen/screening.md`
- `03_search/occupancy_heat_evidence.json`
- `03_search/run_meta.json`
- `03_search/topic_cards/{direction_id}.json` only for passed `topic_id` values.
- `02_topics/topics.md` only for the originating topic anchor.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the orchestrator passes a retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- Full product brief when compressed global files are sufficient.
- All topic cards when only passed cards are needed.
- Stage 6/7 final posts, Feishu docs, image prompts, or formatting reports.
