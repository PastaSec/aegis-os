from aegis.knowledge import Document
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox


def document_label(document: Document) -> str:
    if document.pack:
        return f"{document.pack}: {document.title}"
    return document.title


def render_operator_documents_screen(title: str, documents: list[Document], selected: int) -> str:
    items = [document_label(document) for document in documents]
    return render_frame(title, f"Documents: {len(items)}", render_listbox(items, selected))
