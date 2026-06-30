DEFAULT_FOOTER = "↑↓ Select  Enter Open  Esc Back  Q Quit"


def render_frame(
    title: str,
    status: str,
    body: str,
    footer: str = DEFAULT_FOOTER,
) -> str:
    return (
        f"[bold cyan]{title}[/bold cyan]\n"
        f"{status}\n"
        f"------------------------------\n"
        f"{body}\n"
        f"------------------------------\n"
        f"[dim]{footer}[/dim]"
    )

