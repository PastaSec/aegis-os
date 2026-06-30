from aegis.search import SearchResult
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox
from aegis.widgets.searchbox import render_searchbox


def render_search_input_screen(query: str) -> str:
    body = render_searchbox(query)
    return render_frame("Search", "Universal Search", body, "Type query  Enter Search  Esc Cancel")


def render_search_results_screen(results: list[SearchResult], selected: int) -> str:
    items = [f"{result.pack_name}: {result.document_title}" for result in results[:8]]
    return render_frame("Search Results", f"Results: {len(results)}", render_listbox(items, selected))
