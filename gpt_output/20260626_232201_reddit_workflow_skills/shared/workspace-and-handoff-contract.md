# Workspace And Handoff Contract

## Project Workspace

For every client task, create one local project folder before step 1:

```text
{output_root}/{YYYYMMDD_HHMMSS}_{project_slug}/
```

Rules:

- Use lowercase `project_slug`; replace spaces with `-`; remove punctuation that breaks paths.
- Keep all task artifacts inside this folder.
- Do not overwrite a previous task folder.
- Maintain `manifest.json` and update it at the end of every step.

Recommended structure:

```text
{task_folder}/
  manifest.json
  00_inputs/
  01_product_brief/
  02_topic_plan/
  03_search_occupancy/
    directions/
  04_card_selection/
  05_posts/
    images/
  06_formatted/
  eval_reports/
```

## Manifest Fields

`manifest.json` must include:

```json
{
  "project_name": "",
  "project_slug": "",
  "created_at": "",
  "source_materials": [],
  "product_brief_md": "",
  "topic_plan_md": "",
  "feishu_topic_doc": {
    "title": "",
    "url": "",
    "token": ""
  },
  "search_query_md": "",
  "smartcontent": {
    "project_id": "",
    "run_id": "",
    "selected_direction_ids": [],
    "posts_per_query": 10
  },
  "topic_cards_md": [],
  "selected_topics_md": "",
  "draft_request_json": "",
  "raw_drafts_md": "",
  "optimized_posts_md": "",
  "feishu_posts_doc": {
    "title": "",
    "url": "",
    "token": ""
  },
  "image_assets": [],
  "formatted_posts_md": "",
  "eval_reports": []
}
```

Use empty strings or arrays for fields not yet produced. Never invent IDs or URLs; leave unknown values empty and add an issue in the relevant eval report.

## Cross-Step Naming

Use stable filenames so later skills can locate artifacts:

- `01_product_brief/product_brief.md`
- `02_topic_plan/topic_plan.md`
- `03_search_occupancy/search_queries.md`
- `03_search_occupancy/directions/{direction_id}/search_occupancy_map.md`
- `03_search_occupancy/directions/{direction_id}/topic_cards.md`
- `04_card_selection/topic_card_scores.md`
- `04_card_selection/draft_request.json`
- `04_card_selection/raw_drafts.md`
- `05_posts/optimized_posts.md`
- `05_posts/images/{post_id}/image_prompt.md`
- `05_posts/images/{post_id}/image_metadata.json`
- `06_formatted/formatted_posts.md`

## Handoff Discipline

Every handoff must include:

- Path to the artifact.
- Eval report path.
- Open questions or blocked facts.
- Product facts that must be preserved downstream.
- Claims that must not be used unless validated.

If a downstream step finds a missing upstream field, stop and either repair the upstream artifact or mark the exact field as blocked. Do not silently fill gaps with invented facts.
