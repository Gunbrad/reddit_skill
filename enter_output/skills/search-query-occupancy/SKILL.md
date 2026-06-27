---
name: search-query-occupancy
description: Use after 选题 are locked, when generating long-tail Reddit search queries, when calling the SmartContent search-occupancy workflow API to crawl Reddit and build occupancy maps, when picking mutually-exclusive search directions, or when generating Topic Cards for a direction. Stage 3 of the Reddit posting pipeline.
---

# Search Query + Occupancy Workflow + Topic Cards (Stage 3)

## Overview

Convert each 选题 into long-tail search queries, run them through the SmartContent
search-occupancy workflow (which crawls Reddit and builds a "搜索占位分析地图" per
direction), pick directions that are mutually exclusive, and generate Topic Cards for the
chosen directions. This stage owns the **workflow API integration**.

**Core principle:** queries must be long-tail (specific multi-word intent phrases that map
to a real "demo 之后"/scenario stage), not broad keywords. Chosen directions must not
overlap, so the resulting Topic Cards cover different ground.

## When to use

- `02_topics/topics.md` exists and passed stage-2 EVALS.
- You need search queries, occupancy maps, and/or Topic Cards.

Not for: selecting which cards to draft (stage 4) — that's the next stage.

## Plan: how 选题 → queries → directions → cards

1. **2 queries per 选题** (long-tail). These become `search_directions` in the API run.
2. Run prepare-all; each direction gets a search-occupancy map (some may fail — check
   direction-level status).
3. From the successful directions, **pick 3 that are mutually exclusive / non-overlapping**
   (per the task: 选择方向互斥的 3 个搜索方向).
4. Generate **12 Topic Cards per chosen direction** → 36 cards total feed stage 4.

Note: the platform caps a run at 6 final directions. If you have more than 3 选题, either
run in batches or pick the 6 strongest queries, then down-select to 3 directions after maps.

## API workflow (summary — full detail in api-reference.md)

```
1. GET  /api/auth/me                                              (verify cookie)
2. POST /api/search-occupancy/projects                           (create/reuse project)
3. POST /api/search-occupancy/projects/{pid}/runs                (submit search_directions)
4. POST /api/search-occupancy/projects/{pid}/runs/{rid}/prepare-all
5. GET  /api/search-occupancy/projects/{pid}/runs/{rid}          (poll → succeeded, ~10min)
6. check search_occupancy_map_summary.directions[].status        (per-direction!)
7. download maps/urls/materials for success directions
8. POST /directions/{did}/topic-cards/generate  {count:12,...}
9. GET  /directions/{did}/topic-cards            (or download topic_cards_md)
```

- Auth = `Cookie: planner_session=<session>`. Keep the cookie out of all written files.
- `run.status == succeeded` is NOT sufficient — a direction's map can fail. Only pick
  directions with `status: success` and `map_md/map_json: true`.
- A runnable end-to-end script is in `run_search_occupancy.py` (uses `PLANNER_SESSION` env
  var; never hard-code the cookie). Use it when a working shell is available.

## Required output structure

Write to `03_search/` (UTF-8):

- `search_queries.md` — the queries you generated, grouped by 选题 / 主线, each tagged with
  its `direction_id` and the rationale for why it's long-tail. MANDATORY local artifact.
- `run_meta.json` — `{project_id, run_id, direction_ids, chosen_direction_ids, posts_per_query}`
  (NO cookie). Stage 4 reads this to know which directions/run to draft from.
- `maps/{direction_id}.md` + `.json` — downloaded occupancy maps for chosen directions.
- `materials/{direction_id}/` — downloaded search-urls / raw posts / post_cards as needed.
- `topic_cards/{direction_id}.md` (+ raw) — the 12 cards per chosen direction.

### search_queries.md format

```
# {Product} 搜索 Query (run {run_id})

## 主线一：{...}  (选题 1)
- direction_001 | "long tail query string"
  - 长尾理由：{why this is specific intent, not a broad keyword}
- direction_002 | "another long tail query"
  - 长尾理由：...
```

## Process

1. Read `topics.md`. For each 选题 write 2 long-tail queries → assign `direction_id`s.
2. Write `search_queries.md`. Run the QUERY portion of EVALS; revise weak/broad queries.
3. Create/reuse the project; create the run with all directions; prepare-all; poll.
4. Read `search_occupancy_map_summary`. Keep only success directions.
5. Pick 3 mutually-exclusive directions (run the DIRECTION portion of EVALS for overlap).
6. Download maps/materials for the 3. Generate 12 Topic Cards each. Download/store them.
7. Write `run_meta.json`. Log manifest. Hand off 36 cards to `topic-card-selection`.

## Common mistakes

- Broad keyword queries ("AI app builder") instead of long-tail intent phrases.
- Trusting `run.status: succeeded` and drafting from a direction whose map failed.
- Picking 3 overlapping directions → near-duplicate Topic Cards.
- Hard-coding the session cookie into a file or the script.
- Downloading topic_cards_md before generation (404) — generate first.
