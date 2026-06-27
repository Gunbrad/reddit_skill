---
name: reddit-posting-workflow
description: Use when running the end-to-end Reddit brand-posting pipeline for a client product (from product research to formatted Feishu post), or when unsure which stage skill to invoke next, or when starting a new posting task and needing to set up the run workspace.
---

# Reddit Posting Workflow (Orchestrator)

## Overview

This is the entry point and router for a 6-stage pipeline that takes a client product
from raw product facts to a finished, formatted Reddit post draft in Feishu. Each stage
is a separate skill with its own EVALS. This skill owns: the **trigger chain**, the **run
workspace convention**, and the **handoff contract** that guarantees each stage produces
exactly what the next stage needs.

**Core principle:** every stage reads the previous stage's local artifact, validates it
against that stage's EVALS, and only then proceeds. A stage that fails its own EVALS is
sent back (打回重改) before handoff — never passed downstream broken.

## The 6 stages and their skills

| # | Stage | Skill | Local artifact (the handoff) |
|---|-------|-------|------------------------------|
| 1 | 产品调研 → 产品大纲 | `product-research` | `01_product_brief/product_brief.md` |
| 2 | 选题 + 写入飞书 | `topic-selection` | `02_topics/topics.md` (+ Feishu doc link) |
| 3 | 搜索 query + 工作流接口 + 搜索占位地图 + topic cards | `search-query-occupancy` | `03_search/search_queries.md` (+ maps, run_meta.json) |
| 4 | topic card 选 topN + 补充说明 + 生成草稿 | `topic-card-selection` | `04_drafts/selection.md` (+ drafts) |
| 5 | 帖子优化 + 写入飞书 + 生图 + 去AI化 + 目标社区 | `post-optimization` | `05_optimized/final_posts.md` (+ images, Feishu doc) |
| 6 | 飞书排版 + 评论原生化 | `feishu-formatting` | `06_format/format_report.md` |

## Trigger chain (when to invoke which skill)

```dot
digraph pipeline {
  rankdir=LR;
  "new task / new product" -> "product-research" [label="stage 1"];
  "product-research" -> "topic-selection" [label="brief passes EVALS"];
  "topic-selection" -> "search-query-occupancy" [label="topics in Feishu"];
  "search-query-occupancy" -> "topic-card-selection" [label="3 directions x 12 cards"];
  "topic-card-selection" -> "post-optimization" [label="drafts generated"];
  "post-optimization" -> "feishu-formatting" [label="posts in Feishu"];
  "feishu-formatting" -> "done" [label="format passes EVALS"];
}
```

You do not have to run all 6 in one session. Enter at the stage the user asks for, but
**verify the upstream artifact exists and passed its EVALS** before starting. If it does
not exist, either run the upstream stage or ask the user for it.

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
  01_product_brief/   product_brief.md
  02_topics/          topics.md, feishu_links.md
  03_search/          search_queries.md, run_meta.json, maps/, materials/
  04_drafts/          selection.md, drafts_md/
  05_optimized/       final_posts.md, images/ (png + prompts.md), feishu_links.md
  06_format/          format_report.md
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

## Shared rules (apply to every stage)

See conventions.md for: brand/red-line rules, Feishu CLI usage, the SmartContent API base
+ auth, file encoding, and the EVALS loop protocol. Read it once per task.

## Quick reference

- Stage skills are independent; this skill only routes + owns the workspace.
- One run folder per task, named `{timestamp}_{project_slug}`.
- Each stage: read upstream artifact → do work → write artifact → run EVALS → log manifest.
- A failing EVALS sends the stage back; it does not block the whole pipeline forever, but
  it does block handoff to the next stage.
