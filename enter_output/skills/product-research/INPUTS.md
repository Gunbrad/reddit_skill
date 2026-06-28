# Stage 1 Inputs - product-research

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
