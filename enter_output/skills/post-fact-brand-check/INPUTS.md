# Stage 6b Inputs - post-fact-brand-check

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/native_posts.md`
- `06_optimized/6a_handoff_packet.json` if written by 6a.
- `enter_output/skills/post-fact-brand-check/EVALS.md`
- `enter_output/skills/post-fact-brand-check/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-fact-brand-check/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 6c/6d artifacts before they are approved.
