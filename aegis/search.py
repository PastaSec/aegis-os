from dataclasses import dataclass
from pathlib import Path

from aegis.knowledge import load_packs, read_document
from aegis.journal import categories as journal_categories, entries as journal_entries, title_from_entry
from aegis.inventory import categories as inventory_categories, items as inventory_items, title_from_item


@dataclass
class SearchResult:
    pack_name: str
    document_title: str
    path: Path
    line: int
    preview: str
    tags: list[str] | None = None

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


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


def _search_knowledge_document(source: str, doc, query: str) -> SearchResult | None:
    metadata_text = " ".join(
        [
            doc.title,
            " ".join(doc.tags or []),
            doc.author,
            doc.revision,
            doc.summary,
        ]
    ).lower()
    body = doc.body or read_document(doc.path)

    if query in metadata_text:
        return SearchResult(
            pack_name=source,
            document_title=doc.title,
            path=doc.path,
            line=1,
            preview=(doc.summary or doc.title)[:80],
            tags=doc.tags,
        )

    for idx, line in enumerate(body.splitlines(), start=1):
        if query in line.lower():
            return SearchResult(
                pack_name=source,
                document_title=doc.title,
                path=doc.path,
                line=idx,
                preview=line.strip()[:80],
                tags=doc.tags,
            )
    return None


def search_all(query: str) -> list[SearchResult]:
    query = query.strip().lower()
    if not query:
        return []

    results = []

    for pack in load_packs():
        for doc in pack.documents:
            result = _search_knowledge_document(f"Knowledge/{pack.name}", doc, query)
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
