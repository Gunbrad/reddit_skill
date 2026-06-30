from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import write_json, write_text


def write_stage_manifest(
    stage_dir: Path,
    *,
    stage: str,
    generator_request_id: str,
    eval_request_id: str,
    verdict: str,
    retry_count: int,
    approved_handoff_path: str,
) -> dict[str, Any]:
    manifest = {
        "stage": stage,
        "generator_request_id": generator_request_id,
        "eval_request_id": eval_request_id,
        "verdict": verdict,
        "retry_count": retry_count,
        "approved_handoff_path": approved_handoff_path,
    }
    write_json(stage_dir / "run_manifest.json", manifest)
    write_text(
        stage_dir / "run_manifest.md",
        "\n".join(
            [
                f"# {stage} Run Manifest",
                "",
                f"- generator request id: `{generator_request_id}`",
                f"- eval request id: `{eval_request_id}`",
                f"- verdict: `{verdict}`",
                f"- retry count: `{retry_count}`",
                f"- approved handoff path: `{approved_handoff_path}`",
                "",
            ]
        ),
    )
    return manifest
