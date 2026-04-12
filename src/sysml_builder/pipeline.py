from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .parser import parse_markdown
from .renderer import render_canonical, render_overlay, render_projection_manifest
from .transformer import build_contracts


@dataclass
class TransformResult:
    case_id: str
    contracts: dict[str, Any]
    canonical: str | None
    overlay: str | None
    projection_manifest: dict[str, Any] | None


def transform_markdown(path: Path) -> TransformResult:
    parsed = parse_markdown(path)
    contracts = build_contracts(parsed)
    return TransformResult(
        case_id=parsed.case_id,
        contracts=contracts,
        canonical=render_canonical(parsed.case_id, contracts),
        overlay=render_overlay(parsed.case_id, contracts),
        projection_manifest=render_projection_manifest(parsed.case_id),
    )


def write_result(result: TransformResult, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    contracts_path = output_dir / f"{result.case_id}_contracts.yaml"
    contracts_path.write_text(yaml.safe_dump(result.contracts, sort_keys=False, allow_unicode=True), encoding="utf-8")
    written.append(contracts_path)

    if result.canonical:
        canonical_path = output_dir / f"{result.case_id}_canonical.sysml"
        canonical_path.write_text(result.canonical, encoding="utf-8")
        written.append(canonical_path)

    if result.overlay:
        overlay_path = output_dir / f"{result.case_id}_review_overlay.sysml"
        overlay_path.write_text(result.overlay, encoding="utf-8")
        written.append(overlay_path)

    if result.projection_manifest:
        manifest_path = output_dir / f"{result.case_id}_projection_manifest.yaml"
        manifest_path.write_text(yaml.safe_dump(result.projection_manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
        written.append(manifest_path)

    return written
