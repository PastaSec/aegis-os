from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aegis.knowledge import Document, KnowledgePack, title_from_path


@dataclass(frozen=True)
class NavigatorEntry:
    label: str
    path: Path
    kind: str
    document: Document | None = None

    @property
    def is_folder(self) -> bool:
        return self.kind == "folder"


def docs_root(pack: KnowledgePack) -> Path:
    return pack.path / "docs"


def root_path(pack: KnowledgePack | None) -> Path | None:
    if not pack:
        return None
    return docs_root(pack)


def parent_path(pack: KnowledgePack, current_path: Path) -> Path:
    root = docs_root(pack)
    if current_path == root:
        return root
    parent = current_path.parent
    try:
        parent.relative_to(root)
    except ValueError:
        return root
    return parent


def relative_label(root: Path, current_path: Path) -> str:
    if current_path == root:
        return "Documents"
    return current_path.relative_to(root).as_posix()


def navigator_entries(pack: KnowledgePack | None, current_path: Path | None) -> list[NavigatorEntry]:
    if not pack:
        return []

    root = docs_root(pack)
    current = current_path or root
    if not current.exists() or not current.is_dir():
        current = root

    folders = folder_entries(current)
    documents = document_entries(pack.documents, current)
    return folders + documents


def folder_entries(current_path: Path) -> list[NavigatorEntry]:
    entries = []
    for child in sorted(current_path.iterdir()):
        if child.is_dir() and any(child.rglob("*.md")):
            entries.append(NavigatorEntry(label=f"[DIR] {title_from_path(child)}", path=child, kind="folder"))
    return entries


def document_entries(documents: list[Document], current_path: Path) -> list[NavigatorEntry]:
    entries = []
    for document in documents:
        if document.path.parent == current_path:
            entries.append(
                NavigatorEntry(
                    label=document.title,
                    path=document.path,
                    kind="document",
                    document=document,
                )
            )
    return sorted(entries, key=lambda entry: entry.label.lower())
