# EVALS — Product Brief (Stage 1)

Score the `product_brief.md` before handoff. **Blocking** criteria must all pass.
Threshold: all blocking pass AND total ≥ 80/100.

## Rubric

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| 1 | All 6 sections present in order | ✅ | 10 | 概述 / 用户 / 卖点 / 竞品 / 边界 / 状态速查 all exist with content |
| 2 | Capability tree tagged | ✅ | 15 | Every capability marked verified vs unverified; no untagged capability |
| 3 | No unverified fact stated as verified | ✅ | 15 | Marketing claims clearly separated; "不可说" table exists and is non-empty (or justified empty) |
| 4 | Competitor comparison table | ✅ | 15 | Matrix with ≥3 differentiating columns, yours first; not all-✓; unknowns marked, not guessed |
| 5 | Each competitor has 用户画像 + 定价 | ⬜ | 10 | Persona + price (or "未公开") per competitor |
| 6 | Differentiation conclusion is specific | ✅ | 15 | One defensible wedge, not "better/faster"; tied to capability tree |
| 7 | User personas (优先/扩展/非目标) | ⬜ | 10 | All three present; non-target listed |
| 8 | Sourcing & date | ⬜ | 5 | 整理日期 + source noted; verified snapshot dated |
| 9 | Red-line / boundary section usable downstream | ✅ | 5 | 能力边界 table present; stage 5 can use it to avoid overclaim |

## Failure → action

- Criterion 2/3 fail → product facts unsafe; revise tagging before ANY downstream use.
- Criterion 4 all-✓ or padded → re-pick differentiating columns.
- Criterion 6 vague → rewrite wedge with a concrete capability competitors lack.
- Record per-criterion result + total in `run_manifest.md`.

## Reviewer prompt (optional subagent)

"You are a skeptical product analyst. Read product_brief.md. For each capability, is it
labeled verified or unverified? Find any sentence that states an unverified feature as
fact. Is the competitor table differentiating (not all ✓) and are unknowns marked rather
than guessed? Is the differentiation a specific defensible wedge? List every violation."
