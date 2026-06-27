---
name: reddit-post-optimization
description: Use when SmartContent raw drafts need factual review, Reddit-native rewriting, target-subreddit recommendations, Feishu draft-document creation, image prompt review/generation, and local final post artifacts.
---

# Reddit Post Optimization

## Purpose

Turn raw generated drafts into publishable Reddit-ready post packages. This skill checks product truth, reduces AI-style language, improves native Reddit tone, creates a Feishu review document, recommends target communities, and handles image prompt/image assets when a post needs visuals.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/output-templates.md`
- `../../shared/eval-loop.md`
- `../../evals/05-post-optimization-eval.md`

## Inputs

- `04_card_selection/raw_drafts.md`
- `04_card_selection/topic_card_scores.md`
- Product brief and fact bank.
- Client feedback.
- Image2 API documentation or credentials, if available.

## Workflow

1. Load raw drafts, selected topic notes, and product fact bank.
2. Create or update a Feishu cloud document for the raw draft review package.
3. For each draft, identify:
   - Intended subreddit(s).
   - Post type and format.
   - Disclosure need.
   - Product claims used.
   - Risky or unsupported claims.
   - AI-language patterns.
   - Whether a visual asset is needed.
4. Rewrite and optimize:
   - Preserve the core Reddit intent.
   - Make language natural and community-native.
   - Keep skepticism and trade-offs where useful.
   - Remove ad-like phrasing.
   - Correct product facts.
   - Keep brand mention proportional and disclosed where needed.
5. Recommend at least three target subreddits for each post:
   - One primary.
   - Two or more alternates.
   - Include reason and risk for each.
6. Handle image needs:
   - Decide whether the post truly needs an image.
   - If an image prompt exists, audit the scene for realism and AI smell.
   - Rewrite the scene if it is implausible, too polished, too literal, or too promotional.
   - Save `05_posts/images/{post_id}/image_prompt.md`.
   - If image2 API is available, generate the image and save it locally with metadata.
   - If image2 API is unavailable, save the final prompt and mark generation as blocked.
7. Save final posts to `05_posts/optimized_posts.md`.
8. Save image prompts/assets under `05_posts/images/`.
9. Update Feishu post doc with optimized drafts and image references.
10. Update `manifest.json`.
11. Run the paired eval and revise until it passes.

## Native Reddit Language Rules

Prefer:

- Specific details, small frustrations, and concrete trade-offs.
- Imperfect but readable language.
- Natural contractions and sentence variety.
- Direct questions that invite replies.
- Skepticism about the product when disclosure is needed.
- Community vocabulary from the search maps.

Avoid:

- "In today's fast-paced world".
- Balanced essay structures that read like a blog post.
- Overexplaining obvious context.
- Generic praise.
- Feature dumps.
- Excessive slang.
- Fake personal experience, fake metrics, fake screenshots, or fake customer outcomes.

## Product Truth Rules

- Every product claim must map back to the product brief fact bank.
- If a claim is unverified, remove it or rewrite as a question/uncertain note.
- Do not imply the product replaces engineers, removes all migration work, guarantees revenue, or handles regulated/security-sensitive work without review unless explicitly verified.
- Competitor comparisons must be framed as trade-offs, not attacks.

## Image Prompt Rules

An acceptable image prompt describes:

- Realistic scene.
- Purpose of image in the post.
- Objects, layout, and context.
- Any product UI or device details that are verified.
- Style constraints.
- What to avoid.

Reject prompts that:

- Look like glossy ads.
- Put impossible UI/data on screen.
- Show unverified product claims.
- Use vague "futuristic AI" imagery.
- Add fake logos, fake reviews, or fake metrics.

## Output Contract

Save:

- `05_posts/optimized_posts.md`
- `05_posts/images/{post_id}/image_prompt.md` for every image-needed post.
- `05_posts/images/{post_id}/image_metadata.json` if an image is generated.
- Generated image files, if any.
- `eval_reports/05_post_optimization_eval.md`

## Handoff

Hand off:

- Optimized posts path.
- Feishu posts doc URL/token.
- Image prompts and asset paths.
- Per-post target subreddit list.
- Product claims that were removed or weakened.
- Remaining client-confirmation questions.
