---
name: reddit-post-formatting
description: Use when optimized Reddit post drafts must be converted into final Feishu/local formatting with strict heading structure, comment cleanup, user anonymization, brand highlighting, and final QA.
---

# Reddit Post Formatting

## Purpose

Apply final formatting and comment cleanup so posts are ready for client review or publishing handoff. This skill is formatting-focused: preserve approved post meaning while normalizing headings, comments, usernames, brand highlighting, and metadata removal.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/eval-loop.md`
- `../../evals/06-post-formatting-eval.md`

## Inputs

- `05_posts/optimized_posts.md`
- Feishu posts doc URL/token, if available.
- Brand names and case variants.
- Image assets or image prompt paths.

## Workflow

1. Load optimized posts and image references.
2. For each post, format into the final structure:
   - H1: post number or internal post name.
   - Target subreddit line as paragraph.
   - H2 sections only:
     - `Title`
     - `素材` when materials/images exist.
     - `Body`
     - `评论设计`
3. Remove metadata blocks that are not meant for final review.
4. Preserve material blocks and image references.
5. Convert comment trees:
   - Remove tree labels.
   - Remove blockquote markers.
   - Convert usernames to `User 1`, `User 2`, etc.
   - Use `User X replies to User Y` for replies.
   - Preserve separators between threads.
6. Remove OP replies that explain, defend, or promote the product from the brand-side perspective.
7. Clean comments for native feel:
   - Delete comments that read like product reviews, customer support, or AI essays.
   - Keep useful skepticism, pushback, and specific experiences.
8. Highlight all brand terms and case variants with light-yellow span markup in the Feishu/local artifact.
9. Save local formatted output to `06_formatted/formatted_posts.md`.
10. Apply the same formatting to Feishu when a document is available.
11. Run the paired eval and fix formatting until it passes.
12. Update `manifest.json`.

## Formatting Rules

- Do not introduce new post claims while formatting.
- Do not rewrite approved body text unless required for formatting cleanup.
- Preserve empty spacing in body paragraphs when it improves readability.
- Remove empty paragraphs inside comment design.
- Do not leave `Tree`, `Standalone`, `Comment Trees`, or metadata headings.
- Do not use H3/H4 headings in final output.
- Brand highlighting must cover all variants without highlighting unrelated substrings.

## Output Contract

Save:

- `06_formatted/formatted_posts.md`
- `06_formatted/formatting_report.md`
- `eval_reports/06_post_formatting_eval.md`

## Handoff

Hand off:

- Final formatted local path.
- Feishu document URL/token.
- Formatting eval report.
- Any comments deleted and why.
- Any brand terms that could not be safely highlighted.
