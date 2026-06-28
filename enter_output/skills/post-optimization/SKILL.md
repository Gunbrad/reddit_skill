---
name: post-optimization
description: Stage 6 coordinator for the Reddit posting pipeline. Use after Stage 5 produces chosen drafts and a structured handoff packet. This skill schedules 6a-6d isolated workers; it does not generate the final post content itself.
---

# Post Optimization - Stage 6 Coordinator

## Role

This is the Stage 6 coordinator. It does not perform rewriting, fact checking, subreddit
selection, image generation, Feishu publishing, or evaluation directly.

It only builds sub-stage input packets, launches isolated generator workers, launches
separate isolated evaluator workers, records verdicts in `run_manifest.md`, and promotes
approved artifacts into the Stage 6 `handoff_packet.json`.

## Allowed Inputs

Stage 6 can read only:

- `run_config.json`
- compressed global files:
  - `global/product_fact_index.json`
  - `global/claim_boundary_table.json`
  - `global/brand_safety_rules.md`
- Stage-5 handoff: `05_optimized_cards/handoff_packet.json`
- chosen drafts named by that handoff: `05_optimized_cards/drafts_md/{post_id}.md`
- approved Stage 6 sub-stage artifacts as they are produced

Do not read the full product brief here. If a sub-stage lacks a fact, it must use the
compressed fact files or stop with a blocker for the orchestrator.

## Sub-Stage Order

Run these sub-stage skills in order:

| Sub-stage | Skill | Input | Output |
|---|---|---|---|
| 6a content-optimization | `post-native-rewrite` | Stage-5 handoff + chosen drafts + compressed global files | `06_optimized/native_posts.md` |
| 6b fact / brand gate | `post-fact-brand-check` | `06_optimized/native_posts.md` + compressed global files | `06_optimized/checked_posts.md` |
| 6c subreddit + image packaging | `post-subreddit-image` | `06_optimized/checked_posts.md` + compressed global files | `06_optimized/final_posts.md`, optional `06_optimized/images/*` |
| 6d Feishu publishing | `post-feishu-publish` | `06_optimized/final_posts.md`, images, topic doc files | `06_optimized/feishu_links.md`, optional `06_optimized/images/image_feishu.md` |

The required final Stage 6 artifacts are:

- `06_optimized/final_posts.md`
- `06_optimized/feishu_links.md`
- `06_optimized/handoff_packet.json`

## Coordinator Process

For each sub-stage:

1. Build the sub-stage input packet from that sub-stage's `INPUTS.md`.
2. Launch an isolated generator worker for the sub-stage skill.
3. Launch an isolated evaluator worker with the artifact, sub-stage `EVALS.md`,
   `OUTPUT_SCHEMA.json`, and minimal required context.
4. If evaluation fails, pass only the evaluator failure report plus the original input packet
   to a fresh retry generator worker.
5. If evaluation passes, record the verdict and artifact path in `run_manifest.md`.
6. Pass only the approved artifact path and approved handoff data to the next sub-stage.

Stage 6 has explicit permission to coordinate these 6a-6d sub-workers. Those workers may not
create additional nested workers unless the top-level orchestrator explicitly authorizes it.

## Stage-5 Viral Intent Preservation

The Stage-5 handoff contains per-post `viral_intent`:

- `core_hook`
- `emotional_trigger`
- `comment_engine`
- `must_preserve[]`

6a must preserve that intent. A native-sounding rewrite that loses the Stage-5 hook, tension,
concrete scene, or discussion engine fails the 6a evaluator and cannot proceed to 6b.

## Stage 6 Handoff

After 6d passes, write `06_optimized/handoff_packet.json` with:

- `stage_id: stage_6_post_optimization`
- approved `final_posts.md` path
- approved `feishu_links.md` path
- post Feishu doc URL
- image doc URL or explicit `null`
- per-post viral-intent preservation verdict
- sub-stage evaluator verdicts for 6a, 6b, 6c, and 6d

Only this approved handoff packet can feed Stage 7.
