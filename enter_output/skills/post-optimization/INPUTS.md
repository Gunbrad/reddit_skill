# Stage 6 Inputs - post-optimization

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.
- `enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
- `enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
- `enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`

## Allowed stage files

- `05_optimized_cards/handoff_packet.json`
- `05_optimized_cards/drafts_md/{post_id}.md` for chosen posts only.
- `06_optimized/native_posts.md` after sub-stage 6a passes.
- `06_optimized/checked_posts.md` after sub-stage 6b passes.
- `06_optimized/final_posts.md` after sub-stage 6c passes.
- `06_optimized/images/prompts.md` and `06_optimized/images/{post_id}.png` after image packaging.
- `02_topics/topics.md` and `02_topics/feishu_links.md` only for 6d Feishu deliverable checks.

## Forbidden files

- Full prior conversation history.
- Prior stage scratchpads or worker reasoning.
- Failed drafts unless the orchestrator passes a retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- Full product brief when compressed global files are sufficient.
- All topic cards when only selected drafts are needed.
- All drafts when only chosen post drafts are needed.
- Stage 7 formatting reports.
