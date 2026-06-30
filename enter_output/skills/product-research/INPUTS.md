# Stage 1 Inputs - product-research

## Agent prompt packet

### Role prompt

You are the Stage 1 product-research generator worker. Build a fact-safe Enter product brief
and compressed downstream fact files. Separate verified facts from unverified marketing claims;
do not invent product capabilities.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/product-research/SKILL.md`
6. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.product-research.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run_config.product_sources` for user-provided product source files or URLs for the current run.
- `run_config.provided_artifacts` for user-provided correction notes or source artifacts.
- `run_config.provided_artifacts.product_brief` only when Stage 1 is skipped.

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/product-research/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/product-research/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/product-research/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- None by default. Extra product source files must be named in `run_config` or passed by the orchestrator and logged in `run_manifest.md`.

## Allowed global files

- `run_config.json`
- User-provided product source files or URLs for the current run.
- User-provided correction notes for the current product.

## Allowed stage files

- None. Stage 1 starts the pipeline.
- If `run_config.skip_stages` includes stage 1, read only the user-provided artifact named in `run_config.provided_artifacts.product_brief` and normalize it into the canonical output.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless explicitly referenced in `run_config.provided_artifacts`.
- Unrelated run folders.
- Old Feishu docs from other runs.
- Raw Reddit dumps.
- Topic cards, drafts, optimized posts, or formatting outputs from later stages.
