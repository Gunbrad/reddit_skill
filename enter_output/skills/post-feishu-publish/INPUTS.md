# Stage 6d Inputs - post-feishu-publish

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/final_posts.md`
- `06_optimized/images/prompts.md` when images or pending prompts exist.
- `06_optimized/images/{post_id}.png` when generated images exist.
- `06_optimized/6c_handoff_packet.json` if written by 6c.
- `02_topics/topics.md`
- `02_topics/feishu_links.md`
- `enter_output/skills/post-feishu-publish/EVALS.md`
- `enter_output/skills/post-feishu-publish/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-feishu-publish/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs not linked by the current run.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 7 formatting reports.
- API keys, cookies, or other secrets in any file.
