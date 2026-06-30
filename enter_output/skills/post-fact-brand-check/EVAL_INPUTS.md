# Eval Inputs - post-fact-brand-check

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/post-fact-brand-check/EVALS.md`
3. `repo:enter_output/skills/post-fact-brand-check/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/post-fact-brand-check/HANDOFF_SCHEMA.json`

### Business input files

- `run:06_optimized/checked_posts.md`
- `run:06_optimized/native_posts.md`
- `run:06_optimized/6a_handoff_packet.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Artifact under review.
3. Minimal fact / brand context.
4. Stage-specific upstream context.

### Allowed extra reads

- None by default.

### Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless passed in retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps unless explicitly produced by current run and listed above.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 6c, Stage 6d, or Stage 7 artifacts.
