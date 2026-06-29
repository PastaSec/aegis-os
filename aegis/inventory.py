from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "inventory"


def categories() -> list[str]:
    if not INVENTORY.exists():
        return []
    return sorted([d.name for d in INVENTORY.iterdir() if d.is_dir()])


def items(category: str) -> list[Path]:
    folder = INVENTORY / category
    if not folder.exists():
        return []
    return sorted(folder.glob("*.md"))


def title_from_item(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def read_item(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except Exception as exc:
        return f"# Error\n\nCould not read inventory item:\n\n{exc}"
