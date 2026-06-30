from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import Static

from aegis.inventory import categories as inventory_categories, items as inventory_items, read_item, title_from_item
from aegis.journal import categories as journal_categories, entries as journal_entries, read_entry, title_from_entry
from aegis.knowledge import load_packs, read_document
from aegis.monitor import get_system_state
from aegis.search import search_all


HOME_ITEMS = ["Knowledge", "Field Journal", "Inventory", "Communications", "Navigation", "Hardware", "System"]


class AegisDashboard(App):
    CSS = """
    Screen {
        background: black;
    }

    #screen {
        background: black;
        color: white;
        width: 100%;
        height: 100%;
        padding: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "back", "Back"),
        ("up,k", "cursor_up", "Up"),
        ("down,j", "cursor_down", "Down"),
        ("enter", "select", "Select"),
        ("/", "search", "Search"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.view = "home"
        self.selected = 0
        self.stack = []

        self.packs = []
        self.journal_categories = []
        self.inventory_categories = []

        self.current_pack = None
        self.current_doc = None

        self.current_journal_category = None
        self.current_journal_entry = None

        self.current_inventory_category = None
        self.current_inventory_item = None

        self.search_query = ""
        self.search_results = []

    def compose(self) -> ComposeResult:
        yield Static("", id="screen")

    def on_mount(self) -> None:
        self.refresh_data()
        self.draw()
        self.set_interval(2, self.tick)

    def tick(self) -> None:
        if self.view == "home":
            self.draw()

    def refresh_data(self) -> None:
        self.packs = load_packs()
        self.journal_categories = journal_categories()
        self.inventory_categories = inventory_categories()

    def write(self, text: str) -> None:
        self.query_one("#screen", Static).update(text)

    def action_refresh(self) -> None:
        self.refresh_data()
        self.draw()

    def action_search(self) -> None:
        self.stack.append((self.view, self.selected))
        self.view = "search_input"
        self.selected = 0
        self.search_query = ""
        self.draw()

    def on_key(self, event: Key) -> None:
        if self.view != "search_input":
            return

        event.stop()

        if event.key == "enter":
            self.search_results = search_all(self.search_query)
            self.view = "search_results"
            self.selected = 0
            self.draw()
            return

        if event.key == "backspace":
            self.search_query = self.search_query[:-1]
            self.draw()
            return

        if event.key == "escape":
            self.action_back()
            return

        if len(event.character or "") == 1:
            self.search_query += event.character
            self.draw()

    def action_back(self) -> None:
        if self.stack:
            self.view, self.selected = self.stack.pop()
        else:
            self.view = "home"
            self.selected = 0
        self.draw()

    def item_count(self) -> int:
        if self.view == "home":
            return len(HOME_ITEMS)
        if self.view == "knowledge":
            return len(self.packs)
        if self.view == "pack" and self.current_pack:
            return len(self.current_pack.documents)
        if self.view == "journal":
            return len(self.journal_categories)
        if self.view == "journal_category" and self.current_journal_category:
            return len(journal_entries(self.current_journal_category))
        if self.view == "inventory":
            return len(self.inventory_categories)
        if self.view == "inventory_category" and self.current_inventory_category:
            return len(inventory_items(self.current_inventory_category))
        if self.view == "search_results":
            return min(8, len(self.search_results))
        if self.view in ["hardware", "system", "placeholder"]:
            return 0
        return 0

    def action_cursor_up(self) -> None:
        count = self.item_count()
        if count:
            self.selected = (self.selected - 1) % count
        self.draw()

    def action_cursor_down(self) -> None:
        count = self.item_count()
        if count:
            self.selected = (self.selected + 1) % count
        self.draw()

    def action_select(self) -> None:
        if self.view == "home":
            item = HOME_ITEMS[self.selected]
            if item == "Knowledge":
                self.stack.append((self.view, self.selected))
                self.view = "knowledge"
                self.selected = 0
            elif item == "Field Journal":
                self.stack.append((self.view, self.selected))
                self.view = "journal"
                self.selected = 0
            elif item == "Inventory":
                self.stack.append((self.view, self.selected))
                self.view = "inventory"
                self.selected = 0
            elif item == "Hardware":
                self.stack.append((self.view, self.selected))
                self.view = "hardware"
                self.selected = 0
            elif item == "System":
                self.stack.append((self.view, self.selected))
                self.view = "system"
                self.selected = 0
            else:
                self.stack.append((self.view, self.selected))
                self.view = "placeholder"
                self.selected = 0

        elif self.view == "knowledge" and self.packs:
            self.current_pack = self.packs[self.selected]
            self.stack.append((self.view, self.selected))
            self.view = "pack"
            self.selected = 0

        elif self.view == "pack" and self.current_pack and self.current_pack.documents:
            self.current_doc = self.current_pack.documents[self.selected]
            self.stack.append((self.view, self.selected))
            self.view = "document"
            self.selected = 0

        elif self.view == "journal" and self.journal_categories:
            self.current_journal_category = self.journal_categories[self.selected]
            self.stack.append((self.view, self.selected))
            self.view = "journal_category"
            self.selected = 0

        elif self.view == "journal_category":
            entries = journal_entries(self.current_journal_category)
            if entries:
                self.current_journal_entry = entries[self.selected]
                self.stack.append((self.view, self.selected))
                self.view = "journal_entry"
                self.selected = 0

        elif self.view == "inventory" and self.inventory_categories:
            self.current_inventory_category = self.inventory_categories[self.selected]
            self.stack.append((self.view, self.selected))
            self.view = "inventory_category"
            self.selected = 0

        elif self.view == "inventory_category":
            items = inventory_items(self.current_inventory_category)
            if items:
                self.current_inventory_item = items[self.selected]
                self.stack.append((self.view, self.selected))
                self.view = "inventory_item"
                self.selected = 0

        elif self.view == "search_results" and self.search_results:
            result = self.search_results[self.selected]
            self.current_doc = type("SearchDoc", (), {
                "title": result.document_title,
                "path": result.path,
            })()
            self.current_pack = None
            self.stack.append((self.view, self.selected))
            self.view = "document"
            self.selected = 0

        self.draw()

    def menu(self, items: list[str]) -> str:
        if not items:
            return "  None found"

        lines = []
        for i, item in enumerate(items[:8]):
            pointer = ">" if i == self.selected else " "
            lines.append(f"{pointer} {item}")
        return "\n".join(lines)

    def frame(self, title: str, status: str, body: str, footer: str = "↑↓ Select  Enter Open  Esc Back  Q Quit") -> str:
        return (
            f"[bold cyan]{title}[/bold cyan]\n"
            f"{status}\n"
            f"------------------------------\n"
            f"{body}\n"
            f"------------------------------\n"
            f"[dim]{footer}[/dim]"
        )

    def draw(self) -> None:
        if self.view == "home":
            state = get_system_state()
            body = (
                f"Mission Ready\n"
                f"{state.ip}\n\n"
                f"{self.menu(HOME_ITEMS)}"
            )
            self.write(self.frame("AEGIS OS", f"[bold green]STATUS {state.readiness}[/bold green]", body, "↑↓ Select  Enter Open  / Search  Q Quit"))

        elif self.view == "knowledge":
            items = [f"{pack.icon} {pack.name}".strip() for pack in self.packs]
            self.write(self.frame("Knowledge", f"Packs: {len(items)}", self.menu(items)))

        elif self.view == "pack":
            docs = self.current_pack.documents if self.current_pack else []
            items = [doc.title for doc in docs]
            title = self.current_pack.name if self.current_pack else "Pack"
            self.write(self.frame(title, "Documents", self.menu(items)))

        elif self.view == "document":
            title = self.current_doc.title if self.current_doc else "Document"
            text = read_document(self.current_doc.path) if self.current_doc else "No document selected"
            preview = "\n".join(text.splitlines()[:13])
            self.write(self.frame(title, "Viewer", preview))

        elif self.view == "journal":
            items = [category.title() for category in self.journal_categories]
            self.write(self.frame("Field Journal", f"Categories: {len(items)}", self.menu(items)))

        elif self.view == "journal_category":
            entries = journal_entries(self.current_journal_category)
            items = [title_from_entry(entry) for entry in entries]
            self.write(self.frame(self.current_journal_category.title(), f"Entries: {len(items)}", self.menu(items)))

        elif self.view == "journal_entry":
            title = title_from_entry(self.current_journal_entry)
            preview = "\n".join(read_entry(self.current_journal_entry).splitlines()[:13])
            self.write(self.frame(title, "Field Journal", preview))

        elif self.view == "inventory":
            items = [category.title() for category in self.inventory_categories]
            self.write(self.frame("Inventory", f"Categories: {len(items)}", self.menu(items)))

        elif self.view == "inventory_category":
            items = inventory_items(self.current_inventory_category)
            names = [title_from_item(item) for item in items]
            self.write(self.frame(self.current_inventory_category.title(), f"Items: {len(names)}", self.menu(names)))

        elif self.view == "inventory_item":
            title = title_from_item(self.current_inventory_item)
            preview = "\n".join(read_item(self.current_inventory_item).splitlines()[:13])
            self.write(self.frame(title, "Inventory", preview))

        elif self.view == "search_input":
            body = f"/ {self.search_query}_"
            self.write(self.frame("Search", "Universal Search", body, "Type query  Enter Search  Esc Cancel"))

        elif self.view == "search_results":
            items = [f"{result.pack_name}: {result.document_title}" for result in self.search_results[:8]]
            self.write(self.frame("Search Results", f"Results: {len(self.search_results)}", self.menu(items)))

        elif self.view == "hardware":
            state = get_system_state()
            body = (
                f"Host    {state.host}\n"
                f"IP      {state.ip}\n"
                f"CPU     {state.cpu}\n"
                f"RAM     {state.memory}\n"
                f"Disk    {state.disk}\n"
                f"Temp    {state.temp}\n"
                f"Power   {state.power}\n"
                f"Uptime  {state.uptime}"
            )
            self.write(self.frame("Hardware", "System Diagnostics", body))

        elif self.view == "system":
            body = (
                "AEGIS OS v0.1.0-alpha\n"
                "Mode: Field Terminal\n\n"
                "Update, backup, restore,\n"
                "logs, and configuration\n"
                "will live here."
            )
            self.write(self.frame("System", "Maintenance", body))

        elif self.view == "placeholder":
            self.write(self.frame("AEGIS OS", "Not Built Yet", "This module is reserved for Alpha expansion."))


def run_dashboard() -> None:
    AegisDashboard().run()
