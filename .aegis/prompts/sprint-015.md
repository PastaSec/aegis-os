# AEGIS OS
# Sprint 015
## Implementation Prompt

Read the following documents in order:

1. docs/PROJECT_INDEX.md
2. docs/STATE_OF_PROJECT.md
3. docs/SPRINT_015.md
4. .aegis/CONSTITUTION.md
5. AGENTS.md
6. CODEX.md

Study the repository before proposing any changes.

---

# Goal

Implement Sprint 015 only.

Introduce Foundry-generated Knowledge Pack indexes while preserving complete Runtime compatibility.

The Runtime should consume generated indexes when available and gracefully fall back to the existing Markdown discovery path when indexes are absent.

---

# Before Modifying Any Files

Inspect:

- Runtime Knowledge loading
- KnowledgePack model
- Search implementation
- Operator Memory
- Knowledge Navigator
- Pack Details
- Foundry import pipeline
- Foundry validation
- Current Knowledge Pack layout

Present an implementation plan only.

Do not modify any files until implementation is explicitly approved.

---

# Implementation Plan Must Include

## Current Runtime Loading Flow

Explain how Knowledge Packs are currently discovered and loaded.

## Current Foundry Generation Flow

Explain how packs are currently imported, validated, and written.

## Proposed index.json Format

Recommend a lightweight metadata structure suitable for Runtime loading.

## Runtime Loading Strategy

Describe how Runtime should:

- load manifest.yaml
- load index.json when present
- fall back to recursive Markdown discovery when absent

## Compatibility Strategy

Ensure all existing Knowledge Packs continue working without regeneration.

## Search Impact

Describe how Search will behave with indexed packs.

## Operator Memory Impact

Explain why Favorites, Recent Documents, and Reading Position remain compatible.

## Validation Changes

Describe Foundry validation additions for index.json generation and verification.

## Rollback Plan

Provide a safe rollback path requiring no Knowledge Pack migration.

## Testing Strategy

Include:

- compile verification
- Runtime smoke tests
- Foundry validation
- fallback behavior
- index generation verification
- Search verification
- Operator Memory verification

---

# Constraints

Preserve:

- Knowledge Navigator
- Knowledge Pack Manager
- Search
- Favorites
- Recent Documents
- Reading Position
- Document Viewer
- PiTFT usability
- Offline-first behavior

Do not introduce:

- SQLite
- databases
- cloud services
- runtime editing
- boot changes

Do not modify:

- appliance startup
- boot scripts

Do not commit automatically.

Stop after presenting the implementation plan.