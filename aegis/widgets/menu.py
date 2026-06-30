def render_menu(items: list[str], selected: int, limit: int = 8) -> str:
    if not items:
        return "  None found"

    lines = []
    for index, item in enumerate(items[:limit]):
        pointer = ">" if index == selected else " "
        lines.append(f"{pointer} {item}")
    return "\n".join(lines)

