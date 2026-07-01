# EVAL_WORKER_CONTRACT.md

No self-grading. Every stage must be reviewed by a separate evaluator worker before handoff.

## Required Evaluator Packet

The evaluator receives:

- The current stage artifact.
- The current stage `EVALS.md`.
- The current stage `OUTPUT_SCHEMA.json`.
- The current stage `HANDOFF_SCHEMA.json`.
- The approved upstream handoff packet when needed.
- Minimal global fact/brand files when needed.

The evaluator must not receive raw conversation history, hidden reasoning, failed drafts not
under review, or unrelated artifacts.

## Manifest Logging

`run_manifest.md` must record:

- evaluator identity/isolation mode,
- verdict,
- blocking failures,
- score and threshold,
- retry count,
- approved handoff path.

Reviewer prompts in `EVALS.md` are mandatory. They are not optional suggestions.
