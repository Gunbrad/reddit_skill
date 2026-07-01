# Stage 2 Inputs - community-capture

## Agent prompt packet

### Role prompt

You are the Stage 2 community-capture generator worker. Configure the SmartContent community
builder project, start the long crawl, poll with heartbeat evidence, download artifacts, and
record successful and failed communities. Do not补抓 failed subreddits.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`
6. `repo:subreddit_build/skills/community-capture/SKILL.md`
7. `workspace:reddit/接口test/新工作流接口测试/smartcontent_社区建设功能_API接口文档.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.community-capture.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:01_product_brief/handoff_packet.json`
- `run:01_product_brief/product_brief.md`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/community-capture/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/community-capture/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/community-capture/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live SmartContent responses for the current project/run only.
- Download URLs returned by current run artifact endpoints.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `01_product_brief/handoff_packet.json`
- `01_product_brief/product_brief.md`
- Files created under `02_community_capture/` for this run.

## Forbidden files

- Full prior conversation history.
- Old run folders and old SmartContent artifacts.
- Feishu docs from unrelated runs.
- Raw Reddit dumps outside this run.
- Topic Cards, mechanism variants, drafts, or optimized posts from later stages.
- API cookies, passwords, and other secrets in any file.
