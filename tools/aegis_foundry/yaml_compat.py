from __future__ import annotations

from typing import Any


def safe_load(text: str) -> Any:
    try:
        import yaml

        return yaml.safe_load(text)
    except ModuleNotFoundError:
        return parse_simple_yaml(text)


def parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        stripped = raw_line.strip()
        if stripped.startswith("- "):
            if current_list is None:
                raise ValueError(f"list item without key on line {line_number}")
            data[current_list].append(parse_scalar(stripped[2:].strip()))
            continue

        if raw_line.startswith(" ") and current_list is None:
            raise ValueError(f"unsupported indentation on line {line_number}")

        if ":" not in stripped:
            raise ValueError(f"expected key/value pair on line {line_number}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"empty key on line {line_number}")

        if value:
            data[key] = parse_scalar(value)
            current_list = None
        else:
            data[key] = []
            current_list = key

    return data


def parse_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
