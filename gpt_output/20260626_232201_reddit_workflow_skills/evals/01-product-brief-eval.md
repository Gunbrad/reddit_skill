# Product Brief Eval

Use after `reddit-product-brief` creates or revises `01_product_brief/product_brief.md`.

Threshold: 85/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| No invented facts | No unsourced capability, price, integration, metric, customer result, benchmark, or roadmap claim. |
| Source traceability | Every major claim maps to a source category or is marked `needs-confirmation`. |
| Product boundary present | Verified, unverified, and must-not-claim sections all exist. |
| Competitor matrix present | Includes competitor persona, pricing status, and feature comparison. Unknown pricing is marked `unknown`, not guessed. |
| Downstream safe wording | Fact bank contains safe wording for key claims. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| Source inventory quality | 10 | Covers official/customer/observed/third-party sources, reliability labels, missing-source notes. |
| Capability tree | 15 | Breaks product into modules, user-facing capabilities, integrations, workflow abilities, and limits. |
| Positioning clarity | 10 | One-line positioning is specific, category-aware, and not inflated. |
| Persona depth | 15 | Personas include situation, pain, trigger, objections, and Reddit context. |
| Competitor analysis | 20 | Compares at least three meaningful competitors or explains why fewer are available; includes pricing, personas, features, and trade-offs. |
| Differentiation | 15 | States real advantages, weak points, proof needed, and safe Reddit framing. |
| Risk and boundary handling | 10 | Flags claims that would create legal, platform, product-truth, or Reddit trust risk. |
| Handoff completeness | 5 | Manifest updated; next-step facts and blockers are explicit. |

## Common Failure Patterns

- Uses marketing adjectives without evidence.
- Says "best", "only", "complete", or "production-ready" without proof.
- Treats client aspiration as verified product fact.
- Competitor table compares vague impressions instead of concrete features.
- Omits product limitations, making downstream posts overclaim.

## Required Fixes By Failure Type

- Missing source: add source note or remove claim.
- Unknown competitor pricing: mark `unknown` and add "needs check".
- Weak differentiation: rewrite as trade-off comparison.
- Missing boundary: add `Must Not Claim` and `Needs Client Confirmation`.
- Persona too broad: split by buying trigger and Reddit context.

## Pass Output

The eval report must list:

- Final score.
- Hard gate status.
- Product facts approved for downstream use.
- Claims blocked from downstream use.
- Client questions that remain open.
