from __future__ import annotations

import argparse
from pathlib import Path

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


def command_validate(args: argparse.Namespace) -> int:
    report = validate_path(args.path)
    print(report.render())
    return 1 if report.has_errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aegis-foundry", description="AEGIS Foundry Knowledge Pack tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-packs", help="List Knowledge Packs")
    list_parser.add_argument("path", nargs="?", default=None, help="Optional pack root path")
    list_parser.set_defaults(func=command_list_packs)

    inspect_parser = subparsers.add_parser("inspect-pack", help="Inspect one Knowledge Pack")
    inspect_parser.add_argument("pack", help="Pack directory or pack id")
    inspect_parser.set_defaults(func=command_inspect_pack)

    validate_parser = subparsers.add_parser("validate", help="Validate Knowledge Packs")
    validate_parser.add_argument("path", nargs="?", default=None, help="Optional pack root or pack path")
    validate_parser.set_defaults(func=command_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
