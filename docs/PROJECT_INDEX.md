# AEGIS OS
# Project Index

Version: v0.15.0-alpha
Status: Living Document

---

# Purpose

This document is the map of the AEGIS OS repository. It points to the
canonical documents, source layers, and tooling so that engineers and AI
agents can orient quickly before making changes.

Read this first, then follow the links relevant to the task.

---

# Governing Documents

- `.aegis/CONSTITUTION.md` — engineering constitution, non-negotiables, and the Documentation Lifecycle.
- `AGENTS.md` — engineering guidance for AI coding agents.
- `CODEX.md` — Codex CLI implementation guidance.
- `CLAUDE.md` — Claude Code project instructions.

---

# Product and Architecture

- `docs/PROJECT_BRIEF.md` — why AEGIS exists (mission, vision, principles).
- `docs/ARCHITECTURE.md` — how AEGIS is built (layers, routing, screens).
- `docs/ROADMAP_1_0.md` — engineering roadmap to version 1.0.
- `docs/DECISIONS.md` and `docs/adr/` — recorded architectural decisions.
- `docs/STATE_OF_PROJECT.md` — current implementation status by sprint.

---

# Platform Contracts

These three documents are the stable contract between Runtime, Foundry, and
Knowledge Packs. Change them only with a corresponding architecture update.

- `docs/PACK_SPEC.md` — Knowledge Pack layout, manifest, front matter, and `index.json`.
- `docs/RUNTIME_SPEC.md` — Runtime responsibilities and consumption contract.
- `docs/FOUNDRY_SPEC.md` — Foundry responsibilities, import, index generation, and validation.

---

# Runtime Source (`aegis/`)

- `aegis/app.py`, `aegis/__main__.py` — entrypoints.
- `aegis/dashboard.py` — application shell, routing wiring, and screen dispatch.
- `aegis/core/` — router, screen lifecycle, events, state.
- `aegis/screens/` — one primary screen per capability (rendering only).
- `aegis/widgets/` — reusable terminal UI components.
- `aegis/models/` — data shapes (document viewer, knowledge navigator).
- `aegis/themes/` — visual constants (Field theme).
- `aegis/knowledge.py` — Knowledge Pack loading, index consumption, and search.
- `aegis/operator.py` — Operator Memory (recent, favorites, reading position).
- `aegis/search.py` — universal search across Knowledge, Journal, Inventory.

---

# Foundry Source (`tools/aegis_foundry/`)

- `cli.py` — command-line interface.
- `commands.py` — command handlers (list, inspect, validate, import, generate-index).
- `ingest.py` — import pipeline (sources → Markdown + manifest + index).
- `manifest.py` — manifest model and loading.
- `pack.py` — Knowledge Pack path discovery.
- `index.py` — `index.json` generation.
- `validate.py` — Knowledge Pack and index validation.

---

# Content and State

- `knowledge/packs/<id>/` — deployed Knowledge Packs (`manifest.yaml`, `index.json`, `docs/`).
- `journal/`, `inventory/` — plain-file capability data.
- `state/operator.json` — Operator Memory persistence.

---

# Sprint Documentation

- `docs/SPRINT_xxx.md` — per-sprint definition.
- `.aegis/prompts/sprint-xxx.md` — per-sprint implementation prompt.

Current sprint: **Sprint 015 — Knowledge Pack Index**.

End of Document.
