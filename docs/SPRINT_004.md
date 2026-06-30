# AEGIS OS
# Sprint 004
## Field Document Viewer
Version: v0.4.0-alpha

---

# Sprint Goal

Transform the current document preview into a full-featured offline Field Document Viewer.

This sprint enhances the Knowledge Capability.

It introduces no new operational Capabilities.

---

# Background

Sprint 001 established modular architecture.

Sprint 002 introduced the theme engine.

Sprint 003 completed the reusable widget framework.

The current viewer displays only the first portion of a Markdown document.

Field operators require the ability to comfortably read complete documents while offline.

---

# Objectives

Replace the preview-only viewer with a scrollable document viewer.

Preserve PiTFT usability.

Preserve keyboard-only navigation.

Maintain excellent SSH usability.

---

# Viewer Features

Implement:

- vertical scrolling
- page up
- page down
- jump to beginning
- jump to end
- line counter
- document title
- current position indicator

---

# Markdown Support

Support:

- headings
- bullet lists
- numbered lists
- fenced code blocks
- block quotes
- horizontal rules
- tables (simple rendering)
- inline code

Ignore:

- HTML
- images
- embedded video

Images should display:

[Image omitted]

---

# Keyboard

Up

Down

PageUp

PageDown

Home

End

Esc

Q

---

# Status Bar

Display:

Document

Current Line

Total Lines

Example:

Viewer
Line 84 / 317

---

# Widgets

Enhance:

widgets/markdown.py

if appropriate:

widgets/status.py

No duplicate rendering.

---

# Preserve

Knowledge

Journal

Inventory

Search

Hardware

System

Theme system

Widget framework

PiTFT readability

Boot flow

SSH usability

---

# Non Goals

No syntax highlighting.

No hyperlinks.

No editing.

No search inside document.

No bookmarks.

No annotations.

Those belong to future sprints.

---

# Acceptance Criteria

Large Markdown documents are readable.

Scrolling is smooth.

Current appearance remains Field Terminal.

Keyboard navigation works.

Application compiles.

Pi appliance remains functional.

---

# Final Instruction

Improve the document reading experience.

Do not redesign AEGIS.

Prepared Together.