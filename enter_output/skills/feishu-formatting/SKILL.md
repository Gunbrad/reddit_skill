---
name: feishu-formatting
description: Use as the final step after optimized posts are in a Feishu doc, when applying the Feishu Reddit-post layout standard (h1/h2 structure, comment reformatting, User-X renaming, brand highlight, OP-reply removal), or when a Feishu post draft needs its formatting normalized. Stage 6 of the Reddit posting pipeline.
---

# Feishu Formatting + Comment Normalization (Stage 6)

## Overview

Normalize the Feishu post doc into the house layout standard and make the comment section
read native. This stage edits the Feishu doc **block-by-block** (never full overwrite) and
verifies the result. It is the last gate before the post is considered done.

**Core principle:** structure is strict (only specific heading levels survive, metadata is
deleted, brand words are highlighted), but resources (images/素材) must be preserved exactly.

## When to use

- Optimized posts exist in a Feishu doc (stage 5 output).
- The doc needs layout normalization + comment cleanup + brand highlight.

## Inputs

- The Feishu doc URL from `05_optimized/feishu_links.md`.
- Brand word list (from product brief) for highlighting.

## Layout rules (the standard)

### Heading levels
- `<h1>` = each post title (第一篇 / 第二篇 ...).
- `<h2>` = ONLY four allowed: `Title`/`标题`, `素材`, `Body`/`正文`, `评论设计`. Use one
  language consistently.
- Everything else = `<p>` (Target Subreddit line, body paragraphs, comments).
- Delete ALL other headings (Tree 1, Comment Trees, Standalone, h3 tags, etc.).

### Blocks
- **素材 block: NEVER delete** — preserve structure and content (incl. Engagement Kit etc.).
- **Metadata block (Post Type / Flair / Link Permissibility ...): DELETE entirely.**
- Body paragraphs in `<p>`; keep blank-line `<p> </p>` separators between body paragraphs.
- 评论设计 must start with `<h2>评论设计</h2>`; merge Standalone + Comment Trees under it.

### Comment formatting
- Replace all real usernames (`u/xxx`) with `User 1`, `User 2`... numbered per thread.
- Use `User X replies to User Y` (not parentheses / "replying to"); wrap in `<b>`.
- Thread separators `<hr/>` / `---`: KEEP.
- Delete all `Tree N` labels. Convert `Standalone N` → `**User N**`.
- Delete empty paragraphs in the comment section (`<p></p>` / `<p> </p>`).
- No blockquote `>` in comments — plain paragraphs.
- **Delete OP's own reply comments** (OP replying with product backing/feature/price/
  competitor info = delete-risk). Keep other users' comments and thread flow intact.

### Brand highlight
- Highlight EVERY brand word (all case variants) with
  `<span background-color="light-yellow">brand</span>`.
- Highlight everywhere (body, comments, titles). Do NOT highlight non-brand lookalike words.
- Use `str_replace` per case variant. Verify with `--detail full` (simple detail omits
  inline span tags).

## Comment content quality (native pass)
Apply the de-AI comment standard (delete AI-tell comments): over-complete structure, formal
vocab, no personal specifics, review-like listing, neutral customer-service tone. Keep
native signals: natural slang, personal anecdotes, emotion, light typos (≤3%). Do NOT
change body/title text; preserve all resource blocks and separators.

## Process

1. Read the doc structure + block ids first (don't blind-overwrite). Identify Title/素材/
   Body/评论设计/images/metadata.
2. Apply layout rules via block-level edits: fix headings, delete metadata, normalize
   comments, rename users, delete OP replies, strip empty paragraphs.
3. Highlight all brand-word case variants with `str_replace`.
4. Native pass on comments (delete AI-tell ones).
5. Re-read with `--detail full`: confirm 素材 intact, metadata gone, brand spans written,
   headings correct, no OP replies, separators kept.
6. Run EVALS (the compliance checklist). Fix any failure. Write `06_format/format_report.md`
   (what changed, what was preserved, verification result). Log manifest.

## Common mistakes

- Full-document overwrite → destroys images/素材.
- Forgetting to delete the Metadata block, or accidentally deleting 素材.
- Missing brand-word case variants, or highlighting non-brand lookalikes.
- Leaving OP reply comments in.
- Verifying with `--detail simple` (misses whether span tags were actually written).
