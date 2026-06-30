from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tools.aegis_foundry.yaml_compat import safe_load


REQUIRED_FIELDS = ("name", "id", "version", "description")
LIST_FIELDS = ("categories", "tags")


@dataclass
class Manifest:
    path: Path
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return str(self.data.get("name") or "")

    @property
    def pack_id(self) -> str:
        return str(self.data.get("id") or "")

    @property
    def version(self) -> str:
        return str(self.data.get("version") or "")

    @property
    def description(self) -> str:
        return str(self.data.get("description") or "")

    @property
    def icon(self) -> str:
        return str(self.data.get("icon") or "")

    @property
    def categories(self) -> list[str]:
        return list_values(self.data.get("categories"))

    @property
    def tags(self) -> list[str]:
        return list_values(self.data.get("tags"))


def list_values(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def load_manifest(path: Path) -> Manifest:
    try:
        data = safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise ValueError(f"could not read manifest: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")

    return Manifest(path=path, data=data)
