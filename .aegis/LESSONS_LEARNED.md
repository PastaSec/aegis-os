# AEGIS OS Lessons Learned

## Sprint 001 — Field Terminal Architecture

- Preserve boot flow during refactors.
- Keep `dashboard.py` as a compatibility shell until the new architecture is fully proven.
- Extract one layer at a time.
- Validate on Windows and Raspberry Pi.
- PiTFT verification is mandatory before tagging.

## Sprint 002 — Theme System

- Theme architecture should sit below widgets.
- Preserve exact operator appearance before adding visual variation.
- Runtime theme switching should be deferred until the base theme layer is stable.
- Small, focused sprints reduce risk.