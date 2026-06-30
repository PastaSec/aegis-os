from aegis.widgets.markdown import render_markdown_preview


def render_preview(text: str, lines: int = 13) -> str:
    return render_markdown_preview(text, lines)
