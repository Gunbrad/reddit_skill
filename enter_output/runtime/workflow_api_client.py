from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class WorkflowApiError(RuntimeError):
    pass


class SmartContentWorkflowClient:
    def __init__(self, *, base_url: str | None = None, session_env: str = "PLANNER_SESSION") -> None:
        self.base_url = (base_url or os.environ.get("SMARTCONTENT_BASE_URL") or "https://smartcontent.shifenglab.com").rstrip("/")
        self.session_env = session_env

    def create_search_occupancy_project(self, *, name: str, product_brief_path: Path, notes: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/api/search-occupancy/projects",
            {
                "name": name,
                "product_brief": product_brief_path.read_text(encoding="utf-8"),
                "notes": notes,
            },
        )

    def run_search_occupancy(self, *, project_id: str, config: dict[str, Any], poll_seconds: int = 10) -> dict[str, Any]:
        run = self._request(
            "POST",
            f"/api/search-occupancy/projects/{project_id}/runs",
            {
                "posts_per_query": config.get("posts_per_query", 10),
                "search_directions": config["search_directions"],
            },
        )
        run_id = run["run_id"]
        self._request("POST", f"/api/search-occupancy/projects/{project_id}/runs/{run_id}/prepare-all", {})
        while True:
            status = self._request("GET", f"/api/search-occupancy/projects/{project_id}/runs/{run_id}")
            if status.get("status") in {"succeeded", "failed", "error"}:
                return status
            time.sleep(poll_seconds)

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        planner_session = os.environ.get(self.session_env, "")
        if not planner_session:
            raise WorkflowApiError(f"{self.session_env} is required")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(f"{self.base_url}{path}", data=data, method=method)
        request.add_header("Cookie", f"planner_session={planner_session}")
        request.add_header("Accept", "application/json")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", errors="replace").replace(planner_session, "[REDACTED]")
            raise WorkflowApiError(f"SmartContent API error {exc.code}: {text}") from exc
        except urllib.error.URLError as exc:
            raise WorkflowApiError(f"SmartContent API connection failed: {exc.reason}") from exc
        if not payload:
            return {}
        return json.loads(payload.decode("utf-8"))
