# WORKER_CONTRACT.md — worker roles & I/O

This contract defines the **types of isolated worker** the orchestrator launches. "Worker"
means any context-isolated execution unit: subagent / child agent / task agent / worker
thread / fresh session. It is runtime-agnostic — map it to whatever your system supports.

Default execution tree (worker depth = 1, per CONTEXT_CONTRACT §9):

```
orchestrator
  ├── Stage Generator Worker   (produces the artifact)
  └── Stage Evaluator Worker   (scores the artifact, independently)
```

The generator and the evaluator for a stage are ALWAYS two different workers. A worker never plays both roles.

---

## 1. Stage Generator Worker

**Job:** produce the current stage's artifact. Nothing else.

**May read (whitelist only — see the stage's `INPUTS.md`):**
- Allowed global files (e.g. `run_config.json`, `global/product_fact_index.json`,
  `global/brand_safety_rules.md`, `global/campaign_policy.md`).
- Allowed stage files: the upstream stage's **approved artifact** + **approved
  `handoff_packet.json`** only.

**Must NOT:**
- Read anything in the stage's "Forbidden files" list (full history, prior scratchpads,
  failed drafts, unrelated runs, raw dumps, full product brief when the fact index suffices,
  all cards when only selected cards are needed, all drafts when only selected are needed).
- Declare its own work "final" or "passed". Only an evaluator worker + orchestrator can.
- Spawn nested workers (depth stays 1 unless the orchestrator explicitly allows, e.g. the
  Stage-6 coordinator).

**Must output:**
- The artifact(s) at the canonical path from the stage's `OUTPUT_SCHEMA.json`.
- A **handoff draft** (`handoff_packet.json`) per the stage's `HANDOFF_SCHEMA.json`, with
  `eval_result` left for the evaluator (generator sets `status:"draft"`).
- A short eval-ready summary + any unresolved blockers.
- NOT its raw reasoning (the orchestrator discards intermediate reasoning anyway).

---

## 2. Stage Evaluator Worker

**Job:** judge the artifact against the stage's EVALS. It does NOT create or fix content.

**May read (minimal eval context ONLY):**
- The current stage's output artifact(s).
- The current stage's `EVALS.md`.
- The current stage's `OUTPUT_SCHEMA.json` (to check structural validity).
- Minimal global files needed to judge — typically `global/product_fact_index.json` and/or
  `global/brand_safety_rules.md`. For stages that must preserve Stage-5 intent, also the
  upstream `handoff_packet.json` (to confirm `viral_intent.must_preserve` survived).

**Must NOT:**
- Read the full upstream materials, the generator's reasoning, or the conversation history.
- Edit the artifact in any way.

**Must output:**
- `blocking`: pass / fail (with the exact failing criteria).
- `score`: the weighted score vs the stage threshold.
- `required_fixes`: specific, actionable items (not "make it better").
- `verdict`: pass / fail.

---

## 3. Retry loop (fail handling)

If the evaluator returns fail:
1. The orchestrator passes ONLY the evaluator's **failure report** (`blocking` + `required_fixes`)
   plus the original stage input packet to a **fresh generator/retry worker**.
2. It does NOT pass the previous worker's full context, chat history, or discarded drafts.
3. The retry worker revises the artifact; a **fresh evaluator worker** re-scores it.
4. Repeat until the evaluator returns pass (blocking clear + score ≥ threshold), then the
   orchestrator records the verdict in `run_manifest.md` and produces the approved handoff
   packet.

Every retry is a clean worker. No carry-over of prior attempts beyond the failure report +
the stage inputs.

---

## 4. Summary of guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| Clean context per stage | isolated generator worker, whitelist reads |
| No self-passing | separate evaluator worker (EVAL_WORKER_CONTRACT) |
| No history pollution | orchestrator discards intermediate reasoning; passes only handoff packet |
| Bounded recursion | worker depth = 1 unless explicitly authorized |
| Stable retries | fresh worker + failure report only |
