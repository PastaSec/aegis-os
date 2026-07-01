# AEGIS OS
# Foundry Specification

Version: v0.11.5-alpha
Status: Platform Contract

---

# Purpose

This document defines AEGIS Foundry responsibilities.

Foundry is the desktop-side preparation toolchain for creating Runtime-ready Knowledge Packs.

Foundry performs work before deployment so AEGIS Runtime remains lightweight, offline-first, and field reliable.

---

# Role

Foundry prepares, normalizes, validates, and packages knowledge.

Runtime consumes Foundry output.

Foundry must never require Runtime to perform heavyweight ingestion in the field.

---

# Responsibilities

Foundry owns:

- importing source folders
- reading Markdown and plain text sources
- extracting text from text-based PDFs when optional PDF support is installed
- generating `manifest.yaml`
- generating Markdown documents
- adding front matter where practical
- preserving provenance comments
- validating Knowledge Pack structure
- reporting curation warnings
- keeping output deterministic

Foundry may later own:

- DOCX import
- richer normalization reports
- pack publishing workflows
- optional AI-assisted curation
- OCR

Those future capabilities must not make Runtime cloud-dependent.

---

# Non Responsibilities

Foundry does not own:

- Runtime rendering
- Runtime navigation
- Runtime search UI
- boot behavior
- PiTFT console setup
- appliance startup
- field-side OCR
- field-side PDF ingestion
- mandatory cloud services

---

# Import Contract

The current import command is:

```text
python -m tools.aegis_foundry.cli import-folder <source> <pack_id>
```

Supported current source formats:

- `.md`
- `.markdown`
- `.txt`
- `.pdf` when optional Foundry PDF support is installed

PDF support is text extraction only.

Foundry must not implement OCR as part of this contract.

Dry runs must not require opening or extracting PDF text.

---

# Output Contract

Foundry output must be compatible with PACK_SPEC.

Current Runtime-compatible output places Markdown documents at:

```text
knowledge/packs/<pack-id>/docs/*.md
```

Foundry may preserve curation material in:

```text
sources/
assets/
README.md
```

Runtime must not require those folders today.

---

# Metadata Contract

Foundry should generate or preserve:

- document `title`
- document `category`
- document `tags`
- document `summary`
- source provenance when known

Foundry may preserve:

- `author`
- `revision`
- `source`
- `source_url`
- `imported_by`
- `import_date`

Foundry should not invent authoritative metadata when the source does not support it.

Unknown fields should be explicit, omitted, or left for human curation.

---

# Validation Contract

Foundry validation must detect:

- missing `manifest.yaml`
- invalid manifest structure
- missing required manifest fields
- missing `docs/`
- missing Markdown documents
- unreadable documents
- malformed front matter
- unsupported front matter fields
- incompatible recursive document paths for current Runtime
- missing curated-pack README files

Validation warnings are non-fatal.

Foundry commands should return failure only for structural errors that prevent a pack from being valid.

---

# Curation Workflow

Recommended workflow:

1. Import sources into a temporary pack.
2. Review generated Markdown.
3. Normalize filenames.
4. Add or correct front matter.
5. Preserve provenance comments.
6. Remove extraction noise.
7. Add concise summaries.
8. Apply controlled categories and useful tags.
9. Add `README.md` for curated packs.
10. Validate the pack.
11. Deploy the pack to Runtime.

---

# Dependency Policy

Foundry-specific dependencies must not become Runtime launch requirements.

Optional dependencies should be optional extras when practical.

If optional support is unavailable, Foundry should fail with clear operator-facing errors.

---

# Compatibility Guarantees

Foundry must preserve:

- plain-file Knowledge Packs
- deterministic output paths
- Runtime-compatible Markdown output
- offline usability of generated packs
- clean validation output
- clear separation from Runtime behavior

End of Document.
