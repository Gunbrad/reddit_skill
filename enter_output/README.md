# Reddit Posting Workflow — Skill Family + Evals

Produced for the task in `任务提示词.md`. This is a **skill 族**: 6 workflow-stage skills +
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
    conventions.md           # shared: red lines, API auth, Feishu rules, encoding, eval loop
  product-research/          # stage 1: → product_brief.md (capability tree, competitor matrix, 差异化)
    SKILL.md  EVALS.md
  topic-selection/           # stage 2: → topics.md + Feishu doc (选题)
    SKILL.md  EVALS.md
  search-query-occupancy/    # stage 3: long-tail queries + workflow API + maps + 12 topic cards
    SKILL.md  EVALS.md  api-reference.md  run_search_occupancy.py
  topic-card-selection/      # stage 4: score 36 cards → top-N + supplemental notes → drafts
    SKILL.md  EVALS.md
  post-optimization/         # stage 5: de-AI/native, fact-check, image2, ≥3 subreddits, Feishu  (deepest evals)
    SKILL.md  EVALS.md
  feishu-formatting/         # stage 6: layout standard, comment normalization, brand highlight
    SKILL.md  EVALS.md
live_run/                    # ready-to-run stage-3 API run on project enter-pro (new queries)
  run_config.json  README.md
```

## Per-task workspace

Each posting task creates one run folder `{YYYYMMDD_HHMMSS}_{project_slug}` with numbered
subfolders `01_product_brief/ … 06_format/` and a `run_manifest.md` log. Stages 1/2/3/5 each
write a mandatory local artifact; stage 5 also saves images + prompts locally. See the
orchestrator SKILL.md.

## Local-artifact requirements (from the task)

- Stage 1 → local product brief md.
- Stage 2 → local 选题 md (+ Feishu).
- Stage 3 → local search-query md (+ maps).
- Stage 5 → images + their prompts saved locally (+ Feishu).
- Every task → a new timestamped run folder.

## Evals philosophy

Each EVALS.md is a scored rubric with **blocking** criteria + a threshold. Stage 5's de-AI /
native rubric is the deepest (5 sub-systems, higher bar, blind-reviewer prompt). A stage
hands off only after its blocking criteria pass and the verdict is logged.

## Live run status

`live_run/` is fully prepared with 6 new long-tail queries for project `enter-pro`. It was
NOT executed here because this environment's Bash tool is broken (routes to a non-existent
WSL `/bin/bash`), so no shell could drive the authenticated API. Run the one command in
`live_run/README.md` from a working terminal to execute it.
