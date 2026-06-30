from pathlib import Path
from typing import Protocol

from aegis.knowledge import KnowledgePack, read_document
from aegis.widgets.frame import render_frame
from aegis.widgets.menu import render_menu
from aegis.widgets.viewer import render_preview


class DocumentLike(Protocol):
    title: str
    path: Path


def render_knowledge_screen(packs: list[KnowledgePack], selected: int) -> str:
    items = [f"{pack.icon} {pack.name}".strip() for pack in packs]
    return render_frame("Knowledge", f"Packs: {len(items)}", render_menu(items, selected))


def render_pack_screen(pack: KnowledgePack | None, selected: int) -> str:
    docs = pack.documents if pack else []
    items = [doc.title for doc in docs]
    title = pack.name if pack else "Pack"
    return render_frame(title, "Documents", render_menu(items, selected))


def render_document_screen(document: DocumentLike | None) -> str:
    title = document.title if document else "Document"
    text = read_document(document.path) if document else "No document selected"
    preview = render_preview(text)
    return render_frame(title, "Viewer", preview)

