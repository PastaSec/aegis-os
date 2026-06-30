from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aegis.knowledge import ROOT, Document, load_document


OPERATOR_STATE_PATH = ROOT / "state" / "operator.json"
RECENT_LIMIT = 20


@dataclass
class DocumentRef:
    title: str
    path: str
    pack: str = ""


@dataclass
class OperatorState:
    recent: list[DocumentRef] = field(default_factory=list)
    favorites: list[DocumentRef] = field(default_factory=list)
    positions: dict[str, int] = field(default_factory=dict)


def document_key(path: Path | str) -> str:
    candidate = Path(path)
    try:
        candidate = candidate.resolve()
    except Exception:
        pass

    try:
        value = candidate.relative_to(ROOT.resolve())
    except Exception:
        value = candidate

    return value.as_posix()


def document_ref(document: Any) -> DocumentRef:
    path = getattr(document, "path", "")
    return DocumentRef(
        title=str(getattr(document, "title", "") or Path(path).stem),
        path=document_key(path),
        pack=str(getattr(document, "pack", "") or ""),
    )


def _ref_from_json(value: object) -> DocumentRef | None:
    if not isinstance(value, dict):
        return None

    path = str(value.get("path") or "").strip()
    if not path:
        return None

    return DocumentRef(
        title=str(value.get("title") or Path(path).stem),
        path=path.replace("\\", "/"),
        pack=str(value.get("pack") or ""),
    )


def _refs_from_json(value: object) -> list[DocumentRef]:
    if not isinstance(value, list):
        return []

    refs = []
    seen = set()
    for item in value:
        ref = _ref_from_json(item)
        if ref and ref.path not in seen:
            refs.append(ref)
            seen.add(ref.path)
    return refs


def load_operator_state(path: Path = OPERATOR_STATE_PATH) -> OperatorState:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return OperatorState()

    if not isinstance(data, dict):
        return OperatorState()

    positions = {}
    raw_positions = data.get("positions")
    if isinstance(raw_positions, dict):
        for key, value in raw_positions.items():
            try:
                positions[str(key).replace("\\", "/")] = max(int(value), 0)
            except Exception:
                continue

    return OperatorState(
        recent=_refs_from_json(data.get("recent")),
        favorites=_refs_from_json(data.get("favorites")),
        positions=positions,
    )


def save_operator_state(state: OperatorState, path: Path = OPERATOR_STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "recent": [ref.__dict__ for ref in state.recent],
        "favorites": [ref.__dict__ for ref in state.favorites],
        "positions": state.positions,
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def record_recent(state: OperatorState, document: Any, limit: int = RECENT_LIMIT) -> None:
    ref = document_ref(document)
    state.recent = [item for item in state.recent if item.path != ref.path]
    state.recent.insert(0, ref)
    del state.recent[limit:]


def is_favorite(state: OperatorState, document: Any) -> bool:
    key = document_key(getattr(document, "path", document))
    return any(ref.path == key for ref in state.favorites)


def toggle_favorite(state: OperatorState, document: Any) -> bool:
    ref = document_ref(document)
    for index, item in enumerate(state.favorites):
        if item.path == ref.path:
            del state.favorites[index]
            return False

    state.favorites.append(ref)
    return True


def get_position(state: OperatorState, document: Any) -> int:
    key = document_key(getattr(document, "path", document))
    return state.positions.get(key, 0)


def set_position(state: OperatorState, document: Any, offset: int) -> None:
    key = document_key(getattr(document, "path", document))
    state.positions[key] = max(int(offset), 0)


def path_from_ref(ref: DocumentRef) -> Path:
    path = Path(ref.path)
    if path.is_absolute():
        return path
    return ROOT / path


def resolve_document_ref(ref: DocumentRef) -> Document | None:
    path = path_from_ref(ref)
    if not path.exists():
        return None
    return load_document(path, ref.pack)


def resolve_document_refs(refs: list[DocumentRef]) -> list[Document]:
    documents = []
    for ref in refs:
        document = resolve_document_ref(ref)
        if document:
            documents.append(document)
    return documents
