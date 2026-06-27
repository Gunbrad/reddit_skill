# SmartContent API Contract

## Base URL And Auth

Base URL:

```text
https://smartcontent.shifenglab.com
```

All business requests require a valid session cookie:

```http
Cookie: planner_session=<session>
Accept: application/json
```

Verify authentication first:

```http
GET /api/auth/me
```

If auth fails, stop and ask for a fresh session. Do not continue with placeholder API results.

## Search Occupancy Run

Create or reuse a project:

```http
POST /api/search-occupancy/projects
Content-Type: application/json
```

Body:

```json
{
  "name": "{Product Name}",
  "product_brief": "{full product brief markdown}",
  "notes": "{workflow notes}"
}
```

Create a run:

```http
POST /api/search-occupancy/projects/{project_id}/runs
Content-Type: application/json
```

Body:

```json
{
  "posts_per_query": 10,
  "search_directions": [
    {
      "direction_id": "direction_001",
      "query": "long tail query"
    }
  ]
}
```

Start full preparation:

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/prepare-all
```

Poll:

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}
```

Poll every 5-15 seconds until `status` is `succeeded` or `failed`.

Hard rule: `run.status = succeeded` is not enough. Also inspect:

```text
search_occupancy_map_summary.directions[].status
search_occupancy_map_summary.directions[].map_md
search_occupancy_map_summary.directions[].map_json
```

Only directions with successful map artifacts can be used for topic-card generation.

## Download Assets

Use exact download kinds.

| Asset | Endpoint |
| --- | --- |
| Map summary MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/summary/download/summary_md` |
| Direction map MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/{direction_id}/download/map_md` |
| Direction map JSON | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/{direction_id}/download/map_json` |
| Search URL JSON | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-urls/{direction_id}/download/json` |
| Search URL MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-urls/{direction_id}/download/md` |
| Raw posts MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-materials/{direction_id}/download/raw_posts_md` |
| Post Cards JSONL | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-materials/{direction_id}/download/post_cards_jsonl` |
| Topic Cards MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/download/topic_cards_md` |
| Drafts MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/download/drafts_md` |

If Topic Cards or Drafts are downloaded before generation, the API may return `Search planning artifact not found.` Generate first, then retry.

## Topic Cards

Generate topic cards:

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/topic-cards/generate
Content-Type: application/json
```

Body:

```json
{
  "count": 12,
  "supplemental_context": "{direction-specific instruction}",
  "overwrite": true
}
```

Allowed counts: 12, 18, 24. This workflow defaults to 12 per selected direction.

Query topic cards:

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/topic-cards
```

## Drafts

Create a draft job:

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/drafts/jobs
Content-Type: application/json
```

Body:

```json
{
  "topic_ids": ["topic_001"],
  "topic_supplemental_contexts": {
    "topic_001": "client feedback and missing context"
  },
  "length_multiplier": 1,
  "overwrite": true
}
```

Poll:

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/drafts/jobs/{job_id}
```

Poll every 5-10 seconds until `status` is `completed` or `failed`. Save all `errors`, `completed_topic_ids`, and `failed_count` into the local eval report.

## Failure Handling

- Auth failure: stop and request a valid session.
- Direction map failure: drop that direction unless the user explicitly asks to retry.
- Fewer than 3 successful directions: revise queries or rerun search before topic-card generation.
- Draft job partial failure: keep completed drafts, list failed topics, and either retry failed topics or pick replacement cards.
- API artifact missing: check whether the generation endpoint was called and completed.
- Download kind error: fix endpoint path; do not retry the same invalid kind.
