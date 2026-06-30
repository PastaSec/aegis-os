from aegis.state import SystemState
from aegis.widgets.frame import render_frame
from aegis.widgets.menu import render_menu


def render_home_screen(state: SystemState, items: list[str], selected: int) -> str:
    body = (
        f"Mission Ready\n"
        f"{state.ip}\n\n"
        f"{render_menu(items, selected)}"
    )
    return render_frame("AEGIS OS", f"[bold green]STATUS {state.readiness}[/bold green]", body, "↑↓ Select  Enter Open  / Search  Q Quit")

