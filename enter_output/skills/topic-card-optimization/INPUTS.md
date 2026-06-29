# Stage 5 Inputs - topic-card-optimization

## Agent prompt packet

### Role prompt

You are the Stage 5 topic-card-optimization generator worker. Score every passed card for
viral potential inside the safety guardrails, choose the strongest diverse Top-N, create API
supplemental notes, generate drafts, and write a complete `viral_intent` handoff for Stage 6.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/topic-card-optimization/SKILL.md`
6. `workspace:reddit/接口test/帖子native化/评价体系.md`
7. `workspace:reddit/提示词/爆帖拆解复刻提示词.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.topic-card-optimization.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:04_screen/handoff_packet.json`
- `run:04_screen/passed_cards.json`
- `run:04_screen/screening.md`
- `run:03_search/occupancy_heat_evidence.json`
- `run:03_search/run_meta.json`
- `run:03_search/topic_cards/{direction_id}.json` only for passed `topic_id` values.
- `run:02_topics/topics.md` only for the originating topic anchor.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/topic-card-optimization/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/topic-card-optimization/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/topic-card-optimization/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- None by default. Do not open all cards or unpassed card files unless the Stage 4 handoff specifically names them.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `04_screen/handoff_packet.json`
- `04_screen/passed_cards.json`
- `04_screen/screening.md`
- `03_search/occupancy_heat_evidence.json`
- `03_search/run_meta.json`
- `03_search/topic_cards/{direction_id}.json` only for passed `topic_id` values.
- `02_topics/topics.md` only for the originating topic anchor.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the orchestrator passes a retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- Full product brief when compressed global files are sufficient.
- All topic cards when only passed cards are needed.
- Stage 6/7 final posts, Feishu docs, image prompts, or formatting reports.
