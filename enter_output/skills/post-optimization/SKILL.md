---
name: post-optimization
description: Use after drafts are generated, when making Reddit posts sound native (de-AI), when verifying posts against product facts, when reviewing or generating post images via the image2 API, or when recommending target subreddits and writing posts into Feishu. Stage 5 of the Reddit posting pipeline.
---

# Post Optimization (de-AI, native, images, subreddits) (Stage 5)

## Overview

Take the generated drafts and turn them into posts that read like a real Reddit user wrote
them: de-AI'd, native, fact-accurate, with vetted images and concrete target subreddits.
Then write them into a Feishu doc for stage 6. This is the **deepest** stage — its EVALS
(the de-AI / native rubric) is the heart of quality control.

**Core principle:** native ≠ polished. Real Reddit posts are slightly messy: one core
question, a little doubt, no checklist structure, brand mentioned like an accidental find.

## When to use

- `04_drafts/drafts_md/*.md` exist and passed stage-4 EVALS.
- Posts need de-AI/native rewrite, fact-check, images, subreddit picks, and a Feishu doc.

## Inputs

- `04_drafts/drafts_md/*.md`, `selection.md`.
- `01_product_brief/product_brief.md` (the fact + boundary source of truth).
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

### 2. Fact verification against product brief
Every product claim in the post must match `product_brief.md`. Anything the brief marks
unverified / "不可说" must NOT be stated as fact. Fix or remove violations.

### 3. Image review + generation (image2 API)
For each post that has an image idea:
- Review the draft's image scenario. If it's unreasonable, conflicts with the body, or is
  obviously AI-ish (hero shot, studio, poster, logos, text overlay, a pristine new product
  as the hero) → **rewrite the scenario** to a real-user candid photo that matches the body.
- Then write a final image prompt and call the image2 API to generate.
- Image prompt style: natural lighting, realistic home office, slightly imperfect framing,
  lived-in desk, no logos, no text overlay, scene consistent with the body.
- **Save locally:** `05_optimized/images/{post_id}.png` + record the prompt in
  `05_optimized/images/prompts.md` (prompt + which post + why the scenario was changed).
- image2 API: treat as pluggable — read the client-provided spec at call time; auth/keys
  via env, never written to files. If the spec isn't available yet, write the final prompt
  to `prompts.md` and mark the image as pending.

### 4. Target subreddits (≥3 per post)
Recommend ≥3 subreddits, format exactly `r/xxx or r/xxx or r/xxx`, ordered by:
topic-fit & low risk → audience match → larger but higher filter risk. Each >10k members,
allows advice/experience posts.

## Required output structure

Write to `05_optimized/` (UTF-8):
- `final_posts.md` — per post: Title, Body, comment design, target subreddits line, image
  reference. MANDATORY artifact, the input to stage 6.
- `images/{post_id}.png` + `images/prompts.md` (prompts + scenario-change rationale).
- `feishu_links.md` — the created Feishu doc URL.

Then create a Feishu doc (`lark-doc`) titled `{Product} - 帖子 - {date}`, paste the posts.

## Process

1. Read drafts + brief. For each post: de-AI rewrite → run the de-AI EVALS → revise to pass.
2. Fact-check against the brief; fix overclaims/unverified statements.
3. Review/repair each image scenario; write final prompt; call image2; save png + prompt.
4. Pick ≥3 subreddits per post in the required format.
5. Run full EVALS. Revise until blocking passes.
6. Write `final_posts.md`; create Feishu doc; record links. Log manifest. Hand off to `feishu-formatting`.

## Common mistakes

- "Polished" rewrite that's still obviously AI (too complete, no doubt, checklist).
- Brand mentioned multiple times or with a feature list.
- Image that contradicts the body (pristine new product hero when body is about an old setup).
- Stating an unverified feature as fact.
- Fewer than 3 subreddits or wrong format.
