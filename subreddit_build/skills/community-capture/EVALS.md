# EVALS - Community Capture (Stage 2)

Run by a separate evaluator worker. The evaluator receives `community_capture.md`,
`run_meta.json`, downloaded artifact summaries, `community_insights.json/md`, this file, and
both schemas. Blocking criteria must pass before Stage 3.

## Gate A - API and Config Integrity

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| A1 | Auth verified | ✅ | `GET /api/auth/me` succeeded; no cookie is written to files |
| A2 | Correct API family | ✅ | Uses `/api/projects/...`, not `/api/search-occupancy/...` |
| A3 | Inputs valid | ✅ | Subreddits are normalized without `r/`, count <= 6, planned total <= 120 |
| A4 | Project snapshot recorded | ⬜ | `project_id`, client name, notes, and reference subreddits are in `run_meta.json` |

## Gate B - Long Run Handling

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| B1 | Heartbeat evidence | ✅ | `community_capture.md` logs polling status/stage/elapsed time at least once before terminal status |
| B2 | Terminal status checked | ✅ | Run reached terminal status and artifact endpoint was checked after terminal status |
| B3 | Community failures explicit | ✅ | `failed_subreddits` recorded; no failed community is silently treated as successful |
| B4 | No补抓 | ✅ | No retry run is started for failed subreddits in this workflow version |

## Gate C - Artifact Readiness

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| C1 | At least one successful subreddit | ✅ | `successful_subreddits` has at least one item |
| C2 | Content maps available | ✅ | `content_maps_count >= 1` and `content_maps.json` exists |
| C3 | Embedding status recorded | ✅ | `embeddings_status.json` exists and notes `exists/stale/count/model` if API returns them |
| C4 | Counts consistent | ⬜ | Raw post, post card, and content map counts align with artifact summary |

## Gate D - Community Insights

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| D1 | Insights exist | ✅ | `community_insights.json` and `.md` exist and are listed in the handoff |
| D2 | Successful communities covered | ✅ | Every successful subreddit has one insight object; no failed subreddit is presented as analyzed |
| D3 | Six required insight fields | ✅ | Each subreddit includes positioning, high-frequency topics, transferable patterns, primary content forms, community motivations, and risk warnings |
| D4 | Evidence-grounded | ✅ | Insights cite or clearly derive from content maps/raw post patterns, not generic Reddit advice |

## Failure -> action

- A/B blocking fail -> rerun the stage with corrected API/config handling.
- C1/C2 fail -> stop and ask for user direction; downstream retrieval cannot work.
- C3 fail -> keep polling if run is still building embeddings; otherwise record the blocker.
- D fail -> repair the insight artifact before Stage 3; downstream Topic Cards must not proceed without it.

## Reviewer prompt (MANDATORY evaluator worker)

"Review the Stage 2 community capture artifacts. Did the worker use the community builder
project APIs, validate subreddit count/limits, poll the long run with heartbeat evidence, check
artifact status after terminal state, and explicitly record successful vs failed subreddits
without starting a补抓 run? Are content maps and embeddings status available for retrieval?
Do community_insights.json/md cover every successful subreddit with the six required fields and
evidence-grounded risks/patterns?
List every violation and whether it blocks Stage 3."
