def render_markdown_preview(text: str, lines: int = 13) -> str:
    return "\n".join(text.splitlines()[:lines])

