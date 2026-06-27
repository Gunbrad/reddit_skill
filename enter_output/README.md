# Reddit Posting Workflow — Skill Family + Evals

Produced for the task in `任务提示词.md`. This is a **skill 族**: 7 workflow-stage skills +
1 orchestrator, each stage paired with its own EVALS system, designed so each stage's output
is strictly structured for the next stage and a failing eval sends the stage back for rework
(打回重改) before handoff.

## Install

Copy `skills/*` into your agent's skills directory (e.g. `~/.claude/skills/`). Each folder
has a `SKILL.md` (YAML frontmatter: name + description / trigger) and most have `EVALS.md`.

## Structure

```
skills/
  reddit-posting-workflow/   # orchestrator: trigger chain, run-folder convention, handoff contract
    SKILL.md
    conventions.md           # shared: red lines, API auth, Feishu rules (+public-edit permission), Native 本土化标准, encoding, eval loop
  product-research/          # stage 1: → product_brief.md (capability tree, competitor matrix, 差异化)
    SKILL.md  EVALS.md
  topic-selection/           # stage 2: → topics.md + Feishu doc (选题)
    SKILL.md  EVALS.md
  search-query-occupancy/    # stage 3: top6 选题 × 3 candidate queries → pick 1 each → 6 directions → topic cards
    SKILL.md  EVALS.md  api-reference.md  run_search_occupancy.py
  topic-card-selection/      # stage 4: binary gate — screen ALL cards to the production-safe subset (no top-N)
    SKILL.md  EVALS.md
  topic-card-optimization/   # stage 5: viral (爆帖) potential → top-N → supplemental notes (incl. 选题 anchor) → drafts
    SKILL.md  EVALS.md
  post-optimization/         # stage 6: de-AI/native, fact-check, image2, ≥3 subreddits, Feishu  (deepest evals)
    SKILL.md  EVALS.md  IMAGE_PROMPT_EVALS.md   # + 实体类/虚拟类 image-prompt de-AI evals; builds a 生图 Feishu doc (prompt+image combos) anchor-linked back to each post
  feishu-formatting/         # stage 7: layout standard, comment normalization, brand highlight
    SKILL.md  EVALS.md
live_run/                    # ready-to-run stage-3 API run on project enter-pro (new queries)
  run_config.json  README.md
```

## Per-task workspace

Each posting task creates one run folder `{YYYYMMDD_HHMMSS}_{project_slug}` with numbered
subfolders `01_product_brief/ … 07_format/` and a `run_manifest.md` log. Stages 1/2/3/6 each
write a mandatory local artifact; stage 6 also saves images + prompts locally. See the
orchestrator SKILL.md.

## Customization & decoupling (`run_config.json`)

User overrides live in one file, `run_config.json`, read by every stage (see orchestrator
SKILL.md for the full schema): `skip_stages` + `provided_artifacts` (skip a stage by
supplying its artifact), `topics`/`topic_count` (default 6), `queries_per_topic` (default 3),
`topic_card_count`/`topic_card_length`, `top_n`, `draft_length_multiplier`,
`supplemental_context`, `generate_images`. These OVERRIDE any hard-coded constants; the EVALS
check "matches run_config", not a fixed number (no forced 36-card total).

**Decoupling:** stages depend only on the previous stage's artifact, not on having run it.
Provide a product brief → skip stage 1; provide 选题 → skip stage 2. The skill normalizes
the user's material into the stage's required structure and still runs that stage's EVALS
before proceeding. Free-form text is structured by running the stage, not handed downstream
raw. Secrets never go in `run_config.json` (env only).

## Local-artifact requirements (from the task)

- Stage 1 → local product brief md.
- Stage 2 → local 选题 md (+ Feishu).
- Stage 3 → top6 选题, 3 candidate queries each → pick 1 → 6 directions; local search-query md (+ maps).
- Stage 4 → `04_screen/screening.md`: binary pass/fail over ALL cards (production-safe subset).
- Stage 5 → `05_optimized_cards/`: viral-potential ranking → top-N → per-card supplemental note
  (incl. the originating 选题 as参考-not-script anchor so drafts don't drift) → drafts.
- Stage 6 → per post: main title + ≥3 备用标题 + ≥3 target subreddits; images + their prompts
  saved locally (+ Feishu). De-AI/native follows the Native 本土化标准 (conventions.md §4b):
  slang ≤3/paragraph, typo rate 1-3%, spoken syntax, no Chinglish.
- Stage 7 → preserves the Target Subreddit line and 备用标题 (≥3) when reformatting.
- **All produced Feishu docs** are set to "anyone on the internet with the link can edit"
  (conventions.md §3) — done directly, without asking the user.
- Every task → a new timestamped run folder.

## Evals philosophy

Each EVALS.md is a scored rubric with **blocking** criteria + a threshold. Stage 5 ranks for
爆帖 potential behind a compliance/nativeness precondition gate; stage 6's de-AI/native rubric
is the deepest (5 sub-systems, higher bar, blind-reviewer prompt). A stage hands off only
after its blocking criteria pass and the verdict is logged.

## Live run status

`live_run/` is fully prepared with 6 new long-tail queries for project `enter-pro`. It was
NOT executed here because this environment's Bash tool is broken (routes to a non-existent
WSL `/bin/bash`), so no shell could drive the authenticated API. Run the one command in
`live_run/README.md` from a working terminal to execute it.
