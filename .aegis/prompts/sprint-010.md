# Codex Prompt — Sprint 010

Read in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/ROADMAP_1_0.md
5. docs/SPRINT_010.md
6. AGENTS.md
7. CODEX.md

Implement Sprint 010 only.

Goal:
Add PDF ingestion foundation to AEGIS Foundry.

Before modifying files:

- inspect the current Foundry ingestion pipeline
- inspect import-folder behavior
- inspect validation behavior
- determine the safest PDF text extraction strategy

Produce an implementation plan only.

The plan must include:

- current ingestion pipeline
- proposed PDF extraction approach
- dependency strategy
- failure behavior for scanned/unreadable PDFs
- Markdown conversion strategy
- validation integration
- rollback plan
- testing strategy

Constraints:

- Do not modify Runtime behavior.
- Do not modify boot scripts.
- Do not implement OCR.
- Do not add AI.
- Do not add runtime PDF viewing.
- Do not redesign the CLI.
- Do not commit automatically.

Stop after presenting the implementation plan.