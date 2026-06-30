# Codex Prompt — Sprint 001

You are contributing to AEGIS OS.

Before making any code changes, read these files in order:

1. .aegis/CONSTITUTION.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/DECISIONS.md
5. docs/ROADMAP_1_0.md
6. docs/REPOSITORY_LAYOUT.md
7. docs/adr/ADR-0006-MONOREPOSITORY.md
8. AGENTS.md
9. CODEX.md
10. docs/SPRINT_001.md

Your task is Sprint 001 only.

Do not implement new features.
Do not redesign the product.
Do not change the boot flow.
Do not remove existing behavior.
Do not break PiTFT compatibility.
Do not remove Knowledge, Journal, Inventory, Search, Hardware, or appliance startup behavior.

Use “Capabilities,” not “modules,” in all new architecture, documentation, comments, and user-facing language unless preserving an existing filename for compatibility.

First, inspect the repository and produce an implementation plan.

The plan must include:

- current architecture summary
- proposed file structure
- migration steps
- risk areas
- rollback plan
- proposed commit sequence
- tests to run after each step

Do not modify files until the plan has been presented.

After approval, execute Sprint 001 in small logical commits.

Acceptance criteria:

- python -m py_compile aegis/*.py passes
- application launches with aegis
- PiTFT appliance mode still works
- Knowledge opens
- Journal opens
- Inventory opens
- Hardware opens
- Search still works
- home screen remains mission-focused
- dashboard rendering is moved out of a monolithic file
- router/screen/widget/theme architecture exists
- main branch remains bootable