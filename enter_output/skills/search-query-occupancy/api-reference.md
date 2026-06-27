# SmartContent Search-Occupancy API Reference

Base: `https://smartcontent.shifenglab.com`
Auth: every request sends `Cookie: planner_session=<session>` + `Accept: application/json`.
Keep the cookie in an env var; never write it into committed files.

## 0. Auth check
```
GET /api/auth/me  →  {username, display_name, planner_id}
```

## 1. Projects
```
GET  /api/search-occupancy/projects
POST /api/search-occupancy/projects
     body: {name, product_brief, notes}
     → {project_id, ...}            # project_id is a slug derived from name
GET  /api/search-occupancy/projects/{project_id}
PATCH /api/search-occupancy/projects/{project_id}   # name/product_brief/notes (optional)
```

## 2. Runs (search material prep)
```
GET  /api/search-occupancy/projects/{pid}/runs
POST /api/search-occupancy/projects/{pid}/runs
     body: {posts_per_query, search_directions:[{direction_id, query}, ...]}
     # creating a run only saves directions + dirs; it does NOT crawl
     # platform caps final directions at 6
POST /api/search-occupancy/projects/{pid}/runs/{rid}/prepare-all   # no body; starts pipeline
GET  /api/search-occupancy/projects/{pid}/runs/{rid}              # poll
```

Pipeline stages observed:
`prepare_search_pipeline → collect_search_urls → collect_post_details →
generate_post_cards → generate_search_occupancy_maps → search_pipeline_completed`

Poll every 5-15s. ~10 min for 60 posts. Terminal run status: `succeeded`.

**Critical:** check per-direction map status, not just run status:
```
run.search_occupancy_map_summary.directions[] = {
  direction_id, query, status: "success"|"failed",
  post_cards_count, subreddit_count, map_json: bool, map_md: bool, error?
}
```
Only use directions with `status: success` and `map_md/map_json: true`.

## 3. Read / download
```
GET /api/search-occupancy/projects/{pid}/runs/{rid}/search-occupancy-maps/{did}   # map JSON
```
Download endpoints (all GET, return Content-Disposition attachment):

| Asset | Path suffix (after .../runs/{rid}) |
|-------|------------------------------------|
| Map summary MD | `/search-occupancy-maps/summary/download/summary_md` |
| Direction map MD | `/search-occupancy-maps/{did}/download/map_md` |
| Direction map JSON | `/search-occupancy-maps/{did}/download/map_json` |
| Search URL JSON | `/search-urls/{did}/download/json` |
| Search URL MD | `/search-urls/{did}/download/md` |
| Raw posts MD | `/search-materials/{did}/download/raw_posts_md` |
| Post Cards JSONL | `/search-materials/{did}/download/post_cards_jsonl` |
| Topic Cards MD | `/directions/{did}/download/topic_cards_md`  (after generation) |
| Drafts MD | `/directions/{did}/download/drafts_md`  (after generation) |

Errors: before generation → 404 `Search planning artifact not found.`
Wrong kind → 400 `Invalid search planning download kind.`

## 4. Topic Cards
```
GET  /api/search-occupancy/projects/{pid}/runs/{rid}/directions/{did}/topic-cards   # [] before gen
POST .../directions/{did}/topic-cards/generate
     body: {count: 12|18|24, supplemental_context: str|null, overwrite: bool}
PATCH .../directions/{did}/topic-cards/{topic_id}   # {status:"shortlisted"|"candidate"} (optional)
```
Topic card fields: topic_id, title_direction, content_form, post_format,
expression_mechanism, brand_exposure_method, needs_extra_material, required_material,
reference_logic, source_card_ids, target_subreddit, status.

Selecting cards has NO save endpoint — pass chosen topic_ids to the draft job (stage 4).

## 5. Drafts (stage 4 uses these)
```
GET  .../directions/{did}/drafts
POST .../directions/{did}/drafts/jobs
     body: {topic_ids:[...], topic_supplemental_contexts:{topic_id:note,...},
             length_multiplier:1, overwrite:bool}
     → {job_id, status:"running", ...}
GET  .../directions/{did}/drafts/jobs/{job_id}    # poll 5-10s → status:"completed"
```
Draft markdown fields: post_v1_markdown, post_v2_markdown, comment_design_markdown,
final_markdown (use final_markdown as the post).

## 6. Optional (not required)
```
POST /api/search-occupancy/search-directions/suggest
     body: {product_name, product_brief, notes?, count}   # AI-suggested queries; we hand-write instead
```

## Recommended order
auth → create/reuse project → create run → prepare-all → poll succeeded → check
per-direction status → download assets → generate topic cards → (stage 4) draft job.
