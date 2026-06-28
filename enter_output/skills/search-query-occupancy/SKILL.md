---
name: search-query-occupancy
description: Use after 选题 are locked, when generating long-tail Reddit search queries, when calling the SmartContent search-occupancy workflow API to crawl Reddit and build occupancy maps, or when generating Topic Cards for each direction. Stage 3 of the Reddit posting pipeline.
---

# Search Query + Occupancy Workflow + Topic Cards (Stage 3)

## Overview

Convert each 选题 into long-tail search queries, run them through the SmartContent
search-occupancy workflow (which crawls Reddit and builds a "搜索占位分析地图" per
direction), and generate Topic Cards for every successful direction. This stage owns the
**workflow API integration**.

**Core principle:** queries must be long-tail (specific multi-word intent phrases that map
to a real "demo 之后"/scenario stage), not broad keywords. Each 选题 maps to exactly ONE
chosen query (one direction), so each direction stays anchored to its 选题.

## When to use

- `02_topics/topics.md` exists and passed stage-2 EVALS.
- You need search queries, occupancy maps, and/or Topic Cards.
- Read `run_config.json` for `topic_count` (选题 count, default 6), `queries_per_topic`
  (candidates per 选题, default 3), `topic_card_count`, `topic_card_length`,
  `posts_per_query` (fall back to defaults 6 / 3 / 12 / default / 10).
  Steer card length via the generate call's supplemental_context per `topic_card_length`.

Not for: screening cards (stage 4) — that's the next stage.

## Plan: how 选题 → queries → directions → cards

The workflow run accepts at most **6 search directions**, so the design is **top-6 选题, one
query each**:

1. Take the **top `topic_count` 选题** (default 6) from topics.md.
2. For each 选题, draft **`queries_per_topic` candidate long-tail queries** (default 3) with
   distinct angles, then **pick the single best one**. That chosen query = that 选题's
   `direction_id`. → `topic_count` directions total (default 6), each uniquely tied to a 选题.
3. Run prepare-all; each direction gets a search-occupancy map (some may fail — check
   direction-level status).
4. Generate **`run_config.topic_card_count` Topic Cards per successful direction** (default
   12). ALL successful directions generate cards — no forced down-select. The card set
   (size = successful_directions × topic_card_count) feeds stage 4.

If a direction's map fails, re-run or replace that direction; do not silently drop a 选题.

## API workflow (summary — full detail in api-reference.md)

```
1. GET  /api/auth/me                                              (verify cookie)
2. POST /api/search-occupancy/projects                           (create/reuse project)
3. POST /api/search-occupancy/projects/{pid}/runs                (submit search_directions: 1 chosen query per 选题)
4. POST /api/search-occupancy/projects/{pid}/runs/{rid}/prepare-all
5. GET  /api/search-occupancy/projects/{pid}/runs/{rid}          (poll → succeeded, ~10min)
6. check search_occupancy_map_summary.directions[].status        (per-direction!)
7. download maps/urls/materials for success directions
8. POST /directions/{did}/topic-cards/generate  {count:<topic_card_count>,...}
9. GET  /directions/{did}/topic-cards            (or download topic_cards_md)
```

- Auth = `Cookie: planner_session=<session>`. Keep the cookie out of all written files.
- `run.status == succeeded` is NOT sufficient — a direction's map can fail. Only use
  directions with `status: success` and `map_md/map_json: true`.
- A runnable end-to-end script is in `run_search_occupancy.py` (uses `PLANNER_SESSION` env
  var; never hard-code the cookie). Use it when a working shell is available.

## Required output structure

Write to `03_search/` (UTF-8):

- `search_queries.md` — per 选题: the `queries_per_topic` candidates, which one was chosen,
  the `direction_id`, and the long-tail rationale. MANDATORY local artifact.
- `run_meta.json` — `{project_id, run_id, direction_ids, topic_to_direction, posts_per_query}`
  (NO cookie). `topic_to_direction` maps each 选题 → its direction_id so stages 4/5 can trace
  a card back to its 选题. Stage 4 reads this to know which directions/run to screen.
- `maps/{direction_id}.md` + `.json` — downloaded occupancy maps for successful directions.
- `materials/{direction_id}/` — downloaded search-urls / raw posts / post_cards as needed.
- `topic_cards/{direction_id}.md` (+ raw) — the cards per direction (count per run_config).
- `occupancy_heat_evidence.json` — MANDATORY structured heat evidence per direction, so stage 5
  picks TopN on evidence, not vibes. Per direction record:
  ```json
  {
    "direction_001": {
      "similar_posts": [{"title": "...", "subreddit": "r/...", "upvotes": 0, "comments": 0, "url": "..."}],
      "title_patterns": ["how I ... after ...", "is it just me or ..."],
      "subreddit_behavior": "what gets upvoted / what gets removed here",
      "comment_triggers": ["asking for others' workflow", "tool comparison"],
      "recent_activity": "high/medium/low + rough cadence",
      "moderation_risk": "low/medium/high + why (self-promo filter, etc.)",
      "skepticism_angles": ["users distrust X", "common pushback is Y"]
    }
  }
  ```
  Build it from the downloaded maps + post_cards (the crawl already contains this signal);
  do NOT fabricate numbers — if a field is unknown, mark it so.

### search_queries.md format

```
# {Product} 搜索 Query (run {run_id})

## 选题 1：{选题标题}  (主线一)
候选 query：
1. "candidate query A" — 角度：...
2. "candidate query B" — 角度：...
3. "candidate query C" — 角度：...
入选：direction_001 | "candidate query B"
  - 选择理由：{why B beats A/C for search-occupancy intent}
  - 长尾理由：{why this is specific intent, not a broad keyword}
```

## Process

1. Read `topics.md`. Take the top `topic_count` 选题 (default 6). For each, draft
   `queries_per_topic` candidate queries (default 3) and pick the best 1 → assign `direction_id`.
2. Write `search_queries.md` (candidates + chosen + rationale). Run Gate A of EVALS; revise
   weak/broad queries.
3. Create/reuse the project; create the run with the chosen queries (≤6 directions); prepare-all; poll.
4. Read `search_occupancy_map_summary`. Keep success directions (re-run/replace failures).
5. Run Gate B (direction sanity). Generate `topic_card_count` Topic Cards per success direction. Store them.
6. Build `occupancy_heat_evidence.json` from the maps + post_cards (no fabricated numbers).
7. Write `run_meta.json` (incl. `topic_to_direction`) + `handoff_packet.json`. Log manifest.
   Run Gate C. Hand off the generated cards + heat evidence to `topic-card-selection`.

## Common mistakes

- Broad keyword queries ("AI app builder") instead of long-tail intent phrases.
- More than 6 directions submitted to one run (platform cap is 6).
- Picking a weak candidate query when a sharper one existed (record why the chosen beats the rest).
- Trusting `run.status: succeeded` and proceeding from a direction whose map failed.
- Silently dropping a 选题 whose direction failed instead of re-running/replacing it.
- Hard-coding the session cookie into a file or the script.
- Downloading topic_cards_md before generation (404) — generate first.
