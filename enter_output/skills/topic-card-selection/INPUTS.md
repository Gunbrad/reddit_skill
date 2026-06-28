# Stage 4 Inputs - topic-card-selection

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `03_search/handoff_packet.json`
- `03_search/run_meta.json`
- `03_search/maps/{direction_id}.md`
- `03_search/maps/{direction_id}.json`
- `03_search/topic_cards/{direction_id}.json`
- `03_search/topic_cards/{direction_id}.md` only when the JSON card file lacks required text.
- `03_search/occupancy_heat_evidence.json` for moderation and community-risk clues.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps beyond the current Stage 3 artifacts whitelisted above.
- Full product brief when compressed global files are sufficient.
- Stage 5 optimized notes or drafts.
- Stage 6/7 final posts, Feishu docs, image prompts, or formatting reports.
