---
name: reddit-posting-workflow
description: Use when running the end-to-end Reddit brand-posting pipeline for a client product (from product research to formatted Feishu post), or when unsure which stage skill to invoke next, or when starting a new posting task and needing to set up the run workspace.
---

# Reddit Posting Workflow (Orchestrator)

## Overview

This is the entry point and router for a 7-stage pipeline that takes a client product
from raw product facts to a finished, formatted Reddit post draft in Feishu. Each stage
is a separate skill with its own EVALS. This skill owns: the **trigger chain**, the **run
workspace convention**, and the **handoff contract** that guarantees each stage produces
exactly what the next stage needs.

**Core principle:** every stage reads the previous stage's local artifact, validates it
against that stage's EVALS, and only then proceeds. A stage that fails its own EVALS is
sent back (打回重改) before handoff — never passed downstream broken.

## The 7 stages and their skills

| # | Stage | Skill | Local artifact (the handoff) |
|---|-------|-------|------------------------------|
| 1 | 产品调研 → 产品大纲 | `product-research` | `01_product_brief/product_brief.md` |
| 2 | 选题 + 写入飞书 | `topic-selection` | `02_topics/topics.md` (+ Feishu doc link) |
| 3 | 搜索 query + 工作流接口 + 搜索占位地图 + topic cards | `search-query-occupancy` | `03_search/search_queries.md` (+ maps, run_meta.json) |
| 4 | topic card 筛选(二元门:全量筛出可进生产的卡) | `topic-card-selection` | `04_screen/screening.md` |
| 5 | topic card 优化(爆帖潜能→TopN→补充说明含选题→生成草稿) | `topic-card-optimization` | `05_optimized_cards/optimization.md` (+ drafts) |
| 6 | 帖子优化 + 写入飞书 + 生图 + 去AI化 + 目标社区 | `post-optimization` | `06_optimized/final_posts.md` (+ images, Feishu doc) |
| 7 | 飞书排版 + 评论原生化 | `feishu-formatting` | `07_format/format_report.md` |

## Trigger chain (when to invoke which skill)

```dot
digraph pipeline {
  rankdir=LR;
  "new task / new product" -> "product-research" [label="stage 1"];
  "product-research" -> "topic-selection" [label="brief passes EVALS"];
  "topic-selection" -> "search-query-occupancy" [label="topics in Feishu"];
  "search-query-occupancy" -> "topic-card-selection" [label="6 directions x M cards"];
  "topic-card-selection" -> "topic-card-optimization" [label="cards that pass the gate"];
  "topic-card-optimization" -> "post-optimization" [label="top-N + drafts generated"];
  "post-optimization" -> "feishu-formatting" [label="posts in Feishu"];
  "feishu-formatting" -> "done" [label="format passes EVALS"];
}
```

You do not have to run all 7 in one session. Enter at the stage the user asks for, but
**verify the upstream artifact exists and passed its EVALS** before starting. If it does
not exist, either run the upstream stage or ask the user for it.

## run_config.json — the single source of user customization (MANDATORY to check)

At the start of every task, look for `run_config.json` in the run folder (or ask the user
for these values and write it). Every stage reads it before using its own defaults. This is
the ONE place users override the pipeline; stages must not hard-code what lives here.

```jsonc
{
  "project_name": "Enter Pro",
  "project_slug": "enter-pro",                 // run-folder slug; derived if omitted

  // --- decoupling: skip stages by providing the artifact ---
  "skip_stages": [1],                          // stages to skip because the user supplied the artifact
  "provided_artifacts": {                       // path the user gave; the skill normalizes it to the stage's required structure
    "product_brief": "path/to/brief.md",        // satisfies stage 1
    "topics": "path/to/topics.md"               // satisfies stage 2
  },

  // --- stage 2 ---
  "topics": [],                                 // if non-empty, user-specified 选题 (skip auto-generation); each = the 6-field block
  "topic_count": 6,                             // number of 选题 (default 6 = top6; each → 1 chosen query → 1 direction)

  // --- stage 3 ---
  "posts_per_query": 10,
  "queries_per_topic": 3,                       // candidate long-tail queries per 选题; the best 1 is chosen → that 选题's direction
  "topic_card_count": 12,                       // cards generated per direction (default 12; not a fixed total)
  "topic_card_length": "default",               // "short" | "default" | "long" (prompt-level via supplemental_context)

  // --- stage 4 (screening: binary gate, no top-N here) ---
  // (no count knobs — every card is judged pass/fail; all passers move to stage 5)

  // --- stage 5 (optimization: viral potential → top-N → notes → drafts) ---
  "top_n": null,                                // how many cards to optimize+draft (null = propose & confirm)
  "draft_length_multiplier": 1,                 // passed to the draft job
  "supplemental_context": "",                   // global default note; per-card notes still allowed/override

  // --- stage 6 ---
  "generate_images": "auto"                     // "auto" (per card's post_format) | true | false
}
```

Rules:
- A stage uses the config value if present, else its documented default, else asks the user.
- Values here OVERRIDE any historical hard-coded constants. Stage 3 = `topic_count` 选题
  (default 6), each with `queries_per_topic` candidates → 1 chosen query → 1 direction; ALL
  successful directions generate cards (no forced down-select). Stage 4 is a binary gate over
  ALL cards (no fixed total of 36). The EVALS check "matches run_config", not a fixed number.
- Never put secrets (cookies, API keys) in run_config.json — env only.
- Record the effective config (final values used) in `run_manifest.md`.

## Run workspace convention (MANDATORY)

Every task gets ONE run folder. Create it at the start of stage 1 (or the first stage you
enter) and reuse it for every later stage.

**Naming:** `{YYYYMMDD_HHMMSS}_{project_slug}` (timestamp + project name).
`project_slug` is the product name, lowercased, spaces → hyphens (e.g. `Enter Pro` → `enter-pro`).

**Base path:** create the run folder under the task's output directory the user gave you.
If none was given, ask. Do NOT scatter artifacts outside the run folder.

**Skeleton (created lazily, each stage makes its own subfolder):**

```
{timestamp}_{project_slug}/
  run_config.json     user customization: skip_stages, provided_artifacts, topic_count(6),
                      queries_per_topic(3), topic_card_count/length, top_n, draft length, generate_images
  01_product_brief/   product_brief.md
  02_topics/          topics.md, feishu_links.md
  03_search/          search_queries.md, run_meta.json, maps/, materials/, topic_cards/
  04_screen/          screening.md            (binary gate: pass/fail per card)
  05_optimized_cards/ optimization.md, drafts_md/   (viral-potential top-N + notes + drafts)
  06_optimized/       final_posts.md, images/ (png + prompts.md + image_feishu.md), feishu_links.md
  07_format/          format_report.md
  run_manifest.md     running log: stage, status, artifact paths, EVALS verdict
```

Write/append `run_manifest.md` after every stage with: stage name, timestamp, output
paths, and the EVALS pass/fail verdict. This is how a later session resumes mid-pipeline.

## Handoff contract (what each stage MUST guarantee)

A stage may hand off ONLY when its artifact:
1. Exists at the exact path above.
2. Uses the exact structure that stage's SKILL.md defines (downstream parsing depends on it).
3. Has passed that stage's EVALS (recorded in `run_manifest.md`).

If any check fails, the stage repeats until it passes. Never let the next stage "work
around" a malformed upstream artifact.

## Decoupling: skipping a stage when the user supplies the artifact

Stages are independent; the pipeline only depends on each stage's artifact, not on having
run that stage. So a user can skip a stage by providing its output.

How to skip a stage cleanly:
1. The user lists the stage in `run_config.skip_stages` and points to their material in
   `run_config.provided_artifacts` (e.g. their own product brief or a fixed list of 选题).
2. **Normalize, don't trust blindly.** Convert the user's material into the EXACT structure
   that stage's SKILL.md requires (same headings/fields — downstream parses by them) and
   write it to the canonical path (`01_product_brief/product_brief.md`, `02_topics/topics.md`, …).
3. **Still run that stage's EVALS** on the normalized artifact. A supplied brief that fails
   stage-1 EVALS is unsafe for downstream use — fix it or ask the user, don't skip the check.
4. Log in `run_manifest.md`: "stage N skipped — artifact user-provided, normalized, EVALS: pass".

Handling unstructured input:
- If the user gives free-form text ("our product is X, it does A/B/C") rather than a
  structured artifact, run the upstream stage to STRUCTURE it (that's what the stage is for),
  or ask for the missing fields. Do not hand free-form text to the next stage.

Examples:
- User provides project name + a product outline → skip stage 1: normalize the outline into
  `product_brief.md` (capability tree tagged, boundary table, etc.), run stage-1 EVALS, proceed to stage 2.
- User specifies the 选题 → skip stage 2's auto-generation: put them in `run_config.topics`
  (or `provided_artifacts.topics`), normalize to the 6-field block format, run stage-2 EVALS, proceed to stage 3.

## Shared rules (apply to every stage)

See conventions.md for: brand/red-line rules, Feishu CLI usage, the SmartContent API base
+ auth, file encoding, and the EVALS loop protocol. Read it once per task.

## Quick reference

- Stage skills are independent; this skill only routes + owns the workspace.
- One run folder per task, named `{timestamp}_{project_slug}`.
- Each stage: read upstream artifact → do work → write artifact → run EVALS → log manifest.
- A failing EVALS sends the stage back; it does not block the whole pipeline forever, but
  it does block handoff to the next stage.
