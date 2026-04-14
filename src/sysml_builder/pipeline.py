from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .parser import parse_markdown
from .common_ir import CommonIrModel, build_common_ir
from .renderer import render_canonical, render_overlay, render_projection_manifest
from .v1_projector import V1ProjectionModel, project_to_sysml_v1
from .transformer import build_contracts
from .xmi import generate_sysml_v1_xmi


@dataclass
class TransformResult:
    case_id: str
    contracts: dict[str, Any]
    canonical: str | None
    overlay: str | None
    projection_manifest: dict[str, Any] | None
    common_ir: CommonIrModel
    v1_projection: V1ProjectionModel
    sysml_v1_xmi: dict[str, str]


def transform_markdown(path: Path) -> TransformResult:
    parsed = parse_markdown(path)
    contracts = build_contracts(parsed)
    canonical = render_canonical(parsed.case_id, contracts)
    projection_manifest = render_projection_manifest(parsed.case_id)
    common_ir = build_common_ir(parsed, contracts, projection_manifest)
    v1_projection = project_to_sysml_v1(common_ir)
    sysml_v1_xmi = {}
    if canonical:
        for target in ("cameo", "ea"):
            sysml_v1_xmi[target] = generate_sysml_v1_xmi(canonical, target, projection_manifest=projection_manifest)
    return TransformResult(
        case_id=parsed.case_id,
        contracts=contracts,
        canonical=canonical,
        overlay=render_overlay(parsed.case_id, contracts),
        projection_manifest=projection_manifest,
        common_ir=common_ir,
        v1_projection=v1_projection,
        sysml_v1_xmi=sysml_v1_xmi,
    )


def write_result(result: TransformResult, output_dir: Path, xmi_targets: tuple[str, ...] = ()) -> list[Path]:
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

    for target in xmi_targets:
        xmi = result.sysml_v1_xmi.get(target)
        if not xmi:
            continue
        xmi_path = output_dir / f"{result.case_id}_{target}_v1.xmi"
        xmi_path.write_text(xmi, encoding="utf-8")
        written.append(xmi_path)

    return written
