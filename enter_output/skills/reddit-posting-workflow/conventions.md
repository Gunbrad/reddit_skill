# Shared Conventions (read once per task)

All stage skills in this family depend on these conventions. The orchestrator
(`reddit-posting-workflow`) points here so the rules live in one place.

## 1. Brand & content red lines (apply to every text artifact)

These are hard constraints. Any stage that produces post-facing text must obey them, and
the EVALS for stages 2/3/4/5 check them.

- No fabricated reviews, user stories, revenue, benchmarks, or screenshots.
- No over-promising: ban phrases like "production-ready in minutes", "replaces developers",
  "best tool", "fully zero-waste", "完全/绝对" style absolutes.
- No competitor attacks. Comparisons must read as "different tools fit different stages".
- Disclose the relationship when a post recommends/compares/reviews the client product.
- One account must not flood the same brand content; vary subreddit, timing, and narrative role.
- Anything needing real data/screenshots/test results waits for client-supplied material —
  mark it `needs_extra_material: true` rather than inventing it.
- Respect the product's verified capability boundary. If the product brief says a feature is
  "unverified / 不可说", posts must not state it as fact.

## 2. SmartContent workflow API (used by stages 3 and 4)

- Base URL: `https://smartcontent.shifenglab.com`
- Auth: Cookie session. Every request sends
  `Cookie: planner_session=<session>` and `Accept: application/json`.
  Verify with `GET /api/auth/me` before any business call.
- The session cookie is a secret. Never write it into any committed artifact, manifest, or
  Feishu doc. Pass it via environment variable / runtime input only.
- Long operations: `prepare-all` ~10 min for 60 posts; topic-card generation 1-5 min;
  drafts run as an async job (poll `job_id`). Poll intervals: run status 5-15s, draft job 5-10s.
- **Run status `succeeded` is not enough.** Always check direction-level
  `search_occupancy_map_summary.directions[].status` (and `map_md`/`map_json`). A direction
  can fail its map while the run says succeeded.
- Topic Cards / Drafts download endpoints return 404 `Search planning artifact not found.`
  before generation; the same path returns 200 after. Use the exact download paths from the
  stage-3 reference, not guessed ones (wrong kind → 400 `Invalid search planning download kind.`).
- "Selecting" topic cards has no save endpoint — you pass the chosen `topic_ids` into the
  draft job request body. Per-card supplemental notes go in `topic_supplemental_contexts`.

Full endpoint list and a runnable script live in `search-query-occupancy/`.

## 3. Feishu (lark) usage (stages 2, 5, 6)

- Use the `lark-doc` skill to create/read/edit Feishu docs; `lark-drive` only if a file
  import is needed. First run may need `lark-shared` for auth.
- Stage 2 creates a doc and writes the 选题 into it; stage 5 creates a doc and pastes the
  optimized posts; stage 6 reformats the stage-5 doc in place.
- Stage 6 editing must be **block-level**, never full-document overwrite — images, 素材
  blocks, and manually edited content must survive. Re-read after editing to verify.
- Record every Feishu doc URL into the run folder's `feishu_links.md` and `run_manifest.md`.

## 4. File encoding & local writes

- Write all local `.md`/`.json` as UTF-8 (no BOM). The task input file in this project was
  UTF-16; do not propagate that. If a source file won't open, read it with the Grep tool
  (handles UTF-16 with BOM) rather than failing.
- The Bash tool in this environment may be misconfigured (routing to a missing shell). If
  shell commands fail with a WSL/`/bin/bash` error, fall back to: dedicated file tools for
  file ops, and ask the user to run provided API scripts in a working terminal.

## 5. The EVALS loop protocol (every stage)

Each stage ships an `EVALS.md` defining a scored rubric. The loop:

1. Produce the stage artifact.
2. Score it against that stage's EVALS rubric (each criterion = pass / fail / score).
3. If any **blocking** criterion fails → revise the artifact and re-score. Repeat until all
   blocking criteria pass and the weighted score clears the stage threshold.
4. Record the final verdict (per-criterion + total) in `run_manifest.md`.
5. Only then hand off to the next stage.

Blocking criteria are marked in each EVALS.md. Non-blocking criteria lower the score but do
not by themselves stop handoff; use judgment and note residual risks in the manifest.

## 6. Output discipline

- One run folder per task: `{YYYYMMDD_HHMMSS}_{project_slug}` (see orchestrator).
- Never invent file paths the next stage doesn't expect; match the structure exactly.
- Keep secrets (cookies, API keys) out of all written files.
