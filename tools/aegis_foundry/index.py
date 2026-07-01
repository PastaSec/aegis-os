from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.aegis_foundry.manifest import list_values
from tools.aegis_foundry.pack import KnowledgePackPath
from tools.aegis_foundry.validate import split_front_matter


INDEX_FILENAME = "index.json"
INDEX_SCHEMA = "aegis.pack-index/1"
INDEX_GENERATOR = "AEGIS Foundry"


def _title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def document_entry(pack_path: Path, doc_path: Path) -> dict[str, Any]:
    """Build one lightweight index entry from a Markdown document."""
    relative = doc_path.relative_to(pack_path).as_posix()

    try:
        text = doc_path.read_text(encoding="utf-8")
    except Exception:
        text = ""

    metadata, _body, _error = split_front_matter(text)
    metadata = metadata or {}

    try:
        size = doc_path.stat().st_size
    except OSError:
        size = 0

    return {
        "title": str(metadata.get("title") or _title_from_path(doc_path)),
        "path": relative,
        "summary": str(metadata.get("summary") or ""),
        "category": str(metadata.get("category") or ""),
        "tags": list_values(metadata.get("tags")),
        "author": str(metadata.get("author") or ""),
        "revision": str(metadata.get("revision") or ""),
        "size": size,
    }


def build_index(pack: KnowledgePackPath) -> dict[str, Any]:
    """Build the full index structure for a Knowledge Pack.

    Documents follow ``pack.documents`` ordering (sorted recursive discovery),
    keeping Runtime document ordering deterministic.
    """
    documents = [document_entry(pack.path, doc) for doc in pack.documents]
    pack_id = pack.manifest.pack_id if pack.manifest else pack.path.name

    return {
        "schema": INDEX_SCHEMA,
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generator": INDEX_GENERATOR,
        "pack_id": pack_id,
        "document_count": len(documents),
        "documents": documents,
    }


def write_index(pack: KnowledgePackPath) -> Path:
    """Generate and write index.json to the pack root, returning its path."""
    index = build_index(pack)
    index_path = pack.path / INDEX_FILENAME
    index_path.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return index_path
