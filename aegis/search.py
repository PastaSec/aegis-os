from dataclasses import dataclass
from pathlib import Path

from aegis.knowledge import load_packs
from aegis.journal import categories as journal_categories, entries as journal_entries, title_from_entry
from aegis.inventory import categories as inventory_categories, items as inventory_items, title_from_item


@dataclass
class SearchResult:
    pack_name: str
    document_title: str
    path: Path
    line: int
    preview: str


def _search_file(source: str, title: str, path: Path, query: str) -> SearchResult | None:
    try:
        lines = path.read_text(errors="replace").splitlines()
    except Exception:
        return None

    for idx, line in enumerate(lines, start=1):
        if query in line.lower():
            return SearchResult(
                pack_name=source,
                document_title=title,
                path=path,
                line=idx,
                preview=line.strip()[:80],
            )
    return None


def search_all(query: str) -> list[SearchResult]:
    query = query.strip().lower()
    if not query:
        return []

    results = []

    for pack in load_packs():
        for doc in pack.documents:
            result = _search_file(f"Knowledge/{pack.name}", doc.title, doc.path, query)
            if result:
                results.append(result)

    for category in journal_categories():
        for entry in journal_entries(category):
            result = _search_file(f"Journal/{category.title()}", title_from_entry(entry), entry, query)
            if result:
                results.append(result)

    for category in inventory_categories():
        for item in inventory_items(category):
            result = _search_file(f"Inventory/{category.title()}", title_from_item(item), item, query)
            if result:
                results.append(result)

    return results
