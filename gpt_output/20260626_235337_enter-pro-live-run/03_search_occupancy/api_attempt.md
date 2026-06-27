# SmartContent API Attempt

- Attempted At: 2026-06-26T23:59:00+08:00
- Script: `reddit/接口test/新工作流接口测试/enter_output/skills/search-query-occupancy/run_search_occupancy.py`
- Config: `03_search_occupancy/run_config.json`
- Result: BLOCKED

## Error

```text
ERROR: set PLANNER_SESSION env var to the planner_session cookie value.
```

## Interpretation

The new search directions and run config are ready, but the authenticated SmartContent workflow cannot start without a valid `planner_session` cookie.

## Continue Command

From the repository root:

```powershell
$env:PLANNER_SESSION = "<paste planner_session cookie>"
python 'reddit\接口test\新工作流接口测试\enter_output\skills\search-query-occupancy\run_search_occupancy.py' --config 'reddit\接口test\新工作流接口测试\gpt_output\20260626_235337_enter-pro-live-run\03_search_occupancy\run_config.json' --out 'reddit\接口test\新工作流接口测试\gpt_output\20260626_235337_enter-pro-live-run\03_search_occupancy'
```

Do not store the cookie in any tracked or written artifact.
