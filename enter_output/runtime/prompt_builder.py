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
    eval_inputs_path: Path
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
            eval_inputs_path=skill_dir / "EVAL_INPUTS.md",
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
            if _is_optional_reference_line(source_line):
                ref["optional"] = True
            business_inputs.append(ref)
        business_inputs = _apply_ad_hoc_business_inputs(spec.name, business_inputs, run_config)
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
            "evals_for_self_check_only": True,
        }
        return packet

    def build_evaluator_packet(
        self,
        spec: StageSpec,
        run_dir: Path,
        artifact_paths: list[str],
        *,
        output: dict[str, Any] | None = None,
        handoff: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        business_inputs = [{"path": f"run:{path}", "purpose": "artifact under review"} for path in artifact_paths]
        if spec.eval_inputs_path.exists():
            text = spec.eval_inputs_path.read_text(encoding="utf-8")
            instruction_files = [
                {"path": item, "mandatory": True}
                for item in _path_items(_section_text(text, "### Required instruction files"))
            ]
            instruction_files.extend(
                {"path": item, "mandatory": False}
                for item in _path_items(_section_text(text, "### Optional instruction files"))
            )
            eval_business_inputs = _business_input_refs(_section_text(text, "### Business input files"))
            context = _context_from_refs(eval_business_inputs, run_dir, output or {}, handoff or {})
            expanded_inputs = expand_placeholder_refs(
                eval_business_inputs,
                run_dir,
                spec.name,
                output or {},
                context,
            )
            return {
                "worker_role": "evaluator",
                "stage": spec.name,
                "stage_id": spec.stage_id,
                "run_folder": str(run_dir),
                "role_prompt": _section_text(text, "### Role prompt")
                or "Run the Reviewer prompt from EVALS.md as an independent evaluator.",
                "instruction_files": instruction_files or _default_eval_instruction_files(spec),
                "business_inputs": _dedupe_file_refs(
                    business_inputs + expanded_inputs
                ),
                "read_order": _list_items(_section_text(text, "### Read order")),
                "blind_eval": True,
                "allowed_extra_reads": _list_items(_section_text(text, "### Allowed extra reads")),
                "forbidden_files": _list_items(_section_text(text, "### Forbidden files")),
                "output_schema": f"repo:enter_output/skills/{spec.name}/OUTPUT_SCHEMA.json",
                "handoff_schema": f"repo:enter_output/skills/{spec.name}/HANDOFF_SCHEMA.json",
                "evals": f"repo:enter_output/skills/{spec.name}/EVALS.md",
            }
        minimal_context = []
        for ref in _default_minimal_eval_context():
            if self.resolve_ref(ref, run_dir).exists():
                minimal_context.append({"path": ref, "purpose": "minimal fact/brand context", "optional": True})
        return {
            "worker_role": "evaluator",
            "stage": spec.name,
            "stage_id": spec.stage_id,
            "run_folder": str(run_dir),
            "role_prompt": "Run the Reviewer prompt from EVALS.md as an independent evaluator.",
            "instruction_files": _default_eval_instruction_files(spec),
            "business_inputs": business_inputs + minimal_context,
            "blind_eval": True,
            "allowed_extra_reads": [],
        }

    def packet_manifest(
        self,
        packet: dict[str, Any],
        run_dir: Path,
        *,
        request_id: str | None = None,
        attempt: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        files_included, estimated_chars = self._files_included(packet, run_dir)
        manifest = {
            "stage": packet.get("stage"),
            "kind": packet.get("worker_role"),
            "worker_role": packet.get("worker_role"),
            "attempt": attempt,
            "request_id": request_id,
            "files_included": files_included,
            "instruction_files": packet.get("instruction_files", []),
            "business_inputs": packet.get("business_inputs", []),
            "missing_inputs": self.missing_mandatory_files(packet, run_dir) + self.missing_business_inputs(packet, run_dir),
            "forbidden_files": packet.get("forbidden_files", []),
            "estimated_chars": estimated_chars,
            "metadata": _redact_metadata(metadata or {}),
        }
        if packet.get("evals_for_self_check_only"):
            manifest["evals_for_self_check_only"] = True
        return manifest

    def _files_included(self, packet: dict[str, Any], run_dir: Path) -> tuple[list[str], int]:
        included: list[str] = []
        estimated_chars = 0
        for ref in list(packet.get("instruction_files", [])) + list(packet.get("business_inputs", [])):
            path_ref = ref.get("path")
            if not path_ref:
                continue
            resolved = self.resolve_ref(path_ref, run_dir)
            if resolved is None or not resolved.exists() or resolved.is_dir():
                continue
            included.append(path_ref)
            try:
                estimated_chars += len(resolved.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                estimated_chars += resolved.stat().st_size
        return included, estimated_chars

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

    def missing_business_inputs(self, packet: dict[str, Any], run_dir: Path) -> list[str]:
        missing: list[str] = []
        for ref in packet.get("business_inputs", []):
            if ref.get("optional") or ref.get("mandatory") is False:
                continue
            path_ref = ref.get("path", "")
            if not path_ref.startswith("run:"):
                continue
            relative = path_ref.removeprefix("run:")
            if relative == "run_config.json":
                continue
            if "{" in relative and "}" in relative:
                if packet.get("worker_role") == "evaluator":
                    missing.append(path_ref)
                    continue
                glob_pattern = re.sub(r"\{[^}]+\}", "*", relative)
                if not list(run_dir.glob(glob_pattern)):
                    missing.append(path_ref)
                continue
            if not (run_dir / relative).exists():
                missing.append(path_ref)
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
        for match in re.finditer(r"`([^`]+)`", line):
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


def _business_input_refs(section: str) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for item, source_line in _path_items_with_source(section):
        ref: dict[str, Any] = {"path": item, "purpose": "business input"}
        if _is_optional_reference_line(source_line):
            ref["optional"] = True
        refs.append(ref)
    return refs


def expand_placeholder_refs(
    refs: list[dict[str, Any]],
    run_dir: Path,
    stage: str,
    output: dict[str, Any],
    handoff: dict[str, Any],
) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for ref in refs:
        path_ref = ref.get("path", "")
        placeholders = re.findall(r"\{([^}]+)\}", path_ref)
        if not placeholders:
            expanded.append(ref)
            continue
        replacements = [_placeholder_values(name, output, handoff) for name in placeholders]
        if not replacements or any(not values for values in replacements):
            missing_ref = dict(ref)
            missing_ref["purpose"] = ref.get("purpose", "business input")
            missing_ref["missing_reason"] = "placeholder_not_resolved"
            expanded.append(missing_ref)
            continue
        for values in zip(*replacements):
            concrete_path = path_ref
            for placeholder, value in zip(placeholders, values):
                concrete_path = concrete_path.replace("{" + placeholder + "}", str(value))
            concrete = dict(ref)
            concrete["path"] = concrete_path
            concrete["expanded_from"] = path_ref
            concrete["purpose"] = ref.get("purpose", "business input")
            expanded.append(concrete)
    return expanded


def _apply_ad_hoc_business_inputs(
    stage: str,
    business_inputs: list[dict[str, Any]],
    run_config: dict[str, Any],
) -> list[dict[str, Any]]:
    source_mode = run_config.get("source_mode")
    single_stage = bool(run_config.get("single_stage_mode") or run_config.get("requested_scope") == "single_stage")
    if not source_mode and not single_stage:
        return business_inputs

    by_stage: dict[str, dict[str, Any]] = {
        "post-native-rewrite": {
            "remove_prefixes": ("run:05_optimized_cards/",),
            "source_paths": {
                "feishu_url": run_config.get("expected_artifact") or "input/source_doc.md",
                "inline_text": run_config.get("inline_text_path") or "input/source_post.md",
                "provided_file": run_config.get("source_text_path") or "input/source_post.md",
                "run_artifact": run_config.get("source_artifact_path") or "input/source_post.md",
            },
        },
        "post-fact-brand-check": {
            "remove_prefixes": ("run:06_optimized/native_posts.md", "run:06_optimized/6a_handoff_packet.json"),
            "source_paths": {
                "inline_text": run_config.get("inline_text_path") or "input/native_posts.md",
                "provided_file": run_config.get("source_text_path") or "input/native_posts.md",
                "run_artifact": run_config.get("source_artifact_path") or "input/native_posts.md",
            },
        },
        "post-subreddit-image": {
            "remove_prefixes": ("run:06_optimized/checked_posts.md", "run:06_optimized/6b_handoff_packet.json"),
            "source_paths": {
                "inline_text": run_config.get("inline_text_path") or "input/checked_posts.md",
                "provided_file": run_config.get("source_text_path") or "input/checked_posts.md",
                "run_artifact": run_config.get("source_artifact_path") or "input/checked_posts.md",
            },
        },
        "feishu-formatting": {
            "remove_prefixes": ("run:06_optimized/",),
            "source_paths": {
                "feishu_url": run_config.get("expected_artifact") or "07_format/live_doc_snapshot.md",
                "inline_text": run_config.get("inline_text_path") or "input/source_doc.md",
                "provided_file": run_config.get("source_text_path") or "input/source_doc.md",
                "run_artifact": run_config.get("source_artifact_path") or "input/source_doc.md",
            },
        },
    }
    stage_rule = by_stage.get(stage)
    if not stage_rule:
        return business_inputs
    source_path = stage_rule["source_paths"].get(source_mode)
    if not source_path:
        return business_inputs
    remove_prefixes = stage_rule["remove_prefixes"]
    filtered = [
        ref
        for ref in business_inputs
        if not any(ref.get("path", "").startswith(prefix) for prefix in remove_prefixes)
    ]
    filtered.append({"path": f"run:{source_path}", "purpose": "ad-hoc source input"})
    return _dedupe_file_refs(filtered)


def _context_from_refs(
    refs: list[dict[str, Any]],
    run_dir: Path,
    output: dict[str, Any],
    handoff: dict[str, Any],
) -> dict[str, Any]:
    context: dict[str, Any] = {}
    _merge_context(context, output)
    _merge_context(context, handoff)
    for ref in refs:
        path_ref = ref.get("path", "")
        if "{" in path_ref or not path_ref.startswith("run:") or not path_ref.endswith(".json"):
            continue
        resolved = run_dir / path_ref.removeprefix("run:")
        if not resolved.exists():
            continue
        try:
            loaded = json.loads(resolved.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(loaded, dict):
            _merge_context(context, loaded)
    return context


def _merge_context(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if key not in target:
            target[key] = value


def _placeholder_values(name: str, output: dict[str, Any], handoff: dict[str, Any]) -> list[str]:
    combined = {}
    _merge_context(combined, output)
    _merge_context(combined, handoff)
    if name == "post_id":
        return _post_ids(combined)
    if name == "direction_id":
        return _values_for_keys(
            combined,
            ("direction_id", "selected_direction_id", "chosen_direction_id", "direction_ids", "chosen_direction_ids"),
        )
    if name == "topic_id":
        return _values_for_keys(combined, ("topic_id", "topic_ids", "chosen_topic_ids", "selected_topic_ids"))
    return _values_for_keys(combined, (name, f"{name}s", f"selected_{name}s", f"chosen_{name}s"))


def _post_ids(value: Any) -> list[str]:
    ids = _values_for_keys(value, ("post_id", "post_ids", "selected_post_ids", "chosen_post_ids"))
    for key in ("selected_posts", "chosen_posts", "posts"):
        selected = _find_key_values(value, key)
        for item in selected:
            if isinstance(item, list):
                for child in item:
                    ids.extend(_post_id_from_item(child))
            else:
                ids.extend(_post_id_from_item(item))
    return _unique_strings(ids)


def _post_id_from_item(item: Any) -> list[str]:
    if isinstance(item, str):
        return [item]
    if not isinstance(item, dict):
        return []
    for key in ("post_id", "id", "post_slug", "slug"):
        value = item.get(key)
        if isinstance(value, str):
            return [value]
    return []


def _values_for_keys(value: Any, keys: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for key in keys:
        for found in _find_key_values(value, key):
            if isinstance(found, list):
                values.extend(str(item) for item in found if isinstance(item, (str, int)))
            elif isinstance(found, (str, int)):
                values.append(str(found))
    return _unique_strings(values)


def _find_key_values(value: Any, key: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for current_key, current_value in value.items():
            if current_key == key:
                found.append(current_value)
            found.extend(_find_key_values(current_value, key))
    elif isinstance(value, list):
        for item in value:
            found.extend(_find_key_values(item, key))
    return found


def _unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _is_optional_reference_line(source_line: str) -> bool:
    lowered = source_line.lower()
    return (
        "optional" in lowered
        or "only when" in lowered
        or "if present" in lowered
        or "if written by" in lowered
        or "if runtime" in lowered
        or " when " in lowered
        or " only to " in lowered
    )


def _default_eval_instruction_files(spec: StageSpec) -> list[dict[str, Any]]:
    return [
        {
            "path": "repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md",
            "mandatory": True,
        },
        {"path": f"repo:enter_output/skills/{spec.name}/EVALS.md", "mandatory": True},
        {"path": f"repo:enter_output/skills/{spec.name}/OUTPUT_SCHEMA.json", "mandatory": True},
        {"path": f"repo:enter_output/skills/{spec.name}/HANDOFF_SCHEMA.json", "mandatory": True},
    ]


def _default_minimal_eval_context() -> list[str]:
    return [
        "run:global/product_fact_index.json",
        "run:global/claim_boundary_table.json",
        "run:global/brand_safety_rules.md",
    ]


def _dedupe_file_refs(refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_path: dict[str, dict[str, Any]] = {}
    for ref in refs:
        path = ref.get("path")
        if not path:
            continue
        if path not in by_path:
            by_path[path] = dict(ref)
            continue
        existing = by_path[path]
        if not ref.get("optional") or ref.get("mandatory") is True:
            existing.pop("optional", None)
            if ref.get("mandatory") is True:
                existing["mandatory"] = True
    return list(by_path.values())


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


def _redact_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in metadata.items():
        if any(secret_word in key.lower() for secret_word in ("key", "cookie", "secret", "token")):
            redacted[key] = "[REDACTED]"
        else:
            redacted[key] = value
    return redacted
