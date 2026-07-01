---
name: post-native-rewrite
description: Use after Stage 5 community draft generation, when rewriting Reddit post Title + Body + comment section to read like a real native poster (de-AI), preserving viral intent, checking fact/brand safety, producing ≥3 alternate titles per post, and writing publish-ready final_posts.md for Feishu publishing.
---

# Post Native Rewrite (de-AI Title + Body + comments) (Stage 6a)

## Overview

Take the generated drafts and make the **text** read like a real Reddit user wrote it:
de-AI'd, native, with a believable comment section and ≥3 alternate titles per post. In this
subreddit-build workflow, this stage also performs the fact/brand safety pass because the first
version does not split out separate 6b/6c workers.

**Core principle:** native ≠ polished. Real Reddit posts are slightly messy: one core
question, a little doubt, no checklist structure. BUT native ≠ flattened — the Stage 5 viral
intent (hook, contrast, concrete scene, discussion engine) MUST survive the de-AI pass.

## Preserve Stage 5 viral intent (BLOCKING)

The Stage 5 `handoff_packet.json` gives each post a `viral_intent` (`core_hook`,
`emotional_trigger`, `comment_engine`, `must_preserve[]`) plus `title_pattern_to_preserve`.
De-AI'ing must NOT sand these off. A post that reads perfectly native but has lost its hook,
contrast, concrete details, or discussion driver is a FAIL (EVALS VP1-VP4). Rewrite for voice
while keeping the tension and specifics that make it spread.

## Context (subagent isolation)

Run as an isolated worker (CONTEXT_CONTRACT.md). You receive ONLY:
- Global: run folder, `run_config.json`, `global/product_fact_index.json`,
  `global/claim_boundary_table.json`, `global/brand_safety_rules.md`, `conventions.md`.
- Stage-local input: the Stage 5 `handoff_packet.json` (the per-post `viral_intent`) and
  `05_optimized_cards/drafts_md/{post_id}.md` for the chosen posts only.

Do not read raw crawl dumps, old retrieval rounds, the full product brief, or other stages'
working files (see INPUTS.md forbidden list).

## Tasks (per post)

### 1. De-AI / native rewrite (see EVALS.md — the core rubric)
Rewrite Title + Body so they pass the de-AI rubric. Key moves:
- First-person, one core pain; end on ONE question, not 3-4.
- Kill checklist / "问题-分析-产品-CTA" / 三段论 structure.
- Keep mild doubt/hedging ("maybe I'm overthinking", "not saying it's proven").
- Brand surfaces as "saw X mentioned while searching", not a feature dump (≤1-2 capabilities).
  Because this workflow has no separate 6b, verify every product claim against the compressed
  fact files and remove unverified/"不可说" claims here.
- Apply the **Native 本土化标准** (conventions.md §4b): slang ≤3/paragraph,
  controlled typo rate 1-3% (none in data/technical lines), spoken syntax, no Chinglish.

### 2. Alternate titles (≥3 per post)
Beyond the main Title, produce **at least 3 备用标题** per post. Each independently passes the
A-Title rules (reads like a real poster, no hype words, one core pain). Vary the angle so they
are real options, not restatements.

### 3. Comment section (native)
Design 8-12 comments per post, mixed emotions (共鸣/怀疑/经验/替代方案/等评测), real
disagreement present, brand mentioned ≤1-2 times total, no single comment fully sells the
brand, no off-topic rabbit holes. Apply the Native 本土化标准 to comments too.

### 4. Publish-ready copy

After the evaluator passes, write the same approved content to `06_optimized/final_posts.md`.
This is the exact source that `post-feishu-publish` reads.

## Required output structure

Write to `06_optimized/native_posts.md` and `06_optimized/final_posts.md` (UTF-8). One block
per post:
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
{8-12 comments, native, mixed emotions; usernames as placeholders are fine}

**Target Subreddit**
r/{target_subreddit}
```

Do not generate images in this workflow version.

## Process

1. Read the Stage 5 handoff packet + chosen drafts only. Use the handoff for the 选题 anchor,
   viral_intent, title pattern, expected comments, and subreddit risk note.
2. Per post: de-AI rewrite (main title + ≥3 备用标题 + body) → comment design.
3. Check facts and brand exposure against global fact/brand files.
4. Apply the Native 本土化标准 throughout.
5. Write `native_posts.md` and `final_posts.md`. STOP — hand off to the evaluator worker, then to `post-feishu-publish`.

## Common mistakes

- "Polished" rewrite that's still obviously AI (too complete, no doubt, checklist).
- Brand written like an ad / feature list.
- Fewer than 3 备用标题, or alternates that are mere restatements / fail A-Title rules.
- Chinglish, slang pile-up (>3/paragraph), or typo rate outside 1-3% (conventions.md §4b).
- Writing final Feishu docs here; publishing belongs to `post-feishu-publish`.

