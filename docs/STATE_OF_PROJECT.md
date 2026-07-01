# AEGIS OS
# State of the Project

Version: v0.15.0-alpha
Status: Living Document

---

# Purpose

This document records the current implementation status of AEGIS OS so that
engineers and AI agents can understand what exists before proposing changes.

It is updated as part of each sprint, per the Documentation Lifecycle in
`.aegis/CONSTITUTION.md`.

---

# Snapshot

- Runtime: modular screen architecture, keyboard-first, PiTFT-readable, offline-first.
- Foundry: desktop-side import, metadata generation, validation, and index generation.
- Knowledge Packs: plain-file, metadata-enabled, versioned, with optional `index.json`.

Bootable: yes. Offline-first: yes. Cloud dependencies: none.

---

# Delivered Capabilities

## Runtime

- Modular architecture: `core/`, `screens/`, `widgets/`, `models/`, `themes/`, services.
- Home, Knowledge, Journal, Inventory, Hardware, System screens.
- Universal Search across Knowledge, Journal, and Inventory.
- Knowledge metadata front matter (title, tags, author, revision, summary).
- Field Document Viewer with scrolling and reading position.
- Operator Memory: Recent Documents, Favorites, Reading Position.
- Recursive Knowledge Pack loading (`docs/**/*.md`).
- Knowledge Navigator for nested pack folders.
- Knowledge Pack Manager: Pack Details screen between Pack List and Navigator.
- Knowledge Pack Index consumption with graceful fallback (Sprint 015).

## Foundry

- CLI: `list-packs`, `inspect-pack`, `validate`, `import-folder`, `generate-index`.
- Import of `.md`, `.markdown`, `.txt`, and optional `.pdf` text extraction.
- Manifest generation and front matter normalization.
- Knowledge Pack structure validation (warnings non-fatal).
- `index.json` generation and verification (Sprint 015).

## Knowledge Packs

- Deployed packs: `fema`, `florida`, `linux`, `medical`.
- Manifest contract with required and optional metadata fields.
- Optional Foundry-generated `index.json` for scalable discovery.

---

# Sprint History

- Sprint 001–004: architecture foundation, widget framework, Field Document Viewer.
- Sprint 005–006: Knowledge Engine metadata, Operator Memory.
- Sprint 007–011.5: Foundry foundation, ingestion pipeline, PDF ingestion, curated FEMA pack, frozen platform specs.
- Sprint 012: recursive Knowledge Pack loading.
- Sprint 013: Knowledge Navigator for nested packs.
- Sprint 014: Knowledge Pack Manager (Pack Details).
- Sprint 015: Knowledge Pack Index (Foundry-generated `index.json`, Runtime consumption + fallback). **Current.**

---

# Current Sprint — Sprint 015

Goal: Introduce Foundry-generated Knowledge Pack indexes while preserving
complete Runtime compatibility.

Outcome: Runtime consumes `index.json` when present and falls back to recursive
Markdown discovery when absent. Existing packs continue working without
regeneration. Search, Operator Memory, Navigator, and Pack Details are preserved.

---

# Known Constraints

- Runtime performs no heavy ingestion, OCR, PDF parsing, or AI work in the field.
- No SQLite, databases, cloud services, or boot-script changes.
- Pi-specific hardware fields may show `n/a` when developing on Windows.

End of Document.
