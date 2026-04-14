from __future__ import annotations

import argparse
from pathlib import Path

from .common_ir import build_common_ir
from .parser import parse_markdown
from .renderer import render_projection_manifest
from .sidecar import build_sidecar_request, write_sidecar_request
from .transformer import build_contracts
from .v1_projector import project_to_sysml_v1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit Common IR and SysML v1 sidecar payloads.")
    parser.add_argument("input", type=Path, help="Input markdown file")
    parser.add_argument("--target", choices=("cameo", "ea"), required=True, help="SysML v1 target profile")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output payload file (.yaml or .json)")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    parsed = parse_markdown(args.input)
    contracts = build_contracts(parsed)
    projection_manifest = render_projection_manifest(parsed.case_id)
    common_ir = build_common_ir(parsed, contracts, projection_manifest)
    projection = project_to_sysml_v1(common_ir)
    request = build_sidecar_request(projection, args.target)
    write_sidecar_request(request, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
