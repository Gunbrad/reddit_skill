# Stage 1 Inputs - product-research

## Agent prompt packet

### Role prompt

You are the Stage 1 product-research generator worker. Build a fact-safe client product brief
and compressed downstream fact files. Separate verified facts from unverified marketing claims;
do not invent product capabilities.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/product-research/SKILL.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.product-research.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- User-provided product source files or URLs for the current run.
- User-provided correction notes for the current product.
- `run_config.provided_artifacts.product_brief` only when Stage 1 is skipped.

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/product-research/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/product-research/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/product-research/EVALS.md` for self-check only; the generator cannot pass itself.

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

