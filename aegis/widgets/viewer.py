from aegis.models.document_viewer import DEFAULT_DOCUMENT_HEIGHT, current_line
from aegis.widgets.markdown import render_markdown_preview
from aegis.widgets.markdown import render_markdown_window


def render_preview(text: str, lines: int = 13) -> str:
    return render_markdown_preview(text, lines)


def render_document_view(text: str, offset: int = 0, height: int = DEFAULT_DOCUMENT_HEIGHT) -> tuple[str, str, int]:
    lines, start, total = render_markdown_window(text, offset, height)
    body = "\n".join(lines)
    status = f"Viewer\nLine {current_line(start, total)} / {total}"
    return body, status, start
