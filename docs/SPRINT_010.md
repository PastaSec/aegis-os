# AEGIS OS
# Sprint 010
## PDF Ingestion Foundation

Version: v0.10.0-alpha

---

# Sprint Goal

Add the first PDF ingestion path to AEGIS Foundry.

Foundry should convert text-based PDFs into Markdown documents inside Runtime-ready Knowledge Packs.

---

# Objectives

Support PDF source files in Foundry.

Extract readable text from PDFs.

Convert extracted text into Markdown.

Generate Knowledge Pack documents.

Validate generated packs.

Keep Runtime unchanged.

---

# Supported Inputs

- .pdf

Only text-based PDFs are required.

---

# Non Goals

Do not implement:

- OCR
- scanned PDF support
- AI metadata generation
- layout-perfect conversion
- image extraction
- runtime PDF viewing
- runtime UI changes
- boot script changes

---

# CLI

Extend:

```text
python -m tools.aegis_foundry.cli import-folder <source> <pack_id>

```

---

# Acceptance Criteria

- `import-folder` discovers `.pdf` files.
- Dry runs list PDF import output paths without opening or extracting PDF text.
- Text-based PDFs generate Markdown documents under `docs/`.
- Generated Markdown includes front matter and an AEGIS Foundry provenance comment.
- Scanned or unreadable PDFs fail cleanly without tracebacks.
- Existing TXT and Markdown ingestion behavior remains unchanged.
- Generated packs validate with the existing Foundry validator.
- Runtime behavior, boot scripts, and Runtime PDF viewing remain unchanged.

---

# Dependency Boundary

PDF extraction may use `pypdf` as optional Foundry support.

Runtime must not require `pypdf` to launch.

If PDF support is unavailable, Foundry reports:

```text
PDF import requires pypdf. Install Foundry PDF support first.
```
