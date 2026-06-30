from pathlib import Path

from aegis.journal import entries as journal_entries
from aegis.journal import read_entry, title_from_entry
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox
from aegis.widgets.markdown import render_markdown_preview


def render_journal_screen(categories: list[str], selected: int) -> str:
    items = [category.title() for category in categories]
    return render_frame("Field Journal", f"Categories: {len(items)}", render_listbox(items, selected))


def render_journal_category_screen(category: str, selected: int) -> str:
    entries = journal_entries(category)
    items = [title_from_entry(entry) for entry in entries]
    return render_frame(category.title(), f"Entries: {len(items)}", render_listbox(items, selected))


def render_journal_entry_screen(entry: Path) -> str:
    title = title_from_entry(entry)
    preview = render_markdown_preview(read_entry(entry))
    return render_frame(title, "Field Journal", preview)
