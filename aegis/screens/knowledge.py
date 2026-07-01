from pathlib import Path
from typing import Protocol

from aegis.knowledge import KnowledgePack, read_document
from aegis.models.knowledge_navigator import NavigatorEntry, relative_label, root_path
from aegis.models.document_viewer import DEFAULT_DOCUMENT_HEIGHT
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox
from aegis.widgets.markdown import render_markdown_lines
from aegis.widgets.viewer import render_document_view


DOCUMENT_FOOTER = "↑↓ Scroll  PgUp/PgDn Page  Home/End Jump  F Favorite  Esc Back  Q Quit"
PACK_DETAILS_FOOTER = "Enter Browse Documents  Esc Back  Q Quit"


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


def render_pack_screen(
    pack: KnowledgePack | None,
    entries: list[NavigatorEntry],
    selected: int,
    current_path: Path | None = None,
) -> str:
    items = [entry.label for entry in entries]
    title = pack.name if pack else "Pack"
    root = root_path(pack)
    subtitle = relative_label(root, current_path) if root and current_path else "Documents"
    return render_frame(title, subtitle, render_listbox(items, selected))


def _field_line(label: str, value: str) -> list[str]:
    if not value:
        return []
    return [f"{label:<10} {value}"]


def _pack_title(icon: str, name: str) -> str:
    icon = icon.strip()
    name = name.strip()
    if not icon:
        return name
    icon_lower = icon.lower()
    name_lower = name.lower()
    if name_lower == icon_lower or name_lower.startswith(icon_lower + " "):
        return name
    return f"{icon} {name}"


def render_pack_details_screen(pack: KnowledgePack | None) -> str:
    if not pack:
        return render_frame("Pack", "Documents: 0", "  No pack selected", PACK_DETAILS_FOOTER)

    title = _pack_title(pack.icon, pack.name)
    doc_count = len(pack.documents)

    lines: list[str] = []
    lines += _field_line("Status", pack.status)
    lines += _field_line("Version", pack.version)
    lines += _field_line("Documents", str(doc_count))

    if pack.description:
        if lines:
            lines.append("")
        lines.append(pack.description)

    identity = []
    identity += _field_line("Categories", ", ".join(pack.categories))
    identity += _field_line("Tags", ", ".join(pack.tags))
    if identity:
        lines.append("")
        lines += identity

    provenance = []
    provenance += _field_line("Source", pack.source)
    provenance += _field_line("License", pack.license)
    provenance += _field_line("Author", pack.author)
    provenance += _field_line("Homepage", pack.homepage)
    if provenance:
        lines.append("")
        lines += provenance

    body = "\n".join(lines) if lines else "  No pack details available"
    return render_frame(title, f"Documents: {doc_count}", body, PACK_DETAILS_FOOTER)


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
