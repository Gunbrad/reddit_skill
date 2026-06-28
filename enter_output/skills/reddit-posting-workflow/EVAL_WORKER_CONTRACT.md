# EVAL_WORKER_CONTRACT.md — mandatory independent evaluation

Evaluation is not a courtesy pass by the generator. Under isolated-worker execution, every
stage artifact MUST be judged by a **separate evaluator worker** (subagent / child agent /
task worker / fresh session). This contract makes that mandatory and bounds what the evaluator
may see.

## Core rules (MANDATORY)

1. **No self-grading.** The worker that generated an artifact MUST NOT be the worker that
   scores it. A generator declaring its own output "good enough" does not count as evaluation.
2. **Always launch an evaluator.** After a stage artifact is produced, the orchestrator MUST
   launch an independent evaluator worker before any handoff. No artifact advances unevaluated.
3. **Reviewer prompt is mandatory, not optional.** Each `EVALS.md` ships a "Reviewer prompt".
   Under isolated-worker execution this prompt is the evaluator worker's instructions and is
   REQUIRED.
4. **Minimal eval context.** The evaluator reads ONLY: the stage's output artifact(s), the
   stage's `EVALS.md`, the stage's `OUTPUT_SCHEMA.json`, and the minimal global files needed
   to judge (usually `global/product_fact_index.json` and/or `global/brand_safety_rules.md`;
   plus the upstream `handoff_packet.json` when it must verify preserved intent). It does NOT
   read full upstream materials, the generator's reasoning, or conversation history.
5. **Evaluator cannot edit.** It returns a verdict + required fixes only. It never rewrites the
   artifact. Fixes are applied by a fresh generator/retry worker (WORKER_CONTRACT §3).
6. **All verdicts logged.** Every eval verdict (per-criterion blocking results, weighted score,
   pass/fail, required fixes) MUST be written to `run_manifest.md`. An unlogged eval is treated
   as not having happened.

## Blind evaluation

For de-AI / nativeness / image rubrics, the evaluator runs **BLIND**: it is NOT told the
product is the client's, and it is NOT told the intended answer or how the artifact was made.
It judges only "does this read like a real Reddit post / real photo, or like an ad/AI?".

## Fallback when the runtime has no subagents

Emulate independent evaluation with a **fresh evaluation session** that receives ONLY:
- the artifact,
- the stage `EVALS.md`,
- the stage `OUTPUT_SCHEMA.json`,
- the minimal fact index (and upstream handoff packet where intent-preservation is checked).

Do not reuse the generation context. Note in the manifest that evaluation was an emulated
fresh session rather than a native separate worker.

## Verdict shape (write to manifest, mirror into handoff_packet.eval_result)

```json
{
  "stage_id": "stage_5_topic_card_optimization",
  "blocking": "pass",            // or "fail"
  "score": 87,
  "threshold": 80,
  "failing_criteria": [],         // e.g. ["AB3", "C2"] when blocking == fail
  "required_fixes": [],           // specific, actionable; empty on pass
  "verdict": "pass",
  "evaluator_mode": "isolated_worker"   // or "emulated_fresh_session"
}
```

On `verdict:"fail"`, the orchestrator passes only `failing_criteria` + `required_fixes` (plus
the original input packet) to a fresh retry worker — never the full history.
