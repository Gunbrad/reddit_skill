# Stage 6d Inputs - post-feishu-publish

## Agent prompt packet

### Role prompt

You are the Stage 6d post-feishu-publish generator worker. Create the required Feishu
deliverables from approved final posts and images, verify anchors, record links, and set docs
public-editable. Do not rewrite post content.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/PROMPT_INJECTION_CONTRACT.md`
2. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
3. `repo:enter_output/skills/reddit-posting-workflow/WORKER_CONTRACT.md`
4. `repo:enter_output/skills/reddit-posting-workflow/conventions.md`
5. `repo:enter_output/skills/post-feishu-publish/SKILL.md`
6. `workspace:reddit/提示词/reddit_帖子文档改写通用提示词.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.post-feishu-publish.extra_instruction_files`.

### Business input files

- `run:run_config.json`
- `run:06_optimized/final_posts.md`
- `run:06_optimized/images/prompts.md` when images or pending prompts exist.
- `run:06_optimized/images/{post_id}.png` when generated images exist.
- `run:06_optimized/6c_handoff_packet.json` if written by 6c.
- `run:02_topics/topics.md`
- `run:02_topics/feishu_links.md`
- `run:global/product_fact_index.json`
- `run:global/claim_boundary_table.json`
- `run:global/brand_safety_rules.md`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/post-feishu-publish/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/post-feishu-publish/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/post-feishu-publish/EVALS.md` for self-check only; the generator cannot pass itself.

### Allowed extra reads

- Live Feishu docs created or linked by the current run only.
- No old Feishu docs, API keys, cookies, or unrelated Drive files.

## Allowed global files

- `run_config.json`
- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Allowed stage files

- `06_optimized/final_posts.md`
- `06_optimized/images/prompts.md` when images or pending prompts exist.
- `06_optimized/images/{post_id}.png` when generated images exist.
- `06_optimized/6c_handoff_packet.json` if written by 6c.
- `02_topics/topics.md`
- `02_topics/feishu_links.md`
- `enter_output/skills/post-feishu-publish/EVALS.md`
- `enter_output/skills/post-feishu-publish/OUTPUT_SCHEMA.json`
- `enter_output/skills/post-feishu-publish/HANDOFF_SCHEMA.json`

## Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless the coordinator passes an evaluator failure report for retry.
- Unrelated run folders.
- Old Feishu docs not linked by the current run.
- Raw Reddit dumps.
- `01_product_brief/product_brief.md`.
- Stage 5 raw cards, maps, and unchosen drafts.
- Stage 7 formatting reports.
- API keys, cookies, or other secrets in any file.
