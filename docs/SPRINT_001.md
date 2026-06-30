# AEGIS OS
# Sprint 001
## Field Terminal Architecture
Version: v0.2.0-alpha

---

# Sprint Goal

Refactor AEGIS OS into a modular architecture while preserving **100% of existing functionality**.

This sprint is an architectural refactor.

It intentionally introduces **no major new end-user features**.

The objective is to establish a stable foundation for future capabilities.

---

# Background

The current prototype has successfully demonstrated:

- Appliance boot
- PiTFT support
- Knowledge Packs
- Journal
- Inventory
- Universal Search
- Markdown viewer
- Hardware status
- Boot splash
- Auto-launch

However, much of the implementation currently resides in a monolithic dashboard.

Before adding GPS, Maps, Meshtastic, Weather, or Communications, the architecture must be modularized.

---

# Objectives

Create a maintainable architecture.

Separate presentation from business logic.

Separate routing from rendering.

Introduce reusable UI components.

Preserve every existing feature.

Leave the Raspberry Pi fully operational.

---

# Deliverables

Create the following directories:

```
aegis/

core/
screens/
widgets/
themes/
models/
```

---

## Core

Implement:

```
application.py

router.py

screen.py

events.py

state.py
```

Responsibilities:

- startup
- routing
- shared state
- event dispatch

No rendering.

---

## Screens

Create:

```
home.py

knowledge.py

journal.py

inventory.py

hardware.py

system.py

search.py
```

Each screen owns rendering for one capability.

Screens must not directly manipulate other screens.

---

## Widgets

Create reusable components.

Examples:

Header

Menu

Footer

Viewer

StatusBar

Dialog

ProgressBar

SearchBox

Widgets contain no business logic.

---

## Themes

Create:

```
themes/

field.py
```

Theme controls:

colors

spacing

titles

borders

highlight colors

No application logic.

---

## Services

Existing services remain.

Move business logic out of screens whenever practical.

---

# Preserve

The following functionality MUST continue working:

Knowledge Packs

Journal

Inventory

Universal Search

Markdown Viewer

Boot splash

Boot sequence

PiTFT compatibility

Keyboard navigation

SSH usability

---

# Home Screen

The home screen should become mission-focused.

It should contain:

Knowledge

Journal

Inventory

Communications (placeholder)

Navigation (placeholder)

Hardware

System

Diagnostics should move into Hardware.

---

# Router

Navigation should become:

```
Home

↓

Knowledge

↓

Document

↓

Back

↓

Knowledge

↓

Home
```

Router owns navigation history.

---

# Screen Rules

Each screen should:

load()

render()

handle_input()

return_result()

Use consistent navigation.

---

# Coding Standards

Use type hints.

Use dataclasses where appropriate.

Avoid global state.

Avoid magic numbers.

Avoid duplicate logic.

Split large functions.

Target:

Functions under 50 lines.

Files under 300 lines.

---

# Documentation

Update:

README

ROADMAP

CHANGELOG

Architecture docs where appropriate.

---

# Testing

Verify:

Application starts.

Pi boots.

PiTFT renders.

SSH works.

Knowledge opens.

Journal opens.

Inventory opens.

Search works.

Hardware works.

System placeholder works.

---

# Acceptance Criteria

All existing capabilities continue working.

Application compiles.

Main branch remains bootable.

PiTFT experience is unchanged or improved.

Architecture is significantly cleaner.

Dashboard no longer owns all rendering.

---

# Non Goals

Do NOT implement:

GPS

Offline Maps

Weather

Meshtastic

Winlink

Bookmarks

Favorites

Recent Documents

These belong to later sprints.

---

# Git Strategy

Create focused commits.

Example:

refactor: introduce screen router

refactor: extract knowledge screen

refactor: extract hardware screen

feat: introduce theme engine

docs: update architecture

---

# Rollback

At every commit:

main must boot.

If regression occurs:

Fix immediately before continuing.

Never leave repository broken.

---

# Definition of Done

✓ Code compiles

✓ Pi boots

✓ PiTFT verified

✓ SSH verified

✓ Documentation updated

✓ Commits created

✓ Push successful

✓ Ready for v0.2.0-alpha tag

---

# Final Instruction

Do not redesign AEGIS.

Do not add features.

Do not change behavior.

Improve architecture only.

The operator should notice little or no difference.

Future developers should notice a dramatic improvement.

Prepared Together.