# AEGIS OS
# Sprint 007
## Knowledge Foundry Foundation

Version: v0.7.0-alpha

---

# Sprint Goal

Create the foundation for AEGIS Foundry: desktop-side tools for building, validating, and preparing Knowledge Packs.

The Raspberry Pi Runtime must remain lightweight and offline-first.

---

# Concept

AEGIS has three parts:

1. AEGIS Runtime
   - Runs on Raspberry Pi
   - Consumes validated Knowledge Packs
   - Does not perform heavy import/OCR/PDF work

2. AEGIS Foundry
   - Runs on desktop/dev machine
   - Imports source material
   - Builds Knowledge Packs
   - Validates metadata and manifests

3. Knowledge Packs
   - Portable
   - Plain files
   - Metadata-enabled
   - Runtime-ready

---

# Objectives

Introduce the Foundry directory structure.

Create initial CLI tools.

Validate existing Knowledge Packs.

Prepare for future PDF/TXT/DOCX ingestion.

---

# Deliverables

Create:

```text
tools/
├── aegis_foundry/
│   ├── __init__.py
│   ├── cli.py
│   ├── pack.py
│   ├── validate.py
│   └── manifest.py