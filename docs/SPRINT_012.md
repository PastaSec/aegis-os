# AEGIS OS
# Sprint 012
## Recursive Knowledge Pack Loading

Version: v0.12.0-alpha

---

# Sprint Goal

Allow AEGIS Runtime to load Knowledge Pack documents from nested directories under docs/.

This aligns Runtime behavior with Foundry validation and the Knowledge Pack Specification.

---

# Background

Runtime currently loads only top-level Markdown files:

docs/*.md

Foundry can already validate nested documents:

docs/**/*.md

Sprint 012 closes that gap safely.

---

# Objectives

Support recursive Markdown discovery.

Preserve current top-level document behavior.

Preserve existing Knowledge Packs.

Keep Search working.

Keep Operator Memory working.

Keep document paths stable.

---

# Requirements

Runtime should load:

docs/example.md

and:

docs/power/generator-safety.md
docs/communications/radio-basics.md
docs/medical/bleeding-control.md

Document titles should still come from front matter or filename.

Relative paths should remain stable for:

- Search results
- Favorites
- Recent Documents
- Reading positions

---

# Preserve

Knowledge

Search

Favorites

Recent Documents

Reading Position

Foundry

Boot flow

PiTFT behavior

---

# Non Goals

Do not redesign Knowledge UI.

Do not add folder browsing UI yet.

Do not change Foundry import behavior unless necessary.

Do not add new document formats.

Do not modify boot scripts.

---

# Acceptance Criteria

- Top-level docs still load.
- Nested docs load.
- Search finds nested docs.
- Favorites/Recents work with nested docs.
- Existing packs validate.
- Runtime launches.
- PiTFT remains functional.

---

Prepared Together.