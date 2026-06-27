# EVALS — Topic Selection (Stage 2)

Score `topics.md` before handoff. First score content before creating the Feishu doc, then
verify the Feishu doc link exists. **Blocking** must all pass.
Threshold: all blocking pass AND total ≥ 80/100. Score the SET, then each 选题.

## Set-level rubric

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| S1 | Directions are mutually distinct | ✅ | 15 | No two 选题 would produce near-identical search queries; grouped under distinct 主线 |
| S2 | Coverage of key personas/pains | ⬜ | 10 | Spread across the brief's priority personas, not all on one pain |
| S3 | Count sufficient for stage 3 | ⬜ | 5 | Enough 选题 to yield the planned directions (each → 2 queries) |
| S4 | 选题 Feishu doc created | ✅ | 0 | `02_topics/feishu_links.md` contains the 选题 doc URL; not merely "deferred" |

## Per-选题 rubric (every 选题 must pass blocking)

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| 1 | All 6 fields present | ✅ | 10 | 内容类型/叙事思路/素材/品牌词露出/选择理由 + 标题 all filled |
| 2 | Leads with user pain, not product | ✅ | 15 | 叙事思路 opens from a real scenario/pain; product enters later |
| 3 | Brand exposure is natural, not an ad | ✅ | 15 | 品牌词露出 ties to ≤1-2 verified capabilities; no feature dump; discloses relationship intent |
| 4 | Respects red lines & boundary | ✅ | 10 | No "不可说" feature claimed; no over-promise; no fabricated data |
| 5 | 选择理由 shows real intent | ⬜ | 10 | Explains search/purchase intent + why low platform risk |
| 6 | Material honestly scoped | ⬜ | 5 | 素材/调研 marks client-supplied vs available; nothing invented |

## Failure → action

- S1 fail → merge/replace overlapping 选题 before stage 3 (else duplicate directions).
- S4 fail → create the 选题 Feishu doc from `topics.md`, set public-edit permission, and record
  the URL before handoff.
- Per-选题 blocking fail → rewrite that 选题; do not write it to Feishu.
- Record set-level + per-选题 verdicts in `run_manifest.md`.

## Reviewer prompt (optional subagent)

"You are a Reddit-native content strategist. For each 选题: does it open from a user pain or
from the product? Is the brand exposure natural (≤2 capabilities, no feature dump) or an ad?
Does it claim any feature the product brief marks unverified? Across the set, are any two
directions so similar they'd produce the same search query? List every violation."
