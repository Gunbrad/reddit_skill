import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from enter_output.runtime.external_actions import HttpSearchProjectAdapter, SearchProjectError, create_action_manifest
from enter_output.runtime.model_client import ScriptedModelClient, example_from_schema
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


def test_mock_schema_examples_honor_known_path_patterns() -> None:
    assert example_from_schema({"type": "string", "pattern": "^03_search/maps/.+[.]md$"}) == "03_search/maps/mock.md"
    assert example_from_schema({"type": "string", "pattern": "^03_search/maps/.+[.]json$"}) == "03_search/maps/mock.json"
    assert example_from_schema({"type": "string", "pattern": "^03_search/topic_cards/.+"}) == "03_search/topic_cards/mock.json"
