# Eval Inputs - post-optimization

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/post-optimization/EVALS.md`
3. `repo:enter_output/skills/post-optimization/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/post-optimization/HANDOFF_SCHEMA.json`

### Business input files

- `run:06_optimized/final_posts.md`
- `run:06_optimized/feishu_links.md`
- `run:06_optimized/handoff_packet.json`
- `run:06_optimized/6a_handoff_packet.json`
- `run:06_optimized/6b_handoff_packet.json`
- `run:06_optimized/6c_handoff_packet.json`
- `run:06_optimized/6d_handoff_packet.json`
- `run:05_optimized_cards/handoff_packet.json`
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
