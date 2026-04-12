from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import transform_markdown, write_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transform Markdown requirements into Requirement Contract based SysML artifacts.")
    parser.add_argument("input", type=Path, help="Input markdown file")
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("out"), help="Output directory")
    parser.add_argument(
        "--sysml-v1-xmi",
        choices=("cameo", "ea"),
        nargs="+",
        default=(),
        help="Also emit SysML v1 XMI for the selected target(s).",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = transform_markdown(args.input)
    for path in write_result(result, args.output_dir, tuple(args.sysml_v1_xmi)):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
