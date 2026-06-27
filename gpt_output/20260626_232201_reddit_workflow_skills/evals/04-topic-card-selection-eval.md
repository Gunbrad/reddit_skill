# Topic Card Selection Eval

Use after `reddit-topic-card-selection` scores cards, selects topN, writes supplemental contexts, and generates raw drafts.

Threshold: 88/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| Full pool considered | All generated topic cards are included in the score table or explicitly missing with reason. |
| No hard-ad selection | No selected card depends on a direct product pitch as the core hook. |
| Product truth | Selected card can be supported by the product brief fact bank. |
| Supplemental context | Every selected topic has non-empty, concrete supplemental context. |
| Draft job proof | Draft request JSON, job IDs/status, and raw draft output are saved. |
| Failed drafts handled | Failed or partial draft jobs are documented with retry or replacement plan. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| Search occupancy fit | 15 | Card clearly uses map insights: title patterns, communities, narrative logic. |
| Reddit discussion potential | 15 | Likely to attract comments, disagreement, advice, or experience-sharing. |
| Product relevance | 15 | Natural fit with verified differentiator or user pain. |
| Native framing | 10 | Sounds like a Reddit topic, not a campaign brief. |
| Differentiation from other selected cards | 10 | Adds unique angle, community, format, or persona. |
| Material readiness | 10 | Required screenshots/data/images are available or optional. |
| Risk level | 10 | Low risk of deletion, undisclosed promotion, unsupported claims, or fake story. |
| Supplemental context quality | 15 | Gives draft generation precise fixes, facts, avoid-list, tone, and client feedback. |

## Suggested Scoring Formula

Score each topic card from 0-100:

- 90-100: select unless portfolio coverage is already saturated.
- 80-89: strong backup; select if it fills a missing angle.
- 70-79: needs substantial supplement; use only if strategically necessary.
- Below 70: reject.

## Supplemental Context Requirements

Each selected topic needs:

- `Emphasize:` exact pain or story frame.
- `Use facts:` verified product facts.
- `Avoid:` unsupported claims, ad language, risky comparisons.
- `Tone:` community-specific voice and skepticism level.
- `Materials:` screenshot/image/data needed or "none".
- `Disclosure:` no mention / soft mention / explicit relationship disclosure.

## Rejection Reasons

Use precise labels:

- `duplicate-angle`
- `weak-product-fit`
- `too-promotional`
- `unsupported-claim`
- `wrong-community`
- `needs-unavailable-material`
- `low-comment-potential`
- `high-moderation-risk`

## Required Fixes By Failure Type

- Missing supplement: write a real supplement before draft job.
- Selected cards too similar: replace lower-scoring duplicates.
- Draft failed: retry failed topic or choose replacement and explain.
- Product claim unsupported: revise supplement to remove or weaken claim.

## Pass Output

The eval report must list:

- TopN selected.
- Rejected high-risk cards.
- Draft request file.
- Draft job IDs and completion status.
- Raw drafts path.
