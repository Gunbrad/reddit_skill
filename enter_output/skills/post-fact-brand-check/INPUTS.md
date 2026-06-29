# Stage 6b Inputs - post-fact-brand-check

## Agent prompt packet

### Role prompt

You are the Stage 6b post-fact-brand-check generator worker. Check every product claim and
brand mention in 6a output against the fact index and brand rules. Fix unsafe wording without
undoing the native voice.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/post-fact-brand-check/SKILL.md`
6. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.post-fact-brand-check.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:06_optimized/native_posts.md`
- `run:06_optimized/6a_handoff_packet.json` if written by 6a.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/post-fact-brand-check/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/post-fact-brand-check/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/post-fact-brand-check/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- None by default. Do not read full product brief, Stage 5 raw cards, or later Stage 6 artifacts.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/native_posts.md`
- `06_optimized/6a_handoff_packet.json` if written by 6a.
- `enter_output/skills/post-fact-brand-check/EVALS.md`
- `enter_output/skills/post-fact-brand-check/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-fact-brand-check/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 6c/6d artifacts before they are approved.
