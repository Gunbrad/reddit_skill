---
name: mechanism-variant-selection
description: Use after Topic Cards are generated, when every Topic Card needs one 8-item SmartContent mechanism-variant batch, the best mechanism selected, and the chosen variant applied. Stage 4 of the subreddit build workflow.
---

# Mechanism Variant Selection (Stage 4)

## Overview

For every generated Topic Card, call the mechanism variant endpoint to generate one batch of
8 mechanisms, evaluate those mechanisms, choose the best one, and apply it to the card.

**Core principle:** mechanism selection is not random preference. Pick the variant that best
improves Reddit-native discussion potential while keeping brand exposure natural and safe.

## Inputs

- Stage 3 handoff with `project_id`, `run_id`, `round_id`, `topic_cards.json`, and topic doc URL.
- `reference_post_cards.json` and content map context when needed.
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
3. Score variants.
4. `POST /topic-cards/{topic_id}/mechanism-variants/{variant_id}/apply`.
5. Record the applied card fields.

## Selection Rubric

Prioritize variants that:

- create a stronger hook, conflict, or comment engine;
- preserve the topic direction and source-card reference logic;
- reduce ad/AI flavor;
- fit target subreddit behavior and moderation risk;
- keep brand mention to one natural path tied to verified capability;
- avoid requiring unprovided images, screenshots, or fabricated proof.

## Common Mistakes

- Generating variants for only the cards that look promising.
- Selecting a punchy mechanism that turns into an ad.
- Failing to call the apply endpoint after choosing.
- Losing the original Topic Card's title direction or source-card logic.
