# Stage 2 Inputs - topic-selection

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `01_product_brief/handoff_packet.json`
- `01_product_brief/product_brief.md` only when the compressed fact index lacks a required persona, boundary, or differentiation detail. If read, log the exact reason in `run_manifest.md`.
- User-provided topics only when named in `run_config.topics` or `run_config.provided_artifacts.topics`.

## Forbidden files

- Full prior conversation history.
- Stage 1 scratchpads and raw research notes.
- Failed topic drafts unless explicitly needed for a retry report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps.
- Full product brief when `global/product_fact_index.json` and `global/brand_safety_rules.md` are sufficient.
- Topic cards, screened cards, optimized drafts, or final posts from later stages.
