from pathlib import Path
from typing import Protocol

from aegis.knowledge import KnowledgePack, read_document
from aegis.models.document_viewer import DEFAULT_DOCUMENT_HEIGHT
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox
from aegis.widgets.markdown import render_markdown_lines
from aegis.widgets.viewer import render_document_view


DOCUMENT_FOOTER = "↑↓ Scroll  PgUp/PgDn Page  Home/End Jump  F Favorite  Esc Back  Q Quit"


class DocumentLike(Protocol):
    title: str
    path: Path
    tags: list[str]
    author: str
    revision: str
    summary: str


def metadata_lines(document: DocumentLike | None) -> list[str]:
    if not document:
        return []

    lines = []
    if getattr(document, "author", ""):
        lines.append(document.author)
    if getattr(document, "revision", ""):
        lines.append(f"Revision {document.revision}")
    if getattr(document, "summary", ""):
        lines.append(document.summary)
    tags = getattr(document, "tags", [])
    if tags:
        lines.append("Tags: " + " ".join(tags))
    if lines:
        lines.append("------------------------------")
    return lines


def render_knowledge_screen(packs: list[KnowledgePack], selected: int) -> str:
    items = [f"{pack.icon} {pack.name}".strip() for pack in packs]
    return render_frame("Knowledge", f"Packs: {len(items)}", render_listbox(items, selected))


def render_pack_screen(pack: KnowledgePack | None, selected: int) -> str:
    docs = pack.documents if pack else []
    items = [doc.title for doc in docs]
    title = pack.name if pack else "Pack"
    return render_frame(title, "Documents", render_listbox(items, selected))


def render_document_screen(
    document: DocumentLike | None,
    offset: int = 0,
    height: int = DEFAULT_DOCUMENT_HEIGHT,
) -> str:
    title = document.title if document else "Document"
    text = read_document(document.path) if document else "No document selected"
    metadata = metadata_lines(document)
    if metadata:
        text = "\n".join(metadata) + "\n\n" + text
    body, status, _ = render_document_view(text, offset, height)
    return render_frame(title, status, body, DOCUMENT_FOOTER)


def document_line_count(document: DocumentLike | None) -> int:
    text = read_document(document.path) if document else "No document selected"
    metadata = metadata_lines(document)
    if metadata:
        text = "\n".join(metadata) + "\n\n" + text
    return len(render_markdown_lines(text))
