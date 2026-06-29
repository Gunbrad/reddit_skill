from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .artifacts import (
    append_manifest,
    copy_config,
    declared_paths,
    missing_declared_files,
    read_json,
    stage_runtime_dir,
    write_candidate_files,
    write_json,
)
from .evaluator import eval_passed, normalize_eval_result
from .external_actions import (
    HttpSearchProjectAdapter,
    SearchProjectAdapter,
    SearchProjectError,
    action_result_exists,
    create_action_manifest,
    load_or_create_search_placeholder,
    read_action_result,
    search_placeholder_enabled,
)
from .model_client import ModelClient
from .prompt_builder import PromptBuilder, StageSpec
from .validator import SchemaValidationError, validate_or_raise


DEFAULT_STAGE_ORDER = [
    "product-research",
    "topic-selection",
    "search-query-occupancy",
    "topic-card-selection",
    "topic-card-optimization",
    "post-native-rewrite",
    "post-fact-brand-check",
    "post-subreddit-image",
    "post-feishu-publish",
    "feishu-formatting",
]

STAGE_HANDOFF_ALIASES = {
    "post-native-rewrite": "6a_handoff_packet.json",
    "post-fact-brand-check": "6b_handoff_packet.json",
    "post-subreddit-image": "6c_handoff_packet.json",
    "post-feishu-publish": "6d_handoff_packet.json",
}


@dataclass
class RunOptions:
    stage_order: list[str] = field(default_factory=lambda: list(DEFAULT_STAGE_ORDER))
    max_retries: int = 5
    search_project_adapter: SearchProjectAdapter | None = None


class PipelineRunner:
    def __init__(
        self,
        *,
        repo_root: Path,
        runs_root: Path,
        model_client: ModelClient,
        options: RunOptions | None = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.runs_root = Path(runs_root)
        self.model_client = model_client
        self.options = options or RunOptions()
        self.prompt_builder = PromptBuilder(self.repo_root)
        self.search_project_adapter = self.options.search_project_adapter or HttpSearchProjectAdapter()

    def start(self, config_path: Path, *, run_id: str | None = None) -> dict[str, Any]:
        config_path = Path(config_path)
        config = read_json(config_path)
        if run_id is None:
            run_id = self._new_run_id(config)
        run_dir = self.runs_root / run_id
        config = copy_config(config_path, run_dir)
        state = self._load_or_create_state(run_id, run_dir, config)
        append_manifest(run_dir, f"- run started: `{run_id}`")
        return self._run_until_blocked(run_id, run_dir, config, state)

    def resume(self, run_id: str) -> dict[str, Any]:
        run_dir = self.runs_root / run_id
        config = read_json(run_dir / "run_config.json")
        state = self._load_state(run_dir)
        handled = self._resume_pending_external_work(run_id, run_dir, config, state)
        if handled is not None:
            return handled
        return self._run_until_blocked(run_id, run_dir, config, state)

    def rerun_stage(self, run_id: str, stage: str) -> dict[str, Any]:
        run_dir = self.runs_root / run_id
        config = read_json(run_dir / "run_config.json")
        state = self._load_state(run_dir)
        state["stages"].pop(stage, None)
        self._save_state(run_dir, state)
        return self._run_until_blocked(run_id, run_dir, config, state)

    def _run_until_blocked(
        self,
        run_id: str,
        run_dir: Path,
        config: dict[str, Any],
        state: dict[str, Any],
    ) -> dict[str, Any]:
        for stage in state["stage_order"]:
            stage_state = state["stages"].get(stage, {})
            if stage_state.get("status") == "completed":
                continue
            result = self._run_stage(run_id, run_dir, config, state, stage)
            if result["status"] != "stage_completed":
                self._save_state(run_dir, state)
                return result
        state["status"] = "completed"
        self._save_state(run_dir, state)
        return {"status": "completed", "run_id": run_id, "run_dir": str(run_dir)}

    def _run_stage(
        self,
        run_id: str,
        run_dir: Path,
        config: dict[str, Any],
        state: dict[str, Any],
        stage: str,
    ) -> dict[str, Any]:
        spec = self.prompt_builder.load_stage(stage)
        packet = self.prompt_builder.build_generator_packet(spec, run_dir, config)
        stage_dir = run_dir / spec.output_dir
        write_json(stage_dir / "input_manifest.json", packet)
        missing = self.prompt_builder.missing_mandatory_files(packet, run_dir)
        if missing:
            return self._fail_stage(state, stage, "missing_instruction_file", {"missing": missing})
        missing_inputs = self._missing_business_inputs(packet, run_dir)
        if missing_inputs:
            return self._fail_stage(state, stage, "upstream_artifact_missing", {"missing": missing_inputs})

        failure_report: dict[str, Any] | None = None
        for attempt in range(1, self.options.max_retries + 2):
            result = self._attempt_stage(spec, run_dir, packet, attempt, failure_report)
            if result["status"] == "schema_failed":
                return self._fail_stage(state, stage, "schema_validation_failed", result)
            if result["status"] == "artifact_write_failed":
                return self._fail_stage(state, stage, "artifact_write_failed", result)
            if result["status"] == "artifact_missing":
                return self._fail_stage(state, stage, "artifact_missing", result)
            if result["status"] == "eval_passed":
                approved = self._approve_stage(spec, run_dir, packet, result)
                state["stages"][stage] = {
                    "status": "approved",
                    "attempts": attempt,
                    "approved_output": str(run_dir / spec.output_dir / "approved_output.json"),
                    "approved_handoff": str(run_dir / spec.output_dir / "handoff_packet.json"),
                }
                self._save_state(run_dir, state)
                external = self._after_stage_approved(run_id, run_dir, config, state, spec, approved)
                if external is not None:
                    return external
                state["stages"][stage]["status"] = "completed"
                append_manifest(run_dir, f"- stage `{stage}` passed after attempt {attempt}")
                self._save_state(run_dir, state)
                return {"status": "stage_completed", "stage": stage}
            failure_report = result["eval_result"]

        return self._fail_stage(state, stage, "eval_failed_max_retries", {"eval_result": failure_report})

    def _attempt_stage(
        self,
        spec: StageSpec,
        run_dir: Path,
        packet: dict[str, Any],
        attempt: int,
        failure_report: dict[str, Any] | None,
    ) -> dict[str, Any]:
        runtime_dir = stage_runtime_dir(run_dir, spec.output_dir, attempt)
        messages = self.prompt_builder.messages_for_packet(packet, run_dir)
        if failure_report:
            messages = list(messages) + [
                {
                    "role": "user",
                    "content": "Previous independent evaluator failed this attempt. "
                    "Use only this failure report plus the original packet:\n"
                    + json.dumps(failure_report, ensure_ascii=False, indent=2),
                }
            ]
        generator_response = self.model_client.complete(
            messages,
            kind="generator",
            stage=spec.name,
            attempt=attempt,
            metadata={"output_schema": spec.output_schema, "handoff_schema": spec.handoff_schema},
        )
        write_json(
            runtime_dir / "generator_raw_response.json",
            {
                "request_id": generator_response.request_id,
                "provider": generator_response.provider,
                "model": generator_response.model,
                "content": generator_response.content,
            },
        )
        try:
            candidate = parse_model_json(generator_response.content)
            output = candidate["output"]
            handoff = candidate.get("handoff", {})
            write_json(runtime_dir / "candidate_output.json", output)
            write_json(runtime_dir / "candidate_handoff_packet.json", handoff)
            validate_or_raise(output, spec.output_schema)
        except (KeyError, ValueError, SchemaValidationError) as exc:
            return {"status": "schema_failed", "error": str(exc)}

        files = candidate.get("files", {})
        if not isinstance(files, dict):
            return {"status": "schema_failed", "error": "candidate.files must be an object"}
        try:
            write_candidate_files(run_dir, files)
        except ValueError as exc:
            return {"status": "artifact_write_failed", "error": str(exc)}
        missing_files = missing_declared_files(run_dir, output)
        if missing_files:
            return {"status": "artifact_missing", "missing": missing_files}

        artifact_paths = sorted(declared_paths(output))
        eval_packet = self.prompt_builder.build_evaluator_packet(spec, run_dir, artifact_paths)
        write_json(runtime_dir / "eval_input_manifest.json", eval_packet)
        evaluator_response = self.model_client.complete(
            self.prompt_builder.messages_for_packet(eval_packet, run_dir),
            kind="evaluator",
            stage=spec.name,
            attempt=attempt,
            metadata={"output_schema": spec.output_schema},
        )
        write_json(
            runtime_dir / "eval_raw_response.json",
            {
                "request_id": evaluator_response.request_id,
                "provider": evaluator_response.provider,
                "model": evaluator_response.model,
                "content": evaluator_response.content,
            },
        )
        eval_result = normalize_eval_result(parse_model_json(evaluator_response.content))
        write_json(runtime_dir / "eval_result.json", eval_result)
        if eval_passed(eval_result):
            return {
                "status": "eval_passed",
                "candidate": candidate,
                "output": output,
                "handoff": handoff,
                "eval_result": eval_result,
                "attempt": attempt,
            }
        return {"status": "eval_failed", "eval_result": eval_result, "attempt": attempt}

    def _approve_stage(
        self,
        spec: StageSpec,
        run_dir: Path,
        packet: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        stage_dir = run_dir / spec.output_dir
        output = result["output"]
        handoff = dict(result["handoff"])
        handoff.setdefault("stage_id", spec.stage_id)
        handoff["status"] = "pass"
        handoff.setdefault("inputs_read", [item["path"] for item in packet.get("business_inputs", [])])
        handoff.setdefault("open_questions", [])
        handoff["eval_result"] = _fill_eval_defaults(result["eval_result"], spec.handoff_schema)
        validate_or_raise(handoff, spec.handoff_schema)
        write_json(stage_dir / "approved_output.json", output)
        write_json(stage_dir / "handoff_packet.json", handoff)
        if spec.name in STAGE_HANDOFF_ALIASES:
            write_json(stage_dir / STAGE_HANDOFF_ALIASES[spec.name], handoff)
        return {
            "output": output,
            "handoff": handoff,
            "candidate": result["candidate"],
            "eval_result": handoff["eval_result"],
        }

    def _after_stage_approved(
        self,
        run_id: str,
        run_dir: Path,
        config: dict[str, Any],
        state: dict[str, Any],
        spec: StageSpec,
        approved: dict[str, Any],
    ) -> dict[str, Any] | None:
        if spec.name == "product-research" and search_placeholder_enabled(config):
            product_brief = _first_declared_artifact(run_dir, approved["output"])
            try:
                receipt = load_or_create_search_placeholder(
                    adapter=self.search_project_adapter,
                    run_id=run_id,
                    run_dir=run_dir,
                    product_brief_path=product_brief,
                    config=config,
                )
            except SearchProjectError as exc:
                state["status"] = "paused"
                state["stages"][spec.name]["status"] = "waiting_search_project"
                state["search_project"] = {"status": "failed", "error": str(exc)}
                self._save_state(run_dir, state)
                append_manifest(run_dir, f"- search placeholder failed after `{spec.name}` approval: {exc}")
                return {"status": "paused", "reason": "search_project_failed", "run_id": run_id, "run_dir": str(run_dir)}
            state["search_project"] = {"status": "completed", "receipt": receipt}

        external_actions = approved["candidate"].get("external_actions", [])
        if external_actions:
            created = create_action_manifest(run_dir, external_actions[0])
            manifest = created["manifest"]
            state["status"] = "needs_external_action"
            state["stages"][spec.name]["status"] = "waiting_external_action"
            state.setdefault("external_actions", {})[manifest["action_id"]] = {
                "status": "pending",
                "stage": spec.name,
                "manifest_path": created["manifest_path"],
                "result_file": manifest["result_file"],
            }
            self._save_state(run_dir, state)
            append_manifest(run_dir, f"- external action required for `{spec.name}`: {manifest['action_id']}")
            return {
                "status": "needs_external_action",
                "run_id": run_id,
                "stage": spec.name,
                "action_id": manifest["action_id"],
                "action_manifest": created["manifest_path"],
                "result_file": str(run_dir / manifest["result_file"]),
            }
        if spec.name == "post-feishu-publish":
            self._write_stage_six_coordinator_handoff(run_dir)
        return None

    def _resume_pending_external_work(
        self,
        run_id: str,
        run_dir: Path,
        config: dict[str, Any],
        state: dict[str, Any],
    ) -> dict[str, Any] | None:
        for action_id, action_state in state.get("external_actions", {}).items():
            if action_state.get("status") != "pending":
                continue
            manifest = read_json(Path(action_state["manifest_path"]))
            if not action_result_exists(run_dir, manifest):
                return {
                    "status": "needs_external_action",
                    "run_id": run_id,
                    "stage": action_state["stage"],
                    "action_id": action_id,
                    "action_manifest": action_state["manifest_path"],
                    "result_file": str(run_dir / manifest["result_file"]),
                }
            action_state["status"] = "completed"
            action_state["result"] = read_action_result(run_dir, manifest)
            stage_state = state["stages"][action_state["stage"]]
            stage_state["status"] = "completed"
            if action_state["stage"] == "post-feishu-publish":
                self._write_stage_six_coordinator_handoff(run_dir)
            append_manifest(run_dir, f"- external action completed: {action_id}")
            state["status"] = "running"
            self._save_state(run_dir, state)

        for stage, stage_state in state.get("stages", {}).items():
            if stage_state.get("status") == "waiting_search_project":
                spec = self.prompt_builder.load_stage(stage)
                product_brief = _first_declared_artifact(run_dir, read_json(Path(stage_state["approved_output"])))
                try:
                    receipt = load_or_create_search_placeholder(
                        adapter=self.search_project_adapter,
                        run_id=run_id,
                        run_dir=run_dir,
                        product_brief_path=product_brief,
                        config=config,
                    )
                except SearchProjectError as exc:
                    state["search_project"] = {"status": "failed", "error": str(exc)}
                    self._save_state(run_dir, state)
                    return {"status": "paused", "reason": "search_project_failed", "run_id": run_id, "run_dir": str(run_dir)}
                state["search_project"] = {"status": "completed", "receipt": receipt}
                stage_state["status"] = "completed"
                state["status"] = "running"
                append_manifest(run_dir, f"- search placeholder completed for `{stage}`")
                self._save_state(run_dir, state)
        return None

    def _fail_stage(
        self,
        state: dict[str, Any],
        stage: str,
        reason: str,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        state["status"] = "failed"
        state.setdefault("stages", {})[stage] = {"status": "failed", "reason": reason, "details": details}
        return {"status": "failed", "stage": stage, "reason": reason, "details": details}

    def _missing_business_inputs(self, packet: dict[str, Any], run_dir: Path) -> list[str]:
        missing: list[str] = []
        for ref in packet.get("business_inputs", []):
            if ref.get("optional"):
                continue
            path_ref = ref.get("path", "")
            if not path_ref.startswith("run:"):
                continue
            relative = path_ref.removeprefix("run:")
            if relative == "run_config.json":
                continue
            if "{" in relative and "}" in relative:
                glob_pattern = re.sub(r"\{[^}]+\}", "*", relative)
                if not list(run_dir.glob(glob_pattern)):
                    missing.append(path_ref)
                continue
            if not (run_dir / relative).exists():
                missing.append(path_ref)
        return missing

    def _write_stage_six_coordinator_handoff(self, run_dir: Path) -> None:
        coordinator_dir = self.repo_root / "enter_output" / "skills" / "post-optimization"
        if not coordinator_dir.exists():
            return
        spec = self.prompt_builder.load_stage("post-optimization")
        stage_dir = run_dir / "06_optimized"
        sub_stage_rows = []
        for alias, sub_stage_id, default_artifact in [
            ("6a_handoff_packet.json", "6a_content_optimization", "06_optimized/native_posts.md"),
            ("6b_handoff_packet.json", "6b_fact_brand_check", "06_optimized/checked_posts.md"),
            ("6c_handoff_packet.json", "6c_subreddit_image_packaging", "06_optimized/final_posts.md"),
            ("6d_handoff_packet.json", "6d_feishu_publish", "06_optimized/feishu_links.md"),
        ]:
            handoff_path = stage_dir / alias
            if not handoff_path.exists():
                continue
            handoff = read_json(handoff_path)
            sub_stage_rows.append(
                {
                    "sub_stage_id": sub_stage_id,
                    "worker_role": "isolated_generator_worker",
                    "artifact_path": _first_declared_path_or_default(handoff.get("outputs", {}), default_artifact),
                    "eval_verdict": handoff.get("eval_result", {}).get("verdict", "pass"),
                }
            )
        output = {
            "stage_id": "stage_6_post_optimization",
            "artifact_paths": {
                "native_posts": "06_optimized/native_posts.md",
                "checked_posts": "06_optimized/checked_posts.md",
                "final_posts": "06_optimized/final_posts.md",
                "feishu_links": "06_optimized/feishu_links.md",
            },
            "sub_stage_results": sub_stage_rows,
        }
        deliverables = _load_6d_deliverables(stage_dir)
        viral_intent = _load_6a_viral_intent(stage_dir)
        handoff = {
            "stage_id": "stage_6_post_optimization",
            "status": "pass",
            "inputs_read": [
                "05_optimized_cards/handoff_packet.json",
                "05_optimized_cards/drafts_md/{post_id}.md",
            ],
            "outputs": {
                "final_posts_path": "06_optimized/final_posts.md",
                "feishu_links_path": "06_optimized/feishu_links.md",
                "post_doc_url": deliverables.get("post_doc_url", "mock"),
                "image_doc_url": deliverables.get("image_doc_url"),
                "viral_intent_preservation": viral_intent,
            },
            "eval_result": {"blocking": "pass", "score": 100, "retry_needed": False, "verdict": "pass"},
            "open_questions": [],
        }
        validate_or_raise(output, spec.output_schema)
        validate_or_raise(handoff, spec.handoff_schema)
        write_json(stage_dir / "stage_6_post_optimization_output.json", output)
        write_json(stage_dir / "approved_output.json", output)
        write_json(stage_dir / "handoff_packet.json", handoff)

    def _load_or_create_state(self, run_id: str, run_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
        state_path = run_dir / "run_state.json"
        if state_path.exists():
            return read_json(state_path)
        state = {
            "run_id": run_id,
            "status": "running",
            "stage_order": list(self.options.stage_order),
            "stages": {},
            "external_actions": {},
        }
        self._save_state(run_dir, state)
        return state

    def _load_state(self, run_dir: Path) -> dict[str, Any]:
        return read_json(run_dir / "run_state.json")

    def _save_state(self, run_dir: Path, state: dict[str, Any]) -> None:
        write_json(run_dir / "run_state.json", state)

    def _new_run_id(self, config: dict[str, Any]) -> str:
        project_name = config.get("project_name") or config.get("project_id") or "project"
        base = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + _slugify(str(project_name))
        candidate = base
        suffix = 2
        while (self.runs_root / candidate).exists():
            candidate = f"{base}_{suffix:02d}"
            suffix += 1
        return candidate


def parse_model_json(content: str) -> dict[str, Any]:
    stripped = content.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.DOTALL)
    if fenced:
        stripped = fenced.group(1)
    elif not stripped.startswith("{"):
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError("model response does not contain a JSON object")
        stripped = stripped[start : end + 1]
    parsed = json.loads(stripped)
    if not isinstance(parsed, dict):
        raise ValueError("model response JSON must be an object")
    return parsed


def _fill_eval_defaults(eval_result: dict[str, Any], handoff_schema: dict[str, Any]) -> dict[str, Any]:
    result = dict(eval_result)
    eval_schema = handoff_schema.get("properties", {}).get("eval_result", {})
    threshold_schema = eval_schema.get("properties", {}).get("threshold", {})
    if "threshold" not in result and "const" in threshold_schema:
        result["threshold"] = threshold_schema["const"]
    return result


def _first_declared_artifact(run_dir: Path, output: dict[str, Any]) -> Path:
    paths = sorted(declared_paths(output))
    if not paths:
        return run_dir
    return run_dir / paths[0]


def _first_declared_path_or_default(value: dict[str, Any], default: str) -> str:
    paths = sorted(declared_paths(value))
    return paths[0] if paths else default


def _load_6d_deliverables(stage_dir: Path) -> dict[str, Any]:
    output_path = stage_dir / "approved_output.json"
    if output_path.exists():
        output = read_json(output_path)
        if output.get("stage_id") == "stage_6d_post_feishu_publish":
            return output.get("deliverables", {})
    handoff_path = stage_dir / "6d_handoff_packet.json"
    if handoff_path.exists():
        return read_json(handoff_path).get("outputs", {})
    return {}


def _load_6a_viral_intent(stage_dir: Path) -> list[dict[str, Any]]:
    handoff_path = stage_dir / "6a_handoff_packet.json"
    if not handoff_path.exists():
        return []
    outputs = read_json(handoff_path).get("outputs", {})
    value = outputs.get("viral_intent_preservation", [])
    return value if isinstance(value, list) else []


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip().lower()).strip("-_")
    return slug or "project"
