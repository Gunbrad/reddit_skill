# PIPELINE_CONTRACT.md - subreddit build canonical I/O

This is the source of truth for what each stage reads, writes, and hands off. Every stage's
`INPUTS.md`, `OUTPUT_SCHEMA.json`, and `HANDOFF_SCHEMA.json` must agree with this file.

## Run Workspace

One run uses one folder named `{YYYYMMDD_HHMMSS}_{project_slug}/`.

Required top-level files:

- `run_config.json`
- `run_manifest.md`

Required global files from Stage 1:

- `global/product_fact_index.json`
- `global/claim_boundary_table.json`
- `global/brand_safety_rules.md`

## Counts And Knobs

| Knob | Default | Source |
|---|:---:|---|
| reference subreddits | max 6 | user / run_config |
| posts per subreddit | 15 | run_config |
| total post limit | 120 | SmartContent API |
| retrieval `top_k` | 8 | run_config or user |
| Topic Card count | 12 | run_config; allowed 12, 18, 24 |
| mechanism variants per card | 8 | fixed |
| draft TopN | null -> confirm/user | run_config or user |
| draft length multiplier | 1 | run_config; UI map 更短0.3/稍短0.5/默认1/稍长1.8/更长2.5; one draft job supports one shared multiplier |

## Stage 1 - product-research

- Reads: raw product materials and `run_config.json`.
- Writes: `01_product_brief/product_brief.md`, `global/product_fact_index.json`,
  `global/claim_boundary_table.json`, `global/brand_safety_rules.md`.
- Handoff: `01_product_brief/handoff_packet.json`.

## Stage 2 - community-capture

- Reads: `run_config.json`, Stage 1 handoff, product brief, global fact files.
- Calls: `/api/projects`, `/api/projects/{project_id}/runs` with `run_type=community_builder_rpa_init`,
  run/artifact/content-map/download endpoints.
- Writes:
  - `02_community_capture/community_capture.md`
  - `02_community_capture/run_meta.json`
  - `02_community_capture/artifacts/community_post_urls.json`
  - `02_community_capture/artifacts/community_post_urls.md`
  - `02_community_capture/artifacts/raw_posts.md`
  - `02_community_capture/artifacts/content_maps.json`
  - `02_community_capture/artifacts/community_insights.json`
  - `02_community_capture/artifacts/community_insights.md`
  - `02_community_capture/artifacts/embeddings_status.json`
- Handoff: `02_community_capture/handoff_packet.json`.
- Rule: do not补抓失败社区 in this workflow version. Record failures and continue with successful communities only.

## Stage 3 - community-topic-retrieval

- Reads: `run_config.json`, global fact files, Stage 2 handoff, content maps,
  `community_insights.json/md`, embeddings status.
- Calls: `/retrieval/search`, `/topic-cards/generate`, `/downloads`, `/download/{key}`.
- Writes:
  - `03_topic_retrieval/retrieval_round.json`
  - `03_topic_retrieval/topic_cards.json`
  - `03_topic_retrieval/topic_cards.md`
  - `03_topic_retrieval/reference_post_cards.json`
  - `03_topic_retrieval/feishu_links.md`
- Handoff: `03_topic_retrieval/handoff_packet.json`.

## Stage 4 - mechanism-variant-selection

- Reads: `run_config.json`, global fact files, Stage 3 handoff, `03_topic_retrieval/topic_cards.json`,
  `03_topic_retrieval/reference_post_cards.json`, and Stage 2 `community_insights.json`.
- Calls: mechanism history, generate, and apply endpoints for every Topic Card.
- Writes:
  - `04_mechanism_selection/mechanism_selection.md`
  - `04_mechanism_selection/applied_variants.json`
  - `04_mechanism_selection/variant_history.json`
- Handoff: `04_mechanism_selection/handoff_packet.json`.

## Stage 5 - community-card-draft-generation

- Reads: `run_config.json`, global fact files, Stage 4 handoff, applied Topic Cards, original Topic Cards,
  topic Feishu link, reference post cards, and Stage 2 `community_insights.json`.
- Calls: `/drafts/jobs`, `/drafts/jobs/{job_id}`, `/drafts`, `/downloads`.
- Writes:
  - `05_optimized_cards/optimization.md`
  - `05_optimized_cards/draft_jobs_receipt.json`
  - `05_optimized_cards/drafts_md/{post_id}.md`
  - `05_optimized_cards/handoff_packet.json`
- Handoff: `05_optimized_cards/handoff_packet.json` with per-post `viral_intent`,
  `topic_anchor`, selected mechanism, supplemental context, the draft job's shared length
  multiplier, and claim ids. If selected cards need different lengths, Stage 5 must split
  them into separate draft jobs grouped by `length_multiplier`.

## Stage 6 - post-optimization coordinator

Stage 6 is a coordinator over four sub-workers. It may read only `run_config.json`, global fact
files, Stage 5 handoff, chosen draft files named by that handoff, and approved Stage 6
sub-stage artifacts as they are produced. It must not directly read Stage 2/3 raw artifacts,
including `community_insights`; Stage 5 has already compressed the relevant community risk and
viral intent into its handoff.

Sub-workers:

- **6a `post-native-rewrite`** reads Stage 5 handoff + chosen drafts + global fact files and
  writes `06_optimized/native_posts.md` and `06_optimized/6a_handoff_packet.json`.
- **6b `post-fact-brand-check`** reads `native_posts.md`, `6a_handoff_packet.json`, and global
  fact files; writes `06_optimized/checked_posts.md` and `06_optimized/6b_handoff_packet.json`.
- **6c `post-subreddit-image`** reads `checked_posts.md`, `6b_handoff_packet.json`, and global
  fact files; writes `06_optimized/final_posts.md`, optional `06_optimized/images/*`, and
  `06_optimized/6c_handoff_packet.json`. Images are optional; subreddit packaging is mandatory.
- **6d `post-feishu-publish`** reads `final_posts.md`, optional images, `6c_handoff_packet.json`,
  and `03_topic_retrieval/feishu_links.md`; writes `06_optimized/feishu_links.md`,
  optional `06_optimized/images/image_feishu.md`, and `06_optimized/6d_handoff_packet.json`.

Stage 6 final handoff: `06_optimized/handoff_packet.json` with final posts path, Feishu links,
post doc URL, image doc URL/null, viral-intent preservation verdicts, and 6a/6b/6c/6d evaluator
verdicts.

## Stage 7 - feishu-formatting

- Reads: `run_config.json`, `global/brand_safety_rules.md`, Stage 6 handoff,
  and the post doc URL in `06_optimized/feishu_links.md`.
- Writes: `07_format/format_report.md`; edits the Feishu doc in place.
- Handoff: `07_format/handoff_packet.json`.

## Context Transfer Matrix

| Artifact | Produced by | May be read by | Must not be read by |
|---|---|---|---|
| `global/product_fact_index.json`, `claim_boundary_table.json`, `brand_safety_rules.md` | Stage 1 | Stages 2-7 | none |
| `01_product_brief/product_brief.md` | Stage 1 | Stage 2 only | Stages 3-7 unless `INPUTS.md` explicitly logs a blocker |
| `02_community_capture/artifacts/content_maps.json` | Stage 2 | Stage 3, optionally Stage 4/5 via their `INPUTS.md` | Stage 6/7 |
| `02_community_capture/artifacts/community_insights.json` | Stage 2 | Stage 3, Stage 4, Stage 5 | Stage 6/7 direct reads |
| `03_topic_retrieval/reference_post_cards.json` | Stage 3 | Stage 4 and Stage 5 | Stage 6/7 |
| `03_topic_retrieval/topic_cards.json` | Stage 3 | Stage 4 and Stage 5 | Stage 6/7 |
| `04_mechanism_selection/applied_variants.json` | Stage 4 | Stage 5 | Stage 6/7 |
| `05_optimized_cards/handoff_packet.json` | Stage 5 | Stage 6 coordinator and 6a | Stage 7 direct reads |
| `06_optimized/handoff_packet.json` | Stage 6 | Stage 7 | earlier stages |

## Handoff Rule

The next stage reads only the approved upstream `handoff_packet.json` and the artifact paths
listed in that packet. Reading whole upstream folders, raw scratchpads, old runs, or unrelated
Feishu docs is forbidden unless an `INPUTS.md` file explicitly permits it.
