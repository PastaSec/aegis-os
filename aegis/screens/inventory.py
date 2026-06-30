from pathlib import Path

from aegis.inventory import items as inventory_items
from aegis.inventory import read_item, title_from_item
from aegis.widgets.frame import render_frame
from aegis.widgets.listbox import render_listbox
from aegis.widgets.markdown import render_markdown_preview


def render_inventory_screen(categories: list[str], selected: int) -> str:
    items = [category.title() for category in categories]
    return render_frame("Inventory", f"Categories: {len(items)}", render_listbox(items, selected))


def render_inventory_category_screen(category: str, selected: int) -> str:
    items = inventory_items(category)
    names = [title_from_item(item) for item in items]
    return render_frame(category.title(), f"Items: {len(names)}", render_listbox(names, selected))


def render_inventory_item_screen(item: Path) -> str:
    title = title_from_item(item)
    preview = render_markdown_preview(read_item(item))
    return render_frame(title, "Inventory", preview)
