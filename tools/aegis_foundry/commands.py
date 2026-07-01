from __future__ import annotations

import argparse
from pathlib import Path

from tools.aegis_foundry.index import write_index
from tools.aegis_foundry.ingest import ImportResult, options_from_args, import_folder
from tools.aegis_foundry.pack import discover_packs, resolve_pack_path
from tools.aegis_foundry.validate import validate_pack, validate_path


def format_list(packs) -> str:
    if not packs:
        return "No Knowledge Packs found."

    lines = ["Knowledge Packs:"]
    for pack in packs:
        manifest = pack.manifest
        if manifest:
            lines.append(f"- {manifest.pack_id or pack.path.name}: {manifest.name} ({manifest.version})")
        else:
            lines.append(f"- {pack.path.name}: manifest unavailable")
    return "\n".join(lines)


def command_list_packs(args: argparse.Namespace) -> int:
    packs = discover_packs(args.path)
    print(format_list(packs))
    return 0


def command_inspect_pack(args: argparse.Namespace) -> int:
    pack_path = resolve_pack_path(args.pack)
    packs = discover_packs(pack_path)
    if not packs:
        print(f"ERROR: {Path(args.pack)}: Knowledge Pack not found")
        return 1

    pack = packs[0]
    manifest = pack.manifest
    print(f"Pack: {manifest.name if manifest else pack.path.name}")
    print(f"Path: {pack.path}")
    if manifest:
        print(f"ID: {manifest.pack_id}")
        print(f"Version: {manifest.version}")
        if manifest.status:
            print(f"Status: {manifest.status}")
        if manifest.license:
            print(f"License: {manifest.license}")
        print(f"Description: {manifest.description}")
        print(f"Categories: {', '.join(manifest.categories) if manifest.categories else 'None'}")
        print(f"Tags: {', '.join(manifest.tags) if manifest.tags else 'None'}")
    else:
        print("Manifest: unavailable")
    print(f"Documents: {len(pack.documents)}")

    report = validate_pack(pack)
    if report.errors or report.warnings:
        print(report.render())
    else:
        print("Validation: OK")
    return 1 if report.has_errors else 0


def command_generate_index(args: argparse.Namespace) -> int:
    packs = discover_packs(args.path)
    if not packs:
        target = args.path if args.path else "knowledge/packs"
        print(f"ERROR: {target}: no Knowledge Packs found")
        return 1

    for pack in packs:
        index_path = write_index(pack)
        print(f"Index written: {index_path} ({len(pack.documents)} documents)")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    report = validate_path(args.path)
    print(report.render())
    return 1 if report.has_errors else 0


def command_import_folder(args: argparse.Namespace) -> int:
    result = import_folder(options_from_args(args))
    print_import_summary(result)
    return 1 if result.has_errors else 0


def print_import_summary(result: ImportResult) -> None:
    if result.errors:
        mode = "FAILED"
    elif result.dry_run:
        mode = "DRY RUN"
    else:
        mode = "COMPLETE"
    print(f"Import {mode}")
    print(f"Source: {result.source}")
    print(f"Pack: {result.pack_path}")
    print(f"Documents: {len(result.imported)}")

    for item in result.imported:
        print(f"- {item.source} -> {item.output}")

    for path in result.skipped:
        print(f"Skipped: {path}")

    for error in result.errors:
        print(f"ERROR: {error}")

    if result.validation:
        print(result.validation.render())
    elif result.dry_run and not result.errors:
        print("Validation: skipped for dry run")
