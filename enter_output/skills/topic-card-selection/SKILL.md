---
name: topic-card-selection
description: Use after Topic Cards are generated, when scoring and ranking topic cards to pick the best ones to write, when adding supplemental notes or client feedback to selected cards, or when triggering the draft-generation job for chosen topics. Stage 4 of the Reddit posting pipeline.
---

# Topic Card Selection + Drafting (Stage 4)

## Overview

From the 36 Topic Cards (3 directions × 12), score and rank them, pick the best top-N, write
a supplemental note / client feedback for each chosen card (every card has gaps), then fire
the draft-generation job. Output is a selection record + generated drafts for stage 5.

**Core principle:** selection is *scored*, not vibes. The supplemental note is where you fix
each card's specific weakness before it becomes a post — it is not optional filler.

## When to use

- `03_search/topic_cards/*.md` exist and passed stage-3 EVALS (Gate C).
- You need to choose which cards to draft and generate the drafts.

Not for: optimizing finished posts (stage 5).

## Inputs

- `03_search/topic_cards/{direction_id}.json` (36 cards), the occupancy maps, `run_meta.json`.
- `01_product_brief/product_brief.md` (to score brand-fit and respect boundaries).

## Scoring rubric (pick top-N by weighted score)

Score each of the 36 cards 1-5 per dimension; weighted total ranks them. Default N agreed
with the user (the pipeline default narrative is "top-N of 36").

| Dimension | Weight | 5 = high | 1 = low |
|-----------|:---:|----------|---------|
| Search-occupancy fit | 25% | Title direction matches the map's high-rank title patterns/semantics | Generic, won't rank |
| Pain authenticity | 20% | Opens from a real, relatable pain | Product-first / contrived |
| Brand-fit & safety | 20% | Brand surfaces naturally on a verified capability; low red-line risk | Ad-like or claims unverified feature |
| Subreddit viability | 15% | target_subreddit allows advice/experience posts, >10k, low filter risk | Hostile to brand/self-promo |
| Discussion potential | 10% | Invites comments (question/debate hooks) | Flat, no hook |
| Distinctiveness | 10% | Different from already-picked cards | Duplicate angle/subreddit |

Compute weighted score per card; rank; pick top-N while keeping **diversity** (avoid
multiple picks with the same subreddit + same angle). Record scores in `selection.md`.

## Supplemental note (per chosen card) — required

Every chosen card gets a `supplemental_context` written to fix its weakness. Decide what to
write by checking, in order:

1. `needs_extra_material` true? → state what client material is required; instruct the draft
   to mark placeholders, not fabricate.
2. Brand exposure too strong/weak? → tell the draft to soften to ≤1-2 capabilities, disclose.
3. Lowest-scoring dimension above → give a targeted instruction to raise it.
4. Subreddit risk? → tell the draft to fit that community's norms (less promo, more question).

Keep each note concrete and short — it goes verbatim into the API's
`topic_supplemental_contexts[topic_id]`.

## Draft generation (API)

Use the draft endpoints (see search-query-occupancy/api-reference.md §5), per direction:
```
POST .../directions/{did}/drafts/jobs
  body: {topic_ids:[chosen for this direction],
         topic_supplemental_contexts:{topic_id: note, ...},
         length_multiplier:1, overwrite:true}
GET  .../directions/{did}/drafts/jobs/{job_id}   # poll 5-10s → completed
GET  .../directions/{did}/drafts                  # or download drafts_md
```
Chosen cards span multiple directions → one job per direction. Selecting cards has no save
endpoint; the selection IS the `topic_ids` you pass.

## Required output structure

Write to `04_drafts/` (UTF-8):
- `selection.md` — the 36 cards with scores, the chosen top-N (with per-card supplemental
  note), and the diversity rationale. MANDATORY artifact.
- `drafts_md/{topic_id}.md` — each generated draft's `final_markdown`.
- update `run_meta.json` with the draft `job_id`(s) and chosen `topic_ids`.

## Process

1. Load 36 cards + maps + brief. Score each on the rubric; write the table to `selection.md`.
2. Pick top-N keeping diversity. For each chosen card, write its supplemental note.
3. Run EVALS (selection + note quality). Revise picks/notes until blocking passes.
4. Fire draft job(s) per direction with topic_ids + supplemental contexts; poll to completed.
5. Save drafts. Log manifest. Hand off to `post-optimization`.

## Common mistakes

- Picking by gut instead of the weighted rubric.
- Top-N all from one subreddit/angle (no diversity).
- Empty/generic supplemental notes ("make it better") — must target a specific gap.
- Letting a `needs_extra_material` card draft without a placeholder instruction → fabrication.
