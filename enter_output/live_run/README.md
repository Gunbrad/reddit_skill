# Live API Run — Stage 3 (search-occupancy) on project `enter-pro`

This folder is set up to run the SmartContent search-occupancy workflow end to end with
**new long-tail search queries** (the 6 directions in `run_config.json`, distinct from the
2026-06-26 baseline run).

## Why this wasn't auto-run

The Bash tool in this environment is misconfigured: every shell command is routed through a
WSL relay whose `/bin/bash` does not exist (`execvpe(/bin/bash) failed: No such file or
directory`), and disabling the sandbox does not change the routing. So I could not execute
`python`/`curl` to drive the authenticated API. Everything else (the skill family, the
config, the script) is ready — only the execution step is blocked on a working shell.

## How to run it (one command, in a working terminal)

The cookie is read from an env var so it never lands in a file.

### Windows (cmd.exe)
```cmd
cd /d "D:\personal_workspace\reddit_writting\reddit\接口test\新工作流接口测试\enter_output\live_run"
set PLANNER_SESSION=<paste planner_session value>
python ..\skills\search-query-occupancy\run_search_occupancy.py --config run_config.json --out .
```

### Git Bash / WSL with real bash
```bash
cd "/d/personal_workspace/reddit_writting/reddit/接口test/新工作流接口测试/enter_output/live_run"
export PLANNER_SESSION='<paste planner_session value>'
python ../skills/search-query-occupancy/run_search_occupancy.py --config run_config.json --out .
```

The session value the user provided in this task starts with `eyJleHAiOjE3ODI4OTI2ODci...`.
(Not stored here on purpose. The token also has an `exp` ~ Unix 1782892687, so refresh it if
expired.)

## What the script does

1. `GET /api/auth/me` (verify cookie)
2. Reuses project `enter-pro`, creates a run with the 6 directions
3. `prepare-all` then polls run status (~10 min)
4. Prints per-direction map status (success vs failed)
5. Downloads maps/urls/raw posts for success directions into `maps/` and `materials/`
6. Generates 12 Topic Cards per direction, downloads them into `topic_cards/`
7. Writes `run_meta.json` (project_id, run_id, direction ids, chosen ids) — no cookie

## After it runs

- Check `run_status.json` → `search_occupancy_map_summary.directions[].status`.
- Apply stage-3 EVALS Gate B: pick **3 mutually-exclusive** success directions.
- Then continue with stage 4 (`topic-card-selection`) using `run_meta.json`.
