# Stage 6a Inputs - post-native-rewrite

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `05_optimized_cards/handoff_packet.json`
- `05_optimized_cards/drafts_md/{post_id}.md` for chosen posts named in the Stage 5 handoff.
- `enter_output/skills/post-native-rewrite/EVALS.md`
- `enter_output/skills/post-native-rewrite/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-native-rewrite/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- All topic cards when only chosen drafts are needed.
- All drafts when only selected `post_id` drafts are needed.
- Stage 6b/6c/6d artifacts before they are approved.
