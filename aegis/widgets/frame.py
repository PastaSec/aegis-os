from aegis.themes.field import FIELD_THEME, FieldTheme
from aegis.widgets.footer import render_footer
from aegis.widgets.header import render_header
from aegis.widgets.status import render_status


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
        f"{render_header(title, theme=theme)}\n"
        f"{render_status(status, theme=theme)}\n"
        f"{theme.divider}\n"
        f"{body}\n"
        f"{theme.divider}\n"
        f"{render_footer(footer, theme=theme)}"
    )
