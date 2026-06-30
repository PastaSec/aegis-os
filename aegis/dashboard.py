from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import Static

from aegis.core.router import Router
from aegis.inventory import categories as inventory_categories, items as inventory_items
from aegis.journal import categories as journal_categories, entries as journal_entries
from aegis.knowledge import load_packs
from aegis.screens.hardware import render_hardware_screen
from aegis.screens.inventory import render_inventory_category_screen, render_inventory_item_screen, render_inventory_screen
from aegis.screens.journal import render_journal_category_screen, render_journal_entry_screen, render_journal_screen
from aegis.screens.knowledge import render_document_screen, render_knowledge_screen, render_pack_screen
from aegis.monitor import get_system_state
from aegis.screens.home import render_home_screen
from aegis.screens.placeholder import render_placeholder_screen
from aegis.screens.search import render_search_input_screen, render_search_results_screen
from aegis.screens.system import render_system_screen
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
        self.router = Router()
        self.selected = 0

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

    @property
    def view(self) -> str:
        return self.router.route_name

    def navigate(self, view: str) -> None:
        route = self.router.go(view, selected=0, current_selected=self.selected)
        self.selected = route.selected

    def replace_view(self, view: str) -> None:
        route = self.router.replace(view, selected=0)
        self.selected = route.selected

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
        self.navigate("search_input")
        self.search_query = ""
        self.draw()

    def on_key(self, event: Key) -> None:
        if self.view != "search_input":
            return

        event.stop()

        if event.key == "enter":
            self.search_results = search_all(self.search_query)
            self.replace_view("search_results")
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
        route = self.router.back()
        self.selected = route.selected
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
                self.navigate("knowledge")
            elif item == "Field Journal":
                self.navigate("journal")
            elif item == "Inventory":
                self.navigate("inventory")
            elif item == "Hardware":
                self.navigate("hardware")
            elif item == "System":
                self.navigate("system")
            else:
                self.navigate("placeholder")

        elif self.view == "knowledge" and self.packs:
            self.current_pack = self.packs[self.selected]
            self.navigate("pack")

        elif self.view == "pack" and self.current_pack and self.current_pack.documents:
            self.current_doc = self.current_pack.documents[self.selected]
            self.navigate("document")

        elif self.view == "journal" and self.journal_categories:
            self.current_journal_category = self.journal_categories[self.selected]
            self.navigate("journal_category")

        elif self.view == "journal_category":
            entries = journal_entries(self.current_journal_category)
            if entries:
                self.current_journal_entry = entries[self.selected]
                self.navigate("journal_entry")

        elif self.view == "inventory" and self.inventory_categories:
            self.current_inventory_category = self.inventory_categories[self.selected]
            self.navigate("inventory_category")

        elif self.view == "inventory_category":
            items = inventory_items(self.current_inventory_category)
            if items:
                self.current_inventory_item = items[self.selected]
                self.navigate("inventory_item")

        elif self.view == "search_results" and self.search_results:
            result = self.search_results[self.selected]
            self.current_doc = type("SearchDoc", (), {
                "title": result.document_title,
                "path": result.path,
            })()
            self.current_pack = None
            self.navigate("document")

        self.draw()

    def draw(self) -> None:
        if self.view == "home":
            state = get_system_state()
            self.write(render_home_screen(state, HOME_ITEMS, self.selected))

        elif self.view == "knowledge":
            self.write(render_knowledge_screen(self.packs, self.selected))

        elif self.view == "pack":
            self.write(render_pack_screen(self.current_pack, self.selected))

        elif self.view == "document":
            self.write(render_document_screen(self.current_doc))

        elif self.view == "journal":
            self.write(render_journal_screen(self.journal_categories, self.selected))

        elif self.view == "journal_category":
            self.write(render_journal_category_screen(self.current_journal_category, self.selected))

        elif self.view == "journal_entry":
            self.write(render_journal_entry_screen(self.current_journal_entry))

        elif self.view == "inventory":
            self.write(render_inventory_screen(self.inventory_categories, self.selected))

        elif self.view == "inventory_category":
            self.write(render_inventory_category_screen(self.current_inventory_category, self.selected))

        elif self.view == "inventory_item":
            self.write(render_inventory_item_screen(self.current_inventory_item))

        elif self.view == "search_input":
            self.write(render_search_input_screen(self.search_query))

        elif self.view == "search_results":
            self.write(render_search_results_screen(self.search_results, self.selected))

        elif self.view == "hardware":
            state = get_system_state()
            self.write(render_hardware_screen(state))

        elif self.view == "system":
            self.write(render_system_screen())

        elif self.view == "placeholder":
            self.write(render_placeholder_screen())


def run_dashboard() -> None:
    AegisDashboard().run()
