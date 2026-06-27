# EVALS — Topic Card Selection + Supplemental Notes (Stage 4)

Two gates: (A) selection quality, (B) supplemental-note quality. **Blocking** must pass.
Threshold: all blocking pass AND selection total ≥ 80/100.

## Gate A — Selection quality

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| A1 | All 36 scored on the rubric | ✅ | 20 | Every card has a weighted score recorded in selection.md |
| A2 | Top-N = highest weighted scores | ✅ | 20 | Chosen set matches the ranking (no unexplained low-score picks) |
| A3 | Diversity preserved | ✅ | 20 | No over-concentration on one subreddit + one angle; spread across directions |
| A4 | Brand-safety floor | ✅ | 20 | No chosen card claims an unverified feature or reads as a pure ad |
| A5 | Rationale recorded | ⬜ | 10 | selection.md explains why the top-N were chosen over near-misses |
| A6 | N matches user intent | ⬜ | 10 | Count agreed with user; if unspecified, proposed and confirmed |

## Gate B — Supplemental note quality (per chosen card)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| B1 | Note targets a specific gap | ✅ | Each note addresses that card's weakest dimension / known issue, not generic "improve" |
| B2 | needs_extra_material handled | ✅ | If card needs material, note instructs placeholder + no fabrication |
| B3 | Brand calibration | ⬜ | Note steers brand exposure to ≤1-2 capabilities + disclosure when relevant |
| B4 | Subreddit-fit guidance | ⬜ | Note adapts tone to the target community's promo tolerance |
| B5 | Concise & API-ready | ⬜ | Short enough to pass verbatim as topic_supplemental_contexts value |

## Failure → action

- A1/A2 fail → re-score or re-pick to match ranking.
- A3 fail → swap a duplicate-angle pick for the next diverse high-scorer.
- A4/B2 fail → must fix before drafting (fabrication/overclaim risk).
- B1 generic → rewrite the note against the card's lowest-scoring dimension.
- Record both gate verdicts in `run_manifest.md`.

## Reviewer prompt (optional subagent)

"Read selection.md. Are all 36 cards scored, and does the chosen top-N match the ranking?
Is the set diverse (not all one subreddit/angle)? Does any chosen card claim an unverified
feature or read as an ad? For each chosen card, does its supplemental note target a specific
weakness (not 'make it better'), and does it handle needs_extra_material with a placeholder
instead of fabrication? List every violation."
