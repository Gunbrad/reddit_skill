# EVALS — Post Fact & Brand-Safety Check (Stage 6b)

Run by a SEPARATE evaluator worker (EVAL_WORKER_CONTRACT.md), per post, on
`06_optimized/checked_posts.md` against `global/product_fact_index.json` and
`global/brand_safety_rules.md`. **Blocking** must pass.
Threshold: all blocking pass.

The two sub-systems: (C) brand exposure safety, (D) fact accuracy. A third light check (X)
confirms 6a's nativeness wasn't destroyed.

---

## C. Brand exposure safety

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| C1 | Brand as "stumbled-on option" | ✅ | "saw X mentioned while searching" framing, not "this product solves my problem" |
| C2 | ≤1-2 capabilities per mention | ✅ | No multi-feature pitch in body |
| C3 | Disclosure intent present | ⬜ | Relationship disclosed where recommending/comparing |
| C4 | No competitor attack | ⬜ | Comparisons = "different tools, different stages" |
| C5 | Comment brand discipline | ✅ | Brand ≤1-2 mentions across comments; no single comment fully sells it |

---

## D. Fact accuracy (vs product_fact_index.json)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| D1 | No unverified feature as fact | ✅ | Nothing the brief marks "不可说"/unverified is stated as fact |
| D2 | Claims match capability tree | ✅ | Every product claim traces to a verified capability |
| D3 | No fabricated data | ✅ | No invented revenue/benchmark/review/screenshot |
| D4 | Boundaries respected | ⬜ | Doesn't imply capabilities outside the product boundary |

---

## X. Nativeness preserved (light regression check)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| X1 | Fixes stayed native | ⬜ | Lines edited for facts/brand are still native (no reverted formal/AI prose, no new Chinglish) |
| X2 | Check log present | ⬜ | Each post has a check log (what changed + why, or "no changes") |

---

## Failure → action

- Any C/D blocking fail → fix the offending line and re-score with a fresh evaluator; do NOT
  hand off to 6c.
- D1/D2 fail → remove or correct the claim against the capability tree / "不可说" table.
- C1/C2/C5 fail → reframe brand as a stumbled-on mention, trim to ≤1-2 capabilities.
- X1 fail → re-edit the line natively (conventions.md §4b) rather than leaving formal prose.
- Record per-post C/D verdicts in `run_manifest.md`.

## Reviewer prompt (MANDATORY evaluator worker)

Under isolated-worker execution, this reviewer must run as a separate evaluator worker. It is
not optional. If the runtime does not support subagents, emulate this with a fresh evaluation
session that receives only checked_posts.md, this EVALS.md, OUTPUT_SCHEMA.json, the minimal
fact index, and brand-safety rules.

"You have a product fact index and a Reddit post + comments. (1) Does every
product claim match the fact sheet? Flag any sentence stating an unverified / 不可说 feature as
fact, or any invented number/benchmark/review. (2) Is the brand introduced like an accidental
find or like a pitch? How many times across body + comments? Any multi-feature dump or
competitor attack? List every violation with the exact line."

