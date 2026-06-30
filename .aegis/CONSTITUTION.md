# AEGIS OS Engineering Context

## Identity

AEGIS OS is an Offline-First Field Operating Environment.

It is not a Raspberry Pi demo.
It is not a dashboard.
It is not a web app.
It is not merely a Python application.

It is a dedicated field terminal for knowledge, resilience, local operations, and community preparedness.

## Mission

Preserve knowledge.
Strengthen communities.
Remain operational.

## Three-Part Ecosystem

AEGIS is an ecosystem with three clear responsibilities.

### AEGIS Runtime

AEGIS Runtime is the Raspberry Pi field terminal.

It is offline-first, keyboard-first, and PiTFT-readable.

It consumes validated Knowledge Packs.

It does not perform heavy PDF, OCR, import, or document conversion work in the field.

### AEGIS Foundry

AEGIS Foundry is desktop-side tooling.

It prepares Knowledge Packs before deployment.

It may import PDFs, TXT, Markdown, and later DOCX files.

It may extract text, generate metadata, validate packs, and use AI during ingestion.

AI-assisted ingestion belongs in Foundry. The Runtime remains offline and dependable.

### Knowledge Packs

Knowledge Packs are portable, plain-file based, metadata-enabled, versioned, and validated before deployment.

## Product Principles

- Offline First
- Keyboard First
- Plain Files
- Capabilities, not modules
- Community Before Cloud
- No Linux Exposure
- Everything Searchable
- Main Must Always Boot

## Terminology

Use the word **Capabilities** for major functional areas.

Preferred:

- Knowledge Capability
- Journal Capability
- Inventory Capability
- Communications Capability
- Navigation Capability
- Hardware Capability
- System Capability

Avoid using “modules” for new architecture or user-facing language unless preserving an existing filename.

## Operator Experience

AEGIS should feel like dedicated equipment:

- Garmin GPS
- field radio
- aircraft MFD
- emergency operations terminal

It should be:

- calm
- readable
- fast
- high contrast
- keyboard navigable
- stress tolerant

It should never feel:

- flashy
- cluttered
- desktop-like
- web-dashboard-like
- dependent on Linux knowledge

## Navigation Standard

Every screen should support:

- Up / Down: Move
- Enter: Open
- Esc: Return
- /: Search
- R: Refresh
- Q: Standby / Quit

Do not invent new controls unless absolutely necessary.

## Architecture Direction

Sprint 001 introduces:

- core/
- screens/
- widgets/
- themes/
- models/

Business logic belongs in services.
Rendering belongs in screens.
Reusable interface pieces belong in widgets.
Shared routing and state belong in core.
Visual constants belong in themes.

## Non-Negotiables

Do not break boot.

Do not break PiTFT support.

Do not remove keyboard navigation.

Do not remove Knowledge, Journal, Inventory, Search, Hardware, or appliance startup behavior.

Do not expose Python tracebacks to the operator.

Do not introduce cloud dependency.

Do not move heavy ingestion, PDF processing, OCR, or import pipelines into AEGIS Runtime.

Do not add GPS, maps, Meshtastic, weather, bookmarks, favorites, or recent documents during Sprint 001.

Sprint 001 is architecture only.

## Coding Standards

Prefer:

- type hints
- dataclasses
- small files
- small functions
- clear names
- low coupling
- explicit state
- simple routing

Avoid:

- giant files
- magic numbers
- duplicated rendering logic
- deep inheritance
- global state
- clever abstractions

## Git Rules

Main must remain bootable.

Make small logical commits.

Preserve existing behavior.

If a regression appears, fix it before continuing.

## Definition of Done

A change is done only when:

- code compiles
- app launches
- PiTFT path still works
- SSH path still works
- docs are updated if needed
- behavior is preserved
- Git commit is clean

## Sprint 001 Summary

Refactor the application into a modular screen architecture while preserving 100% of existing functionality.

The operator should notice little or no difference.

Future developers should notice a dramatic improvement.

Prepared Together.
