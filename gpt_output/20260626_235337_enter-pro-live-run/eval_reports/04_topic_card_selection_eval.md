# Eval Report: Topic Card Selection

- Artifact: `04_card_selection/topic_card_scores.md`
- Evaluated At: 2026-06-27T01:09:00+08:00
- Result: PASS
- Score: 92/100

## Hard Gates

| Gate | Result | Evidence | Required Fix |
| --- | --- | --- | --- |
| Full pool considered | PASS | All 36 Topic Cards are scored in `04_card_selection/topic_card_scores.md`. | None. |
| No hard-ad selection | PASS | Selected cards are troubleshooting, checklist, or workflow questions; no selected card depends on a direct product pitch. | None. |
| Product truth | PASS | Selected cards map to verified Auth/Postgres/RLS, code visibility/export/GitHub sync, Plan Mode, and Enter Code facts. | None. |
| Supplemental context | PASS | Every selected topic has concrete API supplemental context with facts, avoid-list, tone, and material need. | None. |
| Draft job proof | PASS | `04_card_selection/draft_request.json` and `04_card_selection/draft_job_statuses.json` saved. Jobs completed: `20260626_165133_c66bf0cb`, `20260626_165326_0386b141`, `20260626_165514_9476bb0e`. | None. |
| Failed drafts handled | PASS | All three jobs completed with `failed_count=0`; no replacement needed. | None. |

## Weighted Rubric

| Criterion | Weight | Score | Evidence | Required Fix |
| --- | ---: | ---: | --- | --- |
| Search occupancy fit | 15 | 14 | Selected cards directly use search maps around client portals, handoff, and prompt drift. | None. |
| Reddit discussion potential | 15 | 14 | Topics invite troubleshooting, disagreement, and workflow sharing. | None. |
| Product relevance | 15 | 14 | Each selected card maps to a verified differentiator. | None. |
| Native framing | 10 | 9 | Selected hooks are Reddit-native; supplemental contexts reduce ad smell. | None. |
| Differentiation | 10 | 9 | Portfolio has two security/data posts, two handoff posts, and two workflow posts. | None. |
| Material readiness | 10 | 10 | All selected cards require no extra images/data/screenshots. | None. |
| Risk level | 10 | 8 | Disclosure and claim limits are required downstream; selected cards are otherwise low risk. | Keep brand mentions disclosed and late. |
| Supplemental context quality | 15 | 14 | Contexts specify pain, verified facts, avoid-list, tone, and no-material status. | None. |

## Revision Log

- Attempt 1: Scored full 36-card pool and selected six cards.
- Attempt 2: Submitted grouped draft jobs through SmartContent and downloaded raw drafts after completion.

## Handoff Notes

- Preserved facts: no "production-ready", no "replaces developers", no "zero migration", no full Stripe-chain claim.
- Blockers: none.
- Next-step inputs: `04_card_selection/raw_drafts.md`, `04_card_selection/topic_card_scores.md`, and product fact bank.

