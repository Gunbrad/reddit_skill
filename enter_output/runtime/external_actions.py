from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from .artifacts import write_json


class SearchProjectError(RuntimeError):
    pass


class SearchProjectAdapter(Protocol):
    def create_placeholder(self, *, run_id: str, run_dir: Path, product_brief_path: Path, config: dict[str, Any]) -> dict[str, Any]:
        ...


class NoopSearchProjectAdapter:
    def create_placeholder(self, *, run_id: str, run_dir: Path, product_brief_path: Path, config: dict[str, Any]) -> dict[str, Any]:
        return {"status": "skipped", "reason": "no adapter configured", "idempotency_key": run_id}


class HttpSearchProjectAdapter:
    """SmartContent search-occupancy project adapter from the existing Skill docs."""

    def create_placeholder(self, *, run_id: str, run_dir: Path, product_brief_path: Path, config: dict[str, Any]) -> dict[str, Any]:
        settings = config.get("search_project_placeholder", {})
        base_url = (
            settings.get("base_url")
            or os.environ.get(settings.get("base_url_env", "SMARTCONTENT_BASE_URL"))
            or "https://smartcontent.shifenglab.com"
        ).rstrip("/")
        url = settings.get("api_url") or f"{base_url}/api/search-occupancy/projects"
        planner_session = os.environ.get(settings.get("session_env", "PLANNER_SESSION"), "")
        if not planner_session:
            raise SearchProjectError("PLANNER_SESSION is required for SmartContent search project creation")
        product_name = settings.get("name") or config.get("project_name") or config.get("project_id") or "Project"
        notes = settings.get("notes") or f"Created by reddit workflow runtime. run_id={run_id}"
        payload = {
            "name": f"{product_name} {run_id}",
            "product_brief": product_brief_path.read_text(encoding="utf-8"),
            "notes": notes,
        }
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        headers["Cookie"] = f"planner_session={planner_session}"
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method=settings.get("method", "POST"),
        )
        try:
            with urllib.request.urlopen(request, timeout=int(settings.get("timeout_seconds", 60))) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise SearchProjectError(f"search placeholder API error {exc.code}: {_redact(planner_session, body)}") from exc
        except urllib.error.URLError as exc:
            raise SearchProjectError(f"search placeholder API connection failed: {exc.reason}") from exc


@dataclass(frozen=True)
class ExternalAction:
    action_id: str
    action_type: str
    title: str
    content_file: str
    result_file: str


def create_action_manifest(run_dir: Path, action: dict[str, Any]) -> dict[str, Any]:
    action_id = _safe_action_id(action.get("action_id") or f"feishu_{uuid.uuid4().hex[:8]}")
    result_file = _safe_result_file(action.get("result_file"), action_id)
    manifest = {
        "status": "needs_external_action",
        "action_id": action_id,
        "action_type": action["action_type"],
        "title": action.get("title", action["action_type"]),
        "content_file": action.get("content_file", ""),
        "result_file": result_file,
    }
    manifest_path = run_dir / "actions" / f"{action_id}.json"
    write_json(manifest_path, manifest)
    return {"manifest": manifest, "manifest_path": str(manifest_path)}


def _safe_action_id(action_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", action_id)


def _safe_result_file(result_file: str | None, action_id: str) -> str:
    fallback = f"actions/{action_id}.result.json"
    if not result_file:
        return fallback
    candidate = Path(result_file)
    normalized = result_file.replace("\\", "/")
    if candidate.is_absolute() or ".." in candidate.parts or not normalized.startswith("actions/"):
        return fallback
    return normalized


def action_result_exists(run_dir: Path, manifest: dict[str, Any]) -> bool:
    return (run_dir / manifest["result_file"]).exists()


def read_action_result(run_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    return json.loads((run_dir / manifest["result_file"]).read_text(encoding="utf-8"))


def search_placeholder_enabled(config: dict[str, Any]) -> bool:
    settings = config.get("search_project_placeholder", {})
    return bool(settings.get("enabled"))


def load_or_create_search_placeholder(
    *,
    adapter: SearchProjectAdapter,
    run_id: str,
    run_dir: Path,
    product_brief_path: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    receipt_path = run_dir / "external" / "search_project.json"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("status") in {"created", "succeeded", "success"} or receipt.get("project_id"):
            return receipt
    receipt = adapter.create_placeholder(
        run_id=run_id,
        run_dir=run_dir,
        product_brief_path=product_brief_path,
        config=config,
    )
    receipt.setdefault("idempotency_key", run_id)
    write_json(receipt_path, receipt)
    return receipt


def _redact(secret: str, text: str) -> str:
    return text.replace(secret, "[REDACTED]") if secret else text
