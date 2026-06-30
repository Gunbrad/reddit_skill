import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from enter_output.runtime.external_actions import HttpSearchProjectAdapter, SearchProjectError, create_action_manifest
from enter_output.runtime.model_client import ScriptedModelClient, example_from_schema
from enter_output.runtime.prompt_builder import PromptBuilder
from enter_output.runtime.runner import PipelineRunner, RunOptions


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(tmp_path: Path, stage_names: list[str]) -> Path:
    repo = tmp_path / "repo"
    workflow = repo / "enter_output" / "skills" / "reddit-posting-workflow"
    write_text(workflow / "CONTEXT_CONTRACT.md", "# Context\n")
    write_text(workflow / "WORKER_CONTRACT.md", "# Worker\n")
    write_text(workflow / "PROMPT_INJECTION_CONTRACT.md", "# Prompt\n")
    write_text(workflow / "EVAL_WORKER_CONTRACT.md", "# Eval\n")
    write_text(workflow / "conventions.md", "# Conventions\n")
    for index, name in enumerate(stage_names, start=1):
        write_stage(repo, name, f"stage_{name.replace('-', '_')}", f"{index:02d}_{name}/main.md")
    write_json(repo / "run_config.json", {"project_name": "Runtime Test", "project_id": "runtime-test"})
    return repo


def write_stage(repo: Path, name: str, stage_id: str, artifact_rel: str) -> None:
    stage = repo / "enter_output" / "skills" / name
    write_text(stage / "SKILL.md", f"# {name}\n")
    write_text(stage / "EVALS.md", "# Reviewer prompt\nReview independently.\n")
    write_text(
        stage / "INPUTS.md",
        f"""# Inputs - {name}

## Agent prompt packet

### Role prompt

You are the {name} generator worker.

### Required instruction files

Read in order:

1. `repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md`
2. `repo:enter_output/skills/{name}/SKILL.md`

### Optional instruction files

- Files listed in `run_config.prompt_packs.{name}.extra_instruction_files`.

### Business input files

- `run:run_config.json`

### Read order

1. Required instruction files.
2. Optional instruction files explicitly listed in `run_config`.
3. Business input files.
4. `repo:enter_output/skills/{name}/OUTPUT_SCHEMA.json`
5. `repo:enter_output/skills/{name}/HANDOFF_SCHEMA.json`
6. `repo:enter_output/skills/{name}/EVALS.md`

### Allowed extra reads

- None.

## Allowed global files

- `run_config.json`

## Allowed stage files

- None.

## Forbidden files

- Full prior conversation history.
- Unrelated run folders.
""",
    )
    write_json(
        stage / "OUTPUT_SCHEMA.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["stage_id", "artifact_paths", "items"],
            "properties": {
                "stage_id": {"const": stage_id},
                "artifact_paths": {
                    "type": "object",
                    "required": ["main"],
                    "properties": {"main": {"const": artifact_rel}},
                    "additionalProperties": False,
                },
                "items": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            },
            "additionalProperties": False,
        },
    )
    write_json(
        stage / "HANDOFF_SCHEMA.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["stage_id", "status", "inputs_read", "outputs", "eval_result", "open_questions"],
            "properties": {
                "stage_id": {"const": stage_id},
                "status": {"enum": ["draft", "pass", "fail"]},
                "inputs_read": {"type": "array", "items": {"type": "string"}},
                "outputs": {
                    "type": "object",
                    "required": ["main_path"],
                    "properties": {"main_path": {"const": artifact_rel}},
                    "additionalProperties": False,
                },
                "eval_result": {
                    "type": "object",
                    "required": ["blocking", "score", "retry_needed", "verdict"],
                    "properties": {
                        "blocking": {"enum": ["pass", "fail"]},
                        "score": {"type": "number"},
                        "retry_needed": {"type": "boolean"},
                        "verdict": {"enum": ["pass", "fail"]},
                    },
                    "additionalProperties": True,
                },
                "open_questions": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": False,
        },
    )


def write_eval_inputs(repo: Path, name: str, business_lines: list[str]) -> None:
    business_inputs = "\n".join(business_lines)
    write_text(
        repo / "enter_output" / "skills" / name / "EVAL_INPUTS.md",
        f"""# Eval Inputs - {name}

## Evaluator prompt packet

### Role prompt

Run the Reviewer prompt from EVALS.md as an independent evaluator.

### Required instruction files

1. `repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md`
2. `repo:enter_output/skills/{name}/EVALS.md`
3. `repo:enter_output/skills/{name}/OUTPUT_SCHEMA.json`
4. `repo:enter_output/skills/{name}/HANDOFF_SCHEMA.json`

### Business input files

{business_inputs}

### Read order

1. Required instruction files.
2. Artifact under review.
3. Minimal fact / brand context.
4. Stage-specific upstream context.

### Allowed extra reads

- None by default.

### Forbidden files

- Full prior conversation history.
- Previous stage scratchpads.
- Failed drafts unless passed in retry failure report.
- Unrelated run folders.
- Old Feishu docs.
- Raw Reddit dumps unless explicitly produced by current run and listed above.
""",
    )


def write_post_optimization_schema(repo: Path) -> None:
    stage = repo / "enter_output" / "skills" / "post-optimization"
    write_text(stage / "SKILL.md", "# post optimization\n")
    write_text(stage / "EVALS.md", "# eval\n")
    write_text(stage / "INPUTS.md", "# inputs\n")
    write_json(
        stage / "OUTPUT_SCHEMA.json",
        {
            "type": "object",
            "required": ["stage_id", "artifact_paths", "sub_stage_results"],
            "properties": {
                "stage_id": {"const": "stage_6_post_optimization"},
                "artifact_paths": {
                    "type": "object",
                    "required": ["native_posts", "checked_posts", "final_posts", "feishu_links"],
                    "properties": {
                        "native_posts": {"const": "06_optimized/native_posts.md"},
                        "checked_posts": {"const": "06_optimized/checked_posts.md"},
                        "final_posts": {"const": "06_optimized/final_posts.md"},
                        "feishu_links": {"const": "06_optimized/feishu_links.md"},
                    },
                    "additionalProperties": False,
                },
                "sub_stage_results": {"type": "array", "minItems": 4, "items": {"type": "object"}},
            },
            "additionalProperties": False,
        },
    )
    write_json(
        stage / "HANDOFF_SCHEMA.json",
        {
            "type": "object",
            "required": ["stage_id", "status", "inputs_read", "outputs", "eval_result", "open_questions"],
            "properties": {
                "stage_id": {"const": "stage_6_post_optimization"},
                "status": {"enum": ["draft", "pass", "fail"]},
                "inputs_read": {"type": "array", "items": {"type": "string"}},
                "outputs": {
                    "type": "object",
                    "required": ["final_posts_path", "feishu_links_path", "post_doc_url", "image_doc_url", "viral_intent_preservation"],
                    "properties": {
                        "final_posts_path": {"const": "06_optimized/final_posts.md"},
                        "feishu_links_path": {"const": "06_optimized/feishu_links.md"},
                        "post_doc_url": {"type": "string"},
                        "image_doc_url": {"type": ["string", "null"]},
                        "viral_intent_preservation": {"type": "array", "items": {"type": "object"}},
                    },
                    "additionalProperties": False,
                },
                "eval_result": {
                    "type": "object",
                    "required": ["blocking", "score", "retry_needed", "verdict"],
                    "additionalProperties": True,
                },
                "open_questions": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": False,
        },
    )


def generator_payload(stage_name: str, artifact_rel: str, *, external_actions=None, stage_id=None) -> dict:
    real_stage_id = stage_id or f"stage_{stage_name.replace('-', '_')}"
    return {
        "output": {
            "stage_id": real_stage_id,
            "artifact_paths": {"main": artifact_rel},
            "items": ["ok"],
        },
        "handoff": {
            "stage_id": real_stage_id,
            "status": "draft",
            "inputs_read": ["run_config.json"],
            "outputs": {"main_path": artifact_rel},
            "open_questions": [],
        },
        "files": {artifact_rel: f"# {stage_name}\n\napproved content\n"},
        "external_actions": external_actions or [],
    }


def eval_payload(verdict: str = "pass") -> dict:
    return {
        "blocking": verdict,
        "score": 100 if verdict == "pass" else 40,
        "retry_needed": verdict != "pass",
        "verdict": verdict,
        "required_fixes": [] if verdict == "pass" else ["fix the artifact"],
    }


def make_runner(repo: Path, client: ScriptedModelClient, stages: list[str], **options) -> PipelineRunner:
    return PipelineRunner(
        repo_root=repo,
        runs_root=repo / "enter_output" / "runs",
        model_client=client,
        options=RunOptions(stage_order=stages, **options),
    )


def test_successful_run_saves_all_artifact_layers_and_uses_independent_requests(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_ok")

    assert status["status"] == "completed"
    assert [call["kind"] for call in client.calls] == ["generator", "evaluator"]
    assert client.calls[0]["request_id"] != client.calls[1]["request_id"]
    run_dir = repo / "enter_output" / "runs" / "run_ok"
    assert (run_dir / "01_alpha" / "main.md").exists()
    assert (run_dir / "01_alpha" / "runtime" / "attempt_001" / "generator_raw_response.json").exists()
    assert (run_dir / "01_alpha" / "runtime" / "attempt_001" / "candidate_output.json").exists()
    assert (run_dir / "01_alpha" / "runtime" / "attempt_001" / "eval_result.json").exists()
    assert (run_dir / "01_alpha" / "approved_output.json").exists()
    manifest = json.loads((run_dir / "01_alpha" / "input_manifest.json").read_text(encoding="utf-8"))
    assert manifest["business_inputs"] == [{"path": "run:run_config.json", "purpose": "business input"}]
    assert "Full prior conversation history." in manifest["forbidden_files"]


def test_evaluator_uses_eval_inputs_md_when_present(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    write_eval_inputs(repo, "alpha", ["- `run:eval_context/extra.md`"])
    run_dir = repo / "enter_output" / "runs" / "run_eval_inputs"
    write_text(run_dir / "eval_context" / "extra.md", "# extra eval context\n")
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_eval_inputs")

    assert status["status"] == "completed"
    manifest = json.loads((run_dir / "01_alpha" / "runtime" / "attempt_001" / "eval_input_manifest.json").read_text(encoding="utf-8"))
    assert {"path": "run:eval_context/extra.md", "purpose": "business input"} in manifest["business_inputs"]
    eval_paths = [item["path"] for item in manifest["business_inputs"]]
    assert "run:01_alpha/main.md" in eval_paths
    assert all("generator_raw_response" not in path for path in eval_paths)
    assert all("candidate_handoff_packet" not in path for path in eval_paths)


def test_stage_6a_eval_receives_stage5_handoff(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    write_eval_inputs(repo, "post-native-rewrite", ["- `run:05_optimized_cards/handoff_packet.json`"])
    run_dir = repo / "enter_output" / "runs" / "run_6a_eval"
    write_json(run_dir / "05_optimized_cards" / "handoff_packet.json", {"stage_id": "stage_5_topic_card_optimization"})
    client = ScriptedModelClient(
        [generator_payload("post-native-rewrite", "06_optimized/native_posts.md"), eval_payload("pass")]
    )
    runner = make_runner(repo, client, ["post-native-rewrite"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_6a_eval")

    assert status["status"] == "completed"
    manifest = json.loads((run_dir / "06_optimized" / "runtime" / "attempt_001" / "eval_input_manifest.json").read_text(encoding="utf-8"))
    assert "run:05_optimized_cards/handoff_packet.json" in [item["path"] for item in manifest["business_inputs"]]


def test_missing_required_eval_input_fails_before_evaluator_request(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    write_eval_inputs(repo, "alpha", ["- `run:eval_context/missing.md`"])
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_missing_eval_input")

    assert status["status"] == "failed"
    assert status["reason"] == "missing_eval_input"
    assert status["details"]["missing"] == ["run:eval_context/missing.md"]
    assert [call["kind"] for call in client.calls] == ["generator"]


def test_eval_inputs_optional_missing_is_skipped(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    write_eval_inputs(repo, "alpha", ["- `run:eval_context/optional.md` if present."])
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_optional_eval_input")

    assert status["status"] == "completed"
    assert [call["kind"] for call in client.calls] == ["generator", "evaluator"]
    manifest = json.loads(
        (
            repo
            / "enter_output"
            / "runs"
            / "run_optional_eval_input"
            / "01_alpha"
            / "runtime"
            / "attempt_001"
            / "eval_input_manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert {"path": "run:eval_context/optional.md", "purpose": "business input", "optional": True} in manifest["business_inputs"]


def test_product_research_and_6b_inputs_have_standard_prompt_packet(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    run_dir = tmp_path / "run"
    builder = PromptBuilder(repo_root)

    product_packet = builder.build_generator_packet(
        builder.load_stage("product-research"),
        run_dir,
        {"prompt_packs": {}},
    )
    product_business_paths = [item["path"] for item in product_packet["business_inputs"]]
    assert product_packet["role_prompt"]
    assert product_packet["instruction_files"]
    assert "run:run_config.json" in product_business_paths
    assert "run_config.product_sources" in product_business_paths
    assert "run_config.provided_artifacts" in product_business_paths

    fact_packet = builder.build_generator_packet(
        builder.load_stage("post-fact-brand-check"),
        run_dir,
        {"prompt_packs": {}},
    )
    fact_business = {item["path"]: item for item in fact_packet["business_inputs"]}
    assert fact_packet["role_prompt"]
    assert fact_packet["instruction_files"]
    assert "run:06_optimized/native_posts.md" in fact_business
    assert fact_business["run:06_optimized/6a_handoff_packet.json"].get("optional") is not True


def test_start_without_run_id_creates_timestamped_project_folder_in_temp_output(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    config_path = repo / "run_config.json"
    write_json(config_path, {"project_name": "hoto", "project_id": "ignored-id"})
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = PipelineRunner(
        repo_root=repo,
        runs_root=repo / "temp_output",
        model_client=client,
        options=RunOptions(stage_order=["alpha"], max_retries=0),
    )

    status = runner.start(config_path)

    assert status["status"] == "completed"
    run_dir = Path(status["run_dir"])
    assert run_dir.parent == repo / "temp_output"
    assert re.match(r"^\d{8}_\d{6}_hoto(?:_\d{2})?$", run_dir.name)
    assert not (repo / "enter_output" / "runs").exists()


def test_repeated_start_without_run_id_creates_distinct_project_folders(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    config_path = repo / "run_config.json"
    write_json(config_path, {"project_name": "hoto"})
    client = ScriptedModelClient(
        [
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("pass"),
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("pass"),
        ]
    )
    runner = PipelineRunner(
        repo_root=repo,
        runs_root=repo / "temp_output",
        model_client=client,
        options=RunOptions(stage_order=["alpha"], max_retries=0),
    )

    first = runner.start(config_path)
    second = runner.start(config_path)

    assert Path(first["run_dir"]).parent == repo / "temp_output"
    assert Path(second["run_dir"]).parent == repo / "temp_output"
    assert first["run_id"] != second["run_id"]


def test_schema_failure_blocks_next_stage_and_skips_evaluator(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "beta"])
    bad_payload = generator_payload("alpha", "01_alpha/main.md")
    bad_payload["output"].pop("items")
    client = ScriptedModelClient([bad_payload])
    runner = make_runner(repo, client, ["alpha", "beta"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_schema_fail")

    assert status["status"] == "failed"
    assert status["reason"] == "schema_validation_failed"
    assert [call["kind"] for call in client.calls] == ["generator"]
    assert not (repo / "enter_output" / "runs" / "run_schema_fail" / "02_beta").exists()


def test_generator_files_cannot_escape_run_directory(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    payload = generator_payload("alpha", "01_alpha/main.md")
    payload["files"] = {"../escaped.md": "nope"}
    client = ScriptedModelClient([payload])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_escape")

    assert status["status"] == "failed"
    assert status["reason"] == "artifact_write_failed"
    assert not (repo / "enter_output" / "runs" / "escaped.md").exists()


def test_missing_upstream_run_artifact_blocks_before_generator(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["beta"])
    inputs = repo / "enter_output" / "skills" / "beta" / "INPUTS.md"
    text = inputs.read_text(encoding="utf-8").replace(
        "- `run:run_config.json`",
        "- `run:run_config.json`\n- `run:01_alpha/handoff_packet.json`",
    )
    inputs.write_text(text, encoding="utf-8")
    client = ScriptedModelClient([generator_payload("beta", "01_beta/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["beta"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_upstream_missing")

    assert status["status"] == "failed"
    assert status["reason"] == "upstream_artifact_missing"
    assert client.calls == []


def test_placeholder_upstream_paths_match_existing_artifacts(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["beta"])
    inputs = repo / "enter_output" / "skills" / "beta" / "INPUTS.md"
    text = inputs.read_text(encoding="utf-8").replace(
        "- `run:run_config.json`",
        "- `run:run_config.json`\n- `run:01_alpha/maps/{direction_id}.md`",
    )
    inputs.write_text(text, encoding="utf-8")
    run_dir = repo / "enter_output" / "runs" / "run_placeholder"
    write_text(run_dir / "01_alpha" / "maps" / "direction_001.md", "# map\n")
    write_json(run_dir / "run_config.json", {"project_name": "Runtime Test", "project_id": "runtime-test"})
    write_json(
        run_dir / "run_state.json",
        {"run_id": "run_placeholder", "status": "running", "stage_order": ["beta"], "stages": {}, "external_actions": {}},
    )
    client = ScriptedModelClient([generator_payload("beta", "01_beta/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["beta"], max_retries=0)

    status = runner.resume("run_placeholder")

    assert status["status"] == "completed"
    assert [call["kind"] for call in client.calls] == ["generator", "evaluator"]


def test_eval_failure_retries_with_fresh_requests_then_stops(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    client = ScriptedModelClient(
        [
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("fail"),
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("fail"),
        ]
    )
    runner = make_runner(repo, client, ["alpha"], max_retries=1)

    status = runner.start(repo / "run_config.json", run_id="run_eval_fail")

    assert status["status"] == "failed"
    assert status["reason"] == "eval_failed_max_retries"
    assert [call["kind"] for call in client.calls] == ["generator", "evaluator", "generator", "evaluator"]
    assert len({call["request_id"] for call in client.calls}) == 4


def test_feishu_action_pauses_and_resume_finishes_without_more_model_calls(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["topic-selection"])
    action = {
        "action_type": "feishu.create_document",
        "title": "Topics",
        "content_file": "01_topic-selection/main.md",
    }
    client = ScriptedModelClient(
        [generator_payload("topic-selection", "01_topic-selection/main.md", external_actions=[action]), eval_payload("pass")]
    )
    runner = make_runner(repo, client, ["topic-selection"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_feishu")

    assert status["status"] == "needs_external_action"
    action_manifest = Path(status["action_manifest"])
    manifest = json.loads(action_manifest.read_text(encoding="utf-8"))
    assert manifest["action_type"] == "feishu.create_document"
    result_file = action_manifest.parent / Path(manifest["result_file"]).name
    write_json(result_file, {"document_id": "doc123", "url": "https://example.test/doc123"})

    resumed = runner.resume("run_feishu")

    assert resumed["status"] == "completed"
    assert len(client.calls) == 2
    state = json.loads((repo / "enter_output" / "runs" / "run_feishu" / "run_state.json").read_text(encoding="utf-8"))
    assert state["external_actions"][manifest["action_id"]]["status"] == "completed"


def test_action_manifest_result_file_is_forced_under_actions_dir(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"

    created = create_action_manifest(
        run_dir,
        {
            "action_id": "feishu_escape",
            "action_type": "feishu.create_document",
            "title": "Doc",
            "content_file": "content.md",
            "result_file": "../outside.json",
        },
    )

    assert created["manifest"]["result_file"] == "actions/feishu_escape.result.json"
    assert (run_dir / "actions" / "feishu_escape.json").exists()


def test_stage_six_substage_handoff_alias_is_written(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    client = ScriptedModelClient(
        [generator_payload("post-native-rewrite", "06_optimized/native_posts.md"), eval_payload("pass")]
    )
    runner = make_runner(repo, client, ["post-native-rewrite"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_6a")

    assert status["status"] == "completed"
    assert (repo / "enter_output" / "runs" / "run_6a" / "06_optimized" / "6a_handoff_packet.json").exists()


def test_stage_six_coordinator_handoff_owns_generic_handoff_path(tmp_path: Path) -> None:
    stages = ["post-native-rewrite", "post-fact-brand-check", "post-subreddit-image", "post-feishu-publish"]
    repo = make_repo(tmp_path, stages)
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    write_stage(repo, "post-fact-brand-check", "stage_post_fact_brand_check", "06_optimized/checked_posts.md")
    write_stage(repo, "post-subreddit-image", "stage_post_subreddit_image", "06_optimized/final_posts.md")
    write_stage(repo, "post-feishu-publish", "stage_post_feishu_publish", "06_optimized/feishu_links.md")
    write_post_optimization_schema(repo)
    client = ScriptedModelClient(
        [
            generator_payload("post-native-rewrite", "06_optimized/native_posts.md"),
            eval_payload("pass"),
            generator_payload("post-fact-brand-check", "06_optimized/checked_posts.md"),
            eval_payload("pass"),
            generator_payload("post-subreddit-image", "06_optimized/final_posts.md"),
            eval_payload("pass"),
            generator_payload("post-feishu-publish", "06_optimized/feishu_links.md"),
            eval_payload("pass"),
        ]
    )
    runner = make_runner(repo, client, stages, max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="run_stage_6")

    assert status["status"] == "completed"
    generic = json.loads((repo / "enter_output" / "runs" / "run_stage_6" / "06_optimized" / "handoff_packet.json").read_text(encoding="utf-8"))
    substage = json.loads((repo / "enter_output" / "runs" / "run_stage_6" / "06_optimized" / "6d_handoff_packet.json").read_text(encoding="utf-8"))
    assert generic["stage_id"] == "stage_6_post_optimization"
    assert substage["stage_id"] == "stage_post_feishu_publish"


class FlakySearchProjectAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def create_placeholder(self, *, run_id: str, run_dir: Path, product_brief_path: Path, config: dict) -> dict:
        self.calls += 1
        if self.calls == 1:
            raise SearchProjectError("temporary outage")
        return {"project_id": "search-project-1", "status": "created", "idempotency_key": run_id}


def test_smartcontent_search_project_adapter_uses_skill_api_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}
    product_brief = tmp_path / "product_brief.md"
    product_brief.write_text("# Hoto brief\n", encoding="utf-8")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self):
            return json.dumps({"project_id": "hoto-20260629", "status": "created"}).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setenv("PLANNER_SESSION", "session-token")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    receipt = HttpSearchProjectAdapter().create_placeholder(
        run_id="20260629_120000_hoto",
        run_dir=tmp_path,
        product_brief_path=product_brief,
        config={"project_name": "Hoto"},
    )

    assert captured["url"] == "https://smartcontent.shifenglab.com/api/search-occupancy/projects"
    assert captured["headers"]["Cookie"] == "planner_session=session-token"
    assert captured["headers"]["Accept"] == "application/json"
    assert captured["body"] == {
        "name": "Hoto 20260629_120000_hoto",
        "product_brief": "# Hoto brief\n",
        "notes": "Created by reddit workflow runtime. run_id=20260629_120000_hoto",
    }
    assert receipt["project_id"] == "hoto-20260629"


def test_search_project_failure_does_not_regenerate_stage_one_on_resume(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["product-research"])
    config_path = repo / "run_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["search_project_placeholder"] = {"enabled": True}
    write_json(config_path, config)
    client = ScriptedModelClient([generator_payload("product-research", "01_product-research/main.md"), eval_payload("pass")])
    search_adapter = FlakySearchProjectAdapter()
    runner = make_runner(repo, client, ["product-research"], max_retries=0, search_project_adapter=search_adapter)

    status = runner.start(config_path, run_id="run_search")

    assert status["status"] == "paused"
    assert status["reason"] == "search_project_failed"
    assert len(client.calls) == 2

    resumed = runner.resume("run_search")

    assert resumed["status"] == "completed"
    assert len(client.calls) == 2
    assert search_adapter.calls == 2
    receipt = json.loads((repo / "enter_output" / "runs" / "run_search" / "external" / "search_project.json").read_text(encoding="utf-8"))
    assert receipt["project_id"] == "search-project-1"


def test_resume_skips_approved_stage_and_restarts_last_failed_stage(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "beta"])
    first_client = ScriptedModelClient(
        [
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("pass"),
            generator_payload("beta", "02_beta/main.md"),
            eval_payload("fail"),
        ]
    )
    runner = make_runner(repo, first_client, ["alpha", "beta"], max_retries=0)

    failed = runner.start(repo / "run_config.json", run_id="run_resume")

    assert failed["status"] == "failed"
    second_client = ScriptedModelClient([generator_payload("beta", "02_beta/main.md"), eval_payload("pass")])
    resumed_runner = make_runner(repo, second_client, ["alpha", "beta"], max_retries=0)

    resumed = resumed_runner.resume("run_resume")

    assert resumed["status"] == "completed"
    assert [call["stage"] for call in second_client.calls] == ["beta", "beta"]


def test_pipeline_script_can_be_run_directly_for_help() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, str(repo_root / "enter_output" / "pipeline.py"), "--help"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Run the Reddit posting workflow Python runtime" in result.stdout


def test_stage_registry_declares_canonical_stage_order_and_outputs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    registry_path = repo_root / "enter_output" / "runtime" / "stage_registry.json"

    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    assert [stage["name"] for stage in registry["stages"]] == [
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
    search_stage = next(stage for stage in registry["stages"] if stage["name"] == "search-query-occupancy")
    assert search_stage["outputs"] == [
        "03_search/search_queries.md",
        "03_search/run_meta.json",
        "03_search/occupancy_heat_evidence.json",
        "03_search/handoff_packet.json",
    ]
    assert search_stage["requires_host_action"] is False
    screen_stage = next(stage for stage in registry["stages"] if stage["name"] == "topic-card-selection")
    assert screen_stage["output_dir"] == "04_screen"
    assert screen_stage["outputs"] == [
        "04_screen/screening.md",
        "04_screen/passed_cards.json",
        "04_screen/handoff_packet.json",
    ]
    optimize_stage = next(stage for stage in registry["stages"] if stage["name"] == "topic-card-optimization")
    assert "04_screen/handoff_packet.json" in optimize_stage["inputs"]


def test_registry_stages_have_eval_inputs_md() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    registry = json.loads((repo_root / "enter_output" / "runtime" / "stage_registry.json").read_text(encoding="utf-8"))

    for stage in registry["stages"]:
        eval_inputs = repo_root / "enter_output" / "skills" / stage["name"] / "EVAL_INPUTS.md"
        assert eval_inputs.exists(), f"missing EVAL_INPUTS.md for {stage['name']}"


def test_run_stage_script_supports_single_stage_range_resume_and_feishu_url_help() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, str(repo_root / "enter_output" / "runtime" / "run_stage.py"), "--help"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--stage" in result.stdout
    assert "--from" in result.stdout
    assert "--to" in result.stdout
    assert "--resume" in result.stdout
    assert "--feishu-url" in result.stdout


def test_run_stage_single_stage_cli_runs_only_requested_stage(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "beta"])
    config_path = repo / "run_config.json"
    client = ScriptedModelClient([generator_payload("beta", "02_beta/main.md"), eval_payload("pass")])

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        stage="beta",
        run_dir=repo / "enter_output" / "runs" / "single_beta",
        config_path=config_path,
        max_retries=0,
    )

    assert status["status"] == "completed"
    assert [call["stage"] for call in client.calls] == ["beta", "beta"]
    assert not (repo / "enter_output" / "runs" / "single_beta" / "01_alpha").exists()
    assert (repo / "enter_output" / "runs" / "single_beta" / "02_beta" / "handoff_packet.json").exists()


def test_single_stage_feishu_url_writes_config(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "feishu-formatting"])
    config_path = repo / "run_config.json"
    run_dir = repo / "enter_output" / "runs" / "single_feishu"
    write_text(run_dir / "07_format" / "live_doc_snapshot.md", "# fetched doc\n")
    client = ScriptedModelClient(
        [generator_payload("feishu-formatting", "02_feishu-formatting/main.md"), eval_payload("pass")]
    )

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        stage="feishu-formatting",
        run_dir=run_dir,
        config_path=config_path,
        feishu_url="https://example.feishu.cn/docx/test",
        max_retries=0,
    )

    assert status["status"] == "completed"
    written_config = json.loads(
        (repo / "enter_output" / "runs" / "single_feishu" / "run_config.json").read_text(encoding="utf-8")
    )
    assert written_config["feishu_url"] == "https://example.feishu.cn/docx/test"
    assert written_config["single_stage_mode"] is True
    assert written_config["source_mode"] == "feishu_url"
    assert [call["stage"] for call in client.calls] == ["feishu-formatting", "feishu-formatting"]
    assert not (repo / "enter_output" / "runs" / "single_feishu" / "01_alpha").exists()


def test_run_stage_range_cli_stops_at_to_stage(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "beta", "gamma"])
    client = ScriptedModelClient(
        [
            generator_payload("alpha", "01_alpha/main.md"),
            eval_payload("pass"),
            generator_payload("beta", "02_beta/main.md"),
            eval_payload("pass"),
        ]
    )

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        from_stage="alpha",
        to_stage="beta",
        run_dir=repo / "enter_output" / "runs" / "range",
        config_path=repo / "run_config.json",
        max_retries=0,
    )

    assert status["status"] == "completed"
    assert [call["stage"] for call in client.calls] == ["alpha", "alpha", "beta", "beta"]
    assert not (repo / "enter_output" / "runs" / "range" / "03_gamma").exists()


def test_host_actions_are_written_as_stage_artifact_and_pause_the_host(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["topic-selection"])
    action = {
        "type": "feishu_create_doc",
        "source_file": "02_topics/topics.md",
        "target": "topic_doc",
        "permission": "public_editable",
        "write_result_to": "02_topics/feishu_links.md",
    }
    client = ScriptedModelClient(
        [
            generator_payload("topic-selection", "01_topic-selection/main.md", external_actions=[]),
            eval_payload("pass"),
        ]
    )
    client._responses[0]["host_actions"] = [action]
    runner = make_runner(repo, client, ["topic-selection"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="host_actions")

    assert status["status"] == "needs_external_action"
    stage_actions = repo / "enter_output" / "runs" / "host_actions" / "01_topic-selection" / "host_actions.json"
    assert json.loads(stage_actions.read_text(encoding="utf-8")) == [action]
    manifest = json.loads(Path(status["action_manifest"]).read_text(encoding="utf-8"))
    assert manifest["type"] == "feishu_create_doc"
    assert manifest["write_result_to"] == "02_topics/feishu_links.md"


def test_stage_run_manifest_records_generator_eval_and_handoff_paths(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="manifest")

    assert status["status"] == "completed"
    manifest = json.loads((repo / "enter_output" / "runs" / "manifest" / "01_alpha" / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["stage"] == "alpha"
    assert manifest["generator_request_id"].startswith("scripted-")
    assert manifest["eval_request_id"].startswith("scripted-")
    assert manifest["verdict"] == "pass"
    assert manifest["retry_count"] == 0
    assert manifest["approved_handoff_path"] == "01_alpha/handoff_packet.json"


def test_search_project_creation_can_be_enabled_by_user_facing_flag(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["product-research"])
    config_path = repo / "run_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["create_search_occupancy_project"] = True
    write_json(config_path, config)
    client = ScriptedModelClient(
        [
            generator_payload("product-research", "01_product-research/main.md"),
            eval_payload("pass"),
        ]
    )
    search_adapter = FlakySearchProjectAdapter()
    search_adapter.calls = 1
    runner = make_runner(repo, client, ["product-research"], max_retries=0, search_project_adapter=search_adapter)

    status = runner.start(config_path, run_id="search_flag")

    assert status["status"] == "completed"
    updated_config = json.loads((repo / "enter_output" / "runs" / "search_flag" / "run_config.json").read_text(encoding="utf-8"))
    handoff = json.loads((repo / "enter_output" / "runs" / "search_flag" / "01_product-research" / "handoff_packet.json").read_text(encoding="utf-8"))
    assert updated_config["search_occupancy_project_id"] == "search-project-1"
    assert handoff["search_occupancy_project_id"] == "search-project-1"


def test_every_stage_has_lightweight_wrapper_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    for stage in [
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
    ]:
        wrapper_name = "run_" + stage.replace("-", "_") + ".py"
        wrapper = repo_root / "enter_output" / "skills" / stage / wrapper_name
        assert wrapper.exists(), f"missing wrapper for {stage}"
        assert "enter_output/runtime/run_stage.py" in wrapper.read_text(encoding="utf-8").replace("\\", "/")


def test_mock_schema_examples_honor_known_path_patterns() -> None:
    assert example_from_schema({"type": "string", "pattern": "^03_search/maps/.+[.]md$"}) == "03_search/maps/mock.md"
    assert example_from_schema({"type": "string", "pattern": "^03_search/maps/.+[.]json$"}) == "03_search/maps/mock.json"
    assert example_from_schema({"type": "string", "pattern": "^03_search/topic_cards/.+"}) == "03_search/topic_cards/mock.json"


def test_intent_file_selects_single_stage_and_records_source_mode(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha", "post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    intent_path = repo / "intent.json"
    write_json(
        intent_path,
        {
            "requested_scope": "single_stage",
            "target_stage": "post-native-rewrite",
            "source_mode": "inline_text",
            "inline_text_path": "input/source_post.md",
            "stop_after_stage": "post-native-rewrite",
            "user_goal": "make the post more Reddit-native",
        },
    )
    run_dir = repo / "enter_output" / "runs" / "intent_native"
    write_text(run_dir / "input" / "source_post.md", "# draft\n")
    client = ScriptedModelClient(
        [generator_payload("post-native-rewrite", "06_optimized/native_posts.md"), eval_payload("pass")]
    )

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        intent_path=intent_path,
        run_dir=run_dir,
        config_path=repo / "run_config.json",
        max_retries=0,
    )

    assert status["status"] == "completed"
    assert [call["stage"] for call in client.calls] == ["post-native-rewrite", "post-native-rewrite"]
    written_config = json.loads((run_dir / "run_config.json").read_text(encoding="utf-8"))
    assert written_config["source_mode"] == "inline_text"
    assert written_config["user_goal"] == "make the post more Reddit-native"
    assert not (run_dir / "01_alpha").exists()


def test_feishu_url_requires_ingest_before_native_rewrite(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    client = ScriptedModelClient([])

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        stage="post-native-rewrite",
        run_dir=repo / "enter_output" / "runs" / "needs_feishu",
        config_path=repo / "run_config.json",
        feishu_url="https://example.feishu.cn/docx/doc123",
        max_retries=0,
    )

    assert status["status"] == "needs_external_action"
    assert status["stage"] == "post-native-rewrite"
    assert status["action_type"] == "feishu.read_document"
    assert status["expected_artifact"].endswith("input/source_doc.md")
    assert len(client.calls) == 0


def test_resume_after_feishu_ingest_runs_native_rewrite(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    first_client = ScriptedModelClient([])
    runner = make_runner(repo, first_client, ["post-native-rewrite"], max_retries=0)
    config_path = repo / "run_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config.update({"source_mode": "feishu_url", "feishu_url": "https://example.feishu.cn/docx/doc123"})
    write_json(config_path, config)

    status = runner.start(config_path, run_id="resume_feishu")

    assert status["status"] == "needs_external_action"
    assert len(first_client.calls) == 0
    run_dir = repo / "enter_output" / "runs" / "resume_feishu"
    write_text(run_dir / "input" / "source_doc.md", "# Feishu source\n")
    write_json(run_dir / "actions" / "feishu_read.result.json", {"url": config["feishu_url"], "artifact": "input/source_doc.md"})

    second_client = ScriptedModelClient(
        [generator_payload("post-native-rewrite", "06_optimized/native_posts.md"), eval_payload("pass")]
    )
    resumed_runner = make_runner(repo, second_client, ["post-native-rewrite"], max_retries=0)

    resumed = resumed_runner.resume("resume_feishu")

    assert resumed["status"] == "completed"
    assert [call["kind"] for call in second_client.calls] == ["generator", "evaluator"]


def test_eval_placeholder_expands_selected_post_ids_only(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    write_eval_inputs(
        repo,
        "post-native-rewrite",
        [
            "- `run:05_optimized_cards/handoff_packet.json`",
            "- `run:05_optimized_cards/drafts_md/{post_id}.md` for selected posts only.",
        ],
    )
    run_dir = repo / "enter_output" / "runs" / "eval_selected"
    write_text(run_dir / "06_optimized" / "native_posts.md", "# native\n")
    write_json(
        run_dir / "05_optimized_cards" / "handoff_packet.json",
        {"selected_posts": [{"post_id": "post_a"}, {"id": "post_b"}]},
    )
    write_text(run_dir / "05_optimized_cards" / "drafts_md" / "post_a.md", "# post a\n")
    write_text(run_dir / "05_optimized_cards" / "drafts_md" / "post_b.md", "# post b\n")
    write_text(run_dir / "05_optimized_cards" / "drafts_md" / "post_c.md", "# post c\n")
    builder = PromptBuilder(repo)
    spec = builder.load_stage("post-native-rewrite")

    packet = builder.build_evaluator_packet(
        spec,
        run_dir,
        ["06_optimized/native_posts.md"],
        output={"artifact_paths": {"native": "06_optimized/native_posts.md"}},
        handoff={"selected_posts": [{"post_id": "post_a"}, {"id": "post_b"}]},
    )

    eval_paths = [item["path"] for item in packet["business_inputs"]]
    assert "run:05_optimized_cards/drafts_md/post_a.md" in eval_paths
    assert "run:05_optimized_cards/drafts_md/post_b.md" in eval_paths
    assert "run:05_optimized_cards/drafts_md/post_c.md" not in eval_paths
    assert "run:05_optimized_cards/drafts_md/{post_id}.md" not in eval_paths
    assert builder.missing_business_inputs(packet, run_dir) == []


def test_eval_placeholder_missing_selected_id_is_missing_eval_input(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["post-native-rewrite"])
    write_stage(repo, "post-native-rewrite", "stage_post_native_rewrite", "06_optimized/native_posts.md")
    write_eval_inputs(
        repo,
        "post-native-rewrite",
        ["- `run:05_optimized_cards/drafts_md/{post_id}.md` for selected posts only."],
    )
    run_dir = repo / "enter_output" / "runs" / "eval_missing_selected"
    write_text(run_dir / "06_optimized" / "native_posts.md", "# native\n")
    builder = PromptBuilder(repo)
    spec = builder.load_stage("post-native-rewrite")

    packet = builder.build_evaluator_packet(
        spec,
        run_dir,
        ["06_optimized/native_posts.md"],
        output={"artifact_paths": {"native": "06_optimized/native_posts.md"}},
        handoff={},
    )

    assert builder.missing_business_inputs(packet, run_dir) == ["run:05_optimized_cards/drafts_md/{post_id}.md"]


def test_dry_run_packet_does_not_call_model_and_writes_preview_manifests(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    run_dir = repo / "enter_output" / "runs" / "dry_run"
    client = ScriptedModelClient([])

    from enter_output.runtime.run_stage import run_with_client

    status = run_with_client(
        repo_root=repo,
        model_client=client,
        stage="alpha",
        run_dir=run_dir,
        config_path=repo / "run_config.json",
        dry_run_packet=True,
    )

    assert status["status"] == "dry_run_packet"
    assert len(client.calls) == 0
    generator_manifest = json.loads((run_dir / "generator_input_manifest.json").read_text(encoding="utf-8"))
    evaluator_manifest = json.loads((run_dir / "evaluator_input_manifest.preview.json").read_text(encoding="utf-8"))
    assert generator_manifest["worker_role"] == "generator"
    assert evaluator_manifest["worker_role"] == "evaluator"
    assert "estimated_chars" in generator_manifest
    assert "missing_inputs" in evaluator_manifest


def test_generator_request_manifest_and_eval_request_manifest_written(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, ["alpha"])
    client = ScriptedModelClient([generator_payload("alpha", "01_alpha/main.md"), eval_payload("pass")])
    runner = make_runner(repo, client, ["alpha"], max_retries=0)

    status = runner.start(repo / "run_config.json", run_id="request_manifests")

    assert status["status"] == "completed"
    attempt_dir = repo / "enter_output" / "runs" / "request_manifests" / "01_alpha" / "runtime" / "attempt_001"
    generator_manifest = json.loads((attempt_dir / "generator_request_manifest.json").read_text(encoding="utf-8"))
    evaluator_manifest = json.loads((attempt_dir / "evaluator_request_manifest.json").read_text(encoding="utf-8"))
    assert generator_manifest["kind"] == "generator"
    assert evaluator_manifest["kind"] == "evaluator"
    assert generator_manifest["request_id"] == client.calls[0]["request_id"]
    assert evaluator_manifest["request_id"] == client.calls[1]["request_id"]
    assert all("raw_response" not in path for path in evaluator_manifest["files_included"])
    assert all("candidate_" not in path for path in evaluator_manifest["files_included"])
