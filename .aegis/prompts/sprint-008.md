# Codex Prompt — Sprint 008

Read in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/ROADMAP_1_0.md
5. docs/SPRINT_008.md
6. AGENTS.md
7. CODEX.md

Implement Sprint 008 only.

Goal:
Add the first AEGIS Foundry ingestion pipeline for TXT and Markdown source folders.

Before modifying files:

- inspect the Foundry implementation
- inspect existing Knowledge Pack structure
- inspect validation rules
- inspect current metadata/front matter behavior

Produce an implementation plan only.

The plan must include:

- current Foundry CLI structure
- proposed import-folder command
- source file discovery strategy
- TXT-to-Markdown strategy
- Markdown normalization strategy
- manifest generation strategy
- metadata/front matter strategy
- output path safety
- validation integration
- rollback plan
- testing strategy

Constraints:

- Do not modify Runtime behavior.
- Do not modify boot scripts.
- Do not add PDF import.
- Do not add OCR.
- Do not add DOCX import.
- Do not add AI.
- Do not add new dependencies.
- Do not commit automatically.

Stop after presenting the implementation plan.