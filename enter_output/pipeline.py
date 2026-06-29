from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enter_output.runtime.model_client import create_model_client
from enter_output.runtime.runner import DEFAULT_STAGE_ORDER, PipelineRunner, RunOptions


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Reddit posting workflow Python runtime.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Create and start a run")
    start.add_argument("--config", required=True, help="Path to run_config.json")
    start.add_argument("--run-id", help="Optional explicit run id; default is timestamp_project-name.")
    start.add_argument("--provider", default="deepseek", help="Model provider: deepseek, mock, openai-compatible")
    start.add_argument("--max-retries", type=int, default=5)
    start.add_argument("--stages", help="Comma-separated stage override for testing or reruns")

    resume = subparsers.add_parser("resume", help="Resume an existing run")
    resume.add_argument("--run-id", required=True)
    resume.add_argument("--provider", default="deepseek")
    resume.add_argument("--max-retries", type=int, default=5)
    resume.add_argument("--stages", help="Comma-separated stage override")

    rerun = subparsers.add_parser("rerun-stage", help="Rerun one stage and continue")
    rerun.add_argument("--run-id", required=True)
    rerun.add_argument("--stage", required=True)
    rerun.add_argument("--provider", default="deepseek")
    rerun.add_argument("--max-retries", type=int, default=5)
    rerun.add_argument("--stages", help="Comma-separated stage override")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    stages = _stages(args.stages)
    client = create_model_client(args.provider)
    runner = PipelineRunner(
        repo_root=repo_root,
        runs_root=repo_root / "temp_output",
        model_client=client,
        options=RunOptions(stage_order=stages, max_retries=args.max_retries),
    )

    if args.command == "start":
        status = runner.start(Path(args.config), run_id=args.run_id)
    elif args.command == "resume":
        status = runner.resume(args.run_id)
    else:
        status = runner.rerun_stage(args.run_id, args.stage)

    print(json.dumps(status, ensure_ascii=False))
    return 0 if status["status"] in {"completed", "stage_completed", "needs_external_action", "paused"} else 1


def _stages(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_STAGE_ORDER)
    return [item.strip() for item in raw.split(",") if item.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
