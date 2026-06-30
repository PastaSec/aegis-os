# AEGIS OS
# Architecture Decisions

Version 0.2.0-alpha

---

## ADR-0001

### Title

Offline First

### Status

Accepted

### Date

2026-06-29

### Decision

AEGIS shall remain fully functional without Internet connectivity.

### Rationale

Internet connectivity cannot be assumed during disasters, travel, field operations, or infrastructure failures.

Offline capability is the defining characteristic of AEGIS.

---

## ADR-0002

### Title

Knowledge Stored as Plain Files

### Status

Accepted

### Decision

Knowledge Packs use human-readable files.

### Rationale

Plain files are:

- future proof
- Git friendly
- backup friendly
- easy to edit
- resilient

---

## ADR-0003

### Title

Keyboard First

### Status

Accepted

### Decision

Every capability shall be fully usable from a keyboard.

### Rationale

Supports:

- PiTFT
- SSH
- Serial Console
- Accessibility
- Low-power devices

---

## ADR-0004

### Title

Capability Architecture

### Status

Accepted

### Decision

Major functionality shall be organized as independent capabilities.

Examples:

- Knowledge
- Journal
- Inventory
- Communications
- Navigation
- Hardware
- System

### Rationale

Capabilities reduce coupling and simplify expansion.

---

## ADR-0005

### Title

No Linux Exposure

### Status

Accepted

### Decision

Operators should never be required to understand Linux internals during normal operation.

### Rationale

AEGIS is an appliance.

Linux is an implementation detail.

---

Future architectural decisions shall be added sequentially.