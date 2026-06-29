from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.widgets import Static

from aegis.inventory import categories as inventory_categories, items as inventory_items, read_item, title_from_item
from aegis.journal import categories as journal_categories, entries as journal_entries, read_entry, title_from_entry
from aegis.knowledge import load_packs, read_document
from aegis.monitor import get_system_state
from aegis.search import search_all


HOME_ITEMS = ["Knowledge", "Field Journal", "Inventory", "Community", "Hardware", "Settings"]


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

        self.journal_categories = []
        self.current_journal_category = None
        self.current_journal_entry = None

        self.inventory_categories = []
        self.current_inventory_category = None
        self.current_inventory_item = None

    def compose(self) -> ComposeResult:
        with Container(id="main"):
            yield Static("AEGIS OS", id="title")
            yield Static("", id="status")
            yield Static("", id="body")
            yield Static("", id="menu")
            yield Static("", id="message")
            yield Static("↑↓ Move | Enter Open | / Search | Esc Back | Q Quit", id="hint")

    def on_mount(self) -> None:
        self.refresh_data()
        self.update_screen()
        self.set_interval(2, self.periodic_update)

    def refresh_data(self) -> None:
        self.packs = load_packs()
        self.journal_categories = journal_categories()
        self.inventory_categories = inventory_categories()

    def periodic_update(self) -> None:
        if self.screen_name == "home":
            self.update_screen()

    def on_key(self, event: Key) -> None:
        if self.screen_name != "search_input":
            return

        event.stop()

        if event.key == "enter":
            self.search_results = search_all(self.search_query)
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

    def action_refresh(self) -> None:
        self.refresh_data()
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
        elif self.screen_name == "journal_entry":
            self.screen_name = "journal_category"
            self.current_journal_entry = None
        elif self.screen_name == "journal_category":
            self.screen_name = "journal"
            self.current_journal_category = None
        elif self.screen_name == "journal":
            self.screen_name = "home"
        elif self.screen_name == "inventory_item":
            self.screen_name = "inventory_category"
            self.current_inventory_item = None
        elif self.screen_name == "inventory_category":
            self.screen_name = "inventory"
            self.current_inventory_category = None
        elif self.screen_name == "inventory":
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
            elif item == "Field Journal":
                self.screen_name = "journal"
            elif item == "Inventory":
                self.screen_name = "inventory"
            else:
                self.query_one("#message", Static).update(f"{item} module not built yet")
                self.update_screen()
                return
            self.selected_index = 0

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
            self.current_doc = type("SearchDoc", (), {"title": result.document_title, "path": result.path})()
            self.screen_name = "document"

        elif self.screen_name == "journal" and self.journal_categories:
            self.current_journal_category = self.journal_categories[self.selected_index]
            self.screen_name = "journal_category"
            self.selected_index = 0

        elif self.screen_name == "journal_category":
            entries = journal_entries(self.current_journal_category) if self.current_journal_category else []
            if entries:
                self.current_journal_entry = entries[self.selected_index]
                self.screen_name = "journal_entry"

        elif self.screen_name == "inventory" and self.inventory_categories:
            self.current_inventory_category = self.inventory_categories[self.selected_index]
            self.screen_name = "inventory_category"
            self.selected_index = 0

        elif self.screen_name == "inventory_category":
            items = inventory_items(self.current_inventory_category) if self.current_inventory_category else []
            if items:
                self.current_inventory_item = items[self.selected_index]
                self.screen_name = "inventory_item"

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
        if self.screen_name == "journal":
            return len(self.journal_categories)
        if self.screen_name == "journal_category" and self.current_journal_category:
            return len(journal_entries(self.current_journal_category))
        if self.screen_name == "inventory":
            return len(self.inventory_categories)
        if self.screen_name == "inventory_category" and self.current_inventory_category:
            return len(inventory_items(self.current_inventory_category))
        return 0

    def update_screen(self) -> None:
        {
            "home": self.render_home,
            "knowledge": self.render_knowledge,
            "pack": self.render_pack,
            "document": self.render_document,
            "search_results": self.render_search_results,
            "journal": self.render_journal,
            "journal_category": self.render_journal_category,
            "journal_entry": self.render_journal_entry,
            "inventory": self.render_inventory,
            "inventory_category": self.render_inventory_category,
            "inventory_item": self.render_inventory_item,
        }.get(self.screen_name, self.render_home)()

    def render_home(self) -> None:
        state = get_system_state()
        color = {"READY": "green", "DEGRADED": "yellow", "HOT": "red"}.get(state.readiness, "white")
        self.query_one("#title", Static).update("AEGIS OS")
        self.query_one("#status", Static).update(f"[{color}]STATUS {state.readiness}[/{color}]")
        self.query_one("#body", Static).update(
            f"Host {state.host}\nIP   {state.ip}\nCPU  {state.cpu}  RAM {state.memory}\n"
            f"Disk {state.disk}  Temp {state.temp}\nPwr  {state.power}\nUp   {state.uptime}"
        )
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {item}" for i, item in enumerate(HOME_ITEMS))
        )
        self.query_one("#message", Static).update("")

    def render_search_input(self) -> None:
        self.query_one("#title", Static).update("Search")
        self.query_one("#status", Static).update("Knowledge Search")
        self.query_one("#body", Static).update("Type search term, Enter to run")
        self.query_one("#menu", Static).update(f"/ {self.search_query}_")
        self.query_one("#message", Static).update("Esc Cancel")

    def render_knowledge(self) -> None:
        self.query_one("#title", Static).update("Knowledge")
        self.query_one("#status", Static).update(f"Installed Packs: {len(self.packs)}")
        self.query_one("#body", Static).update("Select a knowledge pack")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {(pack.icon + ' ' + pack.name).strip()}" for i, pack in enumerate(self.packs)) or "No packs found"
        )
        self.query_one("#message", Static).update("Esc Back | / Search")

    def render_pack(self) -> None:
        docs = self.current_pack.documents if self.current_pack else []
        self.query_one("#title", Static).update(self.current_pack.name if self.current_pack else "Pack")
        self.query_one("#status", Static).update("Documents")
        self.query_one("#body", Static).update(self.current_pack.description if self.current_pack else "")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {doc.title}" for i, doc in enumerate(docs)) or "No Markdown documents found"
        )
        self.query_one("#message", Static).update("Esc Back | / Search")

    def render_search_results(self) -> None:
        self.query_one("#title", Static).update("Search")
        self.query_one("#status", Static).update(f"Results: {len(self.search_results)}")
        self.query_one("#body", Static).update(f"Query: {self.search_query}")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {r.pack_name}: {r.document_title}" for i, r in enumerate(self.search_results[:6])) or "No matches found"
        )
        self.query_one("#message", Static).update("Enter Open | Esc Back")

    def render_document(self) -> None:
        text = read_document(self.current_doc.path) if self.current_doc else "No document selected"
        self.query_one("#title", Static).update(self.current_doc.title if self.current_doc else "Document")
        self.query_one("#status", Static).update("Markdown Viewer")
        self.query_one("#body", Static).update("\n".join(text.splitlines()[:14]))
        self.query_one("#menu", Static).update("")
        self.query_one("#message", Static).update("Esc Back")

    def render_journal(self) -> None:
        self.query_one("#title", Static).update("Field Journal")
        self.query_one("#status", Static).update(f"Categories: {len(self.journal_categories)}")
        self.query_one("#body", Static).update("Select a journal category")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {cat.title()}" for i, cat in enumerate(self.journal_categories)) or "No journal categories found"
        )
        self.query_one("#message", Static).update("Esc Back")

    def render_journal_category(self) -> None:
        entries = journal_entries(self.current_journal_category) if self.current_journal_category else []
        self.query_one("#title", Static).update((self.current_journal_category or "Journal").title())
        self.query_one("#status", Static).update(f"Entries: {len(entries)}")
        self.query_one("#body", Static).update("Select an entry")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {title_from_entry(e)}" for i, e in enumerate(entries)) or "No entries found"
        )
        self.query_one("#message", Static).update("Esc Back")

    def render_journal_entry(self) -> None:
        text = read_entry(self.current_journal_entry) if self.current_journal_entry else "No entry selected"
        self.query_one("#title", Static).update(title_from_entry(self.current_journal_entry) if self.current_journal_entry else "Entry")
        self.query_one("#status", Static).update("Field Journal")
        self.query_one("#body", Static).update("\n".join(text.splitlines()[:14]))
        self.query_one("#menu", Static).update("")
        self.query_one("#message", Static).update("Esc Back")

    def render_inventory(self) -> None:
        self.query_one("#title", Static).update("Inventory")
        self.query_one("#status", Static).update(f"Categories: {len(self.inventory_categories)}")
        self.query_one("#body", Static).update("Select inventory category")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {cat.title()}" for i, cat in enumerate(self.inventory_categories)) or "No inventory categories found"
        )
        self.query_one("#message", Static).update("Esc Back")

    def render_inventory_category(self) -> None:
        items = inventory_items(self.current_inventory_category) if self.current_inventory_category else []
        self.query_one("#title", Static).update((self.current_inventory_category or "Inventory").title())
        self.query_one("#status", Static).update(f"Items: {len(items)}")
        self.query_one("#body", Static).update("Select inventory item")
        self.query_one("#menu", Static).update(
            "\n".join(f"{'>' if i == self.selected_index else ' '} {i + 1} {title_from_item(item)}" for i, item in enumerate(items)) or "No items found"
        )
        self.query_one("#message", Static).update("Esc Back")

    def render_inventory_item(self) -> None:
        text = read_item(self.current_inventory_item) if self.current_inventory_item else "No item selected"
        self.query_one("#title", Static).update(title_from_item(self.current_inventory_item) if self.current_inventory_item else "Item")
        self.query_one("#status", Static).update("Inventory")
        self.query_one("#body", Static).update("\n".join(text.splitlines()[:14]))
        self.query_one("#menu", Static).update("")
        self.query_one("#message", Static).update("Esc Back")


def run_dashboard() -> None:
    app = AegisDashboard()
    app.run()
