# Stage 5 Inputs - community-card-draft-generation

## Agent prompt packet

### Role prompt

You are the Stage 5 community-card-draft-generation generator worker. Rank applied Topic Cards,
choose TopN, write per-card supplemental contexts that copy the original topic direction and
add suitable notes grounded in community insights, choose a job-level length multiplier, create
and poll draft jobs, save drafts, and write a structured viral-intent handoff for native rewrite.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`
6. `repo:subreddit_build/skills/community-card-draft-generation/SKILL.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.community-card-draft-generation.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:04_mechanism_selection/handoff_packet.json`
- `run:04_mechanism_selection/applied_variants.json`
- `run:04_mechanism_selection/mechanism_selection.md`
- `run:03_topic_retrieval/topic_cards.json`
- `run:03_topic_retrieval/reference_post_cards.json`
- `run:03_topic_retrieval/feishu_links.md`
- `run:02_community_capture/artifacts/content_maps.json`
- `run:02_community_capture/artifacts/community_insights.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/community-card-draft-generation/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/community-card-draft-generation/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/community-card-draft-generation/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live SmartContent draft job responses for the current `project_id/run_id/round_id`.
- Round downloads returned by current `/downloads`.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `04_mechanism_selection/handoff_packet.json`
- `04_mechanism_selection/applied_variants.json`
- `04_mechanism_selection/mechanism_selection.md`
- `03_topic_retrieval/topic_cards.json`
- `03_topic_retrieval/reference_post_cards.json`
- `03_topic_retrieval/feishu_links.md`
- `02_community_capture/artifacts/content_maps.json`
- `02_community_capture/artifacts/community_insights.json`
- Files created under `05_optimized_cards/`.

## Forbidden files

- Native rewrites, Feishu post docs, and formatting outputs from later stages.
- Old draft jobs from other runs.
- Full product brief unless required fact is absent from compressed files and the reason is logged.
- Secrets, cookies, or passwords.
