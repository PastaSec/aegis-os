# Codex Prompt — Sprint 014

Read the following documents in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/ROADMAP_1_0.md
5. docs/PACK_SPEC.md
6. docs/FOUNDRY_SPEC.md
7. docs/RUNTIME_SPEC.md
8. docs/SPRINT_014.md
9. AGENTS.md
10. CODEX.md

Implement Sprint 014 only.

# Goal

Introduce a Runtime Knowledge Pack Manager by adding a Pack Details screen between the Pack List and the Knowledge Navigator.

The Pack Details screen should display manifest metadata and provide a clean entry point into browsing the pack.

Before modifying any files:

- inspect current Knowledge Pack loading
- inspect the manifest data model
- inspect the Knowledge screen rendering
- inspect dashboard navigation
- inspect Search behavior
- inspect Operator Memory behavior

Produce an implementation plan only.

The implementation plan must include:

- current Knowledge navigation flow
- proposed Pack Details workflow
- manifest metadata handling
- rendering strategy
- keyboard behavior
- Search impact
- Operator Memory impact
- rollback plan
- testing strategy

# Constraints

Preserve:

- Knowledge Navigator
- Recursive Knowledge Pack loading
- Search
- Favorites
- Recent Documents
- Reading Position
- Field Document Viewer
- Operator Memory
- PiTFT usability

Do not add:

- Runtime pack editing
- Runtime importing
- Runtime validation
- Online repositories
- Cloud synchronization

Do not modify:

- Foundry
- Boot scripts

Do not commit automatically.

Stop after presenting the implementation plan.