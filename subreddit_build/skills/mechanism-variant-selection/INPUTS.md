# Stage 4 Inputs - mechanism-variant-selection

## Agent prompt packet

### Role prompt

You are the Stage 4 mechanism-variant-selection generator worker. For every Topic Card,
generate 8 mechanism variants, select the best one using Reddit-native and brand-safety
criteria, apply it through the API, and write the full selection rationale.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`
6. `repo:subreddit_build/skills/mechanism-variant-selection/SKILL.md`
7. `workspace:reddit/接口test/新工作流接口测试/smartcontent_社区建设功能_API接口文档.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.mechanism-variant-selection.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:03_topic_retrieval/handoff_packet.json`
- `run:03_topic_retrieval/topic_cards.json`
- `run:03_topic_retrieval/reference_post_cards.json`
- `run:02_community_capture/artifacts/content_maps.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/mechanism-variant-selection/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/mechanism-variant-selection/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/mechanism-variant-selection/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live SmartContent mechanism variant responses for the current `project_id/run_id/round_id/topic_id`.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `03_topic_retrieval/handoff_packet.json`
- `03_topic_retrieval/topic_cards.json`
- `03_topic_retrieval/reference_post_cards.json`
- `02_community_capture/artifacts/content_maps.json`
- Files created under `04_mechanism_selection/`.

## Forbidden files

- Drafts, native posts, or final Feishu post docs.
- Old mechanism batches from another run.
- Full prior conversation history.
- Secrets or cookies in any file.
