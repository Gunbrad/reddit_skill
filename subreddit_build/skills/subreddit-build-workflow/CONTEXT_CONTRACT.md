# CONTEXT_CONTRACT.md

Workers receive minimal context. A stage worker may read only:

1. Required instruction files listed in the current stage's `INPUTS.md`.
2. Optional instruction files explicitly named in `run_config.prompt_packs.<stage>`.
3. Business input files listed in the current stage's `INPUTS.md`.
4. Approved upstream handoff packets and only the artifact paths named inside them.

## Isolation Rules

- Run generator and evaluator as isolated workers, child tasks, fresh sessions, or equivalent.
- If no isolation mechanism exists, emulate isolation with a fresh task that receives only the
  `stage_input_packet`; record this fallback in `run_manifest.md`.
- Worker depth is `1` by default. No stage worker may spawn its own workers unless the
  orchestrator explicitly permits it for Feishu tooling.

## Forbidden By Default

- Full prior conversation history.
- Previous scratchpads and failed drafts.
- Unrelated run folders.
- Old Feishu docs not linked by the current run.
- Raw Reddit dumps outside current run artifacts.
- API keys, cookies, session values, or other secrets in any file.

Downstream stages read compressed global fact files instead of the full product brief unless
their `INPUTS.md` explicitly allows a brief read and the reason is logged.
