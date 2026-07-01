# WORKER_CONTRACT.md

## Stage Generator Worker

The generator worker creates the current stage artifact. It may self-check with `EVALS.md`,
but it cannot pass its own work.

Generator responsibilities:

- Read the `stage_input_packet` in order.
- Produce the canonical artifact and draft `handoff_packet.json`.
- Record inputs read, outputs written, API ids, Feishu URLs, and open questions.
- Never write secrets to files or Feishu docs.

## Stage Evaluator Worker

The evaluator worker independently reviews the artifact against `EVALS.md`,
`OUTPUT_SCHEMA.json`, `HANDOFF_SCHEMA.json`, and minimal approved context.

Evaluator responsibilities:

- Verify blocking criteria.
- List exact failures with file paths or artifact ids.
- Return pass/fail, score, threshold, retry_needed, and concise remediation.
- Do not rewrite the artifact.

## Separation Rule

A worker never plays both roles for the same stage. If the runtime lacks worker support, use a
fresh evaluation session and log the fallback.
