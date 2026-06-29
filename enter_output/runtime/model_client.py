from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ModelResponse:
    content: str
    request_id: str
    provider: str
    model: str
    raw: dict[str, Any] | None = None


class ModelClient(Protocol):
    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        kind: str,
        stage: str,
        attempt: int,
        metadata: dict[str, Any] | None = None,
    ) -> ModelResponse:
        ...


class ScriptedModelClient:
    """Deterministic client for tests."""

    def __init__(self, responses: list[dict[str, Any] | str]) -> None:
        self._responses = list(responses)
        self.calls: list[dict[str, Any]] = []

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        kind: str,
        stage: str,
        attempt: int,
        metadata: dict[str, Any] | None = None,
    ) -> ModelResponse:
        request_id = f"scripted-{uuid.uuid4().hex}"
        self.calls.append(
            {
                "request_id": request_id,
                "kind": kind,
                "stage": stage,
                "attempt": attempt,
                "message_count": len(messages),
                "metadata": metadata or {},
            }
        )
        if not self._responses:
            raise RuntimeError("ScriptedModelClient has no response left")
        payload = self._responses.pop(0)
        content = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        return ModelResponse(content=content, request_id=request_id, provider="scripted", model="scripted")


class MockModelClient:
    """Schema-driven mock client that produces valid envelopes for dry runs."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        kind: str,
        stage: str,
        attempt: int,
        metadata: dict[str, Any] | None = None,
    ) -> ModelResponse:
        request_id = f"mock-{uuid.uuid4().hex}"
        self.calls.append({"request_id": request_id, "kind": kind, "stage": stage, "attempt": attempt})
        metadata = metadata or {}
        if kind == "evaluator":
            payload = {
                "blocking": "pass",
                "score": 100,
                "threshold": metadata.get("threshold", 80),
                "retry_needed": False,
                "verdict": "pass",
                "required_fixes": [],
                "evaluator_mode": "emulated_fresh_session",
            }
        else:
            output_schema = metadata.get("output_schema", {})
            handoff_schema = metadata.get("handoff_schema", {})
            output = example_from_schema(output_schema)
            handoff = example_from_schema(handoff_schema)
            handoff.pop("eval_result", None)
            handoff["status"] = "draft"
            files = {path: _mock_file_content(path, stage) for path in sorted(extract_declared_paths(output))}
            payload = {"output": output, "handoff": handoff, "files": files, "external_actions": []}
        return ModelResponse(
            content=json.dumps(payload, ensure_ascii=False),
            request_id=request_id,
            provider="mock",
            model="mock",
        )


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        provider: str,
        api_key: str,
        model: str,
        base_url: str,
        timeout_seconds: int = 120,
        extra_payload: dict[str, Any] | None = None,
    ) -> None:
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.extra_payload = extra_payload or {}

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        kind: str,
        stage: str,
        attempt: int,
        metadata: dict[str, Any] | None = None,
    ) -> ModelResponse:
        request_id = f"{self.provider}-{uuid.uuid4().hex}"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        payload.update(self.extra_payload)
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "X-Request-Id": request_id,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{self.provider} API error {exc.code}: {_redact(body)}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{self.provider} API connection failed: {_redact(str(exc.reason))}") from exc
        content = raw["choices"][0]["message"]["content"]
        return ModelResponse(content=content, request_id=request_id, provider=self.provider, model=self.model, raw=raw)


def create_model_client(provider: str, config: dict[str, Any] | None = None) -> ModelClient:
    config = config or {}
    provider = provider.lower()
    if provider == "mock":
        return MockModelClient()
    if provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is required for provider=deepseek")
        return OpenAICompatibleClient(
            provider="deepseek",
            api_key=api_key,
            model=os.environ.get("DEEPSEEK_MODEL", config.get("model", "deepseek-v4-flash")),
            base_url=os.environ.get("DEEPSEEK_API_BASE_URL", config.get("base_url", "https://api.deepseek.com")),
            timeout_seconds=int(os.environ.get("MODEL_TIMEOUT_SECONDS", "120")),
            extra_payload={
                "thinking": {"type": "enabled"},
                "reasoning_effort": config.get("reasoning_effort", "high"),
            },
        )
    if provider == "openai-compatible":
        api_key = os.environ.get(config.get("api_key_env", "MODEL_API_KEY"))
        base_url = os.environ.get(config.get("base_url_env", "MODEL_API_BASE_URL"))
        model = os.environ.get(config.get("model_env", "MODEL_NAME"), config.get("model", ""))
        if not api_key or not base_url or not model:
            raise RuntimeError("MODEL_API_KEY, MODEL_API_BASE_URL, and MODEL_NAME are required")
        return OpenAICompatibleClient(
            provider="openai-compatible",
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout_seconds=int(os.environ.get("MODEL_TIMEOUT_SECONDS", "120")),
            extra_payload=config.get("extra_payload", {}),
        )
    raise RuntimeError(f"Unknown model provider: {provider}")


def example_from_schema(schema: dict[str, Any]) -> Any:
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        schema_type = next((item for item in schema_type if item != "null"), schema_type[0])
    if schema_type == "object" or "properties" in schema:
        result: dict[str, Any] = {}
        properties = schema.get("properties", {})
        for key in schema.get("required", list(properties.keys())):
            if key in properties:
                result[key] = example_from_schema(properties[key])
        return result
    if schema_type == "array":
        item_schema = schema.get("items", {"type": "string"})
        count = max(1, int(schema.get("minItems", 1)))
        return [example_from_schema(item_schema) for _ in range(count)]
    if schema_type == "integer":
        return int(schema.get("minimum", 1))
    if schema_type == "number":
        return float(schema.get("minimum", 100))
    if schema_type == "boolean":
        return True
    if schema_type == "null":
        return None
    if schema_type == "string" and "pattern" in schema:
        return _example_for_pattern(schema["pattern"])
    return "mock"


def extract_declared_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            paths.update(extract_declared_paths(child))
    elif isinstance(value, list):
        for child in value:
            paths.update(extract_declared_paths(child))
    elif isinstance(value, str) and (value.endswith(".md") or value.endswith(".json")) and "/" in value:
        paths.add(value)
    return paths


def _mock_file_content(path: str, stage: str) -> str:
    if path.endswith(".json"):
        return json.dumps({"mock": True, "stage": stage, "path": path}, ensure_ascii=False, indent=2)
    return f"# Mock artifact for {stage}\n\nPath: `{path}`\n"


def _example_for_pattern(pattern: str) -> str:
    if "03_search/maps/" in pattern and "[.]md" in pattern:
        return "03_search/maps/mock.md"
    if "03_search/maps/" in pattern and "[.]json" in pattern:
        return "03_search/maps/mock.json"
    if "03_search/topic_cards/" in pattern:
        return "03_search/topic_cards/mock.json"
    if pattern.startswith("^") and pattern.endswith("$"):
        return pattern.strip("^$").replace(".+", "mock").replace("[.]", ".")
    return "mock"


def _redact(text: str) -> str:
    for key in ("DEEPSEEK_API_KEY", "MODEL_API_KEY"):
        value = os.environ.get(key)
        if value:
            text = text.replace(value, "[REDACTED]")
    return text


def monotonic_request_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}-{uuid.uuid4().hex}"
