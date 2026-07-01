---
name: post-feishu-publish
description: Use after final_posts.md is ready from native rewrite, when writing optimized Reddit posts into a Feishu 帖子 doc, optionally creating the 生图 doc when images exist, setting docs public-editable, and ensuring the Topic Card doc exists. Stage 6d of the subreddit build workflow.
---

# Post Feishu Publish Prep (Stage 6d)

## Overview

Publish the finished posts into Feishu and guarantee the run's user-facing deliverables exist:
the 帖子 doc (always), the optional 生图 doc when images exist, and the Topic Card doc from
Stage 3. Every created doc is set public-editable. Its output (the 帖子 doc URL) is stage 7's input.

**Core principle:** deliverables are non-negotiable — a run ends with 2 Feishu docs (no
images) or 3 (with images). Anchors must point to the exact same post.

## Context (subagent isolation)

Run as an isolated worker (CONTEXT_CONTRACT.md). You receive ONLY:
- Global: run folder, `run_config.json`, `conventions.md`, `global/product_fact_index.json`,
  `global/claim_boundary_table.json`, and `global/brand_safety_rules.md`.
- Stage-local input: `06_optimized/final_posts.md`, `06_optimized/handoff_packet.json`,
  optional `06_optimized/images/`, and `03_topic_retrieval/topic_cards.md` +
  `03_topic_retrieval/feishu_links.md` (to verify / create the Topic Card doc).
- Feishu access via the `lark-doc` / `lark-drive` skills (first run may need `lark-shared`).

## Tasks

### 0. Ensure the Topic Card doc exists (deliverable check)
Verify `03_topic_retrieval/feishu_links.md` contains the Topic Card Feishu URL. If Stage 3
failed to create it, create the doc from `03_topic_retrieval/topic_cards.md` now, set it
public-editable, and record the URL.

### 1. Create the 帖子 doc
Use `lark-doc` to create `{Product} - 帖子 - {date}` and paste the posts from `final_posts.md`.
Per post, in its `<h2>Title</h2>` block: the main title `<p>`, then `<p>备用标题：</p>` and one
`<p>` per alternate (≥3), then the body, the `<p>Target Subreddit: r/x or r/y or r/z</p>` line,
and the comment design. **Set the doc permission to "anyone on the internet with the link can
edit" via lark-drive — do this directly without asking the user** (conventions.md §3).

### 2. 生图 doc + anchor jump-back (only when images exist)
If any post has an image (or a pending image prompt), create a SEPARATE doc
`{Product} - 生图提示词与配图 - {date}` pairing each prompt with its generated image as a
**组合 (combo)**, one combo per image-bearing post, each linking back to that exact post in the
帖子 doc:
1. After the 帖子 doc exists, use `lark-doc` to read its block structure and capture each
   post-title `<h1>` (or `<h2>Title</h2>`) block's **block_id**.
2. Build the anchor URL per post: `{帖子文档URL}#{block_id}`.
3. For each image-bearing post write one combo block:
   ```
   <h2>组合 N — {post_id}（{帖子简述}）</h2>
   <p>图片类型：实体类 / 虚拟类</p>
   <p>对应帖子：<a href="{帖子文档URL}#{block_id}">→ 跳转到对应帖子</a></p>
   <p>最终提示词：</p>
   <p>{final prompt 全文}</p>
   <p>场景改写理由：{why the scenario was changed}</p>
   <p>生成图片：</p>
   <img ...>   （png 上传到该 docx；API 未就绪则写「图片：pending」）
   <hr/>
   ```
4. The anchor MUST point to the title block of the SAME post_id as the combo. Verify each
   combo→post mapping one by one; a mis-wired anchor is a blocking EVALS failure.
5. Set this doc public-editable too. Record the image-doc URL and the `post_id → block_id`
   mapping in `06_optimized/images/image_feishu.md`, and add the URL to `06_optimized/feishu_links.md`.

Never write any API key / cookie / secret into any doc or artifact (conventions.md §6).

## Required output structure

Write to `06_optimized/` (UTF-8):
- `feishu_links.md` — the 帖子 doc URL, the 生图 doc URL if images exist (else an explicit "no
  image doc created" line), and confirmation the Topic Card doc URL exists in `03_topic_retrieval/feishu_links.md`.
- `images/image_feishu.md` — image-doc URL + `post_id → title block_id` anchor mapping (only when images exist).

## Process

1. Verify/create the Topic Card doc (Task 0); set public-edit; log URL.
2. Create the 帖子 doc from `final_posts.md` (main title + ≥3 备用标题 + Target Subreddit line +
   comments per post); set public-edit; record URL.
3. If images exist: create the 生图 doc with prompt+image combos and anchor links back to each
   post; verify each combo→post anchor; set public-edit; record URL + mapping.
4. Confirm the deliverable count (2 docs no-images / 3 with-images). STOP — hand to the
   evaluator worker (EVALS.md), then to stage 7 (`feishu-formatting`).

## Common mistakes

- Completing with only the 帖子 doc and no recorded Topic Card doc.
- Image-doc anchor wired to the wrong post (combo↔post_id mismatch).
- Forgetting to set a created doc public-editable.
- Dropping the 备用标题 / Target Subreddit / comment design when pasting into Feishu.
- Writing any API key / secret into a doc, prompts.md, image_feishu.md, or the manifest.


