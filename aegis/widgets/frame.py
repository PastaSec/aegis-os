from aegis.themes.field import FIELD_THEME, FieldTheme


DEFAULT_FOOTER = "↑↓ Select  Enter Open  Esc Back  Q Quit"


def render_frame(
    title: str,
    status: str,
    body: str,
    footer: str = DEFAULT_FOOTER,
    *,
    theme: FieldTheme = FIELD_THEME,
) -> str:
    return (
        f"{theme.title(title)}\n"
        f"{theme.status(status)}\n"
        f"{theme.divider}\n"
        f"{body}\n"
        f"{theme.divider}\n"
        f"{theme.footer(footer)}"
    )
