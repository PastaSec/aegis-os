# AEGIS OS
# Sprint 009
## Ingestion Test Corpus

Version: v0.9.0-alpha

---

# Sprint Goal

Validate the AEGIS Foundry ingestion pipeline using real-world documentation.

This sprint focuses on reliability, normalization, and repeatability.

No Runtime behavior changes.

---

# Background

Sprint 008 introduced the first Knowledge Ingestion Pipeline.

Before expanding to PDF, DOCX, OCR, and AI-assisted ingestion, the pipeline must prove it can consistently produce high-quality Knowledge Packs from diverse plain-text sources.

---

# Objectives

Create a representative corpus of source material.

Exercise the import pipeline.

Verify generated Knowledge Packs.

Improve normalization where needed.

Preserve deterministic output.

---

# Test Corpus

Create a temporary test corpus containing examples from:

- FEMA publications (TXT/Markdown)
- Raspberry Pi documentation
- Ubuntu documentation
- Linux man-page exports
- CERT reference notes
- Amateur Radio guides
- Personal SOPs
- Checklists
- Cookbooks
- General plain-text notes

The corpus is for testing only.

It should not become part of the Runtime.

---

# Validation Goals

Verify:

- Nested directories
- Long filenames
- Duplicate filenames
- Unicode
- Large documents
- Empty files
- Mixed TXT/Markdown folders
- Deep directory trees

---

# Import Verification

Each generated Knowledge Pack should be checked for:

- valid manifest
- valid metadata
- preserved hierarchy
- readable Markdown
- deterministic filenames
- provenance comments
- successful validation

---

# Regression Testing

Existing packs must continue to validate.

Runtime behavior must remain unchanged.

No boot scripts may change.

---

# Non Goals

Do not implement:

- PDF
- DOCX
- OCR
- AI
- Runtime indexing
- Runtime UI changes

---

# Acceptance Criteria

- Multiple real-world source folders import successfully.
- Generated packs validate cleanly.
- Existing packs continue to validate.
- No Runtime regressions.
- Pipeline remains deterministic.

---

Prepared Together.