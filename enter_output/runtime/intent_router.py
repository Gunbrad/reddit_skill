from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUESTED_SCOPES = {"full_pipeline", "stage_range", "single_stage"}
SOURCE_MODES = {"run_artifact", "feishu_url", "inline_text", "provided_file"}


def load_intent(path: Path) -> dict[str, Any]:
    intent = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(intent, dict):
        raise ValueError("intent must be a JSON object")
    validate_intent(intent)
    return intent


def validate_intent(intent: dict[str, Any]) -> None:
    scope = intent.get("requested_scope", "full_pipeline")
    if scope not in REQUESTED_SCOPES:
        raise ValueError(f"Unknown requested_scope {scope!r}")
    source_mode = intent.get("source_mode")
    if source_mode is not None and source_mode not in SOURCE_MODES:
        raise ValueError(f"Unknown source_mode {source_mode!r}")
    if scope == "single_stage" and not intent.get("target_stage"):
        raise ValueError("single_stage intent requires target_stage")
    if scope == "stage_range" and not (intent.get("from_stage") or intent.get("to_stage")):
        raise ValueError("stage_range intent requires from_stage or to_stage")
    if source_mode == "feishu_url" and not intent.get("feishu_url"):
        raise ValueError("feishu_url source_mode requires feishu_url")


def stage_selection_from_intent(available: list[str], intent: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
    scope = intent.get("requested_scope", "full_pipeline")
    if scope == "single_stage":
        target_stage = intent.get("target_stage")
        _require_available(available, target_stage)
        return target_stage, None, None
    if scope == "stage_range":
        from_stage = intent.get("from_stage")
        to_stage = intent.get("to_stage") or intent.get("stop_after_stage")
        if from_stage:
            _require_available(available, from_stage)
        if to_stage:
            _require_available(available, to_stage)
        return None, from_stage, to_stage
    stop_after_stage = intent.get("stop_after_stage")
    if stop_after_stage:
        _require_available(available, stop_after_stage)
    return None, None, stop_after_stage


def apply_intent_to_config(config: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    merged = dict(config)
    for key in (
        "requested_scope",
        "target_stage",
        "from_stage",
        "to_stage",
        "source_mode",
        "feishu_url",
        "inline_text_path",
        "source_text_path",
        "source_artifact_path",
        "expected_artifact",
        "stop_after_stage",
        "user_goal",
    ):
        if key in intent:
            merged[key] = intent[key]
    if intent.get("requested_scope") == "single_stage":
        merged["single_stage_mode"] = True
    return merged


def _require_available(available: list[str], stage: str | None) -> None:
    if stage not in available:
        raise ValueError(f"Unknown stage {stage!r}; expected one of {', '.join(available)}")
