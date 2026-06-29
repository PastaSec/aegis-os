from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
JOURNAL = ROOT / "journal"


def categories() -> list[str]:
    if not JOURNAL.exists():
        return []
    return sorted([d.name for d in JOURNAL.iterdir() if d.is_dir()])


def entries(category: str) -> list[Path]:
    folder = JOURNAL / category
    if not folder.exists():
        return []
    return sorted(folder.glob("*.md"), reverse=True)


def title_from_entry(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def read_entry(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except Exception as exc:
        return f"# Error\n\nCould not read journal entry:\n\n{exc}"
