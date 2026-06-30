from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tools.aegis_foundry.manifest import list_values
from tools.aegis_foundry.pack import DEFAULT_PACKS_DIR, KnowledgePackPath, resolve_path
from tools.aegis_foundry.validate import split_front_matter, validate_pack


SUPPORTED_SOURCE_SUFFIXES = {".md", ".markdown", ".txt"}
PACK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


@dataclass
class ImportedDocument:
    source: Path
    output: Path


@dataclass
class ImportResult:
    source: Path
    pack_path: Path
    dry_run: bool = False
    imported: list[ImportedDocument] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    validation: Any = None

    @property
    def has_errors(self) -> bool:
        return bool(self.errors) or bool(getattr(self.validation, "has_errors", False))


@dataclass
class ImportOptions:
    source: Path
    pack_id: str
    output: Path = DEFAULT_PACKS_DIR
    name: str = ""
    description: str = ""
    category: str = "General"
    tag: str = "imported"
    overwrite: bool = False
    dry_run: bool = False


def import_folder(options: ImportOptions) -> ImportResult:
    source = options.source.resolve()
    output_root = options.output.resolve()
    pack_path = (output_root / options.pack_id).resolve()
    result = ImportResult(source=source, pack_path=pack_path, dry_run=options.dry_run)

    validate_import_options(options, source, output_root, pack_path, result)
    if result.errors:
        return result

    sources = discover_sources(source)
    if not sources:
        result.errors.append(f"No supported source files found under {source}")
        return result

    output_paths = planned_output_paths(source, pack_path / "docs", sources)
    for source_file, output_file in zip(sources, output_paths):
        result.imported.append(ImportedDocument(source=source_file, output=output_file))

    if options.dry_run:
        return result

    if pack_path.exists() and options.overwrite:
        shutil.rmtree(pack_path)

    write_pack(options, pack_path, source, sources, output_paths)
    result.validation = validate_pack(KnowledgePackPath(path=pack_path))
    return result


def validate_import_options(
    options: ImportOptions,
    source: Path,
    output_root: Path,
    pack_path: Path,
    result: ImportResult,
) -> None:
    if not source.exists():
        result.errors.append(f"Source path does not exist: {source}")
    elif not source.is_dir():
        result.errors.append(f"Source path must be a directory: {source}")

    if not PACK_ID_PATTERN.match(options.pack_id):
        result.errors.append("Pack id must use lowercase letters, numbers, hyphen, or underscore")

    try:
        pack_path.relative_to(output_root)
    except ValueError:
        result.errors.append(f"Output pack path must stay inside output root: {output_root}")

    if pack_path.exists() and not options.overwrite and not options.dry_run:
        result.errors.append(f"Output pack already exists: {pack_path}")


def discover_sources(source: Path) -> list[Path]:
    files = []
    for path in source.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SOURCE_SUFFIXES:
            files.append(path)
    return sorted(files)


def planned_output_paths(source_root: Path, docs_root: Path, sources: list[Path]) -> list[Path]:
    used: set[Path] = set()
    outputs = []

    for source in sources:
        relative = source.relative_to(source_root)
        output = docs_root / relative.with_suffix(".md")
        output = unique_path(output, used)
        used.add(output)
        outputs.append(output)

    return outputs


def unique_path(path: Path, used: set[Path]) -> Path:
    candidate = path
    index = 2
    while candidate in used:
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        index += 1
    return candidate


def write_pack(
    options: ImportOptions,
    pack_path: Path,
    source_root: Path,
    sources: list[Path],
    output_paths: list[Path],
) -> None:
    docs_root = pack_path / "docs"
    docs_root.mkdir(parents=True, exist_ok=True)
    write_manifest(pack_path / "manifest.yaml", options)

    for source, output in zip(sources, output_paths):
        output.parent.mkdir(parents=True, exist_ok=True)
        relative_source = source.relative_to(source_root).as_posix()
        output.write_text(render_document(source, relative_source, options), encoding="utf-8")


def write_manifest(path: Path, options: ImportOptions) -> None:
    name = options.name or title_from_slug(options.pack_id)
    description = options.description or f"Imported Knowledge Pack from {options.source.name}."
    text = (
        f"name: {name}\n"
        f"id: {options.pack_id}\n"
        "version: 0.1.0\n"
        "icon: KP\n"
        f"description: {description}\n"
        "categories:\n"
        f"  - {options.category}\n"
        "tags:\n"
        f"  - {options.tag}\n"
    )
    path.write_text(text, encoding="utf-8")


def render_document(source: Path, relative_source: str, options: ImportOptions) -> str:
    text = source.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    if source.suffix.lower() in {".md", ".markdown"}:
        return render_markdown_document(source, relative_source, text, options)
    return render_text_document(source, relative_source, text, options)


def render_markdown_document(source: Path, relative_source: str, text: str, options: ImportOptions) -> str:
    metadata, body, error = split_front_matter(text)
    if metadata is not None and error is None:
        merged = default_metadata(source, relative_source, options)
        merged.update(metadata)
        return front_matter(merged) + provenance_comment(relative_source) + ensure_heading(body, merged["title"])

    metadata = default_metadata(source, relative_source, options)
    return front_matter(metadata) + provenance_comment(relative_source) + ensure_heading(text, metadata["title"])


def render_text_document(source: Path, relative_source: str, text: str, options: ImportOptions) -> str:
    metadata = default_metadata(source, relative_source, options)
    return front_matter(metadata) + provenance_comment(relative_source) + ensure_heading(text, metadata["title"])


def default_metadata(source: Path, relative_source: str, options: ImportOptions) -> dict[str, object]:
    return {
        "title": title_from_slug(source.stem),
        "category": options.category,
        "tags": [options.tag],
        "summary": f"Imported from {relative_source}.",
    }


def front_matter(metadata: dict[str, object]) -> str:
    lines = ["---"]
    for key in ("title", "category", "tags", "author", "revision", "summary"):
        if key not in metadata:
            continue
        value = metadata[key]
        if key == "tags":
            values = list_values(value)
            if values:
                lines.append("tags:")
                for item in values:
                    lines.append(f"  - {item}")
            continue
        if value is not None and str(value).strip():
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def provenance_comment(relative_source: str) -> str:
    return f"<!-- Imported by AEGIS Foundry. Source: {relative_source} -->\n\n"


def ensure_heading(text: str, title: str) -> str:
    body = text.strip()
    if not body:
        return f"# {title}\n"
    if body.lstrip().startswith("#"):
        return body + "\n"
    return f"# {title}\n\n{body}\n"


def title_from_slug(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").title()


def options_from_args(args: Any) -> ImportOptions:
    return ImportOptions(
        source=resolve_path(args.source),
        pack_id=args.pack_id,
        output=resolve_path(args.output),
        name=args.name or "",
        description=args.description or "",
        category=args.category,
        tag=args.tag,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )
