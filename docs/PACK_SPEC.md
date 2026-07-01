# AEGIS OS
# Knowledge Pack Specification

Version: v0.11.5-alpha
Status: Platform Contract

---

# Purpose

This document defines the stable Knowledge Pack contract between AEGIS Foundry and AEGIS Runtime.

A Knowledge Pack is a portable, offline-first collection of human-readable files prepared before deployment and consumed by Runtime in the field.

Knowledge Packs must remain useful without AEGIS software.

---

# Compatibility Rule

AEGIS Runtime loads Markdown documents from:

```text
knowledge/packs/<pack-id>/docs/**/*.md
```

Top-level documents under `docs/*.md` remain supported.

Recursive document folders under `docs/` are part of the Runtime contract.

---

# Required Layout

```text
knowledge/packs/<pack-id>/
  manifest.yaml
  docs/
    <document>.md
    <folder>/
      <document>.md
```

Recommended layout for curated packs:

```text
knowledge/packs/<pack-id>/
  manifest.yaml
  README.md
  docs/
    <document>.md
    <folder>/
      <document>.md
  sources/
  assets/
```

`sources/` and `assets/` are reserved for curation, provenance, and future Runtime support. Runtime must not require them for current Markdown document loading.

---

# Pack Identity

Pack IDs must be stable lowercase slugs.

Allowed characters:

```text
a-z
0-9
-
_
```

The pack directory name should match `manifest.yaml` field `id`.

Changing a pack ID is a breaking compatibility change.

---

# Manifest Contract

Required fields:

```yaml
name: FEMA Preparedness
id: fema
version: 0.1.0
description: Curated FEMA and Ready.gov preparedness references for field use.
```

Optional fields:

```yaml
status: curated
icon: FEMA
author: FEMA / Ready.gov
license: U.S. Government Work
source: Ready.gov
homepage: https://www.ready.gov/
categories:
  - Preparedness
  - Operations
tags:
  - fema
  - emergency kit
```

Allowed `status` values:

- `experimental`
- `curated`
- `validated`
- `official`

Manifest `categories` and `tags` should be YAML lists.

---

# Document Contract

Documents must be UTF-8 Markdown files.

Documents should remain readable in a plain text editor.

Production documents should include YAML front matter:

```yaml
---
title: Emergency Supply Kit
category: Preparedness
tags:
  - emergency kit
  - supplies
author: FEMA / Ready.gov
revision: 2026
summary: Core supplies to keep available before a disaster or outage.
source: Ready.gov Emergency Supply Kit
source_url: https://www.ready.gov/kit
imported_by: AEGIS Foundry
import_date: 2026-07-01
---
```

Recommended fields:

- `title`
- `category`
- `tags`
- `summary`

Optional fields:

- `author`
- `revision`
- `source`
- `source_url`
- `imported_by`
- `import_date`

Runtime currently uses:

- `title`
- `tags`
- `author`
- `revision`
- `summary`

Other metadata is preserved for Foundry, search quality, provenance, and future Runtime behavior.

---

# Category Taxonomy

Use this controlled vocabulary when practical:

- `Preparedness`
- `Power`
- `Communications`
- `Networking`
- `Medical`
- `Hardware`
- `Operations`
- `Recovery`
- `Security`
- `Navigation`
- `Reference`

Pack-level `categories` describe broad domain coverage.

Document-level `category` describes the operator task area.

---

# Provenance

Imported or curated documents should preserve provenance through front matter and a comment near the top of the body:

```markdown
<!-- Imported by AEGIS Foundry. Source: Ready.gov Emergency Supply Kit -->
```

Provenance must not make Runtime dependent on Internet access.

URLs are references only.

---

# Versioning

Pack versions should use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Increment:

- `PATCH` for metadata corrections, typo fixes, or formatting cleanup.
- `MINOR` for added documents or meaningful content additions.
- `MAJOR` for pack ID changes, document removal, or incompatible structure changes.

---

# Validation Expectations

Foundry validates pack structure before deployment.

Validation errors indicate invalid pack structure.

Validation warnings indicate curation or compatibility concerns.

Recursive Markdown documents under `docs/` are valid.

Warnings are non-fatal unless a future release explicitly changes the validation policy.

---

# Non Goals

The pack format does not require:

- cloud access
- databases
- Runtime PDF parsing
- OCR
- AI-generated metadata
- proprietary formats

End of Document.
