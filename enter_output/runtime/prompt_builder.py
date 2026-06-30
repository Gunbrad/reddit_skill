from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FileRef:
    path: str
    mandatory: bool = True
    purpose: str = "instruction"


@dataclass(frozen=True)
class StageSpec:
    name: str
    stage_id: str
    skill_dir: Path
    inputs_path: Path
    skill_path: Path
    evals_path: Path
    output_schema_path: Path
    handoff_schema_path: Path
    output_schema: dict[str, Any]
    handoff_schema: dict[str, Any]
    output_dir: str


class PromptBuilder:
    def __init__(self, repo_root: Path, workspace_root: Path | None = None) -> None:
        self.repo_root = repo_root
        self.workspace_root = workspace_root or repo_root.parent.parent.parent

    def load_stage(self, stage_name: str) -> StageSpec:
        skill_dir = self.repo_root / "enter_output" / "skills" / stage_name
        output_schema = _read_json(skill_dir / "OUTPUT_SCHEMA.json")
        handoff_schema = _read_json(skill_dir / "HANDOFF_SCHEMA.json")
        stage_id = output_schema.get("properties", {}).get("stage_id", {}).get("const", stage_name)
        output_dir = _derive_output_dir(output_schema, stage_name)
        return StageSpec(
            name=stage_name,
            stage_id=stage_id,
            skill_dir=skill_dir,
            inputs_path=skill_dir / "INPUTS.md",
            skill_path=skill_dir / "SKILL.md",
            evals_path=skill_dir / "EVALS.md",
            output_schema_path=skill_dir / "OUTPUT_SCHEMA.json",
            handoff_schema_path=skill_dir / "HANDOFF_SCHEMA.json",
            output_schema=output_schema,
            handoff_schema=handoff_schema,
            output_dir=output_dir,
        )

    def build_generator_packet(self, spec: StageSpec, run_dir: Path, run_config: dict[str, Any]) -> dict[str, Any]:
        text = spec.inputs_path.read_text(encoding="utf-8")
        role_prompt = _section_text(text, "### Role prompt")
        instruction_files = [
            {"path": item, "mandatory": True}
            for item in _path_items(_section_text(text, "### Required instruction files"))
        ]
        instruction_files.extend(_optional_instruction_files(run_config, spec.name))
        business_inputs = []
        for item, source_line in _path_items_with_source(_section_text(text, "### Business input files")):
            ref = {"path": item, "purpose": "business input"}
            lowered = source_line.lower()
            if (
                "only when" in lowered
                or "if present" in lowered
                or "if written by" in lowered
                or " when " in lowered
                or " only to " in lowered
            ):
                ref["optional"] = True
            business_inputs.append(ref)
        packet = {
            "worker_role": "generator",
            "stage": spec.name,
            "stage_id": spec.stage_id,
            "run_folder": str(run_dir),
            "role_prompt": role_prompt,
            "instruction_files": instruction_files,
            "business_inputs": business_inputs,
            "read_order": _list_items(_section_text(text, "### Read order")),
            "allowed_extra_reads": _list_items(_section_text(text, "### Allowed extra reads")),
            "allowed_global_files": _list_items(_section_text(text, "## Allowed global files")),
            "allowed_stage_files": _list_items(_section_text(text, "## Allowed stage files")),
            "forbidden_files": _list_items(_section_text(text, "## Forbidden files")),
            "output_schema": f"repo:enter_output/skills/{spec.name}/OUTPUT_SCHEMA.json",
            "handoff_schema": f"repo:enter_output/skills/{spec.name}/HANDOFF_SCHEMA.json",
            "evals": f"repo:enter_output/skills/{spec.name}/EVALS.md",
        }
        return packet

    def build_evaluator_packet(self, spec: StageSpec, run_dir: Path, artifact_paths: list[str]) -> dict[str, Any]:
        business_inputs = [{"path": f"run:{path}", "purpose": "artifact under review"} for path in artifact_paths]
        minimal_context = []
        for ref in [
            "run:global/product_fact_index.json",
            "run:global/claim_boundary_table.json",
            "run:global/brand_safety_rules.md",
        ]:
            if self.resolve_ref(ref, run_dir).exists():
                minimal_context.append({"path": ref, "purpose": "minimal fact/brand context", "optional": True})
        return {
            "worker_role": "evaluator",
            "stage": spec.name,
            "stage_id": spec.stage_id,
            "run_folder": str(run_dir),
            "role_prompt": "Run the Reviewer prompt from EVALS.md as an independent evaluator.",
            "instruction_files": [
                {
                    "path": "repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md",
                    "mandatory": True,
                },
                {"path": f"repo:enter_output/skills/{spec.name}/EVALS.md", "mandatory": True},
                {"path": f"repo:enter_output/skills/{spec.name}/OUTPUT_SCHEMA.json", "mandatory": True},
                {"path": f"repo:enter_output/skills/{spec.name}/HANDOFF_SCHEMA.json", "mandatory": True},
            ],
            "business_inputs": business_inputs + minimal_context,
            "blind_eval": True,
            "allowed_extra_reads": [],
        }

    def messages_for_packet(self, packet: dict[str, Any], run_dir: Path) -> list[dict[str, str]]:
        missing = self.missing_mandatory_files(packet, run_dir)
        if missing:
            raise FileNotFoundError("Missing mandatory packet files: " + ", ".join(missing))
        content_parts = [
            "# Prompt Packet",
            json.dumps(_without_large_schema(packet), ensure_ascii=False, indent=2),
        ]
        for ref in packet.get("instruction_files", []):
            resolved = self.resolve_ref(ref["path"], run_dir)
            if resolved and resolved.exists():
                content_parts.append(f"\n# Instruction: {ref['path']}\n{resolved.read_text(encoding='utf-8')}")
        for ref in packet.get("business_inputs", []):
            resolved = self.resolve_ref(ref["path"], run_dir)
            if resolved and resolved.exists():
                content_parts.append(f"\n# Business Input: {ref['path']}\n{resolved.read_text(encoding='utf-8')}")
        if packet["worker_role"] == "generator":
            content_parts.append(
                "\nReturn one JSON object with keys: output, handoff, files, external_actions. "
                "The output object must match OUTPUT_SCHEMA.json. files maps run-relative paths to file content. "
                "Do not include secrets."
            )
        else:
            content_parts.append(
                "\nReturn one JSON object with blocking, score, retry_needed, verdict, required_fixes."
            )
        return [
            {"role": "system", "content": packet.get("role_prompt", "")},
            {"role": "user", "content": "\n".join(content_parts)},
        ]

    def missing_mandatory_files(self, packet: dict[str, Any], run_dir: Path) -> list[str]:
        missing: list[str] = []
        for ref in packet.get("instruction_files", []):
            if not ref.get("mandatory", True):
                continue
            resolved = self.resolve_ref(ref["path"], run_dir)
            if resolved is None or not resolved.exists():
                missing.append(ref["path"])
        return missing

    def resolve_ref(self, ref: str, run_dir: Path) -> Path | None:
        if ref.startswith("repo:"):
            return self.repo_root / ref.removeprefix("repo:")
        if ref.startswith("run:"):
            return run_dir / ref.removeprefix("run:")
        if ref.startswith("workspace:"):
            return self.workspace_root / ref.removeprefix("workspace:")
        if ref.startswith("absolute:"):
            return Path(ref.removeprefix("absolute:"))
        if ref.startswith("run_config."):
            return None
        return self.repo_root / ref


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _section_text(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    start = text.find("\n", start)
    if start == -1:
        return ""
    next_heading = re.search(r"\n#{1,3} ", text[start + 1 :])
    if not next_heading:
        return text[start + 1 :].strip()
    end = start + 1 + next_heading.start()
    return text[start + 1 : end].strip()


def _path_items(section: str) -> list[str]:
    return [item for item, _source_line in _path_items_with_source(section)]


def _path_items_with_source(section: str) -> list[tuple[str, str]]:
    items: list[str] = []
    for line in section.splitlines():
        match = re.search(r"`([^`]+)`", line)
        if match:
            item = match.group(1).strip()
            if _looks_like_ref(item):
                items.append((item, line.strip()))
    return items


def _list_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            items.append(stripped[2:].strip())
        elif re.match(r"^\d+[.]\s+", stripped):
            items.append(re.sub(r"^\d+[.]\s+", "", stripped).strip())
    return items


def _looks_like_ref(item: str) -> bool:
    return item.startswith(("repo:", "run:", "workspace:", "absolute:", "run_config.")) or "/" in item or "\\" in item


def _optional_instruction_files(run_config: dict[str, Any], stage: str) -> list[dict[str, Any]]:
    prompt_packs = run_config.get("prompt_packs", {})
    stage_pack = prompt_packs.get(stage, {})
    refs = stage_pack.get("extra_instruction_files", [])
    return [{"path": ref, "mandatory": True} for ref in refs]


def _derive_output_dir(schema: dict[str, Any], fallback: str) -> str:
    for path in _schema_const_paths(schema):
        if "/" in path:
            return path.split("/", 1)[0]
    return fallback


def _schema_const_paths(schema: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(schema, dict):
        const = schema.get("const")
        if isinstance(const, str) and (const.endswith(".md") or const.endswith(".json")):
            paths.append(const)
        for child in schema.values():
            paths.extend(_schema_const_paths(child))
    elif isinstance(schema, list):
        for child in schema:
            paths.extend(_schema_const_paths(child))
    return paths


def _without_large_schema(packet: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in packet.items() if key not in {"output_schema_json", "handoff_schema_json"}}
