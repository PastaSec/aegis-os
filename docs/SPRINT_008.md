# AEGIS OS
# Sprint 008
## Knowledge Ingestion Pipeline

Version: v0.8.0-alpha

---

# Sprint Goal

Create the first AEGIS Foundry ingestion pipeline.

Foundry should be able to import plain text and Markdown source folders into Runtime-ready Knowledge Packs.

---

# Objectives

Add source-folder ingestion.

Support Markdown and TXT inputs.

Generate Knowledge Pack structure.

Generate manifest.yaml.

Generate document front matter where practical.

Validate generated packs.

Keep Runtime unchanged.

---

# Supported Inputs

- .md
- .markdown
- .txt

Source folders may contain nested directories.

---

# CLI

Add:

```text
python -m tools.aegis_foundry.cli import-folder <source> <pack_id>