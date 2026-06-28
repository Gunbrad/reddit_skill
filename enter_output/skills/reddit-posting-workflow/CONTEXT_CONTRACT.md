# CONTEXT_CONTRACT.md — global context-isolation rules

This contract governs HOW the pipeline is executed, independent of WHAT each stage produces.
Every skill in this family (orchestrator + stages + sub-workers + evaluators) MUST obey it.
It is written to be **runtime-agnostic**: wherever it says "isolated worker", use whichever
context-isolation mechanism your agent runtime provides — a **subagent**, **child agent**,
**task agent**, **worker thread**, or a **fresh session / fresh run**. Do not assume Codex,
Claude Code, or any one product; any system that can start an execution with a clean,
minimal context satisfies this contract.

## Why this exists

The pipeline is 7 stages long. Running all of them in one continuously-growing context causes:
context pollution (earlier stages' detail biases later ones), oversized context (attention
degrades, cost rises), unclear hand-offs (the next stage rummages through raw history), and
unstable EVALS (a generator that also grades itself passes itself too leniently). Isolation
fixes all four.

## The 9 principles (MANDATORY)

1. **No monolithic run.** The orchestrator MUST NOT run the full 7-stage pipeline inside one
   continuous context. Each stage is a separate isolated execution.
2. **Isolated worker per stage.** Entering a new stage MUST first launch an isolated worker
   for that stage. The orchestrator coordinates; it does not "become" the stage.
3. **Use real isolation when available.** If the runtime supports subagent / child agent /
   task worker / fresh session, you MUST use it for each generator worker and each evaluator
   worker.
4. **Emulate isolation when not available.** If the runtime cannot spawn workers, simulate
   isolation with a **fresh task / fresh run / cleared context** that is handed ONLY the
   current stage's input packet (the files whitelisted in that stage's `INPUTS.md`). Note in
   the manifest that isolation was emulated, not native.
5. **Whitelist-only reads.** A stage worker may read ONLY the files allowed by that stage's
   `INPUTS.md` (its "Allowed global files" + "Allowed stage files"). Reading anything in the
   "Forbidden files" list is a contract violation.
6. **No inherited context.** A stage worker MUST NOT inherit: the full prior conversation,
   previous stages' scratchpads, failed/abandoned drafts, raw exploration logs, or unrelated
   run folders. It starts clean and loads only its input packet.
7. **Structured return only.** A stage worker may return ONLY:
   - the final artifact path(s),
   - a structured handoff packet (`handoff_packet.json`, per the stage's `HANDOFF_SCHEMA.json`),
   - an eval-ready summary (short, factual, for the evaluator),
   - a list of unresolved blockers / open questions.
   It MUST NOT return its raw chain-of-thought or working notes.
8. **Orchestrator discards intermediate reasoning.** The orchestrator keeps the approved
   artifact + approved handoff packet and DISCARDS the worker's intermediate reasoning. Only
   the approved handoff packet is passed to the next stage.
9. **Worker depth = 1 by default.** A stage worker MUST NOT recursively spawn its own nested
   workers unless the orchestrator explicitly authorizes it (e.g. the Stage-6 coordinator is
   explicitly authorized to run its sub-workers 6a-6d). Default tree is: orchestrator →
   {generator worker, evaluator worker}.

## Minimal-context principle (works with §5)

Prefer the smallest sufficient input. Downstream stages read the **compressed global files**
(`global/product_fact_index.json`, `global/claim_boundary_table.json`,
`global/brand_safety_rules.md`) rather than the full `01_product_brief/product_brief.md`. The
full brief is read back ONLY when the fact index lacks something needed, and that re-read must
be logged (which fact, why) in `run_manifest.md`.

## Relationship to the other contracts

- `WORKER_CONTRACT.md` — defines the worker roles (generator vs evaluator) and their I/O.
- `PIPELINE_CONTRACT.md` — defines the canonical inputs/outputs/handoff path per stage.
- `EVAL_WORKER_CONTRACT.md` — defines mandatory, independent evaluation.
- Per-stage `INPUTS.md` — the concrete read whitelist/forbidden list for that stage.
- Per-stage `OUTPUT_SCHEMA.json` / `HANDOFF_SCHEMA.json` — the concrete artifact/handoff shape.

A stage is correctly executed only if ALL of: its worker was isolated, it read only its
whitelist, it returned a schema-valid artifact + handoff packet, and a separate evaluator
worker scored it.
