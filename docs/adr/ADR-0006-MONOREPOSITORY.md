# ADR-0006
# Monorepository Architecture

Status: Accepted

Date: 2026-06-29

---

## Context

As AEGIS OS evolves, the project will encompass far more than application source code.

The repository will contain:

- Core software
- Documentation
- Knowledge Packs
- Community content
- Hardware designs
- 3D printable enclosures
- Wiring diagrams
- PCB designs
- Development utilities
- Tests
- Build scripts
- Engineering specifications

One option is to separate these into multiple repositories.

Another is to maintain a single monorepository.

---

## Decision

AEGIS OS shall use a **single Git monorepository**.

Logical separation will be achieved through directory structure rather than multiple repositories.

The repository shall remain the authoritative source for all project assets.

---

## Rationale

A single repository provides:

- One clone
- One issue tracker
- One project board
- One release history
- One documentation source
- One contributor workflow

Contributors should be able to clone one repository and immediately begin contributing.

---

## Benefits

### Simplicity

No repository synchronization.

No dependency confusion.

No cross-repository version mismatch.

---

### Discoverability

Developers can easily locate:

- documentation
- hardware
- plugins
- knowledge packs
- examples

without changing repositories.

---

### Shared Versioning

Documentation, hardware, and software evolve together.

Every release represents a complete snapshot of AEGIS.

---

### Community

New contributors only need one URL.

This reduces onboarding friction.

---

## Tradeoffs

The repository will become larger over time.

This is considered acceptable.

Repository organization is preferred over repository fragmentation.

---

## Repository Philosophy

Everything required to understand, build, deploy, document, and extend AEGIS belongs in one place.

---

## Consequences

Future additions should create directories rather than repositories whenever practical.

Examples include:

Community Knowledge Packs

Hardware

Examples

Documentation

Reference Material

Engineering Specifications

---

Accepted.

Prepared Together.