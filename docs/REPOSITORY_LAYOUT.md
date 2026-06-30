# AEGIS OS Repository Layout

Version: 1.0

---

# Philosophy

The repository should be understandable within five minutes.

Directory names should communicate intent.

Structure should prioritize discoverability over cleverness.

---

# Root

```
aegis-os/

aegis/
assets/
community/
docs/
examples/
hardware/
inventory/
journal/
knowledge/
logs/
plugins/
reference/
scripts/
specs/
systemd/
tests/
tools/

README.md
CHANGELOG.md
LICENSE
NOTICE
```

---

# aegis/

Core application.

Contains all executable software.

Future layout:

```
core/
screens/
widgets/
services/
themes/
models/
capabilities/
```

---

# assets/

Images

Icons

Logos

Fonts

Audio

Branding

---

# community/

Community-created content.

Examples:

```
cert/

ham-radio/

medical/

preparedness/

templates/
```

---

# docs/

Project documentation.

```
architecture/

adr/

guides/

knowledge-packs/

hardware/

sprints/
```

---

# examples/

Example plugins.

Example packs.

Example configurations.

Reference implementations.

---

# hardware/

Everything physical.

```
bom/

cad/

enclosures/

pcb/

schematics/

stl/

wiring/
```

---

# inventory/

Sample inventory database.

Templates.

---

# journal/

Sample journals.

Templates.

---

# knowledge/

Official Knowledge Packs.

```
packs/

templates/

schemas/
```

---

# plugins/

Optional capabilities.

Future examples:

GPS

Weather

Camera

Meshtastic

APRS

Maps

---

# reference/

Engineering references.

Developer-facing only.

Never displayed to operators.

Examples:

Datasheets

Protocols

Specifications

Hardware manuals

---

# scripts/

Utilities.

Migration scripts.

Maintenance.

Deployment.

---

# specs/

Engineering specifications.

Product requirements.

Module specs.

Design standards.

---

# tests/

Unit tests.

Integration tests.

Hardware validation.

---

# tools/

Developer utilities.

Generators.

Importers.

Converters.

Pack builders.

---

# Guiding Rule

A contributor should always know where a file belongs.

If uncertainty exists:

Improve the structure.

Never add confusion.

---

Prepared Together.