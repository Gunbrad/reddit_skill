from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_config(config_path: Path, run_dir: Path) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    target = run_dir / "run_config.json"
    if not target.exists():
        shutil.copyfile(config_path, target)
    return read_json(target)


def append_manifest(run_dir: Path, line: str) -> None:
    manifest = run_dir / "run_manifest.md"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")


def write_candidate_files(run_dir: Path, files: dict[str, str]) -> list[str]:
    written: list[str] = []
    root = run_dir.resolve()
    for relative_path, content in files.items():
        if Path(relative_path).is_absolute():
            raise ValueError(f"Artifact path must be run-relative, got {relative_path}")
        target = (run_dir / relative_path).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"Artifact path escapes run directory: {relative_path}")
        write_text(target, content)
        written.append(relative_path)
    return written


def declared_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            paths.update(declared_paths(child))
    elif isinstance(value, list):
        for child in value:
            paths.update(declared_paths(child))
    elif isinstance(value, str):
        normalized = value.replace("\\", "/")
        if "/" in normalized and (normalized.endswith(".md") or normalized.endswith(".json")):
            paths.add(normalized)
    return paths


def missing_declared_files(run_dir: Path, output: dict[str, Any]) -> list[str]:
    missing = []
    for relative_path in sorted(declared_paths(output)):
        if not (run_dir / relative_path).exists():
            missing.append(relative_path)
    return missing


def stage_runtime_dir(run_dir: Path, stage_dir: str, attempt: int) -> Path:
    return run_dir / stage_dir / "runtime" / f"attempt_{attempt:03d}"
