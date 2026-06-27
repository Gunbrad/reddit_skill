---
name: post-optimization
description: Use after drafts are generated, when making Reddit posts sound native (de-AI), when verifying posts against product facts, when reviewing or generating post images via the image2 API, or when recommending target subreddits and writing posts into Feishu. Stage 6 of the Reddit posting pipeline.
---

# Post Optimization (de-AI, native, images, subreddits) (Stage 6)

## Overview

Take the generated drafts and turn them into posts that read like a real Reddit user wrote
them: de-AI'd, native, fact-accurate, with vetted images and concrete target subreddits.
Then write them into a Feishu doc for stage 7. This is the **deepest** stage — its EVALS
(the de-AI / native rubric) is the heart of quality control.

**Core principle:** native ≠ polished. Real Reddit posts are slightly messy: one core
question, a little doubt, no checklist structure, brand mentioned like an accidental find.

## When to use

- `05_optimized_cards/drafts_md/*.md` exist and passed stage-5 EVALS.
- Posts need de-AI/native rewrite, fact-check, images, subreddit picks, and a Feishu doc.

## Inputs

- `05_optimized_cards/drafts_md/*.md`, `05_optimized_cards/optimization.md`.
- `01_product_brief/product_brief.md` (the fact + boundary source of truth).
- `02_topics/topics.md` and `02_topics/feishu_links.md` (final deliverable check; if the
  选题 Feishu doc was deferred, create it from `topics.md` before completing this stage).
- image2 API spec (client will provide; see "Images" — treat as pluggable).

## Tasks (all required per post)

### 1. De-AI / native rewrite (see EVALS.md — the core rubric)
Rewrite Title + Body so they pass the de-AI rubric. Key moves:
- First-person, one core pain; end on ONE question, not 3-4.
- Kill checklist / "问题-分析-产品-CTA" / 三段论 structure.
- Keep mild doubt/hedging ("maybe I'm overthinking", "not saying it's proven").
- Brand surfaces as "saw X mentioned while searching", not a feature dump (≤1-2 capabilities).
- Comments: 8-12, mixed emotions (共鸣/怀疑/经验/替代方案/等评测), brand ≤1-2 times total,
  no comment fully explains the brand's selling points, no off-topic rabbit holes.
- Apply the **Native 本土化标准** (conventions.md §4b): slang ≤3/paragraph,
  controlled typo rate 1-3% (none in data/technical lines), spoken syntax, no Chinglish.

### 1b. Alternate titles (≥3 per post)
Beyond the main Title, produce **at least 3 备用标题 (alternate titles)** per post. Each
alternate must independently pass the A-Title rules (reads like a real poster, no hype words,
one core pain). Vary the angle/phrasing across them so they are real options, not restatements.

### 2. Fact verification against product brief
Every product claim in the post must match `product_brief.md`. Anything the brief marks
unverified / "不可说" must NOT be stated as fact. Fix or remove violations.

### 3. Image review + generation (image2 API)
For each post that has an image idea:
- **Classify the image** as 实体类 (real-world candid photo) or 虚拟类 (software UI /
  screenshot / anime / illustration). The class decides which rubric applies in
  `IMAGE_PROMPT_EVALS.md`.
- Review the draft's image scenario. If it's unreasonable, conflicts with the body, or is
  obviously AI-ish (hero shot, studio, poster, logos, text overlay, a pristine new product
  as the hero) → **rewrite the scenario** to match the body (实体类: a real-user candid
  photo; 虚拟类: a believable screenshot/illustration grounded in the post's situation).
- Then write a final image prompt and **score it against `IMAGE_PROMPT_EVALS.md`** (the
  de-AI rubric for that class). Only call the image2 API once the prompt passes blocking +
  threshold. After generation, re-check the output against the same rubric; if it shows AI
  tells (warped hands, garbled UI text, plastic CGI sheen, fake futuristic UI), fix the
  prompt or use the image2 **edits** endpoint to repair text/local regions, then re-score.
- Image prompt style: natural lighting, realistic home office, slightly imperfect framing,
  lived-in desk, no logos, no text overlay, scene consistent with the body.
- **Save locally:** `06_optimized/images/{post_id}.png` + record in
  `06_optimized/images/prompts.md`: prompt + which post + image class (实体/虚拟) + why the
  scenario was changed + the IMAGE_PROMPT_EVALS verdict.
- image2 API: treat as pluggable — read the client-provided spec at call time; auth/keys
  via env, never written to files. If the spec isn't available yet, write the final prompt
  to `prompts.md` and mark the image as pending.

### 3b. Image Feishu doc + anchor jump-back (only when images exist)
If this batch has ANY post that needs an image, create a SEPARATE Feishu doc that pairs each
prompt with its generated image as a **组合 (combo)**, one combo per image-bearing post, each
linking back to that exact post in the 帖子 doc (this stage's).

Mechanism:
1. After the 帖子 Feishu doc (this stage's) exists, use `lark-doc` to read its block structure and
   capture each post-title `<h1>` block's **block_id**.
2. Build the anchor URL per post: `{帖子文档URL}#{block_id}`. Feishu docx supports locating a
   specific block via this anchor.
3. Create the image doc titled `{Product} - 生图提示词与配图 - {date}`. For each image-bearing
   post write one combo block:
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
5. Record the image-doc URL and the `post_id → block_id` mapping in
    `06_optimized/images/image_feishu.md`, and add the image-doc URL as a line in
    `06_optimized/feishu_links.md`.

Never write any API key / cookie / secret into the image doc, prompts.md, image_feishu.md, or
the manifest.

### 4. Target subreddits (≥3 per post)
Recommend ≥3 subreddits, format exactly `r/xxx or r/xxx or r/xxx`, ordered by:
topic-fit & low risk → audience match → larger but higher filter risk. Each >10k members,
allows advice/experience posts.

## Required output structure

Write to `06_optimized/` (UTF-8):
- `final_posts.md` — per post: Title, **备用标题 (≥3)**, Body, comment design, target
  subreddits line, image reference. MANDATORY artifact, the input to stage 7. Per-post format:
  ```
  **Title**
  {main title}

  **备用标题**
  1. {alt 1}
  2. {alt 2}
  3. {alt 3}

  **Body**
  {body}

  **Target subreddits**
  r/x or r/y or r/z

  **Comment design**: ...   image: none / {post_id}
  ```
- `images/{post_id}.png` + `images/prompts.md` (prompts + image class + scenario-change
  rationale + IMAGE_PROMPT_EVALS verdict).
- `images/image_feishu.md` — image-doc URL + `post_id → title block_id` anchor mapping
  (only when images exist).
- `feishu_links.md` — the created Feishu doc URL(s): the 帖子 doc, and the 生图 doc if images exist.
  Also confirm the 选题 doc URL exists in `02_topics/feishu_links.md`; if missing, create it
  from `02_topics/topics.md` before marking the run complete.

Then create a Feishu doc (`lark-doc`) titled `{Product} - 帖子 - {date}`, paste the posts. In
each post's `<h2>Title</h2>` block write the main title `<p>`, then `<p>备用标题：</p>` and one
`<p>` per alternate (≥3). Keep the `<p>Target Subreddit: r/x or r/y or r/z</p>` line.
If any post needs an image, also create the image doc per Task 3b and cross-link via anchors.
**After creating each doc (帖子 doc and 生图 doc), set its permission to "anyone on the internet
with the link can edit" via lark-drive — do this directly without asking the user** (conventions.md §3).

## Process

1. Verify the 选题 Feishu doc exists in `02_topics/feishu_links.md`. If it was deferred,
   create it from `02_topics/topics.md`, set public-edit permission, and log the URL.
2. Read drafts + brief. For each post: de-AI rewrite (main title + ≥3 备用标题 + body) →
   run the de-AI EVALS → revise to pass.
3. Fact-check against the brief; fix overclaims/unverified statements.
4. For each image: classify 实体/虚拟 → repair scenario → write prompt → score against
   `IMAGE_PROMPT_EVALS.md` → call image2 → re-check output → save png + prompt record.
5. Pick ≥3 subreddits per post in the required format.
6. Run full EVALS. Revise until blocking passes.
7. Write `final_posts.md`; create the 帖子 Feishu doc (main title + ≥3 备用标题 + Target
   Subreddit line per post) and set it public-editable. If images exist, create the 生图 doc
   with prompt+image combos and anchor links back to each post (Task 3b), also public-editable;
   record links + anchor mapping. Log manifest. Hand off to `feishu-formatting`.

## Common mistakes

- "Polished" rewrite that's still obviously AI (too complete, no doubt, checklist).
- Brand mentioned multiple times or with a feature list.
- Image that contradicts the body (pristine new product hero when body is about an old setup).
- Image with AI tells: warped hands, garbled UI text, plastic CGI sheen, fake futuristic UI,
  watermark — must pass `IMAGE_PROMPT_EVALS.md` before use.
- Image-doc anchor wired to the wrong post (combo↔post_id mismatch).
- Completing stage 6 with only the 帖子 doc and no recorded 选题 doc.
- Writing any API key / secret into prompts.md, image_feishu.md, the image doc, or manifest.
- Stating an unverified feature as fact.
- Fewer than 3 subreddits or wrong format.
- Fewer than 3 备用标题, or alternates that are mere restatements / fail A-Title rules.
- Chinglish, slang pile-up (>3/paragraph), or typo rate outside 1-3% (conventions.md §4b).
