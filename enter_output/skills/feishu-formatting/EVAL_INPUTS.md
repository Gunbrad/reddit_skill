# Eval Inputs - feishu-formatting

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/feishu-formatting/EVALS.md`
3. `repo:enter_output/skills/feishu-formatting/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/feishu-formatting/HANDOFF_SCHEMA.json`

### Business input files

- `run:07_format/format_report.md`
- `run:06_optimized/handoff_packet.json`
- `run:06_optimized/feishu_links.md`
- `run:06_optimized/final_posts.md`
- `run:07_format/live_doc_snapshot.md` if present.
- `run:07_format/live_doc_check.json` if present.
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
- All topic cards or unchosen drafts.
