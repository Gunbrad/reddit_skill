# EVALS — Post Optimization (Stage 6) — split across the four sub-skills

Stage 6 is now a coordinator (see SKILL.md). The eval rubrics moved into the four sub-skills,
each scored by a **separate evaluator worker** (EVAL_WORKER_CONTRACT.md):

| Sub | Skill | EVALS file | Covers |
|-----|-------|-----------|--------|
| 6a | `post-native-rewrite` | `post-native-rewrite/EVALS.md` | VP: viral intent preserved, A: de-AI Title+Body, B: comment nativeness (threshold ≥85) |
| 6b | `post-fact-brand-check` | `post-fact-brand-check/EVALS.md` | C: brand-exposure safety, D: fact accuracy |
| 6c | `post-subreddit-image` | `post-subreddit-image/EVALS.md` + `post-subreddit-image/IMAGE_PROMPT_EVALS.md` | E: subreddits, I: images |
| 6d | `post-feishu-publish` | `post-feishu-publish/EVALS.md` | F: Feishu deliverables, G: image-doc anchors |

Stage 6 passes only when all four sub-stage EVALS pass (see SKILL.md "Stage-6 exit criteria").
Do not score stage 6 from this file alone. The coordinator must launch a mandatory evaluator
worker for each sub-skill, then mirror those verdicts into `run_manifest.md` and
`06_optimized/handoff_packet.json`.

## Coordinator reviewer prompt (MANDATORY evaluator worker)

Under isolated-worker execution, this reviewer must run as a separate evaluator worker. It is
not optional. If the runtime does not support subagents, emulate this with a fresh evaluation
session that receives only this EVALS.md, OUTPUT_SCHEMA.json, the four sub-stage verdicts,
`06_optimized/handoff_packet.json`, and the Stage-5 handoff packet needed to confirm
`viral_intent` preservation.

"Read the Stage 6 sub-stage verdicts and handoff packet. Did 6a preserve the Stage-5
viral_intent (`core_hook`, `emotional_trigger`, `comment_engine`, `must_preserve`), did 6b
pass fact/brand safety, did 6c preserve titles/body/comments while adding subreddits/images,
and did 6d create the required Feishu docs and permissions? List every missing or failed gate."
