from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.aegis_foundry.manifest import Manifest, load_manifest


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKS_DIR = REPO_ROOT / "knowledge" / "packs"


@dataclass
class KnowledgePackPath:
    path: Path
    manifest: Manifest | None = None

    @property
    def docs_dir(self) -> Path:
        return self.path / "docs"

    @property
    def documents(self) -> list[Path]:
        if not self.docs_dir.exists():
            return []
        return sorted(self.docs_dir.rglob("*.md"))

    @property
    def display_name(self) -> str:
        if self.manifest and self.manifest.name:
            return self.manifest.name
        return self.path.name


def resolve_path(path: str | Path | None = None) -> Path:
    if path is None:
        return DEFAULT_PACKS_DIR
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def resolve_pack_path(pack: str | Path) -> Path:
    candidate = resolve_path(pack)
    if candidate.exists():
        return candidate

    pack_id = Path(pack)
    if len(pack_id.parts) == 1:
        return DEFAULT_PACKS_DIR / str(pack)

    return candidate


def discover_packs(path: str | Path | None = None) -> list[KnowledgePackPath]:
    root = resolve_path(path)
    if not root.exists():
        return []

    if (root / "manifest.yaml").exists():
        return [load_pack_path(root)]

    packs = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "manifest.yaml").exists():
            packs.append(load_pack_path(child))
    return packs


def load_pack_path(path: Path) -> KnowledgePackPath:
    manifest_path = path / "manifest.yaml"
    manifest = None
    if manifest_path.exists():
        try:
            manifest = load_manifest(manifest_path)
        except ValueError:
            manifest = None
    return KnowledgePackPath(path=path, manifest=manifest)
