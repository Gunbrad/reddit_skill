# Stage 7 Inputs - feishu-formatting

## Allowed global files

- `run_config.json`
- `global/brand_safety_rules.md`
- `global/product_fact_index.json` only for brand-name and claim-boundary verification.

## Allowed stage files

- `06_optimized/handoff_packet.json`
- `06_optimized/feishu_links.md`
- The live Feishu post doc URL recorded in `06_optimized/feishu_links.md`.
- `06_optimized/final_posts.md` only to restore dropped title, subreddit, backup-title, body, comment, or resource blocks.
- `06_optimized/images/image_feishu.md` only when image anchors must be verified.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the orchestrator passes a retry failure report.
- Unrelated run folders.
- Old Feishu docs not linked by the current run.
- Raw Reddit dumps.
- Full product brief when compressed global files are sufficient.
- All topic cards.
- All drafts when `final_posts.md` and the live Feishu doc are sufficient.
