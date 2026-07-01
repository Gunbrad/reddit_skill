---
name: feishu-formatting
description: Use as the final step after optimized posts are in a Feishu doc, when applying the Feishu Reddit-post layout standard (h1/h2 structure, comment reformatting, User-X renaming, brand highlight, OP-reply removal), or when a Feishu post draft needs its formatting normalized. Stage 7 of the Reddit posting pipeline.
---

# Feishu Formatting + Comment Normalization (Stage 7)

## Overview

Normalize the Feishu post doc into the house layout standard and make the comment section
read native. This stage edits the Feishu doc **block-by-block** (never full overwrite) and
verifies the result. It is the last gate before the post is considered done.

**Core principle:** structure is strict (only specific heading levels survive, metadata is
deleted, brand words are highlighted), but resources (images/素材) must be preserved exactly.

## When to use

- Optimized posts exist in a Feishu doc (stage 6 output).
- The doc needs layout normalization + comment cleanup + brand highlight.

## Inputs

- The Feishu doc URL from `06_optimized/feishu_links.md`.
- Brand word list (from product brief) for highlighting.

## Layout rules (the standard)

### Heading levels
- `<h1>` = each post title (第一篇 / 第二篇 ...).
- `<h2>` = ONLY four allowed: `Title`/`标题`, `素材`, `Body`/`正文`, `评论设计`. Use one
  language consistently.
- Everything else = `<p>` (main title, 备用标题 lines, Target Subreddit line, body paragraphs, comments).
- Delete ALL other headings (Tree 1, Comment Trees, Standalone, h3 tags, etc.).

### Must-preserve blocks (NEVER delete)
- **素材 block** — structure + content intact (incl. Engagement Kit etc.).
- **Target Subreddit line** (`r/x or r/y or r/z`, ≥3) — keep as `<p>` under its post.
- **备用标题 block** (≥3 alternate titles) — keep under the post's `<h2>Title</h2>`, below the main title, each as `<p>`.
- **Resource blocks** (`<img>`/`<source>`/`<whiteboard>`).

### Blocks
- **素材 block: NEVER delete** — preserve structure and content (incl. Engagement Kit etc.).
- **Metadata block (Post Type / Flair / Link Permissibility ...): DELETE entirely.**
- Under `<h2>Title</h2>`: main title `<p>`, then `<p>备用标题：</p>` + one `<p>` per alternate
  (≥3). Keep all; do not promote any to a heading.
- Body paragraphs in `<p>`; keep blank-line `<p> </p>` separators between body paragraphs.
- Keep the Target Subreddit `<p>` line (≥3 subreddits) in its post.
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
native signals per the **Native 本土化标准** (conventions.md §4b): natural
slang ≤3/comment, native-style typos at 1-3% rate, personal anecdotes, emotion, no Chinglish.
Do NOT change body/title text; preserve all resource blocks and separators.

## Process

1. Read the doc structure + block ids first (don't blind-overwrite). Identify Title/备用标题/
   Target Subreddit/素材/Body/评论设计/images/metadata.
2. Apply layout rules via block-level edits: fix headings, delete metadata, normalize
   comments, rename users, delete OP replies, strip empty paragraphs. Keep 备用标题 (≥3) and
   the Target Subreddit line intact.
3. Highlight all brand-word case variants with `str_replace`.
4. Native pass on comments (delete AI-tell ones).
5. Re-read with `--detail full`: confirm 素材 intact, metadata gone, brand spans written,
   headings correct, no OP replies, separators kept, 备用标题 (≥3) and Target Subreddit (≥3) present.
   Also confirm the doc permission is still "anyone with the link can edit" (conventions.md §3);
   if it isn't, set it via lark-drive directly — no need to ask the user.
6. Run EVALS (the compliance checklist). Fix any failure. Write `07_format/format_report.md`
   (what changed, what was preserved incl. 备用标题 + Target Subreddit, verification result). Log manifest.

## Common mistakes

- Full-document overwrite → destroys images/素材.
- Forgetting to delete the Metadata block, or accidentally deleting 素材.
- Deleting / dropping the Target Subreddit line or the 备用标题 block.
- Promoting 备用标题 to a heading (must stay `<p>` under the Title h2).
- Missing brand-word case variants, or highlighting non-brand lookalikes.
- Leaving OP reply comments in.
- Verifying with `--detail simple` (misses whether span tags were actually written).

