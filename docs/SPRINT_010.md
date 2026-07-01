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