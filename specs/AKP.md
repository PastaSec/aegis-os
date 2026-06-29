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

## Folder Structure

```
Florida-Hurricane.akp/

manifest.yaml

README.md

docs/

images/

pdf/

assets/
```

---

## Manifest

```yaml
name: Florida Hurricane Guide
id: florida-hurricane
version: 1.0.0
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

---

## Supported Formats

* Markdown
* PDF
* HTML
* Images
* Plain Text

Future

* EPUB
* ZIM
* Video
* Audio

---

## Design Philosophy

Knowledge belongs to the community.

AEGIS provides access.

It does not own the information.
