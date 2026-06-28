# Stage 6c Inputs - post-subreddit-image

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/checked_posts.md`
- `06_optimized/6b_handoff_packet.json` if written by 6b.
- `enter_output/skills/post-subreddit-image/EVALS.md`
- `enter_output/skills/post-subreddit-image/IMAGE_PROMPT_EVALS.md`
- `enter_output/skills/post-subreddit-image/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-subreddit-image/HANDOFF_SCHEMA.json`
- Image API reference supplied for the current run, with credentials from environment only.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 6d Feishu docs before they are created by 6d.
