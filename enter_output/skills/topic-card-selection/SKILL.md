---
name: topic-card-selection
description: Use after Topic Cards are generated, when screening every topic card with a binary pass/fail gate to keep only the cards that are community-compliant, product-relevant, production-ready, and low-risk. Stage 4 of the Reddit posting pipeline. Does NOT pick a top-N or write drafts — that is stage 5 (topic-card-optimization).
---

# Topic Card Screening (binary gate) (Stage 4)

## Overview

Screen **every** generated Topic Card with a **binary pass/fail gate**. The only question
here is: *can this card safely enter the production pipeline?* — i.e. is it
community-compliant, product-relevant, writable into a real post, and low brand-risk.
Every card that passes moves on to stage 5; failing cards are dropped with a recorded reason.

**Core principle:** this stage is a SAFETY/READINESS filter, not a quality ranking. Do NOT
rank, do NOT pick a top-N, do NOT write supplemental notes or drafts here — that is stage 5
(`topic-card-optimization`). Keep the bar at "production-safe", and let stage 5 find the
viral winners among the passers.

## When to use

- `03_search/topic_cards/*.md` exist and passed stage-3 EVALS (Gate C).
- You need to filter the full card set down to the production-safe subset.

Not for: viral-potential ranking, supplemental notes, or drafting (stage 5).

## Inputs

Read only the files allowed by `INPUTS.md`.

- `03_search/handoff_packet.json`, `03_search/topic_cards/{direction_id}.json`, the occupancy
  maps, `03_search/occupancy_heat_evidence.json`, and `run_meta.json`.
- `global/product_fact_index.json`, `global/claim_boundary_table.json`, and
  `global/brand_safety_rules.md` for capability boundary and red lines. Do not read the full
  product brief unless the compressed files are missing a needed fact and the manifest records why.
- `run_config.json` (no count knobs apply here — the gate judges every card; total is whatever stage 3 produced, not forced to 36).

## The binary gate (judge EVERY card pass/fail)

A card **PASSES** only if ALL of these hold; otherwise it FAILS:

1. **Community-compliant** — its `target_subreddit` allows this kind of advice/experience
   post; not a community hostile to the topic or to any self-promo.
2. **Production-ready** — required fields are complete and coherent (title_direction,
   content_form, post_format, expression_mechanism, brand_exposure_method, target_subreddit);
   it describes a writable post with a real, identifiable user pain (not a vague stub).
3. **Product-relevant** — the card's user pain, subreddit, and planned brand exposure trace
   to the current product brief: a priority persona/pain, a verified capability, or a stated
   differentiation. A generally interesting Reddit topic FAILS if it cannot lead to a
   truthful, natural mention of this product.
4. **Low risk** — does not require an unverified / "不可说" feature from the brief; does not
   read as a pure ad / feature dump; no red-line violation; brand exposure is at most a
   natural mention.

Borderline cards that need only a small fix to be safe can pass **with a noted caveat**; cards
that would need fabrication, overclaim, or a hostile-community move FAIL.

## Required output structure

Write to `04_screen/` (UTF-8):
- `screening.md` — MANDATORY artifact. A row per card:
  ```
  | topic_id | direction | target_subreddit | verdict | reason |
  |----------|-----------|------------------|:------:|--------|
  | t_003_01 | direction_003 | r/SaaS | PASS | real pain, fields complete, brand只软提及 |
  | t_004_07 | direction_004 | r/webdev | FAIL | 需要未验证的 Analytics 数据当事实 |
  ```
  Then a `## Passed set` list of the passing topic_ids (this is the handoff to stage 5).
- update `run_meta.json` with `screened_pass_ids` (the passing topic_ids).

## Process

1. Load ALL current-run cards + maps + compressed global files. For each card, apply the
   4-part binary gate.
2. Record verdict + reason per card in `screening.md`; collect the passing topic_ids.
3. Run EVALS (screening completeness + correctness). Fix any mis-judgment.
4. Log manifest. Hand off the passing set to `topic-card-optimization`.

## Common mistakes

- Ranking or picking a top-N here (that's stage 5).
- Writing supplemental notes or firing the draft job here (that's stage 5).
- Passing a card that needs an unverified feature or fabricated data.
- Passing a card that is safe in general but not connected to the current product's personas,
  pains, verified capabilities, or differentiation.
- Failing a card just for being "average" — average-but-safe still PASSES (stage 5 ranks).
- Forcing the count to 36 — the total is whatever stage 3 generated.
