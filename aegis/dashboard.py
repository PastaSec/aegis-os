from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import Static

from aegis.core.router import Router
from aegis.inventory import categories as inventory_categories, items as inventory_items
from aegis.journal import categories as journal_categories, entries as journal_entries
from aegis.knowledge import load_document, load_packs
from aegis.models.document_viewer import DocumentViewState
from aegis.operator import (
    get_position,
    load_operator_state,
    record_recent,
    resolve_document_refs,
    save_operator_state,
    set_position,
    toggle_favorite,
)
from aegis.screens.hardware import render_hardware_screen
from aegis.screens.inventory import render_inventory_category_screen, render_inventory_item_screen, render_inventory_screen
from aegis.screens.journal import render_journal_category_screen, render_journal_entry_screen, render_journal_screen
from aegis.screens.knowledge import document_line_count, render_document_screen, render_knowledge_screen, render_pack_screen
from aegis.monitor import get_system_state
from aegis.screens.home import render_home_screen
from aegis.screens.operator import render_operator_documents_screen
from aegis.screens.placeholder import render_placeholder_screen
from aegis.screens.search import render_search_input_screen, render_search_results_screen
from aegis.screens.system import render_system_screen
from aegis.search import search_all


HOME_ITEMS = [
    "Knowledge",
    "Recent Documents",
    "Favorites",
    "Field Journal",
    "Inventory",
    "Communications",
    "Navigation",
    "Hardware",
    "System",
]


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
        ("pageup", "page_up", "Page Up"),
        ("pagedown", "page_down", "Page Down"),
        ("home", "document_home", "Top"),
        ("end", "document_end", "Bottom"),
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
        self.operator_state = load_operator_state()
        self.recent_documents = []
        self.favorite_documents = []

        self.current_pack = None
        self.current_doc = None

        self.current_journal_category = None
        self.current_journal_entry = None

        self.current_inventory_category = None
        self.current_inventory_item = None

        self.search_query = ""
        self.search_results = []
        self.document_view = DocumentViewState()

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
        self.operator_state = load_operator_state()
        self.refresh_operator_documents()

    def refresh_operator_documents(self) -> None:
        self.recent_documents = resolve_document_refs(self.operator_state.recent)
        self.favorite_documents = resolve_document_refs(self.operator_state.favorites)

    def save_operator_state(self) -> None:
        save_operator_state(self.operator_state)
        self.refresh_operator_documents()

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
        if self.view == "document" and event.key.lower() == "f":
            event.stop()
            self.action_toggle_favorite()
            return

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
        if self.view == "document":
            self.save_document_position()
        route = self.router.back()
        self.selected = route.selected
        self.draw()

    def document_total_lines(self) -> int:
        return document_line_count(self.current_doc)

    def scroll_document(self, amount: int) -> None:
        self.document_view.scroll(amount, self.document_total_lines())
        self.save_document_position()
        self.draw()

    def save_document_position(self) -> None:
        if self.current_doc:
            set_position(self.operator_state, self.current_doc, self.document_view.offset)
            self.save_operator_state()

    def open_document(self, document) -> None:
        self.current_doc = document
        self.document_view.offset = get_position(self.operator_state, document)
        self.document_view.scroll(0, self.document_total_lines())
        record_recent(self.operator_state, document)
        self.save_operator_state()
        self.navigate("document")

    def item_count(self) -> int:
        if self.view == "home":
            return len(HOME_ITEMS)
        if self.view == "knowledge":
            return len(self.packs)
        if self.view == "pack" and self.current_pack:
            return len(self.current_pack.documents)
        if self.view == "recent_documents":
            return len(self.recent_documents)
        if self.view == "favorites":
            return len(self.favorite_documents)
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
        if self.view == "document":
            self.scroll_document(-1)
            return

        count = self.item_count()
        if count:
            self.selected = (self.selected - 1) % count
        self.draw()

    def action_cursor_down(self) -> None:
        if self.view == "document":
            self.scroll_document(1)
            return

        count = self.item_count()
        if count:
            self.selected = (self.selected + 1) % count
        self.draw()

    def action_page_up(self) -> None:
        if self.view == "document":
            self.document_view.page_up(self.document_total_lines())
            self.save_document_position()
            self.draw()

    def action_page_down(self) -> None:
        if self.view == "document":
            self.document_view.page_down(self.document_total_lines())
            self.save_document_position()
            self.draw()

    def action_document_home(self) -> None:
        if self.view == "document":
            self.document_view.home()
            self.save_document_position()
            self.draw()

    def action_document_end(self) -> None:
        if self.view == "document":
            self.document_view.end(self.document_total_lines())
            self.save_document_position()
            self.draw()

    def action_toggle_favorite(self) -> None:
        if self.view != "document" or not self.current_doc:
            return

        toggle_favorite(self.operator_state, self.current_doc)
        self.save_operator_state()
        self.draw()

    def action_select(self) -> None:
        if self.view == "home":
            item = HOME_ITEMS[self.selected]
            if item == "Knowledge":
                self.navigate("knowledge")
            elif item == "Recent Documents":
                self.navigate("recent_documents")
            elif item == "Favorites":
                self.navigate("favorites")
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
            self.open_document(self.current_pack.documents[self.selected])

        elif self.view == "recent_documents" and self.recent_documents:
            self.open_document(self.recent_documents[self.selected])

        elif self.view == "favorites" and self.favorite_documents:
            self.open_document(self.favorite_documents[self.selected])

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
            source = result.pack_name.split("/", 1)[1] if "/" in result.pack_name else result.pack_name
            self.current_doc = load_document(result.path, source)
            self.current_pack = None
            self.open_document(self.current_doc)

        self.draw()

    def draw(self) -> None:
        if self.view == "home":
            state = get_system_state()
            self.write(render_home_screen(state, HOME_ITEMS, self.selected))

        elif self.view == "knowledge":
            self.write(render_knowledge_screen(self.packs, self.selected))

        elif self.view == "pack":
            self.write(render_pack_screen(self.current_pack, self.selected))

        elif self.view == "recent_documents":
            self.write(render_operator_documents_screen("Recent Documents", self.recent_documents, self.selected))

        elif self.view == "favorites":
            self.write(render_operator_documents_screen("Favorites", self.favorite_documents, self.selected))

        elif self.view == "document":
            self.write(render_document_screen(self.current_doc, self.document_view.offset, self.document_view.height))

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
