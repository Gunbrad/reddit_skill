# Stage 4 Inputs - topic-card-selection

## Agent prompt packet

### Role prompt

You are the Stage 4 topic-card-selection generator worker. Judge every generated Topic Card
with the binary gate: community-compliant, production-ready, product-relevant, and low-risk.
Do not rank cards here.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/topic-card-selection/SKILL.md`
6. `workspace:reddit/接口test/帖子native化/评价体系.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.topic-card-selection.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:03_search/handoff_packet.json`
- `run:03_search/run_meta.json`
- `run:03_search/maps/{direction_id}.md`
- `run:03_search/maps/{direction_id}.json`
- `run:03_search/topic_cards/{direction_id}.json`
- `run:03_search/occupancy_heat_evidence.json`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/topic-card-selection/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/topic-card-selection/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/topic-card-selection/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- `run:03_search/topic_cards/{direction_id}.md` only when the JSON card file lacks required text.
- No unrelated raw Reddit dumps or later-stage artifacts.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`
- `global/campaign_policy.md` if present.

## Allowed stage files

- `03_search/handoff_packet.json`
- `03_search/run_meta.json`
- `03_search/maps/{direction_id}.md`
- `03_search/maps/{direction_id}.json`
- `03_search/topic_cards/{direction_id}.json`
- `03_search/topic_cards/{direction_id}.md` only when the JSON card file lacks required text.
- `03_search/occupancy_heat_evidence.json` for moderation and community-risk clues.

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps beyond the current Stage 3 artifacts whitelisted above.
- Full product brief when compressed global files are sufficient.
- Stage 5 optimized notes or drafts.
- Stage 6/7 final posts, Feishu docs, image prompts, or formatting reports.
