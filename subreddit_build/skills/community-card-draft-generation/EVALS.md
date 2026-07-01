# EVALS - Community Card Draft Generation (Stage 5)

Run by a separate evaluator worker. The evaluator receives `optimization.md`,
`draft_jobs_receipt.json`, generated drafts, the Stage 5 handoff packet, this file, and schemas.

## Gate A - TopN Selection

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| A1 | All applied cards considered | ✅ | `optimization.md` scores or explicitly reviews every applied Topic Card |
| A2 | TopN honored | ✅ | Chosen count matches user/run_config TopN |
| A3 | Viral and safe | ✅ | Chosen cards have breakout potential and do not rely on ad-heavy, unsafe, or unverified claims |
| A4 | Diversity kept | ⬜ | Selected set avoids over-concentrating one subreddit, format, or same hook |

## Gate B - Supplemental Context

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| B1 | Original topic copied | ✅ | Every note includes `原选题方向（复制自选题卡...）` with the original direction |
| B2 | Card-specific notes | ✅ | Notes refer to the selected mechanism, source-card context, target subreddit, and concrete writing need |
| B3 | Community insight cited | ✅ | Notes cite relevant community insight positioning, motivation, transferable pattern, content form, or risk warning |
| B4 | Brand boundary | ✅ | Notes include verified-claim boundary and natural exposure guidance |
| B5 | Material risk handled | ✅ | If extra material is needed, placeholder/no-fabrication instructions are present |
| B6 | Job-level length valid | ✅ | Every draft job has exactly one `length_multiplier`; all topic ids in that job share it; different lengths are split into separate jobs |
| B7 | Length justified | ⬜ | Length multiplier is recorded with a reason and not blindly maxed |

## Gate C - Draft Job And Handoff

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| C1 | Draft jobs completed | ✅ | All selected topic ids completed in their length-grouped jobs or failures are explicit blockers |
| C2 | Drafts saved | ✅ | Every selected post has `05_optimized_cards/drafts_md/{post_id}.md` |
| C3 | Viral intent complete | ✅ | Handoff has core_hook, emotional_trigger, comment_engine, and must_preserve[] per post |
| C4 | Community context compressed | ✅ | Handoff includes community_insight_refs and subreddit_risk_note so Stage 6 does not read Stage 2 directly |
| C5 | Claim ids bound | ✅ | Handoff includes allowed_claim_ids and forbidden_claim_ids from global fact files |
| C6 | Native stage ready | ✅ | Handoff gives enough topic/mechanism/context detail for native rewrite to preserve the idea |

## Failure -> action

- A fail -> re-rank and choose a valid TopN.
- B fail -> rewrite supplemental contexts before creating/recreating drafts.
- C fail -> poll/repair draft job or regenerate only failed drafts.

## Reviewer prompt (MANDATORY evaluator worker)

"Review Stage 5. Did the worker consider all applied cards, choose the requested TopN with
viral potential and safety, write per-card supplemental contexts that copy the original topic
direction and add concrete card-specific notes, group draft jobs by one shared length multiplier
per job, choose justified lengths, complete draft jobs, save drafts, and hand off complete viral
intent and claim boundaries? List every violation."
