# EVALS — Topic Card Screening (Stage 4, binary gate)

This stage is a binary safety/readiness filter. EVALS verify the screening was done
**completely** and **correctly**, not that a top-N was ranked. **Blocking** must pass.

## Gate — Screening quality

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| S1 | Every card judged | ✅ | All generated cards have a PASS/FAIL verdict in screening.md (none skipped) |
| S2 | Verdict uses the 3-part gate | ✅ | Each verdict reflects community-compliant + production-ready + low-risk; not vibes |
| S3 | No unsafe card passed | ✅ | No PASS card requires an unverified/"不可说" feature, fabricated data, or reads as a pure ad |
| S4 | No safe card wrongly failed | ⬜ | "Average but safe" cards are PASS, not FAIL; FAILs have a concrete red-line/readiness reason |
| S5 | Reason recorded | ⬜ | Each verdict has a short, specific reason (not blank / not "ok") |
| S6 | Passed set handed off | ✅ | `## Passed set` lists the passing topic_ids; `screened_pass_ids` written to run_meta.json |

Note: there is **no top-N and no fixed total** at this stage. Do not penalize the count.

## Failure → action

- S1 fail → finish judging the un-screened cards.
- S2/S3 fail → re-judge with the 3-part gate; demote any unsafe card to FAIL before handoff.
- S4 fail → restore wrongly-failed safe cards to PASS (stage 5 will rank them).
- S6 fail → write the passed set + `screened_pass_ids` before handing off.
- Record the gate verdict in `run_manifest.md`.

## Reviewer prompt (optional subagent)

"Read screening.md. Is every generated card given a PASS/FAIL with a concrete reason? Does any
PASS card require an unverified feature, fabricated data, a hostile community, or read as a
pure ad (should be FAIL)? Is any merely-average-but-safe card wrongly FAILed (should be PASS)?
Is the passed set listed for handoff? List every violation. Do NOT rank for quality — that is
stage 5's job."
