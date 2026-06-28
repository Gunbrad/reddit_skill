---
name: topic-card-optimization
description: Use after topic cards pass the stage-4 screening gate, when ranking the production-safe cards by viral (爆帖) potential, picking the top-N, writing per-card supplemental notes (including the originating 选题 so drafts don't drift), and firing the draft-generation job. Stage 5 of the Reddit posting pipeline.
---

# Topic Card Optimization (viral potential → top-N → notes → drafts) (Stage 5)

## Overview

Stage 4 already removed unsafe cards. This stage finds the **breakout (爆帖) winners** among
the production-safe passers: rank them by viral potential, pick the **top-N**, write a
**supplemental note** per chosen card (which MUST fold in the card's originating 选题 so the
generated draft stays on-direction), then **fire the draft-generation job** and hand the
drafts to stage 6.

**Core principle:** chase viral potential, but only *within* the guardrails — a card scores
on 爆帖 potential ONLY IF it first clears the gate of being community-compliant and NOT heavy
on AI/marketing/promo flavor. A viral idea that reads as an ad is not a winner here.

## When to use

- `04_screen/screening.md` exists with a passed set (stage-4 EVALS passed).
- You need to rank by viral potential, pick top-N, write notes, and generate drafts.

Not for: de-AI rewriting finished posts / images / Feishu (stage 6).

## Inputs

- `04_screen/screening.md` + `run_meta.json.screened_pass_ids` (the production-safe cards).
- `03_search/topic_cards/{direction_id}.json` (full card fields, only for passed ids), the occupancy `maps/`.
- `03_search/occupancy_heat_evidence.json` (**evidence for TopN — pick on data, not vibes**).
- `02_topics/topics.md` (**the 选题 — needed so notes keep drafts on-direction**).
- `run_meta.json.topic_to_direction` (maps each card's direction back to its 选题).
- `global/product_fact_index.json` + `global/brand_safety_rules.md` (capability boundary, red lines).
- `run_config.json` for `top_n`, `draft_length_multiplier`, `supplemental_context`.

## Step 1 — Score viral potential (see EVALS.md — the core rubric)

Score every passed card on the 爆帖 rubric. **Precondition gate (blocking): a card is only
eligible if it stays community-compliant AND is not heavy on AI/marketing/promo flavor.** Then
rank eligible cards by weighted viral score. (Full rubric in EVALS.md.)

## Step 2 — Pick top-N

N = `run_config.top_n` if set, else propose a count and confirm with the user. Pick the
highest-scoring eligible cards while keeping **diversity** (don't take N cards that are the
same subreddit + same angle). **Justify each pick with `occupancy_heat_evidence.json`** — cite
the similar_posts / title_patterns / comment_triggers / skepticism_angles that make the card
likely to break out, not just a subjective hunch. Record scores + the chosen set + the cited
evidence in `optimization.md`.

## Step 3 — Supplemental note per chosen card (REQUIRED)

Each chosen card gets a `supplemental_context` string. It MUST contain, in order:

1. **Viral lift** — a concrete instruction targeting that card's weakest viral dimension
   (e.g. "sharpen the hook into one counter-intuitive opening line"), not generic "make it better".
2. **选题 anchor (mandatory)** — a short summary of the card's originating 选题 (look it up via
   `topic_to_direction`), prefixed with this exact framing so the workflow treats it as guidance,
   not a script:
   > 原选题方向（供参考，不必逐字一致，但不要偏移该方向）：{选题标题 + 叙事思路一句话 + 品牌词露出方式}
   This keeps the draft anchored to the 选题 even though the workflow generates from crawled posts.
3. **Safety calibration** — needs_extra_material → instruct placeholders, no fabrication;
   brand exposure → ≤1-2 capabilities + disclosure; subreddit tone fit.

Keep it concise — it goes verbatim into the API's `topic_supplemental_contexts[topic_id]`.

## Step 4 — Draft generation (API)

### Choosing `length_multiplier` (don't default to "longer")

`length_multiplier` controls draft length. **Longer is NOT always better.** More content =
more surface area to expose the post as marketing/AI (露馅); too short = the product is under-
explained. Pick a value that fits the card: for most Reddit-native posts **稍短 or 默认** reads
most believable. Use the user-specified value when given (`run_config.draft_length_multiplier`),
otherwise choose by situation using this UI→value map:

| UI 选项 | `length_multiplier` |
|--------|:------------------:|
| 更短 | `0.3` |
| 稍短 | `0.5` |
| 默认 | `1` |
| 稍长 | `1.8` |
| 更长 | `2.5` |

Rule of thumb: short venting/asking posts → `0.3–0.5`; standard experience/story posts →
`1`; only go `1.8–2.5` when the card genuinely needs a detailed walkthrough AND the extra
length won't make it read like an ad. Record the chosen multiplier + why in `optimization.md`.

Use the draft endpoints (see search-query-occupancy/api-reference.md §5), one job per direction:
```
POST .../directions/{did}/drafts/jobs
  body: {topic_ids:[chosen for this direction],
         topic_supplemental_contexts:{topic_id: note, ...},
         length_multiplier:<chosen per the map above; run_config.draft_length_multiplier or per-card>, overwrite:true}
GET  .../directions/{did}/drafts/jobs/{job_id}   # poll 5-10s → completed
GET  .../directions/{did}/drafts                  # or download drafts_md
```
Chosen cards span multiple directions → one job per direction. Selecting cards has no save
endpoint; the selection IS the `topic_ids` you pass.

## Required output structure

Write to `05_optimized_cards/` (UTF-8):
- `optimization.md` — MANDATORY. The viral scores for all passed cards, the chosen top-N, the
  heat-evidence cited per pick, per-card supplemental note (with the 选题 anchor visible), plus
  the diversity rationale.
- `drafts_md/{topic_id}.md` — each generated draft's `final_markdown`.
- update `run_meta.json` with the draft `job_id`(s) and chosen `topic_ids`.
- `handoff_packet.json` (per HANDOFF_SCHEMA.json) — the **structured viral intent** that Stage 6
  must preserve. Per chosen post it MUST carry:
  ```json
  {
    "post_id": "post_001",
    "topic_id": "topic_003",
    "draft_path": "05_optimized_cards/drafts_md/post_001.md",
    "topic_anchor": "one-line 选题 direction",
    "viral_intent": {
      "core_hook": "the single counter-intuitive/tension hook",
      "emotional_trigger": "the feeling that drives upvote/share",
      "comment_engine": "the prompt that makes people reply/argue",
      "must_preserve": ["concrete detail 1", "conflict/contrast 2", "not a tool pitch"]
    },
    "title_pattern_to_preserve": "the high-ranking title structure from heat evidence",
    "expected_comment_types": ["共鸣", "怀疑", "替代方案", "等评测"],
    "subreddit_risk_note": "moderation/self-promo risk + how to stay safe",
    "allowed_claim_ids": ["C001", "C004"],
    "forbidden_claim_ids": ["C009"]
  }
  ```
  Derive `title_pattern_to_preserve` + `expected_comment_types` from
  `occupancy_heat_evidence.json`; derive allowed/forbidden claim ids from
  `global/product_fact_index.json`. Stage 6 reads THIS, not the raw cards.

## Process

1. Load passed cards + maps + heat evidence + topics.md + fact index + topic_to_direction.
2. Score every passed card on the viral rubric (precondition gate first). Write scores to optimization.md.
3. Pick top-N keeping diversity, **citing heat evidence per pick**. For each chosen card, write
   its supplemental note INCLUDING the 选题 anchor.
4. Run EVALS (viral ranking + note quality + 选题 anchor + handoff viral_intent completeness).
   Revise until blocking passes.
5. Fire draft job(s) per direction with topic_ids + supplemental contexts; choose
   `length_multiplier` per card (user value, else situational — don't max for length); poll to completed.
6. Save drafts. Write `handoff_packet.json` with per-post `viral_intent`. Log manifest. Hand
   off to `post-optimization`.

## Common mistakes

- Scoring viral potential on a card that is actually ad/AI-heavy (precondition gate must fail it).
- Picking top-N all from one subreddit/angle (no diversity).
- Supplemental note missing the 选题 anchor → draft drifts off the 选题 direction.
- Phrasing the 选题 anchor as a rigid script instead of "参考、不必一致、不要偏移".
- Generic notes ("make it better") instead of a specific viral-lift instruction.
- Letting a `needs_extra_material` card draft without a placeholder instruction → fabrication.
- Maxing `length_multiplier` for length — more content is easier to expose as an ad; pick 稍短/默认 unless the card needs detail.
