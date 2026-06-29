# PIPELINE_CONTRACT.md — canonical inputs / outputs / handoff per stage

The single source of truth for what each stage reads, writes, and hands off. Every stage's
`INPUTS.md`, `OUTPUT_SCHEMA.json`, and `HANDOFF_SCHEMA.json` must agree with this table. A
stage may depend ONLY on an upstream stage's **approved artifact** + **approved
`handoff_packet.json`**. Reading any file not whitelisted in the stage's `INPUTS.md` or
`PROMPT_INJECTION_CONTRACT.md` prompt packet is forbidden (CONTEXT_CONTRACT §5).

## Pipeline shape

- **7 logical stages.** Stage 6 is a coordinator over sub-workers 6a-6d (see below).
- Run workspace: one folder `{YYYYMMDD_HHMMSS}_{project_slug}/` (see orchestrator SKILL.md).
- Compressed global files live under `{run}/global/` and are produced by Stage 1.

## Counts (canonical — keep all docs consistent with these)

| Knob | Default | Source |
|------|:--:|--------|
| 选题 count (`topic_count`) | 6 | run_config |
| candidate queries per 选题 (`queries_per_topic`) | 3 → pick 1 | run_config |
| search directions per run | = chosen queries (≤6 platform cap) | derived |
| topic cards per direction (`topic_card_count`) | 12 | run_config |
| stage-4 screening | binary gate, no top-N | — |
| stage-5 top-N (`top_n`) | null → propose & confirm | run_config |
| draft length (`draft_length_multiplier`) | 1 (更短0.3/稍短0.5/默认1/稍长1.8/更长2.5) | run_config |

## Global compressed files (produced by Stage 1, read by Stages 2–7)

| File | Purpose |
|------|---------|
| `global/product_fact_index.json` | claim-level fact index for fact-checking (id, claim, status, allowed/forbidden wording) |
| `global/claim_boundary_table.json` | verified / unverified / forbidden claim buckets |
| `global/brand_safety_rules.md` | brand-exposure boundary, 不可说 content, sensitive wording |

Downstream stages read these instead of the full `01_product_brief/product_brief.md`. The full
brief is re-read ONLY if the index is missing something, and the re-read is logged in the manifest.

## Stage-by-stage I/O

### Stage 1 — product-research
- **Reads:** raw product facts / source material; `run_config.json`.
- **Writes:** `01_product_brief/product_brief.md` **and** the three `global/*` compressed files.
- **Handoff:** `01_product_brief/handoff_packet.json` → points to brief + global files.

### Stage 2 — topic-selection
- **Reads (allowed):** `run_config.json`, `global/product_fact_index.json`,
  `global/brand_safety_rules.md`; Stage 1 handoff packet.
- **Writes:** `02_topics/topics.md` (+ 选题 Feishu doc link in `02_topics/feishu_links.md`).
- **Handoff:** `02_topics/handoff_packet.json` (the 选题 set, 主线 grouping).

### Stage 3 — search-query-occupancy
- **Reads (allowed):** `run_config.json`, `global/*` (fact index + brand rules); Stage 2
  handoff packet + `02_topics/topics.md`.
- **Writes:** `03_search/search_queries.md`, `03_search/run_meta.json`,
  `03_search/maps/{did}.md|json`, `03_search/topic_cards/{did}.json`, and
  `03_search/occupancy_heat_evidence.json` (structured heat evidence per direction).
- **Handoff:** `03_search/handoff_packet.json` (direction_ids, topic_to_direction, heat-evidence path).

### Stage 4 — topic-card-selection
- **Reads (allowed):** `run_config.json`, `global/*`; Stage 3 handoff packet,
  `03_search/topic_cards/{did}.json`, `03_search/maps/*`, `03_search/run_meta.json`.
- **Writes:** `04_screen/screening.md`, `04_screen/passed_cards.json` (the passing cards),
  updates `run_meta.json.screened_pass_ids`.
- **Handoff:** `04_screen/handoff_packet.json` (passed card ids only — NOT all cards).

### Stage 5 — topic-card-optimization
- **Reads (allowed):** `run_config.json`, `global/*`; Stage 4 handoff packet +
  `04_screen/passed_cards.json`; `03_search/occupancy_heat_evidence.json`;
  `03_search/topic_cards/{did}.json` (only for passed ids); `02_topics/topics.md`
  (选题 anchor), `run_meta.json.topic_to_direction`.
- **Writes:** `05_optimized_cards/optimization.md`, `05_optimized_cards/drafts_md/{post_id}.md`,
  updates `run_meta.json` with job ids + chosen topic_ids.
- **Handoff:** `05_optimized_cards/handoff_packet.json` — MUST carry per post: `viral_intent`
  (`core_hook`, `emotional_trigger`, `comment_engine`, `must_preserve[]`), `title_pattern_to_preserve`,
  `expected_comment_types[]`, `subreddit_risk_note`, `allowed_claim_ids[]`, `forbidden_claim_ids[]`.

### Stage 6 — post-optimization (coordinator over 6a-6d)
Explicitly authorized to run sub-workers (worker depth > 1 allowed here only).
- **Reads (allowed):** `run_config.json`, `global/*`; Stage 5 handoff packet +
  `05_optimized_cards/drafts_md/{post_id}.md` (only chosen drafts).
- Sub-workers and their I/O:
  - **6a content-optimization** (`post-native-rewrite`): drafts + Stage-5 handoff →
    `06_optimized/native_posts.md`. MUST preserve `viral_intent` (blocking eval).
  - **6b fact-brand check** (`post-fact-brand-check`): `native_posts.md` + fact index + brand
    rules → `06_optimized/checked_posts.md`.
  - **6c packaging: subreddit + image** (`post-subreddit-image`): `checked_posts.md` →
    `06_optimized/final_posts.md` plus optional `06_optimized/images/*`.
  - **6d packaging: Feishu publish** (`post-feishu-publish`): `final_posts.md` + images →
    Feishu docs + `06_optimized/feishu_links.md`.
  > Minimum required split: **content-optimization (6a)** vs **packaging (6c+6d)**. The
  > four post-* skill folders implement this; 6b is the fact/brand gate between them.
- **Writes:** `06_optimized/final_posts.md`, `06_optimized/images/*`, `06_optimized/feishu_links.md`.
- **Handoff:** `06_optimized/handoff_packet.json` (帖子 doc URL, image doc URL or "none",
  per-post viral_intent preservation verdict).

### Stage 7 — feishu-formatting
- **Reads (allowed):** `run_config.json`, `global/brand_safety_rules.md`; Stage 6 handoff
  packet + the 帖子 Feishu doc URL from `06_optimized/feishu_links.md`.
- **Writes:** `07_format/format_report.md`; edits the Feishu doc in place (block-level).
- **Handoff:** `07_format/handoff_packet.json` (final doc URLs, formatting verdict).

## Handoff rule

Each stage's worker writes `{stage_dir}/handoff_packet.json` conforming to that stage's
`HANDOFF_SCHEMA.json`. The next stage reads the **handoff packet first** and only opens the
specific upstream artifacts the packet references — never the whole upstream working set.
