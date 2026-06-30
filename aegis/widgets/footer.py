from aegis.themes.field import FIELD_THEME, FieldTheme


def render_footer(text: str, *, theme: FieldTheme = FIELD_THEME) -> str:
    return theme.footer(text)

