# Stage 6 Inputs - post-optimization

## Agent prompt packet

### Role prompt

You are the Stage 6 post-optimization coordinator worker. Do not rewrite posts yourself.
Build sub-stage prompt packets for 6a-6d, launch isolated generator and evaluator workers,
record verdicts, and promote only approved artifacts.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/EVAL_WORKER_CONTRACT.md`
5. `repo:subreddit_build/skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`
6. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
7. `repo:subreddit_build/skills/post-optimization/SKILL.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.post-optimization.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:05_optimized_cards/handoff_packet.json`
- `run:05_optimized_cards/drafts_md/{post_id}.md` for chosen posts only.
- Approved 6a-6d artifacts after each sub-stage passes.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files for the current sub-stage only.
4. The target sub-stage `INPUTS.md`, `SKILL.md`, schemas, and `EVALS.md`.
5. `repo:subreddit_build/skills/post-optimization/OUTPUT_SCHEMA.json`
6. `repo:subreddit_build/skills/post-optimization/HANDOFF_SCHEMA.json`
7. `repo:subreddit_build/skills/post-optimization/EVALS.md` for coordinator self-check only.

### Allowed extra reads

- Stage 6 sub-stage files (`post-native-rewrite`, `post-fact-brand-check`, `post-subreddit-image`, `post-feishu-publish`) as needed to build their prompt packets.
- Do not read creative prompt files directly unless a sub-stage `INPUTS.md` or `run_config.prompt_packs` assigns them to that sub-stage.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.
- `subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
- `subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
- `subreddit_build/skills/subreddit-build-workflow/EVAL_WORKER_CONTRACT.md`

## Allowed stage files

- `05_optimized_cards/handoff_packet.json`
- `05_optimized_cards/drafts_md/{post_id}.md` for chosen posts only.
- `06_optimized/native_posts.md` after sub-stage 6a passes.
- `06_optimized/checked_posts.md` after sub-stage 6b passes.
- `06_optimized/final_posts.md` after sub-stage 6c passes.
- `06_optimized/images/prompts.md` and `06_optimized/images/{post_id}.png` after image packaging.
- `03_topic_retrieval/topic_cards.md` and `03_topic_retrieval/feishu_links.md` only for 6d Feishu deliverable checks.

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
- Stage 2 community artifacts including `community_insights.json`; Stage 5 handoff already carries compressed per-post community context.

