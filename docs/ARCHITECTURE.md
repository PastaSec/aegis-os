# AEGIS OS
# Architecture Specification
Version 0.2.0-alpha

---

# Purpose

This document defines the software architecture of AEGIS OS.

It exists to ensure the project remains maintainable, modular, and scalable while preserving a consistent user experience across all supported hardware.

This document describes **how** AEGIS is built.

The Project Brief describes **why**.

---

# High-Level Architecture

AEGIS is organized into six primary layers.

```
             AEGIS OS
                 │
        ┌────────┴────────┐
        │                 │
    Boot System       Application
                          │
        ┌─────────────────┴────────────────┐
        │                                  │
     Screen Router                  Services
        │                                  │
        ├──────────────┐                   │
        │              │                   │
    Screens         Widgets            Data Layer
```

Each layer has a single responsibility.

---

# Repository Layout

```
aegis-os/

aegis/
    app.py
    dashboard.py

    core/
    screens/
    widgets/
    services/
    themes/
    models/

knowledge/
journal/
inventory/

assets/

docs/

specs/

tests/

plugins/

scripts/
```

---

# Core Layer

The Core layer owns application behavior.

It should never know implementation details of individual screens.

Components:

```
application.py

router.py

screen.py

events.py

state.py
```

Responsibilities:

- startup
- shutdown
- routing
- event dispatch
- shared state

---

# Router

The Router controls screen transitions.

It should never render UI.

Example:

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

The router owns history.

Screens never manipulate other screens directly.

---

# Screen Layer

Each capability has exactly one primary screen.

Examples:

```
HomeScreen

KnowledgeScreen

JournalScreen

InventoryScreen

HardwareScreen

SystemScreen

SearchScreen
```

Each screen should be fewer than approximately 300 lines whenever practical.

Large screens should be split.

---

# Screen Lifecycle

Every screen follows the same lifecycle.

```
Load

↓

Build

↓

Render

↓

Handle Input

↓

Return Result
```

Consistency is more important than cleverness.

---

# Widgets

Widgets are reusable UI components.

Examples:

```
Header

Menu

Footer

StatusBar

Viewer

Dialog

ProgressBar

SearchBox
```

Widgets never contain business logic.

---

# Theme Layer

Themes define appearance.

Themes never contain application logic.

Themes control:

- colors
- borders
- spacing
- typography
- icons
- highlights

Future themes:

```
Field

Night

CERT

Search & Rescue

Amateur Radio
```

---

# Services

Services perform work.

Examples:

```
knowledge.py

journal.py

inventory.py

hardware.py

search.py
```

Services never render UI.

Screens call services.

---

# Models

Models represent structured data.

Examples:

```
KnowledgeDocument

InventoryItem

JournalEntry

HardwareStatus
```

Models should be plain Python objects or dataclasses.

---

# Knowledge System

Knowledge Packs are independent.

```
knowledge/

packs/

florida/

medical/

linux/

radio/
```

Each pack contains:

manifest

documents

optional assets

Future support:

images

pdf

zim

sqlite indexes

---

# Journal

Journal entries remain plain Markdown files.

Advantages:

- human readable
- Git friendly
- backup friendly
- future proof

---

# Inventory

Inventory remains plain files during Alpha.

Future versions may add metadata indexes while preserving human-readable source files.

---

# Plugin Architecture

Capabilities should eventually load dynamically.

Example:

```
plugins/

gps/

weather/

meshtastic/

radio/

camera/
```

Each plugin provides:

metadata

screens

services

assets

configuration

The Core should not require modification when adding a plugin.

---

# Search Engine

Search becomes a first-class service.

Search indexes:

Knowledge

Journal

Inventory

Plugins

Future maps

Future contacts

Future communications

Search should never require Internet access.

---

# Boot Sequence

Desired startup:

```
Power

↓

Linux Boot

↓

Splash

↓

Initialization

↓

Capability Loading

↓

Mission Ready

↓

Home Screen
```

Linux boot details should remain hidden whenever practical.

---

# Data Philosophy

Store information in open formats.

Preferred formats:

Markdown

JSON

YAML

PNG

JPEG

TXT

Avoid proprietary formats.

---

# Error Handling

Never expose stack traces to the operator.

Instead display:

```
Capability Unavailable

Details recorded in logs.
```

Logs remain available under System.

---

# Logging

All significant events should be logged.

Examples:

startup

shutdown

plugin load

errors

warnings

hardware failures

Logs should remain human readable.

---

# Testing Strategy

Every capability should support:

unit tests

integration tests

Pi hardware verification

PiTFT verification

SSH verification

---

# Coding Standards

Prefer:

small functions

small classes

clear names

explicit behavior

Avoid:

magic numbers

duplicate code

deep inheritance

global state

---

# Performance Goals

Cold boot:

<15 seconds

Capability switch:

<250 ms

Search:

instant for typical knowledge packs

Rendering:

responsive on Raspberry Pi hardware

---

# Security Philosophy

Offline first.

Least privilege.

Plain files.

No telemetry.

No mandatory accounts.

No cloud dependency.

---

# Final Rule

Architecture exists to preserve simplicity.

Whenever two designs are possible:

Choose the simpler one.

Future contributors should immediately understand the system after reading this document.

End of Document.