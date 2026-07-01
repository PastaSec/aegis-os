# AEGIS OS
# Sprint 013
## Knowledge Navigator

Version: v0.13.0-alpha

---

# Sprint Goal

Expose nested Knowledge Pack organization in the Runtime UI.

AEGIS now supports recursive Knowledge Pack loading. This sprint makes that structure visible and navigable to the operator.

---

# Background

Sprint 012 enabled Runtime loading of:

```
docs/**/*.md
```

However, the Knowledge screen still presents documents as a largely flat list.

Sprint 013 introduces the **Knowledge Navigator**, allowing operators to browse Knowledge Packs using their directory structure while preserving the existing search experience.

---

# Objectives

- Improve navigation for large Knowledge Packs.
- Support folder/category browsing.
- Preserve existing flat document behavior.
- Maintain consistent keyboard navigation.
- Keep the interface simple and PiTFT-friendly.

---

# Example

A Knowledge Pack may contain:

```text
docs/
├── preparedness/
│   ├── emergency-supply-kit.md
│   └── evacuation.md
├── power/
│   └── power-outage.md
└── weather/
    └── hurricane-preparedness.md
```

Runtime should present:

```text
Preparedness
Power
Weather
```

Selecting a folder should open that category.

Selecting a document should open the Field Document Viewer.

---

# Requirements

Support:

- Folder/category entries
- Document entries
- Enter opens a folder or document
- Escape returns to the previous level
- Search remains unchanged
- Favorites remain unchanged
- Recent Documents remain unchanged
- Reading Position remains unchanged

---

# Preserve

- Knowledge loading
- Search
- Favorites
- Recent Documents
- Reading Position
- Field Document Viewer
- Operator Memory
- Foundry
- Boot flow
- PiTFT usability

---

# Non Goals

Do not add:

- Folder editing
- Pack editing
- Runtime importing
- Tag management UI
- New document formats
- Boot script changes

---

# Acceptance Criteria

- Existing top-level documents still appear.
- Nested folders appear as navigable entries.
- Nested documents open correctly.
- Search still finds nested documents.
- Favorites open nested documents correctly.
- Recent Documents open nested documents correctly.
- Reading Position continues to restore correctly.
- Escape/back navigation behaves consistently.
- Runtime launches normally.
- PiTFT remains fully usable.

---

# Final Instruction

Build upon Sprint 012 by exposing the existing recursive Knowledge Pack structure to the operator without increasing interface complexity.

Prepared Together.