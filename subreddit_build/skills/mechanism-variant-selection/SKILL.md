---
name: mechanism-variant-selection
description: Use after Topic Cards are generated, when every Topic Card needs one 8-item SmartContent mechanism-variant batch, the best mechanism selected, and the chosen variant applied. Stage 4 of the subreddit build workflow.
---

# Mechanism Variant Selection (Stage 4)

## Overview

For every generated Topic Card, call the mechanism variant endpoint to generate one batch of
8 mechanisms, score every mechanism with the required matrix, choose the best one, apply it to
the card, and confirm the API marks that variant as active.

**Core principle:** mechanism selection is not random preference. Pick the variant that best
improves Reddit-native discussion potential while keeping brand exposure natural and safe.

## Inputs

- Stage 3 handoff with `project_id`, `run_id`, `round_id`, `topic_cards.json`, and topic doc URL.
- `reference_post_cards.json`, content map context, and Stage 2 `community_insights.json`.
- Global fact and brand files.

## Required Output

Write to `04_mechanism_selection/`:

- `mechanism_selection.md` - per Topic Card: original mechanism, 8 variants, selected variant, rationale.
- `variant_history.json` - raw or normalized history from the API.
- `applied_variants.json` - `topic_id -> active_variant_id` and applied fields.
- `handoff_packet.json`.

## API Flow

For every Topic Card:

1. `GET /topic-cards/{topic_id}/mechanism-variants`.
2. `POST /topic-cards/{topic_id}/mechanism-variants/generate` with `{ "count": 8 }`.
3. Score all 8 variants with the required scoring matrix.
4. `POST /topic-cards/{topic_id}/mechanism-variants/{variant_id}/apply`.
5. Re-read mechanism history or the apply response and record `active_variant_id`.
6. Confirm `active_variant_id == selected_variant_id`; otherwise stop with a blocker.

## Required Scoring Matrix

For every variant, write a scorecard in `mechanism_selection.md` and `applied_variants.json`.
Use 1-5 integer scores for each dimension and a weighted total out of 100:

| Dimension | Weight | What to reward |
|---|---:|---|
| Hook strength | 20 | Specific tension, curiosity, or contrast that makes the post clickable without hype |
| Comment engine | 20 | Easy for readers to answer, disagree, share experience, or add alternatives |
| Community fit | 20 | Fits target subreddit positioning, content forms, motivations, and risk warnings |
| Brand naturalness | 15 | Keeps the product mention light, believable, and tied to verified capability |
| Topic/source preservation | 15 | Preserves original title direction and source-card reference logic |
| Material feasibility and risk | 10 | Avoids unprovided screenshots, fake proof, risky claims, or moderation traps |

Select the highest total score unless there is a written blocker such as fabricated material,
unsafe brand exposure, or conflict with the target community. If the selected variant is not
the highest total, record the override reason.

## Selection Rubric

Prioritize variants that:

- create a stronger hook, conflict, or comment engine;
- preserve the topic direction and source-card reference logic;
- reduce ad/AI flavor;
- fit target subreddit behavior and moderation risk;
- cite the relevant community insight field when choosing a mechanism for a target subreddit;
- keep brand mention to one natural path tied to verified capability;
- avoid requiring unprovided images, screenshots, or fabricated proof.
- have a clearly better weighted score than the original or a written reason for preserving
  a lower-risk variant.

## Common Mistakes

- Generating variants for only the cards that look promising.
- Selecting a punchy mechanism that turns into an ad.
- Failing to call the apply endpoint after choosing.
- Failing to confirm the post-apply `active_variant_id`.
- Losing the original Topic Card's title direction or source-card logic.
