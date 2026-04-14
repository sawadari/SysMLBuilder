from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

from .v1_projector import V1ProjectionModel


def build_sidecar_request(projection: V1ProjectionModel, target: str) -> dict[str, Any]:
    return {
        "request_version": "sysml_v1_sidecar_request_v1alpha1",
        "target": target,
        "projection_profile": projection.projection_profile,
        "model": projection.to_dict(),
    }


def write_sidecar_request(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def invoke_sidecar_cli(command: list[str], request_path: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*command, "--input", str(request_path), "--output", str(output_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
