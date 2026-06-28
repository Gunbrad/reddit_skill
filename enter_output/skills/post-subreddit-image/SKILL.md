---
name: post-subreddit-image
description: Use after a post is fact- and brand-checked (stage 6b), when recommending ≥3 target subreddits per post and when reviewing/generating de-AI post images via the image2 API. Produces the consolidated final_posts.md that feeds Feishu publishing. Stage 6c of the Reddit posting pipeline. Does NOT rewrite text, fact-check, or touch Feishu.
---

# Post Subreddit Picks + Image Packaging (Stage 6c)

## Overview

Take the fact-/brand-checked posts and add the two "packaging" pieces a post needs before
publishing: **target subreddits** (≥3 per post) and **vetted images** (classified, scenario-
repaired, generated, and re-checked so they don't look AI-made or like an ad). Then write the
consolidated `final_posts.md` that 6d publishes to Feishu.

**Core principle:** an image must look like a real person snapped it / a real screenshot, not
a hero shot. The image rubric (`IMAGE_PROMPT_EVALS.md`) is blocking.

## Context (subagent isolation)

Run as an isolated worker (CONTEXT_CONTRACT.md). You receive ONLY:
- Global: run folder, `run_config.json`, `conventions.md`, `global/product_fact_index.json`,
  `global/claim_boundary_table.json`, and `global/brand_safety_rules.md`.
- Stage-local input: `06_optimized/checked_posts.md` (6b output).
- The image2 API spec (client-provided; treat as pluggable; auth/keys via env, never in files).
- `run_config.generate_images` ("auto" per the post's image idea | true | false).

## Tasks (per post)

### 1. Target subreddits (≥3 per post)
Recommend ≥3 subreddits, format exactly `r/xxx or r/xxx or r/xxx`, ordered:
topic-fit & low risk → audience match → larger but higher filter risk. Each >10k members,
allows advice/experience posts.

### 2. Image review + generation (image2 API)
For each post that has an image idea (and isn't disabled by `generate_images`):
- **Classify** the image as 实体类 (real-world candid photo) or 虚拟类 (software UI /
  screenshot / anime / illustration). The class decides which rubric applies in
  `IMAGE_PROMPT_EVALS.md`.
- Review the 6a image idea. If it's unreasonable, conflicts with the body, or is obviously
  AI-ish (hero shot, studio, poster, logos, text overlay, pristine new product as hero) →
  **rewrite the scenario** to match the body (实体类: a real-user candid photo; 虚拟类: a
  believable screenshot/illustration grounded in the post's situation).
- Write a final image prompt and **score it against `IMAGE_PROMPT_EVALS.md`**. Only call the
  image2 API once the prompt passes blocking + threshold. After generation, re-check the
  output against the same rubric; if it shows AI tells (warped hands, garbled UI text, plastic
  CGI sheen, fake futuristic UI), fix the prompt or use the image2 **edits** endpoint to repair
  text/local regions, then re-score.
- Image style: natural lighting, realistic home office, slightly imperfect framing, lived-in
  desk, no logos, no text overlay, scene consistent with the body.
- **Save locally:** `06_optimized/images/{post_id}.png` + record in
  `06_optimized/images/prompts.md`: prompt + which post + image class (实体/虚拟) + why the
  scenario was changed + the IMAGE_PROMPT_EVALS verdict.
- If the image2 spec isn't available yet, write the final prompt to `prompts.md` and mark the
  image **pending** (6d will record it as pending in the 生图 doc).

Never write any API key / cookie / secret into prompts.md or any artifact (conventions.md §6).

## Required output structure

Write to `06_optimized/` (UTF-8):
- `final_posts.md` — MANDATORY, the input to 6d. Per post:
  ```
  ## {post_id}

  **Title**
  {main title}

  **备用标题**
  1. {alt 1}
  2. {alt 2}
  3. {alt 3}

  **Body**
  {body}

  **Comment design**
  {the 6b comment section}

  **Target subreddits**
  r/x or r/y or r/z

  **image**: none / {post_id}  (+ class 实体/虚拟 if present; "pending" if not yet generated)
  ```
- `images/{post_id}.png` + `images/prompts.md` (prompts + image class + scenario-change
  rationale + IMAGE_PROMPT_EVALS verdict). Only when images exist.

## Process

1. Read `checked_posts.md` + compressed global fact/brand files. Per post: pick ≥3 subreddits
   in the required format.
2. For each image: classify 实体/虚拟 → repair scenario → write prompt → score against
   `IMAGE_PROMPT_EVALS.md` → call image2 (if spec available) → re-check output → save png + record.
3. Write `final_posts.md` (carrying Title + ≥3 备用标题 + Body + Comment design + Target
   subreddits + image ref). STOP — hand to the evaluator worker (EVALS.md), then to 6d.

## Common mistakes

- Fewer than 3 subreddits or wrong format.
- Image that contradicts the body (pristine new-product hero when body is about an old setup).
- Image with AI tells: warped hands, garbled UI text, plastic CGI sheen, fake futuristic UI,
  watermark — must pass `IMAGE_PROMPT_EVALS.md` before use.
- Dropping the 备用标题 / Comment design carried from 6a/6b (final_posts.md must keep them).
- Writing any API key / secret into prompts.md.
- Doing 6a/6b/6d work (rewrite, fact-check, Feishu) — out of scope.
