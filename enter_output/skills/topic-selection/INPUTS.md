# Stage 2 Inputs - topic-selection

## Agent prompt packet

### Role prompt

You are the Stage 2 topic-selection generator worker. Create distinct Reddit-native topic
directions grounded in user pain, verified Enter capabilities, and low-risk brand exposure.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/topic-selection/SKILL.md`
6. `workspace:reddit/接口test/帖子native化/评价体系.md`
7. `workspace:reddit/提示词/爆帖拆解复刻提示词.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.topic-selection.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:01_product_brief/handoff_packet.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`
- User-provided topics only when named in `run_config.topics` or `run_config.provided_artifacts.topics`.

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/topic-selection/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/topic-selection/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/topic-selection/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- `run:01_product_brief/product_brief.md` only when compressed global files lack a required persona, boundary, or differentiation detail. Log the exact reason in `run_manifest.md`.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `01_product_brief/handoff_packet.json`
- `01_product_brief/product_brief.md` only when the compressed fact index lacks a required persona, boundary, or differentiation detail. If read, log the exact reason in `run_manifest.md`.
- User-provided topics only when named in `run_config.topics` or `run_config.provided_artifacts.topics`.

## Forbidden files

- Full prior conversation history.
- Stage 1 scratchpads and raw research notes.
- Failed topic drafts unless explicitly needed for a retry report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- Full product brief when `global/product_fact_index.json` and `global/brand_safety_rules.md` are sufficient.
- Topic cards, screened cards, optimized drafts, or final posts from later stages.
