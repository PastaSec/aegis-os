from aegis.themes.field import FIELD_THEME, FieldTheme


def render_listbox(
    items: list[str],
    selected: int,
    limit: int = 8,
    *,
    theme: FieldTheme = FIELD_THEME,
) -> str:
    if not items:
        return theme.empty_menu

    lines = []
    for index, item in enumerate(items[:limit]):
        pointer = theme.selection(index == selected)
        lines.append(f"{pointer} {item}")
    return "\n".join(lines)

