# EVALS — Topic Card Screening (Stage 4, binary gate)

This stage is a binary safety/readiness filter. EVALS verify the screening was done
**completely** and **correctly**, not that a top-N was ranked. **Blocking** must pass.

## Gate — Screening quality

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| S1 | Every card judged | ✅ | All generated cards have a PASS/FAIL verdict in screening.md (none skipped) |
| S2 | Verdict uses the 4-part gate | ✅ | Each verdict reflects community-compliant + production-ready + product-relevant + low-risk; not vibes |
| S3 | Product relevance checked | ✅ | No PASS card is merely a general Reddit topic; it traces to the current product brief's personas/pains, verified capabilities, or differentiation |
| S4 | No unsafe card passed | ✅ | No PASS card requires an unverified/"不可说" feature, fabricated data, reads as a pure ad, or lacks a truthful path to mention this product |
| S5 | No safe card wrongly failed | ⬜ | "Average but safe and product-relevant" cards are PASS, not FAIL; FAILs have a concrete red-line/readiness/relevance reason |
| S6 | Reason recorded | ⬜ | Each verdict has a short, specific reason (not blank / not "ok") |
| S7 | Passed set handed off | ✅ | `## Passed set` lists the passing topic_ids; `screened_pass_ids` written to run_meta.json |

Note: there is **no top-N and no fixed total** at this stage. Do not penalize the count.

## Failure → action

- S1 fail → finish judging the un-screened cards.
- S2/S3/S4 fail → re-judge with the 4-part gate; demote unsafe or product-irrelevant cards to FAIL before handoff.
- S5 fail → restore wrongly-failed safe, product-relevant cards to PASS (stage 5 will rank them).
- S7 fail → write the passed set + `screened_pass_ids` before handing off.
- Record the gate verdict in `run_manifest.md`.

## Reviewer prompt (optional subagent)

"Read screening.md. Is every generated card given a PASS/FAIL with a concrete reason? Does any
PASS card require an unverified feature, fabricated data, a hostile community, lack a clear
connection to the current product brief, or read as a pure ad (should be FAIL)? Is any
merely-average-but-safe and product-relevant card wrongly FAILed (should be PASS)?
Is the passed set listed for handoff? List every violation. Do NOT rank for quality — that is
stage 5's job."
