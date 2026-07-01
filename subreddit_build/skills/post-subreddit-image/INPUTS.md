# Stage 6c Inputs - post-subreddit-image

## Agent prompt packet

### Role prompt

You are the Stage 6c post-subreddit-image generator worker. Preserve the checked text, choose
viable subreddits, and package image prompts or images that look like real Reddit artifacts,
not ads or AI output.

### Required instruction files

Read in order:

1. `repo:subreddit_build/skills/subreddit-build-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:subreddit_build/skills/subreddit-build-workflow/CONTEXT_CONTRACT.md`
3. `repo:subreddit_build/skills/subreddit-build-workflow/WORKER_CONTRACT.md`
4. `repo:subreddit_build/skills/subreddit-build-workflow/conventions.md`
5. `repo:subreddit_build/skills/post-subreddit-image/SKILL.md`
6. `repo:subreddit_build/skills/post-subreddit-image/IMAGE_PROMPT_EVALS.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.post-subreddit-image.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:06_optimized/checked_posts.md`
- `run:06_optimized/6b_handoff_packet.json` if written by 6b.
- `run:05_optimized_cards/handoff_packet.json`
- Image API reference supplied for the current run, with credentials from environment only.
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:subreddit_build/skills/post-subreddit-image/OUTPUT_SCHEMA.json`
5. `repo:subreddit_build/skills/post-subreddit-image/HANDOFF_SCHEMA.json`
6. `repo:subreddit_build/skills/post-subreddit-image/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Image API reference only when supplied for the current run.
- No API keys, cookies, or secrets may be read from files; use environment variables only.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/checked_posts.md`
- `06_optimized/6b_handoff_packet.json` if written by 6b.
- `05_optimized_cards/handoff_packet.json`
- `subreddit_build/skills/post-subreddit-image/EVALS.md`
- `subreddit_build/skills/post-subreddit-image/IMAGE_PROMPT_EVALS.md`
- `subreddit_build/skills/post-subreddit-image/OUTPUT_SCHEMA.json`
- `subreddit_build/skills/post-subreddit-image/HANDOFF_SCHEMA.json`
- Image API reference supplied for the current run, with credentials from environment only.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 6d Feishu docs before they are created by 6d.
- Stage 2 community artifacts including `community_insights.json`; use the compressed Stage 5 handoff instead.

