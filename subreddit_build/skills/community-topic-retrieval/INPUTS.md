# Stage 3 Inputs - community-topic-retrieval

## Agent prompt packet

### Role prompt

You are the Stage 3 community-topic-retrieval generator worker. Create a semantic retrieval
round from the user's topic requirement, generate Topic Cards grounded in retrieved community
posts, and write the Topic Cards to a Feishu topic document.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`
6. `repo:subreddit_build/skills/community-topic-retrieval/SKILL.md`
7. `workspace:reddit/接口test/新工作流接口测试/smartcontent_社区建设功能_API接口文档.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.community-topic-retrieval.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:02_community_capture/handoff_packet.json`
- `run:02_community_capture/run_meta.json`
- `run:02_community_capture/artifacts/content_maps.json`
- `run:02_community_capture/artifacts/embeddings_status.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/community-topic-retrieval/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/community-topic-retrieval/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/community-topic-retrieval/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live SmartContent retrieval/topic-card responses for the current `project_id/run_id/round_id`.
- The Feishu topic doc created by this stage.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `02_community_capture/handoff_packet.json`
- `02_community_capture/run_meta.json`
- `02_community_capture/artifacts/content_maps.json`
- `02_community_capture/artifacts/embeddings_status.json`
- Files created under `03_topic_retrieval/`.

## Forbidden files

- Full product brief unless the fact index is missing a required capability and the read is logged.
- Old retrieval rounds from other runs.
- Later-stage mechanism variants, drafts, native posts, or Feishu post docs.
- Secrets, cookies, or passwords.
