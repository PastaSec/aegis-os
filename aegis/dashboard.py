from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static

from aegis.monitor import get_system_state


MENU_ITEMS = [
    "Knowledge",
    "Community",
    "Notes",
    "Network",
    "Hardware",
    "Settings",
]


class AegisDashboard(App):
    CSS = """
    Screen {
        background: black;
    }

    #main {
        padding: 0 1;
        height: 100%;
    }

    #title {
        text-style: bold;
        color: cyan;
        height: 1;
    }

    #status {
        text-style: bold;
        height: 1;
    }

    #stats {
        color: white;
        height: auto;
    }

    #menu {
        color: green;
        height: auto;
    }

    #message {
        color: yellow;
        height: 1;
    }

    #hint {
        color: gray;
        height: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("up,k", "cursor_up", "Up"),
        ("down,j", "cursor_down", "Down"),
        ("enter", "select", "Select"),
        ("1", "choose_1", "Knowledge"),
        ("2", "choose_2", "Community"),
        ("3", "choose_3", "Notes"),
        ("4", "choose_4", "Network"),
        ("5", "choose_5", "Hardware"),
        ("6", "choose_6", "Settings"),
    ]

    selected_index = 0

    def compose(self) -> ComposeResult:
        with Container(id="main"):
            yield Static("AEGIS OS", id="title")
            yield Static("", id="status")
            yield Static("", id="stats")
            yield Static("", id="menu")
            yield Static("", id="message")
            yield Static("↑↓ Select | Enter Open | Q Quit", id="hint")

    def on_mount(self) -> None:
        self.update_dashboard()
        self.set_interval(2, self.update_dashboard)

    def action_refresh(self) -> None:
        self.update_dashboard()

    def action_cursor_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(MENU_ITEMS)
        self.update_dashboard()

    def action_cursor_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(MENU_ITEMS)
        self.update_dashboard()

    def action_select(self) -> None:
        item = MENU_ITEMS[self.selected_index]
        self.query_one("#message", Static).update(f"{item} module not built yet")

    def _choose(self, index: int) -> None:
        self.selected_index = index
        self.action_select()
        self.update_dashboard()

    def action_choose_1(self) -> None:
        self._choose(0)

    def action_choose_2(self) -> None:
        self._choose(1)

    def action_choose_3(self) -> None:
        self._choose(2)

    def action_choose_4(self) -> None:
        self._choose(3)

    def action_choose_5(self) -> None:
        self._choose(4)

    def action_choose_6(self) -> None:
        self._choose(5)

    def update_dashboard(self) -> None:
        state = get_system_state()

        status_color = {
            "READY": "green",
            "DEGRADED": "yellow",
            "HOT": "red",
            "UNKNOWN": "white",
        }.get(state.readiness, "white")

        self.query_one("#status", Static).update(
            f"[{status_color}]STATUS {state.readiness}[/{status_color}]"
        )

        self.query_one("#stats", Static).update(
            f"Host {state.host}\n"
            f"IP   {state.ip}\n"
            f"CPU  {state.cpu}  RAM {state.memory}\n"
            f"Disk {state.disk}  Temp {state.temp}\n"
            f"Pwr  {state.power}\n"
            f"Up   {state.uptime}"
        )

        lines = []
        for i, item in enumerate(MENU_ITEMS):
            prefix = ">" if i == self.selected_index else " "
            lines.append(f"{prefix} {i + 1} {item}")

        self.query_one("#menu", Static).update("\n".join(lines))


def run_dashboard() -> None:
    app = AegisDashboard()
    app.run()
