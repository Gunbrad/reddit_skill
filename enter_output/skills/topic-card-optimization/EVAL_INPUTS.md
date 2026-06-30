# Eval Inputs - topic-card-optimization

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/topic-card-optimization/EVALS.md`
3. `repo:enter_output/skills/topic-card-optimization/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/topic-card-optimization/HANDOFF_SCHEMA.json`

### Business input files

- `run:05_optimized_cards/optimization.md`
- `run:05_optimized_cards/drafts_md/{post_id}.md`
- `run:04_screen/handoff_packet.json`
- `run:04_screen/passed_cards.json`
- `run:03_search/occupancy_heat_evidence.json`
- `run:global/product_fact_index.json`
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
- Full product brief when compressed global files are sufficient.
- Stage 6 or Stage 7 artifacts.
