# AEGIS Knowledge Pack (AKP) Specification

Version: 1.0 Draft

## Purpose

An AEGIS Knowledge Pack (AKP) is a self-contained bundle of offline information.

Knowledge Packs are designed to be:

* portable
* versioned
* searchable
* offline-first
* community shareable

The AEGIS platform never hardcodes knowledge.

Knowledge is distributed as packs.

---

## Production Folder Structure

```text
knowledge/packs/<pack-id>/
  manifest.yaml
  README.md
  docs/
    <document>.md
  sources/
  assets/
```

`README.md` is recommended for every curated pack.

Current Runtime support is intentionally narrower than the full AKP vision:

* Runtime loads Markdown documents from top-level `docs/*.md`.
* Recursive document folders under `docs/` remain a future PACK_SPEC enhancement.
* `sources/` and `assets/` are preserved for curation and future Runtime support, but they are not required for Runtime document loading today.

---

## Manifest

```yaml
name: Florida Hurricane Guide
id: florida-hurricane
version: 1.0.0
status: curated
author: NOAA
license: Public Domain
description: Hurricane preparation for Florida residents.
categories:
  - Florida
  - Emergency
tags:
  - hurricane
  - flooding
  - generator
```

Required manifest fields:

* name
* id
* version
* description

Optional manifest fields:

* status
* author
* license
* icon
* categories
* tags
* source
* homepage

Allowed `status` values:

* experimental
* curated
* validated
* official

---

## Document Metadata

Production documents should include front matter when practical:

```yaml
---
title: Generator Safety
category: Power
tags:
  - generator
  - outage
author: FEMA / Ready.gov
revision: 2026
summary: Safe generator operation during power outages.
source: Ready.gov Power Outages
source_url: https://www.ready.gov/power-outages
imported_by: AEGIS Foundry
import_date: 2026-07-01
---
```

Recommended fields:

* title
* category
* tags
* summary

Optional fields:

* author
* revision
* source
* source_url
* imported_by
* import_date

---

## Category Taxonomy

Use a small controlled vocabulary for document categories:

* Preparedness
* Power
* Communications
* Networking
* Medical
* Hardware
* Operations
* Recovery
* Security
* Navigation
* Reference

Pack-level `categories` describe the broad pack domain.

Document-level `category` describes the operator task area.

---

## Curation Workflow

1. Import source material with Foundry into a temporary pack.
2. Review generated Markdown for readability.
3. Normalize filenames to stable lowercase slugs.
4. Add or correct front matter.
5. Preserve provenance comments.
6. Remove extraction noise, duplicate headers, and broken formatting.
7. Write concise field-use summaries.
8. Apply controlled categories and useful tags.
9. Add a pack `README.md`.
10. Validate the pack before deployment.

Foundry validation may warn about curation issues, but those warnings remain non-fatal.

---

## Supported Formats

* Markdown
* PDF
* HTML
* Images
* Plain Text

Future:

* EPUB
* ZIM
* Video
* Audio

---

## Design Philosophy

Knowledge belongs to the community.

AEGIS provides access.

It does not own the information.
