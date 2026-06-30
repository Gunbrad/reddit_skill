# Eval Inputs - product-research

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/product-research/EVALS.md`
3. `repo:enter_output/skills/product-research/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/product-research/HANDOFF_SCHEMA.json`

### Business input files

- `run:01_product_brief/product_brief.md`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`
- `run:run_config.json` optional.
- `run_config.product_sources` optional when run_config declares source files or URLs.
- `run_config.provided_artifacts` optional when run_config declares source artifacts.

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
- Topic cards, drafts, optimized posts, or formatting outputs from later stages.
