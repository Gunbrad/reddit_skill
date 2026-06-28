---
name: reddit-posting-workflow
description: Use when starting, resuming, or routing the end-to-end Reddit brand-posting pipeline, or when deciding which stage skill should run next.
---

# Reddit Posting Workflow - Orchestrator

## Role

This skill is the pipeline orchestrator. It is a dispatcher, not a content generator.

It coordinates the 7 logical stages documented in `PIPELINE_CONTRACT.md` and the repository
`README.md`. It must not personally write topics, queries, posts, comments, image prompts, or
Feishu formatting. Stage work belongs to isolated generator workers; evaluation belongs to
separate isolated evaluator workers.

Read these contracts before routing a run:

- `PIPELINE_CONTRACT.md` - canonical stages, paths, counts, and handoff files.
- `CONTEXT_CONTRACT.md` - context isolation, whitelist reads, fresh-session fallback.
- `WORKER_CONTRACT.md` - generator worker vs evaluator worker responsibilities.
- `EVAL_WORKER_CONTRACT.md` - mandatory independent evaluation and manifest logging.

## Execution Model

For every stage, execute this sequence:

1. Read the run folder's `run_config.json`.
2. Read `PIPELINE_CONTRACT.md` and the current stage's `INPUTS.md`.
3. Build `stage_input_packet` containing only allowed global files and allowed stage files.
4. Launch an **isolated generator worker** with that packet.
5. Collect the stage artifact and draft `handoff_packet.json`.
6. Launch an **isolated evaluator worker** with only the artifact, `EVALS.md`,
   `OUTPUT_SCHEMA.json`, and minimal fact / brand / upstream handoff context.
7. Write the evaluator verdict, score, failures, retries, and artifact paths to
   `run_manifest.md`.
8. If evaluation fails, launch a fresh retry generator worker with only the original
   `stage_input_packet` plus the evaluator failure report.
9. If evaluation passes, promote the draft into the **approved handoff packet**.
10. Pass only the approved handoff packet and approved artifact paths to the next stage.

Use any runtime-supported isolation mechanism: isolated worker, subagent, child agent, task
agent, worker thread, fresh session, or equivalent context-isolated execution. If no native
worker mechanism exists, emulate isolation with a fresh task / fresh run that receives only
the `stage_input_packet`, and record the fallback in `run_manifest.md`.

## Canonical Stages

| Stage | Skill | Canonical output |
|---|---|---|
| 1 product research | `product-research` | `01_product_brief/product_brief.md` plus `global/product_fact_index.json`, `global/claim_boundary_table.json`, `global/brand_safety_rules.md` |
| 2 topic selection | `topic-selection` | `02_topics/topics.md`, `02_topics/feishu_links.md` |
| 3 search/query occupancy | `search-query-occupancy` | `03_search/search_queries.md`, `03_search/run_meta.json`, `03_search/occupancy_heat_evidence.json`, maps, topic cards |
| 4 topic-card screening | `topic-card-selection` | `04_screen/screening.md`, `04_screen/passed_cards.json` |
| 5 topic-card optimization | `topic-card-optimization` | `05_optimized_cards/optimization.md`, `05_optimized_cards/drafts_md/*`, structured `viral_intent` handoff |
| 6 post optimization coordinator | `post-optimization` | `06_optimized/final_posts.md`, `06_optimized/feishu_links.md`, `06_optimized/handoff_packet.json` |
| 7 Feishu formatting | `feishu-formatting` | `07_format/format_report.md` |

Stage 6 is a coordinator over four sub-stage skills:

| Sub-stage | Skill | Output |
|---|---|---|
| 6a content optimization | `post-native-rewrite` | `06_optimized/native_posts.md` |
| 6b fact / brand gate | `post-fact-brand-check` | `06_optimized/checked_posts.md` |
| 6c subreddit + image packaging | `post-subreddit-image` | `06_optimized/final_posts.md`, optional `06_optimized/images/*` |
| 6d Feishu publishing | `post-feishu-publish` | `06_optimized/feishu_links.md`, optional `06_optimized/images/image_feishu.md` |

## Run Workspace

One run uses one run folder named `{YYYYMMDD_HHMMSS}_{project_slug}`. The orchestrator creates
or reuses that folder and never scatters artifacts outside it.

Required top-level run files:

- `run_config.json` - user configuration and supplied-artifact references.
- `run_manifest.md` - stage status, artifact paths, evaluator verdicts, retries, isolation
  mode, and approved handoff packet paths.

Stage folders are created lazily according to `PIPELINE_CONTRACT.md`.

## Context Rules

Downstream stages read compressed global files by default:

- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

The full `01_product_brief/product_brief.md` may be re-read only when the compressed files
lack a required fact. The worker must log the exact reason in `run_manifest.md`.

Workers must not inherit full conversation history, previous scratchpads, failed drafts, raw
exploration logs, unrelated run folders, old Feishu docs, or raw Reddit dumps unless the
current stage's `INPUTS.md` explicitly whitelists them.

## Handoff Rules

A stage can advance only when:

1. The artifact exists at the canonical path.
2. The artifact matches `OUTPUT_SCHEMA.json`.
3. `handoff_packet.json` matches `HANDOFF_SCHEMA.json`.
4. A separate evaluator worker passes the artifact against `EVALS.md`.
5. The verdict is written to `run_manifest.md`.
6. The orchestrator marks the packet as the approved handoff packet.

The next stage reads the approved handoff packet first, then only the artifact paths named
inside that packet.

## Skipping A Stage

A user-supplied artifact can satisfy a stage only when `run_config.json` lists the skipped
stage and the provided path. Normalize the supplied material into the canonical artifact
format, run that stage's evaluator worker, and log the result in `run_manifest.md`. Do not
pass free-form user material directly to downstream stages.

## Completion Gate

Do not mark a run complete until:

- `02_topics/feishu_links.md` contains the topic Feishu doc URL.
- `06_optimized/feishu_links.md` contains the post Feishu doc URL.
- If images or image prompts exist, the image Feishu doc URL and anchor mapping are recorded.
- Stage 7 evaluator passes and `07_format/format_report.md` is written.
