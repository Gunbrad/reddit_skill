---
name: community-capture
description: Use after product research when filling the SmartContent community builder project with client name, product brief, reference subreddits, posts-per-subreddit, and notes, then starting and waiting for the long community crawl. Stage 2 of the subreddit build workflow.
---

# Community Capture (Stage 2)

## Overview

Create or update the SmartContent community builder project, start the `community_builder_rpa_init`
run, wait for the long crawl to finish, and download the successful run artifacts. This stage
owns the slow API integration and the run heartbeat.

**Core principle:** run success is not community success. A crawl can return `status=succeeded`
while some subreddits failed. This workflow records failed subreddits but does not补抓 them.

## Inputs

- `run_config.json` with `client_name`, `reference_subreddits`, `posts_per_subreddit`, and optional `notes`.
- Stage 1 handoff and `01_product_brief/product_brief.md`.
- Global fact files for brand boundary context.
- `PLANNER_SESSION` environment variable for the SmartContent cookie.

## Required Output

Write to `02_community_capture/`:

- `community_capture.md` - human-readable run summary, heartbeat log, successful/failed subreddit list.
- `run_meta.json` - `project_id`, `run_id`, `status`, `successful_subreddits`, `failed_subreddits`, counts, API paths.
- `artifacts/community_post_urls.json`
- `artifacts/community_post_urls.md`
- `artifacts/raw_posts.md`
- `artifacts/content_maps.json`
- `artifacts/community_insights.json`
- `artifacts/community_insights.md`
- `artifacts/embeddings_status.json`
- `handoff_packet.json`

## API Flow

1. `GET /api/auth/me` to verify auth.
2. Create or update project with `POST /api/projects` or `PATCH /api/projects/{project_id}`.
3. Start run with `POST /api/projects/{project_id}/runs` and `run_type=community_builder_rpa_init`.
4. Poll `GET /api/projects/{project_id}/runs/{run_id}` until terminal status.
5. Check `GET /api/projects/{project_id}/runs/{run_id}/artifacts`.
6. Download available community URLs, raw posts, content maps, and embedding status.

## Process

1. Normalize subreddit names without `r/`; enforce max 6 and total planned posts <= 120.
2. Submit the project payload using the Stage 1 product brief as `product_brief`.
3. Start the crawl run and poll with heartbeat entries recording stage, status, elapsed time,
   raw post count, post card count, and failed subreddit count.
4. When terminal, inspect artifact counts. Continue only if at least one subreddit succeeded and
   embeddings exist or the run has reached `build_embeddings/finalize`.
5. Download only available artifacts. Do not guess download keys and do not use `HEAD`.
6. Derive `community_insights` from the successful communities' content maps and raw/post-card
   evidence. For each successful subreddit, write exactly these fields: community positioning,
   high-frequency topics, transferable patterns, primary content forms, community motivations,
   and risk warnings. Do not synthesize insights for failed subreddits.
7. Write `run_meta.json` and the approved handoff packet.

## Common Mistakes

- Treating `status=succeeded` as all communities succeeded.
- Re-running failed subreddits even though this workflow version explicitly does not补抓.
- Saving the cookie in config, artifacts, or manifests.
- Sending Chinese JSON through non-UTF-8 PowerShell request bodies.
