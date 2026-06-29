from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "knowledge" / "packs"


@dataclass
class Document:
    title: str
    path: Path


@dataclass
class KnowledgePack:
    name: str
    pack_id: str
    description: str
    icon: str
    path: Path
    documents: list[Document]


def title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def load_pack(pack_path: Path) -> KnowledgePack | None:
    manifest_path = pack_path / "manifest.yaml"
    if not manifest_path.exists():
        return None

    data = yaml.safe_load(manifest_path.read_text()) or {}
    docs_dir = pack_path / "docs"

    documents = []
    if docs_dir.exists():
        for doc in sorted(docs_dir.glob("*.md")):
            documents.append(Document(title=title_from_path(doc), path=doc))

    return KnowledgePack(
        name=data.get("name", pack_path.name),
        pack_id=data.get("id", pack_path.name),
        description=data.get("description", ""),
        icon=data.get("icon", ""),
        path=pack_path,
        documents=documents,
    )


def load_packs() -> list[KnowledgePack]:
    if not PACKS_DIR.exists():
        return []

    packs = []
    for pack_path in sorted(PACKS_DIR.iterdir()):
        if pack_path.is_dir():
            pack = load_pack(pack_path)
            if pack:
                packs.append(pack)

    return packs


def read_document(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except Exception as exc:
        return f"# Error\n\nCould not read document:\n\n{exc}"
