from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]


class SchemaValidationError(ValueError):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def validate_or_raise(instance: Any, schema: dict[str, Any]) -> None:
    result = validate(instance, schema)
    if not result.valid:
        raise SchemaValidationError(result.errors)


def validate(instance: Any, schema: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    _validate(instance, schema, "$", errors)
    return ValidationResult(valid=not errors, errors=errors)


def _validate(instance: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")
        return

    if "type" in schema and not _type_matches(instance, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']!r}, got {type(instance).__name__}")
        return

    if isinstance(instance, dict):
        _validate_object(instance, schema, path, errors)
    elif isinstance(instance, list):
        _validate_array(instance, schema, path, errors)
    elif isinstance(instance, str):
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: expected >= {minimum}, got {instance}")
        if maximum is not None and instance > maximum:
            errors.append(f"{path}: expected <= {maximum}, got {instance}")


def _validate_object(instance: dict[str, Any], schema: dict[str, Any], path: str, errors: list[str]) -> None:
    for key in schema.get("required", []):
        if key not in instance:
            errors.append(f"{path}: missing required key {key!r}")

    properties = schema.get("properties", {})
    for key, value in instance.items():
        child_schema = properties.get(key)
        if child_schema is None:
            if schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected key {key!r}")
            continue
        _validate(value, child_schema, f"{path}.{key}", errors)


def _validate_array(instance: list[Any], schema: dict[str, Any], path: str, errors: list[str]) -> None:
    min_items = schema.get("minItems")
    max_items = schema.get("maxItems")
    if min_items is not None and len(instance) < min_items:
        errors.append(f"{path}: expected at least {min_items} items, got {len(instance)}")
    if max_items is not None and len(instance) > max_items:
        errors.append(f"{path}: expected at most {max_items} items, got {len(instance)}")

    item_schema = schema.get("items")
    if isinstance(item_schema, dict):
        for index, item in enumerate(instance):
            _validate(item, item_schema, f"{path}[{index}]", errors)


def _type_matches(instance: Any, schema_type: str | list[str]) -> bool:
    if isinstance(schema_type, list):
        return any(_type_matches(instance, item) for item in schema_type)
    if schema_type == "object":
        return isinstance(instance, dict)
    if schema_type == "array":
        return isinstance(instance, list)
    if schema_type == "string":
        return isinstance(instance, str)
    if schema_type == "boolean":
        return isinstance(instance, bool)
    if schema_type == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if schema_type == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if schema_type == "null":
        return instance is None
    return True
