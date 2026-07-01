# AEGIS Foundry

AEGIS Foundry is the desktop-side tooling layer for preparing AEGIS Knowledge Packs.

The Raspberry Pi Runtime stays lightweight, offline-first, and focused on field operation.

Foundry performs heavier preparation work on a desktop or development machine.

## Current Commands

Run from the repository root.

```powershell
python -m tools.aegis_foundry.cli list-packs
python -m tools.aegis_foundry.cli inspect-pack florida
python -m tools.aegis_foundry.cli validate
python -m tools.aegis_foundry.cli import-folder .\source-docs field-pack --output .\.tmp\packs
```

## Import Support

`import-folder` creates Runtime-ready Knowledge Packs from source folders.

Supported source files:

- Markdown: `.md`, `.markdown`
- Plain text: `.txt`
- Text-based PDF: `.pdf`

PDF import is a Foundry-only capability. It extracts readable text and writes Markdown documents with front matter and an AEGIS Foundry provenance comment. It does not perform OCR, image extraction, layout-perfect conversion, or Runtime PDF viewing.

Install PDF support before importing PDFs:

```powershell
python -m pip install .[foundry-pdf]
```

If PDF support is not installed, PDF imports fail with:

```text
PDF import requires pypdf. Install Foundry PDF support first.
```

## Curated Pack Standard

Curated packs should use this Runtime-compatible layout:

```text
knowledge/packs/<pack-id>/
  manifest.yaml
  README.md
  docs/
    <document>.md
```

Runtime currently loads top-level `docs/*.md` only. Recursive documents under `docs/` remain a future PACK_SPEC enhancement.

Recommended manifest metadata:

- `status`: `experimental`, `curated`, `validated`, or `official`
- `license`
- `categories`
- `tags`

Recommended document metadata:

- `title`
- `category`
- `tags`
- `summary`
- `source`
- `source_url`
- `imported_by`
- `import_date`

Foundry validation reports curation concerns as warnings. Warnings do not block validation or Runtime use.
