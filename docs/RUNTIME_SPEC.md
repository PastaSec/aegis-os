# AEGIS OS
# Runtime Specification

Version: v0.11.5-alpha
Status: Platform Contract

---

# Purpose

This document defines AEGIS Runtime responsibilities.

Runtime is the Raspberry Pi field terminal experience. It consumes validated Knowledge Packs and presents them to the operator without depending on Internet access or heavy document-processing tools.

---

# Role

Runtime is field equipment.

It must be:

- offline-first
- keyboard-first
- PiTFT-readable
- calm
- reliable
- fast enough for Raspberry Pi class hardware

Runtime consumes Knowledge Packs prepared by Foundry.

Runtime does not prepare Knowledge Packs.

---

# Responsibilities

Runtime owns:

- loading Knowledge Packs from `knowledge/packs/`
- reading pack manifests
- listing available packs
- loading Markdown documents from `docs/**/*.md`
- displaying Markdown documents
- displaying supported document metadata
- searching loaded Knowledge documents
- preserving field operation without Internet
- failing gracefully when content is unavailable

---

# Non Responsibilities

Runtime does not own:

- PDF ingestion
- OCR
- DOCX conversion
- AI metadata generation
- bulk import
- pack curation
- pack publishing
- cloud synchronization
- boot script changes for content ingestion

Heavy processing belongs to Foundry before deployment.

---

# Current Knowledge Loading Contract

Runtime loads packs from:

```text
knowledge/packs/<pack-id>/
```

Runtime expects:

```text
manifest.yaml
docs/**/*.md
```

Runtime loads top-level and nested Markdown documents:

```text
docs/*.md
docs/<folder>/*.md
docs/<folder>/<subfolder>/*.md
```

Recursive document folders under `docs/` are part of the current Runtime contract.

Document ordering must remain deterministic.

---

# Manifest Consumption

Runtime currently consumes:

- `name`
- `id`
- `description`
- `icon`

Runtime should tolerate additional manifest fields.

Additional fields are reserved for Foundry, pack repositories, future Runtime behavior, and curation workflows.

---

# Document Metadata Consumption

Runtime currently consumes document front matter:

- `title`
- `tags`
- `author`
- `revision`
- `summary`

Runtime should tolerate additional document metadata fields.

Additional fields must not break document loading.

---

# Search Contract

Runtime search should include:

- document title
- tags
- author
- revision
- summary
- document body text

Search must remain local.

Search must not require Internet access.

---

# Error Handling

Runtime must not expose Python tracebacks to operators during normal field use.

Operator-facing errors should be calm and actionable.

Technical details belong in logs or developer diagnostics.

---

# Performance Expectations

Runtime should preserve:

- fast pack listing
- responsive document navigation
- local search over typical deployed packs
- Raspberry Pi compatibility
- PiTFT readability

Runtime should avoid large processing jobs at startup.

---

# Compatibility Guarantees

Runtime must preserve:

- bootability
- keyboard navigation
- existing Knowledge, Journal, Inventory, Search, Hardware, and System behavior
- plain-file Knowledge Pack consumption
- offline operation
- compatibility with Foundry-generated packs that follow PACK_SPEC

---

# Future Enhancements

Future Runtime work may add:

- richer metadata display
- document indexes
- image display
- Runtime PDF viewing
- pack repository browsing
- bookmarks
- favorites

These enhancements must not weaken the Foundry/Runtime separation.

End of Document.
