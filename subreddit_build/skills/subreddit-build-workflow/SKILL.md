---
name: subreddit-build-workflow
description: Use when starting, resuming, or routing the SmartContent Reddit community-building workflow, including product research, community crawling, retrieval, Topic Card generation, mechanism variant selection, draft generation, native rewrite, Feishu publishing, and Feishu formatting.
---

# Subreddit Build Workflow - Orchestrator

## Role

This skill is the pipeline orchestrator. It dispatches stage workers and enforces contracts; it
does not personally write product briefs, Topic Cards, mechanism choices, drafts, native posts,
or Feishu formatting.

Read these contracts before routing a run:

- `PIPELINE_CONTRACT.md` - canonical stages, paths, counts, API ids, and handoff files.
- `CONTEXT_CONTRACT.md` - context isolation and whitelist reads.
- `WORKER_CONTRACT.md` - generator worker vs evaluator worker responsibilities.
- `EVAL_WORKER_CONTRACT.md` - mandatory independent evaluation.
- `PROMPT_INJECTION_CONTRACT.md` - prompt packet structure and read order.
- `conventions.md` - SmartContent, Reddit, and Feishu workflow conventions.

## Execution Model

For every stage:

1. Read the run folder's `run_config.json`.
2. Read `PIPELINE_CONTRACT.md`, `PROMPT_INJECTION_CONTRACT.md`, and the current stage's `INPUTS.md`.
3. Build a `stage_input_packet` containing the stage `Role prompt`, required instruction files,
   optional prompt files from `run_config.prompt_packs`, business inputs, read order, and only
   the allowed global / stage files.
4. Launch an isolated generator worker.
5. Collect the stage artifact and draft `handoff_packet.json`.
6. Launch an isolated evaluator worker with only the artifact, `EVALS.md`, `OUTPUT_SCHEMA.json`,
   `HANDOFF_SCHEMA.json`, and minimal approved upstream context.
7. Write verdict, score, failures, retry count, and artifact paths to `run_manifest.md`.
8. If evaluation fails, retry with a fresh generator worker that receives only the original
   packet plus the evaluator failure report.
9. If evaluation passes, mark the packet as the approved handoff packet and route the next stage.

Use any runtime-supported isolation mechanism. If no worker support exists, emulate isolation
with a fresh task/run that receives only the `stage_input_packet`, and record that fallback in
`run_manifest.md`.

## Stages

| Stage | Skill | Canonical output |
|---|---|---|
| 1 | `product-research` | `01_product_brief/product_brief.md`, `global/*` |
| 2 | `community-capture` | `02_community_capture/community_capture.md`, SmartContent run ids, raw posts, post cards, content maps |
| 3 | `community-topic-retrieval` | `03_topic_retrieval/topic_cards.md`, `topic_cards.json`, topic Feishu doc |
| 4 | `mechanism-variant-selection` | `04_mechanism_selection/mechanism_selection.md`, applied variants |
| 5 | `community-card-draft-generation` | `05_optimized_cards/optimization.md`, `drafts_md/*`, viral-intent handoff |
| 6a | `post-native-rewrite` | `06_optimized/native_posts.md`, `06_optimized/final_posts.md` |
| 6d | `post-feishu-publish` | `06_optimized/feishu_links.md` |
| 7 | `feishu-formatting` | `07_format/format_report.md` |

The `6a` and `6d` labels intentionally mirror the previous workflow. In this community
builder first version, fact/brand safety and subreddit packaging are folded into the native
rewrite and publishing evals instead of separate `6b/6c` workers.

## Handoff Rules

A stage can advance only when:

1. The canonical artifact exists.
2. The artifact matches `OUTPUT_SCHEMA.json`.
3. `handoff_packet.json` matches `HANDOFF_SCHEMA.json`.
4. A separate evaluator worker passes the artifact against `EVALS.md`.
5. The verdict is written to `run_manifest.md`.
6. The orchestrator marks the packet as approved.

Downstream stages read the approved handoff packet first, then only the artifact paths named
inside that packet.

## Completion Gate

Do not mark a run complete until:

- `03_topic_retrieval/feishu_links.md` contains the Topic Card Feishu doc URL.
- `06_optimized/feishu_links.md` contains the final post Feishu doc URL.
- `07_format/format_report.md` exists and the final formatting evaluator passes.
