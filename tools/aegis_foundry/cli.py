from __future__ import annotations

import argparse

from tools.aegis_foundry.commands import (
    command_generate_index,
    command_import_folder,
    command_inspect_pack,
    command_list_packs,
    command_validate,
)


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

    import_parser = subparsers.add_parser("import-folder", help="Import TXT and Markdown sources into a pack")
    import_parser.add_argument("source", help="Source folder containing .txt, .md, or .markdown files")
    import_parser.add_argument("pack_id", help="Output Knowledge Pack id")
    import_parser.add_argument("--output", default=None, help="Output pack root; defaults to knowledge/packs")
    import_parser.add_argument("--name", default="", help="Pack display name")
    import_parser.add_argument("--description", default="", help="Pack description")
    import_parser.add_argument("--category", default="General", help="Generated category")
    import_parser.add_argument("--tag", default="imported", help="Generated tag")
    import_parser.add_argument("--overwrite", action="store_true", help="Replace existing output pack")
    import_parser.add_argument("--dry-run", action="store_true", help="Show planned import without writing files")
    import_parser.set_defaults(func=command_import_folder)

    index_parser = subparsers.add_parser("generate-index", help="Generate index.json for Knowledge Packs")
    index_parser.add_argument("path", nargs="?", default=None, help="Optional pack root or pack path")
    index_parser.set_defaults(func=command_generate_index)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
