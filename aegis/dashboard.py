from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from aegis.monitor import get_system_state


class AegisDashboard(App):
    CSS = """
    Screen {
        background: black;
    }

    #main {
        padding: 1;
        height: 100%;
    }

    #title {
        text-style: bold;
        color: cyan;
        content-align: center middle;
        height: 1;
    }

    #status {
        margin-top: 1;
        text-style: bold;
        height: 1;
    }

    #stats {
        margin-top: 1;
        color: white;
    }

    #menu {
        margin-top: 1;
        color: green;
    }

    #hint {
        margin-top: 1;
        color: gray;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main"):
            yield Static("AEGIS OS", id="title")
            yield Static("", id="status")
            yield Static("", id="stats")
            yield Static("", id="menu")
            yield Static("Q Quit | R Refresh", id="hint")
        yield Footer()

    def on_mount(self) -> None:
        self.update_dashboard()
        self.set_interval(2, self.update_dashboard)

    def action_refresh(self) -> None:
        self.update_dashboard()

    def update_dashboard(self) -> None:
        state = get_system_state()

        status_color = {
            "READY": "green",
            "DEGRADED": "yellow",
            "HOT": "red",
            "UNKNOWN": "white",
        }.get(state.readiness, "white")

        self.query_one("#status", Static).update(
            f"[{status_color}]MISSION STATUS: {state.readiness}[/{status_color}]"
        )

        self.query_one("#stats", Static).update(
            f"Host   {state.host}\n"
            f"IP     {state.ip}\n"
            f"CPU    {state.cpu}\n"
            f"RAM    {state.memory}\n"
            f"Disk   {state.disk}\n"
            f"Temp   {state.temp}\n"
            f"Power  {state.power}\n"
            f"Up     {state.uptime}"
        )

        self.query_one("#menu", Static).update(
            "1 Knowledge\n"
            "2 Community\n"
            "3 Notes\n"
            "4 Network\n"
            "5 Hardware\n"
            "6 Settings"
        )


def run_dashboard() -> None:
    app = AegisDashboard()
    app.run()
