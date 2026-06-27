---
name: reddit-product-brief
description: Use when researching a client product before Reddit promotion, especially when Codex must turn official materials, customer notes, or websites into a factual product outline, capability boundaries, personas, competitor matrix, and local handoff artifact.
---

# Reddit Product Brief

## Purpose

Create the factual foundation for all downstream Reddit content. This skill turns product materials into a local product brief that defines what the product can say, what it must not say, who it serves, how it differs from competitors, and which facts downstream posts must preserve.

## Required References

Read before working:

- `../../shared/workspace-and-handoff-contract.md`
- `../../shared/output-templates.md`
- `../../shared/eval-loop.md`
- `../../evals/01-product-brief-eval.md`

## Inputs

Accept any combination of:

- Official website, docs, pricing page, changelog, demo, screenshots, app access, or client notes.
- Existing product materials in Markdown, PDF, slides, sheets, or raw text.
- Competitor names or category keywords.
- Client constraints, claims to emphasize, and claims to avoid.

If a source cannot be accessed, record it under `Source Inventory` with the failure reason.

## Workflow

1. Create or locate the task folder using the shared workspace convention.
2. Save raw inputs or source notes under `00_inputs/`.
3. Build a source inventory with reliability labels: official, customer-provided, observed in product, third-party, inferred, unverified.
4. Extract a capability tree:
   - Product modules.
   - User-facing capabilities.
   - Technical/infrastructure capabilities.
   - Workflow capabilities.
   - Integrations.
   - Limits and prerequisites.
5. Define product positioning:
   - One-line positioning.
   - Category.
   - Main problem solved.
   - Why now.
   - What the product is not.
6. Define user personas:
   - Primary and secondary users.
   - Pain, trigger, objections, buying context.
   - Reddit communities or search contexts where the pain appears.
7. Research competitors conservatively:
   - Include pricing only when sourced.
   - Use `unknown` instead of guessing.
   - Compare personas, pricing, core features, feature gaps, and switching concerns.
8. Build a feature comparison matrix. Use columns that matter for this product category, not generic columns.
9. Write a differentiation summary:
   - Where the product is stronger.
   - Where competitors are stronger.
   - Where claims need proof.
   - Safe wording for Reddit.
10. Create a fact bank with claim status:
    - `verified`
    - `client-provided`
    - `observed`
    - `needs-confirmation`
    - `do-not-use`
11. Save the final brief to `01_product_brief/product_brief.md`.
12. Run the paired eval and revise until it passes.
13. Update `manifest.json`.

## Output Contract

The product brief must contain:

- Source inventory.
- One-line positioning.
- Capability tree.
- Product boundary with verified, unverified, and forbidden claims.
- Target user table.
- Competitor matrix with pricing and feature comparison.
- Differentiation summary.
- Reddit messaging angles.
- Fact bank with safe wording.
- Open questions for the client.

## Quality Rules

- Never invent capabilities, pricing, performance, revenue, user count, integrations, or customer results.
- Treat "not found" as information; list it under unknowns.
- Use product facts as constraints, not ad copy.
- Capture negative boundaries because they prevent downstream hallucination.
- Prefer specific safe wording over broad claims.

## Handoff

Hand off:

- `product_brief.md` path.
- Eval report path.
- Product facts downstream posts may use.
- Claims that require client confirmation.
- Competitor comparison fields that should shape topic planning.
