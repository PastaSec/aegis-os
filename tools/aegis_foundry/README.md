# AEGIS Foundry

AEGIS Foundry is the desktop-side tooling layer for preparing AEGIS Knowledge Packs.

The Raspberry Pi Runtime stays lightweight, offline-first, and focused on field operation.

Foundry performs heavier preparation work on a desktop or development machine.

## Current Commands

Run from the repository root.

`powershell
python -m tools.aegis_foundry.cli list-packs
python -m tools.aegis_foundry.cli inspect-pack florida
python -m tools.aegis_foundry.cli validate
