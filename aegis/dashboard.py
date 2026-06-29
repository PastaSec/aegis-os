from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static

from aegis.knowledge import load_packs, read_document
from aegis.monitor import get_system_state


HOME_ITEMS = [
    "Knowledge",
    "Community",
    "Notes",
    "Network",
    "Hardware",
    "Settings",
]


class AegisDashboard(App):
    CSS = """
    Screen { background: black; }
    #main { padding: 0 1; height: 100%; }
    #title { text-style: bold; color: cyan; height: 1; }
    #status { text-style: bold; height: 1; }
    #body { color: white; height: auto; }
    #menu { color: green; height: auto; }
    #message { color: yellow; height: 1; }
    #hint { color: gray; height: 1; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "back", "Back"),
        ("r", "refresh", "Refresh"),
        ("up,k", "cursor_up", "Up"),
        ("down,j", "cursor_down", "Down"),
        ("enter", "select", "Select"),
        ("1", "choose_1", "One"),
        ("2", "choose_2", "Two"),
        ("3", "choose_3", "Three"),
        ("4", "choose_4", "Four"),
        ("5", "choose_5", "Five"),
        ("6", "choose_6", "Six"),
    ]

    def __init__(self):
        super().__init__()
        self.screen_name = "home"
        self.selected_index = 0
        self.packs = []
        self.current_pack = None
        self.current_doc = None

    def compose(self) -> ComposeResult:
        with Container(id="main"):
            yield Static("AEGIS OS", id="title")
            yield Static("", id="status")
            yield Static("", id="body")
            yield Static("", id="menu")
            yield Static("", id="message")
            yield Static("↑↓ Move | Enter Open | Esc Back | Q Quit", id="hint")

    def on_mount(self) -> None:
        self.packs = load_packs()
        self.update_screen()
        self.set_interval(2, self.periodic_update)

    def periodic_update(self) -> None:
        if self.screen_name == "home":
            self.update_screen()

    def action_refresh(self) -> None:
        self.packs = load_packs()
        self.update_screen()

    def action_back(self) -> None:
        if self.screen_name == "document":
            self.screen_name = "pack"
            self.current_doc = None
        elif self.screen_name == "pack":
            self.screen_name = "knowledge"
            self.current_pack = None
        elif self.screen_name == "knowledge":
            self.screen_name = "home"
        self.selected_index = 0
        self.update_screen()

    def action_cursor_up(self) -> None:
        count = self.item_count()
        if count:
            self.selected_index = (self.selected_index - 1) % count
        self.update_screen()

    def action_cursor_down(self) -> None:
        count = self.item_count()
        if count:
            self.selected_index = (self.selected_index + 1) % count
        self.update_screen()

    def action_select(self) -> None:
        if self.screen_name == "home":
            item = HOME_ITEMS[self.selected_index]
            if item == "Knowledge":
                self.screen_name = "knowledge"
                self.selected_index = 0
            else:
                self.query_one("#message", Static).update(f"{item} module not built yet")

        elif self.screen_name == "knowledge":
            if self.packs:
                self.current_pack = self.packs[self.selected_index]
                self.screen_name = "pack"
                self.selected_index = 0

        elif self.screen_name == "pack":
            docs = self.current_pack.documents if self.current_pack else []
            if docs:
                self.current_doc = docs[self.selected_index]
                self.screen_name = "document"

        self.update_screen()

    def choose_number(self, number: int) -> None:
        index = number - 1
        if index < self.item_count():
            self.selected_index = index
            self.action_select()

    def action_choose_1(self): self.choose_number(1)
    def action_choose_2(self): self.choose_number(2)
    def action_choose_3(self): self.choose_number(3)
    def action_choose_4(self): self.choose_number(4)
    def action_choose_5(self): self.choose_number(5)
    def action_choose_6(self): self.choose_number(6)

    def item_count(self) -> int:
        if self.screen_name == "home":
            return len(HOME_ITEMS)
        if self.screen_name == "knowledge":
            return len(self.packs)
        if self.screen_name == "pack" and self.current_pack:
            return len(self.current_pack.documents)
        return 0

    def update_screen(self) -> None:
        if self.screen_name == "home":
            self.render_home()
        elif self.screen_name == "knowledge":
            self.render_knowledge()
        elif self.screen_name == "pack":
            self.render_pack()
        elif self.screen_name == "document":
            self.render_document()

    def render_home(self) -> None:
        state = get_system_state()
        status_color = {
            "READY": "green",
            "DEGRADED": "yellow",
            "HOT": "red",
            "UNKNOWN": "white",
        }.get(state.readiness, "white")

        self.query_one("#title", Static).update("AEGIS OS")
        self.query_one("#status", Static).update(
            f"[{status_color}]STATUS {state.readiness}[/{status_color}]"
        )
        self.query_one("#body", Static).update(
            f"Host {state.host}\n"
            f"IP   {state.ip}\n"
            f"CPU  {state.cpu}  RAM {state.memory}\n"
            f"Disk {state.disk}  Temp {state.temp}\n"
            f"Pwr  {state.power}\n"
            f"Up   {state.uptime}"
        )

        lines = []
        for i, item in enumerate(HOME_ITEMS):
            prefix = ">" if i == self.selected_index else " "
            lines.append(f"{prefix} {i + 1} {item}")

        self.query_one("#menu", Static).update("\n".join(lines))
        self.query_one("#message", Static).update("")

    def render_knowledge(self) -> None:
        self.query_one("#title", Static).update("Knowledge")
        self.query_one("#status", Static).update(f"Installed Packs: {len(self.packs)}")
        self.query_one("#body", Static).update("Select a knowledge pack")

        if not self.packs:
            menu = "No packs found\nAdd packs to knowledge/packs/"
        else:
            lines = []
            for i, pack in enumerate(self.packs):
                prefix = ">" if i == self.selected_index else " "
                label = f"{pack.icon} {pack.name}".strip()
                lines.append(f"{prefix} {i + 1} {label}")
            menu = "\n".join(lines)

        self.query_one("#menu", Static).update(menu)
        self.query_one("#message", Static).update("Esc Back")

    def render_pack(self) -> None:
        pack = self.current_pack
        self.query_one("#title", Static).update(pack.name if pack else "Pack")
        self.query_one("#status", Static).update("Documents")
        self.query_one("#body", Static).update(pack.description if pack else "")

        docs = pack.documents if pack else []
        if not docs:
            menu = "No Markdown documents found"
        else:
            lines = []
            for i, doc in enumerate(docs):
                prefix = ">" if i == self.selected_index else " "
                lines.append(f"{prefix} {i + 1} {doc.title}")
            menu = "\n".join(lines)

        self.query_one("#menu", Static).update(menu)
        self.query_one("#message", Static).update("Esc Back")

    def render_document(self) -> None:
        doc = self.current_doc
        text = read_document(doc.path) if doc else "No document selected"
        lines = text.splitlines()
        preview = "\n".join(lines[:14])

        self.query_one("#title", Static).update(doc.title if doc else "Document")
        self.query_one("#status", Static).update("Markdown Viewer")
        self.query_one("#body", Static).update(preview)
        self.query_one("#menu", Static).update("")
        self.query_one("#message", Static).update("Esc Back")


def run_dashboard() -> None:
    app = AegisDashboard()
    app.run()
