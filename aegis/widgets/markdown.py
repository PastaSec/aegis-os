def escape_markup(text: str) -> str:
    return text.replace("[", r"\[")


def _is_horizontal_rule(line: str) -> bool:
    stripped = line.strip()
    return stripped in {"---", "***", "___"}


def _is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def _render_table_line(line: str) -> str:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return " | ".join(cells)


def _render_markdown_line(line: str, in_code: bool) -> tuple[str | None, bool]:
    stripped = line.strip()

    if stripped.startswith("```"):
        return None, not in_code

    if in_code:
        return escape_markup(line), in_code

    if stripped.startswith("!["):
        return escape_markup("[Image omitted]"), in_code

    if stripped.startswith("#"):
        heading = stripped.lstrip("#").strip()
        return escape_markup(heading), in_code

    if stripped.startswith(">"):
        return escape_markup(f"| {stripped[1:].strip()}"), in_code

    if _is_horizontal_rule(line):
        return "------------------------------", in_code

    if _is_table_line(line):
        return escape_markup(_render_table_line(line)), in_code

    return escape_markup(line.replace("`", "")), in_code


def render_markdown_lines(text: str) -> list[str]:
    rendered: list[str] = []
    in_code = False

    for line in text.splitlines():
        rendered_line, in_code = _render_markdown_line(line, in_code)
        if rendered_line is not None:
            rendered.append(rendered_line)

    return rendered


def render_markdown_window(text: str, offset: int = 0, lines: int = 13) -> tuple[list[str], int, int]:
    rendered = render_markdown_lines(text)
    total = len(rendered)
    start = max(0, min(offset, max(total - lines, 0)))
    return rendered[start : start + lines], start, total


def render_markdown_preview(text: str, lines: int = 13) -> str:
    visible, _, _ = render_markdown_window(text, 0, lines)
    return "\n".join(visible)
