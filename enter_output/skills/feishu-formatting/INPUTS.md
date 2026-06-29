# Stage 7 Inputs - feishu-formatting

## Agent prompt packet

### Role prompt

You are the Stage 7 feishu-formatting generator worker. Normalize the final Feishu post doc
layout, comments, brand highlighting, and permissions without rewriting the approved body or
title text.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/feishu-formatting/SKILL.md`
6. `workspace:reddit/提示词/改排版+评论内容.md`
7. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.feishu-formatting.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:06_optimized/handoff_packet.json`
- `run:06_optimized/feishu_links.md`
- The live Feishu post doc URL recorded in `run:06_optimized/feishu_links.md`.
- `run:06_optimized/final_posts.md` only to restore dropped approved blocks.
- `run:06_optimized/images/image_feishu.md` only when image anchors must be verified.
- `run:global/brand_safety_rules.md`
- `run:global/product_fact_index.json` only for brand-name and claim-boundary verification.

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/feishu-formatting/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/feishu-formatting/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/feishu-formatting/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live Feishu post doc detail for the current run.
- No old Feishu docs or unrelated Drive files.

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
