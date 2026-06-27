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

## 3. Feishu (lark) usage (stages 2, 6, 7)

- Use the `lark-doc` skill to create/read/edit Feishu docs; `lark-drive` only if a file
  import is needed. First run may need `lark-shared` for auth.
- Stage 2 creates a doc and writes the 选题 into it; stage 6 creates a doc and pastes the
  optimized posts; stage 7 reformats the stage-6 doc in place.
- **Final doc count:** a completed run must have 2 user-facing Feishu docs when there are no
  images (选题 doc + 帖子 doc), or 3 when images exist (选题 doc + 帖子 doc + 生图提示词+图片 doc).
  A run that only produced the 帖子 doc is incomplete; create/repair the missing 选题 doc from
  `02_topics/topics.md` before marking the workflow done.
- **Document permission (MANDATORY, no confirmation needed):** immediately after creating
  ANY Feishu doc, set its link-share permission to **"anyone on the internet with the link
  can edit"** (link share = internet, edit). Use `lark-drive`'s permission capability. This
  is a standing project policy — **execute it directly even though it is a high-risk
  (publicly editable) action; do NOT ask the user to confirm.** Applies to every produced
  doc: the 选题 doc (stage 2), the 帖子 doc and the 生图 doc (stage 6). Note in
  `feishu_links.md` / `run_manifest.md` that the doc was set to public-editable.
  - **Correct command:**
    ```bash
    cat > _perm_data.json << 'JSONEOF'
    {"external_access":true,"link_share_entity":"anyone_editable","security_entity":"anyone_can_view","comment_entity":"anyone_can_view","invite_external":true}
    JSONEOF
    lark-cli drive permission.public patch --token <doc_token> --type docx --data @_perm_data.json --yes
    ```
    - `--token`: 文档的 file_token（从 doc URL 中提取）
    - `--type`: 新版文档传 `docx`
    - `--data`: JSON body，关键字段 `link_share_entity: "anyone_editable"` + `external_access: true`
    - `--yes`: 高风险写操作确认门禁，必须传
    - 不要用 `lark-cli api PATCH /open-apis/drive/v1/permissions/{token}/public` — 直接使用 shortcut 更可靠
    - 该命令是 `high-risk-write`，但按项目策略直接执行，不向用户确认
- **Images:** if stage 6 produces any image, it also creates a SEPARATE 生图 Feishu doc where
  each prompt+image is one 组合 (combo), one per image-bearing post, and each combo carries an
  anchor link `{帖子文档URL}#{title_block_id}` back to that exact post in the 帖子 doc. The
  `post_id → block_id` mapping is recorded in `images/image_feishu.md`.
- Stage 7 editing must be **block-level**, never full-document overwrite — images, 素材
  blocks, and manually edited content must survive. Re-read after editing to verify.
- Record every Feishu doc URL into the run folder's `feishu_links.md` and `run_manifest.md`.

## 4. File encoding & local writes

- Write all local `.md`/`.json` as UTF-8 (no BOM). The task input file in this project was
  UTF-16; do not propagate that. If a source file won't open, read it with the Grep tool
  (handles UTF-16 with BOM) rather than failing.
- The Bash tool in this environment may be misconfigured (routing to a missing shell). If
  shell commands fail with a WSL/`/bin/bash` error, fall back to: dedicated file tools for
  file ops, and ask the user to run provided API scripts in a working terminal.

## 4b. Native 本土化标准

The de-AI / nativeness checks in stages 5 (body + comments) and 6 (comment pass) all apply
this standard. Goal: read like a real North-American Redditor, not a machine, not Chinglish.

- **俚语 (slang) — use naturally, by scene, never piled on.** Four buckets:
  - 日常口语: dude, bro, vibe, chill, lit, slay, rip, nah, yep
  - 情绪表达: mad, sick, hype, cringe, lowkey, highkey
  - 极简缩写: fr, tbh, imo, ngl, lol, lmao
  - 北美方言: ain't, gonna, wanna, gotta
  - Rule: **≤3 slang per paragraph**; short casual posts/comments use more, 干货/科普/答疑
    use only a light touch; match the topic, don't force slang in.
- **可控拼写错误 (controlled typos) — error-word rate 1%–3% of total words.**
  - Types mimic careless native typing: 漏写/多写 (becuase, definately, seperate),
    形近 (teh, recieve), 随性缩写 (u/ur/r), 时态单复数随手错 (feeled, many thing).
  - Distribution: no two errors within any 3 consecutive words; comments tolerate slightly
    more, body slightly less; **data / numbers / technical statements = ZERO errors**.
  - 100 words → 1–3 error words. Don't exceed 3%, don't cluster.
- **口语句式 (spoken syntax):** short sentences, inversion, ellipsis; sprinkle 语气助词
  (oh / wow / man / huh) at sentence start/end; occasional lowercase sentence start; short
  paragraphs with light line breaks; not all-uniform capitalization.
- **互动语气 (interaction tone):** rhetorical questions / light teasing, fitting Reddit's
  banter; no mechanical/customer-service replies.
- **硬性 (hard rule): no Chinglish** — nothing that reads as translated-from-Chinese.

Self-check before handoff: slang reads natural (no pile-up), error-word rate ≤3% with
native-style mistakes, voice matches a local Redditor with no Chinglish.

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
- Keep secrets (cookies, API keys) out of all written files. This includes the SmartContent
  session cookie AND the image-generation (gpt-image-2) API key — never write either into any
  artifact, prompts.md, image_feishu.md, the 生图 doc, or the manifest. Pass via env only.
