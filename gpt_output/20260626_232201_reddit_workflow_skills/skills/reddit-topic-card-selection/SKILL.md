---
name: reddit-topic-card-selection
description: Use when generated topic cards must be scored, ranked, shortlisted into topN, supplemented with client feedback or missing context, and sent to the SmartContent draft-generation API.
---

# Reddit Topic Card Selection

## Purpose

Choose the strongest topic cards from the generated pool and prepare them for draft generation. The selection process must explain why each selected card is worth writing, what must be fixed before drafting, and what supplemental context the draft API should receive.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/output-templates.md`
- `../../shared/smartcontent-api-contract.md`
- `../../shared/eval-loop.md`
- `../../evals/04-topic-card-selection-eval.md`

## Inputs

- Three selected direction folders from search occupancy.
- `topic_cards.md` for each selected direction.
- Product brief and topic plan.
- Desired `topN`. If absent, ask the user; if the user is unavailable, select 6 as the working default and mark the assumption.
- Client feedback or product emphasis notes, if provided.

## Workflow

1. Parse all available topic cards into a single list.
2. Confirm the expected pool size. Default workflow expects 36 cards.
3. Score every card with the paired eval rubric.
4. Reject cards that fail hard gates before ranking.
5. Rank candidates and select topN.
6. Ensure selected cards are not all the same:
   - Spread across directions when possible.
   - Include varied content forms.
   - Avoid repeating the same subreddit and title mechanism unless strategically necessary.
7. For each selected card, write supplemental context:
   - What to emphasize.
   - Product facts to preserve.
   - What to avoid.
   - Missing material or client feedback.
   - Tone and disclosure guidance.
8. Save `04_card_selection/topic_card_scores.md`.
9. Build `04_card_selection/draft_request.json` grouped by direction because draft jobs are direction-specific.
10. Call the draft-generation API for each direction group:
    - Pass selected `topic_ids`.
    - Pass `topic_supplemental_contexts`.
    - Use `length_multiplier: 1` unless instructed otherwise.
    - Use `overwrite: true` only when replacing old drafts intentionally.
11. Poll each draft job until complete or failed.
12. Save raw drafts to `04_card_selection/raw_drafts.md`.
13. Update `manifest.json`.
14. Run the paired eval and revise/retry until it passes.

## Supplemental Context Rules

Every selected topic needs a concrete supplement. Do not leave it blank because every topic card has gaps.

Include:

- The exact user pain to foreground.
- Whether brand mention should be absent, soft, disclosed, or explicit.
- Product facts that must stay accurate.
- Claims or words to avoid.
- Material needed if the post needs proof.
- Community tone guidance.
- A skepticism angle if the brand mention risks sounding promotional.

## Draft Request Shape

Save a local JSON file:

```json
{
  "direction_001": {
    "topic_ids": ["topic_001"],
    "topic_supplemental_contexts": {
      "topic_001": "..."
    },
    "length_multiplier": 1,
    "overwrite": true
  }
}
```

## Output Contract

Save:

- `04_card_selection/topic_card_scores.md`
- `04_card_selection/draft_request.json`
- `04_card_selection/raw_drafts.md`
- `eval_reports/04_topic_card_selection_eval.md`

## Handoff

Hand off:

- Selected topic IDs and directions.
- Draft job IDs and status.
- Raw drafts path.
- Supplemental contexts.
- Any failed draft topics and replacement recommendations.
