from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tools.aegis_foundry.manifest import LIST_FIELDS, REQUIRED_FIELDS, Manifest, list_values, load_manifest
from tools.aegis_foundry.pack import KnowledgePackPath, discover_packs, resolve_path
from tools.aegis_foundry.yaml_compat import safe_load


SUPPORTED_FRONT_MATTER_FIELDS = {
    "title",
    "category",
    "tags",
    "author",
    "revision",
    "summary",
    "source",
    "source_url",
    "imported_by",
    "import_date",
}
ALLOWED_PACK_STATUSES = {"experimental", "curated", "validated", "official"}
CURATED_PACK_STATUSES = {"curated", "validated", "official"}


@dataclass
class ValidationIssue:
    level: str
    path: Path
    message: str

    def render(self) -> str:
        return f"{self.level}: {self.path}: {self.message}"


@dataclass
class ValidationReport:
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def error(self, path: Path, message: str) -> None:
        self.errors.append(ValidationIssue("ERROR", path, message))

    def warning(self, path: Path, message: str) -> None:
        self.warnings.append(ValidationIssue("WARNING", path, message))

    def extend(self, other: "ValidationReport") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    def render(self) -> str:
        lines = []
        for issue in self.errors + self.warnings:
            lines.append(issue.render())
        lines.append(f"Summary: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        return "\n".join(lines)


def split_front_matter(text: str) -> tuple[dict[str, Any] | None, str, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            raw_metadata = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            if text.endswith("\n"):
                body += "\n"
            try:
                metadata = safe_load(raw_metadata) or {}
            except Exception as exc:
                return None, text, f"front matter could not be parsed: {exc}"
            if not isinstance(metadata, dict):
                return None, text, "front matter must be a mapping"
            return metadata, body, None

    return None, text, "front matter start marker has no closing marker"


def validate_manifest(path: Path, pack_dir: Path, report: ValidationReport) -> Manifest | None:
    if not path.exists():
        report.error(path, "manifest.yaml is required")
        return None

    try:
        manifest = load_manifest(path)
    except ValueError as exc:
        report.error(path, str(exc))
        return None

    for field_name in REQUIRED_FIELDS:
        if not str(manifest.data.get(field_name) or "").strip():
            report.error(path, f"required field missing or empty: {field_name}")

    for field_name in LIST_FIELDS:
        value = manifest.data.get(field_name)
        if value is not None and not isinstance(value, list):
            report.warning(path, f"{field_name} should be a list")

    icon = manifest.data.get("icon")
    if icon is not None and not isinstance(icon, str):
        report.warning(path, "icon should be a string")

    status = str(manifest.data.get("status") or "").strip()
    if status and status not in ALLOWED_PACK_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_PACK_STATUSES))
        report.warning(path, f"status should be one of: {allowed}")

    license_value = manifest.data.get("license")
    if license_value is not None and not isinstance(license_value, str):
        report.warning(path, "license should be a string")

    if manifest.pack_id and manifest.pack_id != pack_dir.name:
        report.warning(path, f"id '{manifest.pack_id}' does not match directory '{pack_dir.name}'")

    return manifest


def validate_document(path: Path, report: ValidationReport) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        report.error(path, f"document could not be read: {exc}")
        return

    if not text.strip():
        report.warning(path, "document is empty")
        return

    metadata, body, error = split_front_matter(text)
    if error:
        report.warning(path, error)
        return

    if metadata is None:
        return

    for key in metadata:
        if key not in SUPPORTED_FRONT_MATTER_FIELDS:
            report.warning(path, f"unsupported front matter field: {key}")

    tags = metadata.get("tags")
    if tags is not None and not isinstance(tags, (list, str)):
        report.warning(path, "tags should be a list or comma-separated string")

    if not body.strip():
        report.warning(path, "document body is empty after front matter")


def validate_pack(pack: KnowledgePackPath) -> ValidationReport:
    report = ValidationReport()
    manifest = validate_manifest(pack.path / "manifest.yaml", pack.path, report)
    pack.manifest = manifest

    if not pack.docs_dir.exists():
        report.error(pack.docs_dir, "docs directory is required")
        return report

    documents = pack.documents
    if not documents:
        report.error(pack.docs_dir, "at least one Markdown document is required")
        return report

    if manifest and manifest.status in CURATED_PACK_STATUSES and not (pack.path / "README.md").exists():
        report.warning(pack.path / "README.md", "README.md is recommended for curated Knowledge Packs")

    for document in documents:
        validate_document(document, report)

    validate_index(pack, report)

    return report


def validate_index(pack: KnowledgePackPath, report: ValidationReport) -> None:
    """Verify a generated index.json. All findings are warnings (non-fatal)."""
    # Imported lazily: index.py imports from this module.
    from tools.aegis_foundry.index import INDEX_FILENAME, INDEX_SCHEMA, build_index

    index_path = pack.path / INDEX_FILENAME
    if not index_path.exists():
        report.warning(index_path, "index.json is missing; run generate-index to create it")
        return

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as exc:
        report.warning(index_path, f"index.json could not be parsed: {exc}")
        return

    if not isinstance(data, dict):
        report.warning(index_path, "index.json root must be an object")
        return

    if data.get("schema") != INDEX_SCHEMA:
        report.warning(index_path, f"index.json schema should be '{INDEX_SCHEMA}'")

    entries = data.get("documents")
    if not isinstance(entries, list):
        report.warning(index_path, "index.json documents must be a list")
        return

    expected = {entry["path"]: entry for entry in build_index(pack)["documents"]}
    seen: set[str] = set()

    for entry in entries:
        if not isinstance(entry, dict):
            report.warning(index_path, "index entry must be an object")
            continue

        relative = str(entry.get("path") or "").strip()
        if not relative:
            report.warning(index_path, "index entry is missing a path")
            continue

        seen.add(relative)
        if relative not in expected:
            report.warning(index_path, f"indexed document missing on disk: {relative}")
            continue

        reference = expected[relative]
        for field_name in ("title", "summary", "category", "author", "revision"):
            if str(entry.get(field_name) or "") != str(reference.get(field_name) or ""):
                report.warning(index_path, f"index {field_name} mismatch for {relative}")
        if list_values(entry.get("tags")) != reference.get("tags"):
            report.warning(index_path, f"index tags mismatch for {relative}")

    for relative in expected:
        if relative not in seen:
            report.warning(index_path, f"document not represented in index: {relative}")


def validate_path(path: str | Path | None = None) -> ValidationReport:
    target = resolve_path(path)
    report = ValidationReport()

    if not target.exists():
        report.error(target, "path does not exist")
        return report

    packs = discover_packs(target)
    if not packs:
        report.error(target, "no Knowledge Packs found")
        return report

    for pack in packs:
        report.extend(validate_pack(pack))

    return report
