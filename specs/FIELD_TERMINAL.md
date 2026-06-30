# AEGIS OS v0.2 — Field Terminal

AEGIS OS is designed as an offline-first field appliance.

It should feel less like a Linux computer and more like dedicated equipment:
a GPS unit, field radio, aircraft display, or emergency operations terminal.

## Design Rules

1. Offline first.
2. Three keystrokes maximum to reach critical information.
3. No Linux exposure in normal operation.
4. Everything searchable.
5. Consistent navigation everywhere.

## Navigation Standard

- Up / Down: Move
- Enter: Open
- Esc: Return
- /: Search
- R: Refresh
- Q: Standby

## Home Screen Philosophy

The home screen should show missions, not diagnostics.

Primary missions:

- Knowledge
- Journal
- Inventory
- Communications
- Navigation
- Hardware
- System

Diagnostics belong under Hardware.

System maintenance belongs under System.

## Product Identity

AEGIS OS should present itself as a dedicated field terminal.

The boot sequence should be:

1. AEGIS logo
2. System initialization checks
3. Mission Ready
4. Home screen

The operator should never need to know that Linux, Python, or Textual is underneath.
