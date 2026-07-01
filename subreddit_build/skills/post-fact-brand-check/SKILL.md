---
name: post-fact-brand-check
description: Use after the native rewrite (stage 6a), when verifying every product claim in a Reddit post against the product brief and checking brand-exposure safety (stumbled-on framing, ≤1-2 capabilities, disclosure, no competitor attack, no fabricated data). Stage 6b of the subreddit build workflow. Does NOT rewrite for nativeness, pick subreddits, make images, or touch Feishu.
---

# Post Fact & Brand-Safety Check (Stage 6b)

## Overview

The native text from 6a may read great but still overclaim or expose the brand like an ad.
This sub-skill is the **truth + safety gate**: every product claim must trace to the product
fact index, nothing marked unverified / "不可说" may be stated as fact, and brand exposure must read
as an accidental find, not a pitch. It fixes violations in place but must NOT undo 6a's
nativeness.

**Core principle:** a believable-but-false post is worse than a plain one. Accuracy and brand
safety are non-negotiable; preserve the native voice while correcting facts.

## Context (subagent isolation)

Run as an isolated worker (CONTEXT_CONTRACT.md). You receive ONLY:
- Global: run folder, `run_config.json`, `conventions.md`, `global/product_fact_index.json`,
  `global/claim_boundary_table.json`, and `global/brand_safety_rules.md` (the fact + boundary
  source of truth).
- Stage-local input: `06_optimized/native_posts.md` (6a output).

## Tasks (per post)

### 1. Fact verification against the product fact index
Every product claim in Title, Body, and comments must match `global/product_fact_index.json`
and the claim boundary table. Anything marked unverified / "不可说" must NOT be stated as
fact. Fix or remove violations. No fabricated revenue / benchmark / review / screenshot.

### 2. Brand-exposure safety
- Brand surfaces as a "stumbled-on option" ("saw X mentioned while searching"), not "this
  product solves my problem".
- ≤1-2 capabilities per mention; no multi-feature pitch in the body.
- Disclose the relationship where the post recommends / compares / reviews the client product.
- No competitor attack — comparisons read as "different tools fit different stages".
- Brand mentioned ≤1-2 times total across the comment section; no single comment fully sells it.

### 3. Preserve nativeness
When you edit a line for facts/brand, keep it native (conventions.md §4b). Do not turn it back
into formal/AI prose. If a fix would damage the voice, rephrase natively rather than reverting.

## Required output structure

Write to `06_optimized/checked_posts.md` (UTF-8): the same per-post structure as
`native_posts.md` (Title / 备用标题 / Body / Comment design / image idea), now fact- and
brand-safe. Add a short `**check log**` line per post listing what was changed and why (claim
corrected, unverified feature removed, brand reframed, disclosure added) — or "no changes".

## Process

1. Read `native_posts.md` + the compressed global fact and brand files.
2. Per post: check every claim against the fact index + "不可说" table; fix overclaims.
3. Check brand framing / count / disclosure / competitor tone; fix violations natively.
4. Write `checked_posts.md` with the per-post check log. STOP — hand to the evaluator worker
   (EVALS.md), then to 6c.

## Common mistakes

- Leaving an unverified ("不可说") feature stated as fact.
- Brand mentioned multiple times or with a feature list still present from 6a.
- Reverting native lines into formal/AI prose while "fixing" them.
- Adding a competitor attack while differentiating.
- Inventing data/screenshots to make a claim land.
- Doing 6a/6c/6d work (style rewrite, subreddits, images, Feishu) — out of scope.

