# AEGIS OS
# Sprint 006
## Operator Memory

Version: v0.6.0-alpha

---

# Sprint Goal

Introduce persistent operator memory for the Knowledge Capability.

AEGIS should remember what the operator considers important without requiring configuration or cloud services.

Everything remains offline.

---

# Objectives

Implement lightweight persistent state using plain files.

Improve operator workflow without changing the existing interface.

---

# Features

## Recently Viewed

Maintain a history of recently opened Knowledge documents.

Limit:

20 documents

Persist across restarts.

Newest first.

Duplicates move to the top.

---

## Favorites

Allow an operator to mark a Knowledge document as a Favorite.

Persist locally.

Favorites are independent of Knowledge Packs.

Deleting a Knowledge Pack should simply invalidate the reference.

---

## Reading Position

Remember the last scroll position for each document.

Reopening a document should restore the previous location.

---

## Local State

Store all operator memory in a simple JSON file.

Suggested location:

state/operator.json

Example:

{
    "recent": [],
    "favorites": [],
    "positions": {}
}

Human readable.

Version controllable.

Easy to back up.

---

# UI

Home screen gains:

Recent Documents

Favorites

These behave like every other Capability.

Keyboard navigation remains identical.

---

# Preserve

Knowledge

Journal

Inventory

Hardware

System

Search

Document Viewer

Theme System

Widget Framework

Boot Flow

PiTFT compatibility

---

# Non Goals

No cloud sync

No accounts

No AI

No editing

No annotations

No OCR

No import pipeline

---

# Acceptance Criteria

Favorites persist.

Recents persist.

Reading position restores.

State survives reboot.

Search unchanged.

Pi appliance unchanged.

Prepared Together.