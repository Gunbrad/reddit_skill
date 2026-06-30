# Stage 6a Inputs - post-native-rewrite

## Agent prompt packet

### Role prompt

You are the Stage 6a post-native-rewrite generator worker. Rewrite chosen drafts into
Reddit-native Title, Body, and comment designs while preserving every Stage-5 `viral_intent`
field. Native but flattened is a failure.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/post-native-rewrite/SKILL.md`
6. `workspace:reddit/提示词/reddit_帖子文档改写通用提示词.md`
7. `workspace:reddit/提示词/爆帖拆解复刻提示词.md`
8. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.post-native-rewrite.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:05_optimized_cards/handoff_packet.json`
- `run:05_optimized_cards/drafts_md/{post_id}.md` for chosen posts named in the Stage 5 handoff.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Ad-hoc single-stage input files

When `run_config.single_stage_mode` is true, the runtime may replace the Stage 5 handoff
and draft inputs with one current-run source artifact:

- `run:input/source_post.md` for inline or provided Reddit post text.
- `run:input/source_doc.md` after a Feishu URL has been fetched by the host action.

The generator must normalize the ad-hoc source into canonical Stage 6a output,
especially `06_optimized/native_posts.md` and `06_optimized/6a_handoff_packet.json`.

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/post-native-rewrite/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/post-native-rewrite/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/post-native-rewrite/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- None by default. Do not open Stage 3 maps, Stage 4 screening detail, all topic cards, or unchosen drafts.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `05_optimized_cards/handoff_packet.json`
- `05_optimized_cards/drafts_md/{post_id}.md` for chosen posts named in the Stage 5 handoff.
- `input/source_post.md` only in ad-hoc native-rewrite runs.
- `input/source_doc.md` only after current-run Feishu ingest.
- `enter_output/skills/post-native-rewrite/EVALS.md`
- `enter_output/skills/post-native-rewrite/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-native-rewrite/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- All topic cards when only chosen drafts are needed.
- All drafts when only selected `post_id` drafts are needed.
- Stage 6b/6c/6d artifacts before they are approved.
