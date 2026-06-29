from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.widgets import Static

from aegis.knowledge import load_packs, read_document, search_documents
from aegis.monitor import get_system_state


HOME_ITEMS = ["Knowledge", "Community", "Notes", "Network", "Hardware", "Settings"]


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
        ("/", "search", "Search"),
        ("up,k", "cursor_up", "Up"),
        ("down,j", "cursor_down", "Down"),
        ("enter", "select", "Select"),
    ]

    def __init__(self):
        super().__init__()
        self.screen_name = "home"
        self.selected_index = 0
        self.packs = []
        self.current_pack = None
        self.current_doc = None
        self.search_results = []
        self.search_query = ""

    def compose(self) -> ComposeResult:
        with Container(id="main"):
            yield Static("AEGIS OS", id="title")
            yield Static("", id="status")
            yield Static("", id="body")
            yield Static("", id="menu")
            yield Static("", id="message")
            yield Static("↑↓ Move | Enter Open | / Search | Esc Back | Q Quit", id="hint")

    def on_mount(self) -> None:
        self.packs = load_packs()
        self.update_screen()
        self.set_interval(2, self.periodic_update)

    def periodic_update(self) -> None:
        if self.screen_name == "home":
            self.update_screen()

    def on_key(self, event: Key) -> None:
        if self.screen_name != "search_input":
            return

        event.stop()

        if event.key == "enter":
            self.search_results = search_documents(self.search_query)
            self.screen_name = "search_results"
            self.selected_index = 0
            self.update_screen()
            return

        if event.key == "backspace":
            self.search_query = self.search_query[:-1]
            self.render_search_input()
            return

        if event.key == "escape":
            self.action_back()
            return

        if len(event.character or "") == 1:
            self.search_query += event.character
            self.render_search_input()

    def action_search(self) -> None:
        self.screen_name = "search_input"
        self.search_query = ""
        self.render_search_input()

    def render_search_input(self) -> None:
        self.query_one("#title", Static).update("Search")
        self.query_one("#status", Static).update("Knowledge Search")
        self.query_one("#body", Static).update("Type search term, Enter to run")
        self.query_one("#menu", Static).update(f"/ {self.search_query}_")
        self.query_one("#message", Static).update("Esc Cancel")

    def action_refresh(self) -> None:
        self.packs = load_packs()
        self.update_screen()

    def action_back(self) -> None:
        if self.screen_name == "search_input":
            self.screen_name = "home"
            self.search_query = ""
        elif self.screen_name == "search_results":
            self.screen_name = "home"
            self.search_results = []
        elif self.screen_name == "document":
            self.screen_name = "pack" if self.current_pack else "search_results"
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

        elif self.screen_name == "knowledge" and self.packs:
            self.current_pack = self.packs[self.selected_index]
            self.screen_name = "pack"
            self.selected_index = 0

        elif self.screen_name == "pack":
            docs = self.current_pack.documents if self.current_pack else []
            if docs:
                self.current_doc = docs[self.selected_index]
                self.screen_name = "document"

        elif self.screen_name == "search_results" and self.search_results:
            result = self.search_results[self.selected_index]
            self.current_pack = None
            self.current_doc = type("SearchDoc", (), {
                "title": result.document_title,
                "path": result.path,
            })()
            self.screen_name = "document"

        self.update_screen()

    def item_count(self) -> int:
        if self.screen_name == "home":
            return len(HOME_ITEMS)
        if self.screen_name == "knowledge":
            return len(self.packs)
        if self.screen_name == "pack" and self.current_pack:
            return len(self.current_pack.documents)
        if self.screen_name == "search_results":
            return len(self.search_results)
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
        elif self.screen_name == "search_results":
            self.render_search_results()

    def render_home(self) -> None:
        state = get_system_state()
        color = {"READY": "green", "DEGRADED": "yellow", "HOT": "red"}.get(state.readiness, "white")

        self.query_one("#title", Static).update("AEGIS OS")
        self.query_one("#status", Static).update(f"[{color}]STATUS {state.readiness}[/{color}]")
        self.query_one("#body", Static).update(
            f"Host {state.host}\n"
            f"IP   {state.ip}\n"
            f"CPU  {state.cpu}  RAM {state.memory}\n"
            f"Disk {state.disk}  Temp {state.temp}\n"
            f"Pwr  {state.power}\n"
            f"Up   {state.uptime}"
        )

        self.query_one("#menu", Static).update(
            "\n".join(
                f"{'>' if i == self.selected_index else ' '} {i + 1} {item}"
                for i, item in enumerate(HOME_ITEMS)
            )
        )
        self.query_one("#message", Static).update("")

    def render_knowledge(self) -> None:
        self.query_one("#title", Static).update("Knowledge")
        self.query_one("#status", Static).update(f"Installed Packs: {len(self.packs)}")
        self.query_one("#body", Static).update("Select a knowledge pack")

        self.query_one("#menu", Static).update(
            "\n".join(
                f"{'>' if i == self.selected_index else ' '} {i + 1} {(pack.icon + ' ' + pack.name).strip()}"
                for i, pack in enumerate(self.packs)
            ) or "No packs found"
        )
        self.query_one("#message", Static).update("Esc Back | / Search")

    def render_pack(self) -> None:
        pack = self.current_pack
        docs = pack.documents if pack else []

        self.query_one("#title", Static).update(pack.name if pack else "Pack")
        self.query_one("#status", Static).update("Documents")
        self.query_one("#body", Static).update(pack.description if pack else "")
        self.query_one("#menu", Static).update(
            "\n".join(
                f"{'>' if i == self.selected_index else ' '} {i + 1} {doc.title}"
                for i, doc in enumerate(docs)
            ) or "No Markdown documents found"
        )
        self.query_one("#message", Static).update("Esc Back | / Search")

    def render_search_results(self) -> None:
        self.query_one("#title", Static).update("Search")
        self.query_one("#status", Static).update(f"Results: {len(self.search_results)}")
        self.query_one("#body", Static).update(f"Query: {self.search_query}")

        self.query_one("#menu", Static).update(
            "\n".join(
                f"{'>' if i == self.selected_index else ' '} {result.pack_name}: {result.document_title}"
                for i, result in enumerate(self.search_results[:6])
            ) or "No matches found"
        )
        self.query_one("#message", Static).update("Enter Open | Esc Back")

    def render_document(self) -> None:
        doc = self.current_doc
        text = read_document(doc.path) if doc else "No document selected"
        preview = "\n".join(text.splitlines()[:14])

        self.query_one("#title", Static).update(doc.title if doc else "Document")
        self.query_one("#status", Static).update("Markdown Viewer")
        self.query_one("#body", Static).update(preview)
        self.query_one("#menu", Static).update("")
        self.query_one("#message", Static).update("Esc Back")


def run_dashboard() -> None:
    app = AegisDashboard()
    app.run()
