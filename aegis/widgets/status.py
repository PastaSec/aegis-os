from aegis.themes.field import FIELD_THEME, FieldTheme


def render_status(text: str, *, theme: FieldTheme = FIELD_THEME) -> str:
    return theme.status(text)

