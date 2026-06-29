from __future__ import annotations

from typing import Any


def normalize_eval_result(payload: dict[str, Any]) -> dict[str, Any]:
    verdict = payload.get("verdict") or payload.get("blocking") or "fail"
    blocking = payload.get("blocking") or verdict
    score = payload.get("score", 0)
    retry_needed = payload.get("retry_needed", verdict != "pass")
    result = dict(payload)
    result["blocking"] = "pass" if blocking == "pass" else "fail"
    result["score"] = score
    result["retry_needed"] = bool(retry_needed)
    result["verdict"] = "pass" if verdict == "pass" and result["blocking"] == "pass" else "fail"
    result.setdefault("required_fixes", [])
    return result


def eval_passed(result: dict[str, Any]) -> bool:
    return result.get("verdict") == "pass" and result.get("blocking") == "pass"
