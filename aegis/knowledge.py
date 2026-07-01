import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "knowledge" / "packs"

PACK_INDEX_FILENAME = "index.json"
PACK_INDEX_SCHEMA = "aegis.pack-index/1"


@dataclass
class Document:
    title: str
    path: Path
    pack: str = ""
    body: str = ""
    tags: list[str] | None = None
    author: str = ""
    revision: str = ""
    summary: str = ""

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


@dataclass
class KnowledgePack:
    name: str
    pack_id: str
    description: str
    icon: str
    path: Path
    documents: list[Document]
    version: str = ""
    status: str = ""
    license: str = ""
    source: str = ""
    homepage: str = ""
    author: str = ""
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


def title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def normalize_tags(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [str(value).strip()]


def split_front_matter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            raw_metadata = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            if text.endswith("\n"):
                body += "\n"
            try:
                metadata = yaml.safe_load(raw_metadata) or {}
            except Exception:
                return {}, text
            if not isinstance(metadata, dict):
                return {}, text
            return metadata, body

    return {}, text


def load_document(path: Path, pack_name: str = "") -> Document:
    try:
        raw = path.read_text(errors="replace")
    except Exception:
        raw = ""

    metadata, body = split_front_matter(raw)
    title = str(metadata.get("title") or title_from_path(path))

    return Document(
        title=title,
        path=path,
        pack=pack_name,
        body=body,
        tags=normalize_tags(metadata.get("tags")),
        author=str(metadata.get("author") or ""),
        revision=str(metadata.get("revision") or ""),
        summary=str(metadata.get("summary") or ""),
    )


def index_documents(pack_path: Path, pack_name: str) -> list[Document] | None:
    """Build documents from a Foundry-generated index.json.

    Returns None when the index is absent, unreadable, wrong schema, or yields
    no usable documents, so the caller falls back to recursive discovery.
    """
    index_path = pack_path / PACK_INDEX_FILENAME
    if not index_path.exists():
        return None

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(data, dict) or data.get("schema") != PACK_INDEX_SCHEMA:
        return None

    entries = data.get("documents")
    if not isinstance(entries, list):
        return None

    documents = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        relative = str(entry.get("path") or "").strip()
        if not relative:
            continue
        doc_path = pack_path / relative
        if not doc_path.exists():
            continue
        documents.append(
            Document(
                title=str(entry.get("title") or title_from_path(doc_path)),
                path=doc_path,
                pack=pack_name,
                body="",
                tags=normalize_tags(entry.get("tags")),
                author=str(entry.get("author") or ""),
                revision=str(entry.get("revision") or ""),
                summary=str(entry.get("summary") or ""),
            )
        )

    return documents or None


def discover_documents(docs_dir: Path, pack_name: str) -> list[Document]:
    documents = []
    if docs_dir.exists():
        for doc in sorted(docs_dir.rglob("*.md")):
            documents.append(load_document(doc, pack_name))
    return documents


def load_pack(pack_path: Path) -> KnowledgePack | None:
    manifest_path = pack_path / "manifest.yaml"
    if not manifest_path.exists():
        return None

    data = yaml.safe_load(manifest_path.read_text()) or {}
    docs_dir = pack_path / "docs"
    pack_name = data.get("name", pack_path.name)

    documents = index_documents(pack_path, pack_name)
    if documents is None:
        documents = discover_documents(docs_dir, pack_name)

    return KnowledgePack(
        name=data.get("name", pack_path.name),
        pack_id=data.get("id", pack_path.name),
        description=data.get("description", ""),
        icon=data.get("icon", ""),
        path=pack_path,
        documents=documents,
        version=str(data.get("version") or ""),
        status=str(data.get("status") or ""),
        license=str(data.get("license") or ""),
        source=str(data.get("source") or ""),
        homepage=str(data.get("homepage") or ""),
        author=str(data.get("author") or ""),
        categories=normalize_tags(data.get("categories")),
        tags=normalize_tags(data.get("tags")),
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
        raw = path.read_text(errors="replace")
        _, body = split_front_matter(raw)
        return body
    except Exception as exc:
        return f"# Error\n\nCould not read document:\n\n{exc}"


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


def search_documents(query: str) -> list[SearchResult]:
    query = query.strip().lower()
    if not query:
        return []

    results = []
    for pack in load_packs():
        for doc in pack.documents:
            metadata_text = " ".join(
                [
                    doc.title,
                    " ".join(doc.tags or []),
                    doc.author,
                    doc.revision,
                    doc.summary,
                ]
            ).lower()
            if query in metadata_text:
                results.append(
                    SearchResult(
                        pack_name=pack.name,
                        document_title=doc.title,
                        path=doc.path,
                        line=1,
                        preview=(doc.summary or doc.title)[:80],
                        tags=doc.tags,
                    )
                )
                continue

            lines = (doc.body or read_document(doc.path)).splitlines()

            for idx, line in enumerate(lines, start=1):
                if query in line.lower():
                    results.append(
                        SearchResult(
                            pack_name=pack.name,
                            document_title=doc.title,
                            path=doc.path,
                            line=idx,
                            preview=line.strip()[:80],
                            tags=doc.tags,
                        )
                    )
                    break

    return results
