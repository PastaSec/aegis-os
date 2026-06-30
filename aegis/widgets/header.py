from aegis.themes.field import FIELD_THEME, FieldTheme


def render_header(title: str, *, theme: FieldTheme = FIELD_THEME) -> str:
    return theme.title(title)

