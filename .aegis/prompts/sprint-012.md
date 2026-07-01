# Codex Prompt — Sprint 012

Read in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/ROADMAP_1_0.md
5. docs/PACK_SPEC.md
6. docs/FOUNDRY_SPEC.md
7. docs/RUNTIME_SPEC.md
8. docs/SPRINT_012.md
9. AGENTS.md
10. CODEX.md

Implement Sprint 012 only.

Goal:
Update Runtime Knowledge loading so documents under docs/**/*.md are discovered safely.

Before modifying files:

- inspect current Knowledge loading behavior
- inspect Search behavior
- inspect Operator Memory path handling
- inspect Foundry validation behavior
- produce an implementation plan only

The plan must include:

- current Runtime document discovery flow
- recursive loading strategy
- path stability strategy
- Search impact
- Operator Memory impact
- rollback plan
- testing strategy

Constraints:

- Preserve existing top-level document behavior.
- Preserve Search.
- Preserve Favorites, Recent Documents, and Reading Position.
- Do not redesign the Knowledge UI.
- Do not add folder browsing UI.
- Do not modify boot scripts.
- Do not commit automatically.

Stop after presenting the implementation plan.