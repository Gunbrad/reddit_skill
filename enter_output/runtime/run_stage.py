from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from enter_output.runtime.artifacts import write_json
from enter_output.runtime.intent_router import apply_intent_to_config, load_intent, stage_selection_from_intent
from enter_output.runtime.model_client import ModelClient, create_model_client
from enter_output.runtime.runner import DEFAULT_STAGE_ORDER, PipelineRunner, RunOptions


def load_stage_registry(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / "enter_output" / "runtime" / "stage_registry.json").read_text(encoding="utf-8"))


def stage_order(repo_root: Path) -> list[str]:
    registry_path = repo_root / "enter_output" / "runtime" / "stage_registry.json"
    if registry_path.exists():
        return [stage["name"] for stage in load_stage_registry(repo_root)["stages"]]
    skills_dir = repo_root / "enter_output" / "skills"
    if skills_dir.exists():
        discovered = [
            path.name
            for path in skills_dir.iterdir()
            if path.is_dir() and (path / "OUTPUT_SCHEMA.json").exists() and (path / "HANDOFF_SCHEMA.json").exists()
        ]
        if discovered:
            return discovered
    return list(DEFAULT_STAGE_ORDER)


def select_stages(
    available: list[str],
    *,
    stage: str | None = None,
    from_stage: str | None = None,
    to_stage: str | None = None,
) -> list[str]:
    if stage:
        _require_stage(available, stage)
        return [stage]
    start = available.index(from_stage) if from_stage else 0
    end = available.index(to_stage) if to_stage else len(available) - 1
    if end < start:
        raise ValueError("--to stage must not come before --from stage")
    return available[start : end + 1]


def run_with_client(
    *,
    repo_root: Path,
    model_client: ModelClient,
    stage: str | None = None,
    from_stage: str | None = None,
    to_stage: str | None = None,
    run_dir: Path | None = None,
    config_path: Path | None = None,
    max_retries: int = 5,
    resume: bool = False,
    feishu_url: str | None = None,
    intent_path: Path | None = None,
    source_text: Path | None = None,
    dry_run_packet: bool = False,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    available = stage_order(repo_root)
    intent = load_intent(intent_path) if intent_path else None
    if intent:
        intent_stage, intent_from, intent_to = stage_selection_from_intent(available, intent)
        stage = stage or intent_stage
        from_stage = from_stage or intent_from
        to_stage = to_stage or intent_to
    selected = select_stages(available, stage=stage, from_stage=from_stage, to_stage=to_stage)
    if run_dir is None:
        runs_root = repo_root / "temp_output"
        run_id = None
    else:
        run_dir = Path(run_dir)
        runs_root = run_dir.parent
        run_id = run_dir.name
    config_path = _prepare_config(repo_root, run_dir, config_path, feishu_url, intent, source_text)
    runner = PipelineRunner(
        repo_root=repo_root,
        runs_root=runs_root,
        model_client=model_client,
        options=RunOptions(stage_order=selected, max_retries=max_retries),
    )
    if dry_run_packet:
        return runner.dry_run_packet(config_path, run_id=run_id)
    if resume:
        if not run_id:
            raise ValueError("--resume requires --run-dir")
        return runner.resume(run_id)
    return runner.start(config_path, run_id=run_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Reddit workflow stage, a stage range, or resume a run.")
    parser.add_argument("--stage", help="Run exactly one stage.")
    parser.add_argument("--from", dest="from_stage", help="First stage to run.")
    parser.add_argument("--to", dest="to_stage", help="Last stage to run.")
    parser.add_argument("--run-dir", help="Explicit run directory. Its name is used as run_id.")
    parser.add_argument("--config", help="Path to run_config.json. Defaults to enter_output/live_run/run_config.json.")
    parser.add_argument("--provider", default="deepseek", help="Model provider: deepseek, mock, openai-compatible.")
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--resume", action="store_true", help="Resume the run identified by --run-dir.")
    parser.add_argument("--feishu-url", help="Feishu document URL for single-stage Feishu/native rewrite tasks.")
    parser.add_argument("--intent", help="Path to an intent JSON file.")
    parser.add_argument("--source-text", help="Path to a local source text file for ad-hoc single-stage runs.")
    parser.add_argument("--dry-run-packet", action="store_true", help="Write packet manifests without calling a model.")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    client = create_model_client(args.provider)
    status = run_with_client(
        repo_root=repo_root,
        model_client=client,
        stage=args.stage,
        from_stage=args.from_stage,
        to_stage=args.to_stage,
        run_dir=Path(args.run_dir) if args.run_dir else None,
        config_path=Path(args.config) if args.config else None,
        max_retries=args.max_retries,
        resume=args.resume,
        feishu_url=args.feishu_url,
        intent_path=Path(args.intent) if args.intent else None,
        source_text=Path(args.source_text) if args.source_text else None,
        dry_run_packet=args.dry_run_packet,
    )
    print(json.dumps(status, ensure_ascii=False))
    return 0 if status["status"] in {"completed", "stage_completed", "needs_external_action", "paused", "dry_run_packet"} else 1


def _prepare_config(
    repo_root: Path,
    run_dir: Path | None,
    config_path: Path | None,
    feishu_url: str | None,
    intent: dict[str, Any] | None,
    source_text: Path | None,
) -> Path:
    if config_path is None:
        config_path = repo_root / "enter_output" / "live_run" / "run_config.json"
    if not (feishu_url or intent or source_text):
        return config_path
    target_dir = run_dir or repo_root / "temp_output" / "_ad_hoc_config"
    target = target_dir / "run_config.json"
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    if intent:
        data = apply_intent_to_config(data, intent)
    if feishu_url:
        data["feishu_url"] = feishu_url
        data["single_stage_mode"] = True
        data["source_mode"] = "feishu_url"
    if source_text:
        source_text = Path(source_text)
        target_source = target_dir / "input" / "source_post.md"
        target_source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_text, target_source)
        data["single_stage_mode"] = True
        data["source_mode"] = "provided_file"
        data["source_text_path"] = "input/source_post.md"
    write_json(target, data)
    return target


def _require_stage(available: list[str], stage: str) -> None:
    if stage not in available:
        raise ValueError(f"Unknown stage {stage!r}; expected one of {', '.join(available)}")


if __name__ == "__main__":
    raise SystemExit(main())
