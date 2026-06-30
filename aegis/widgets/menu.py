from aegis.themes.field import FIELD_THEME, FieldTheme
from aegis.widgets.listbox import render_listbox


def render_menu(
    items: list[str],
    selected: int,
    limit: int = 8,
    *,
    theme: FieldTheme = FIELD_THEME,
) -> str:
    return render_listbox(items, selected, limit, theme=theme)
