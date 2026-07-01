# Codex Prompt — Sprint 013

Read in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/ROADMAP_1_0.md
5. docs/PACK_SPEC.md
6. docs/FOUNDRY_SPEC.md
7. docs/RUNTIME_SPEC.md
8. docs/SPRINT_013.md
9. AGENTS.md
10. CODEX.md

Implement Sprint 013 only.

Goal:

Expose nested Knowledge Pack organization in the Runtime UI by introducing a Knowledge Navigator.

Before modifying files:

- inspect current Knowledge loading
- inspect Knowledge screen rendering
- inspect dashboard navigation
- inspect Search
- inspect Operator Memory

Produce an implementation plan only.

The plan must include:

- current navigation flow
- proposed navigator model
- rendering strategy
- keyboard behavior
- Search impact
- Operator Memory impact
- rollback plan
- testing strategy

Constraints:

- Preserve current document loading.
- Preserve Search.
- Preserve Favorites.
- Preserve Recent Documents.
- Preserve Reading Position.
- Preserve Field Document Viewer.
- Preserve keyboard navigation.
- Do not modify Foundry.
- Do not modify boot scripts.
- Do not commit automatically.

Stop after presenting the implementation plan.