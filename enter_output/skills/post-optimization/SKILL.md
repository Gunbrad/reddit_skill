---
name: post-optimization
description: Stage 6 coordinator of the Reddit posting pipeline. Use after stage-5 drafts are generated to turn them into finished, fact-safe, native Reddit posts in Feishu. This skill no longer does the work itself; it sequences four isolated worker sub-skills (post-native-rewrite -> post-fact-brand-check -> post-subreddit-image -> post-feishu-publish), each with its own mandatory evaluator worker.
---

# Post Optimization — Stage 6 Coordinator

## Why this is now a coordinator

Stage 6 used to do everything in one context: de-AI rewrite, comment design, fact-check,
alternate titles, subreddit picks, image prompts, image generation + re-check, Feishu writing,
the 生图 doc, anchor mapping, and permissions. That is too much for one context: attention
degrades and earlier concerns pollute later ones. Stage 6 is now a coordinator over
**content-optimization** and **packaging**, implemented as four focused sub-skills. Each
sub-skill runs as an **isolated worker** with its own EVALS scored by a **separate evaluator
worker**.

The Stage-5 `handoff_packet.json` is the core input. Its per-post `viral_intent`
(`core_hook`, `emotional_trigger`, `comment_engine`, `must_preserve[]`) must survive 6a and be
reported in the Stage-6 handoff.

## The four sub-stages (run in order)

| Sub | Skill | Input -> Output | Owns |
|-----|-------|-----------------|------|
| 6a content-optimization | `post-native-rewrite` | `05_optimized_cards/drafts_md/*` + Stage-5 handoff -> `06_optimized/native_posts.md` | de-AI Title+Body, >=3 backup titles, native comments, viral_intent preservation |
| 6b content-optimization gate | `post-fact-brand-check` | `native_posts.md` -> `06_optimized/checked_posts.md` | fact accuracy vs fact index, brand-exposure safety |
| 6c packaging | `post-subreddit-image` | `checked_posts.md` -> `06_optimized/final_posts.md` (+ `images/`) | >=3 subreddits, image classify/prompt/generate/re-check |
| 6d packaging | `post-feishu-publish` | `final_posts.md` (+ `images/`) -> Feishu docs + `feishu_links.md` | post doc, image doc + anchors, topic doc check, permissions |

Each sub-skill ships its own `SKILL.md` + `EVALS.md` (6c also ships `IMAGE_PROMPT_EVALS.md`).
The de-AI / native rubric (6a) is still the heart of stage-6 quality control.

## Coordinator process

For each sub-stage in order 6a -> 6b -> 6c -> 6d:
1. Build the sub-stage input packet from `INPUTS.md`, the Stage-5 handoff, and the already
   approved Stage-6 artifact from the previous sub-stage.
2. Spawn an **isolated generator worker** for that sub-skill. Give it only the compressed
   global files (`global/product_fact_index.json`, `global/claim_boundary_table.json`,
   `global/brand_safety_rules.md`), `run_config.json`, and declared stage-local artifact paths.
   Do not pass prior workers' reasoning.
3. Spawn a **separate isolated evaluator worker** with that sub-skill's `EVALS.md`,
   `OUTPUT_SCHEMA.json`, the artifact, and minimal fact/brand or Stage-5 handoff context.
4. If any blocking criterion fails -> send back to a fresh generator worker (打回重改) and
   re-evaluate. Only on pass, record the verdict in `run_manifest.md` and proceed to the next sub-stage.
5. Pass **artifacts and approved handoff packets, not contexts**, between sub-stages.

Do not run all four in one context yourself. If your runtime has no worker/subagent support,
emulate isolation: between sub-stages, start a fresh session and re-read only that sub-stage's
declared inputs (note the fallback in the manifest).

## Stage-6 exit criteria (before handing to stage 7)

- 6a EVALS pass (de-AI total ≥ 85, blocking pass).
- 6a viral-intent preservation passes: final title/body/comment design retain Stage-5
  `core_hook`, `emotional_trigger`, `comment_engine`, and every `must_preserve` detail.
- 6b EVALS pass (no unverified feature as fact; brand-safe).
- 6c EVALS pass (≥3 subreddits; any image passes IMAGE_PROMPT_EVALS).
- 6d EVALS pass (帖子 doc + 选题 doc exist; 生图 doc when images exist; correct doc count;
  docs public-editable).
- The 帖子 doc URL is recorded in `06_optimized/feishu_links.md` → this is stage 7's input.

## Common mistakes

- Running stage 6 as one big context instead of four isolated workers.
- Letting the generator worker that wrote an artifact grade its own work (use a separate evaluator).
- Skipping a sub-stage's EVALS and handing a broken artifact downstream.
- Passing prior sub-agents' full reasoning instead of just the next input artifact.
- Flattening the Stage-5 viral_intent while trying to make the post sound native.
