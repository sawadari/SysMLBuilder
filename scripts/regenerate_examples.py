from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "example"
TOOL_JAR = ROOT / "tools" / "MCSysMLv2.jar"

sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


GENERATED_SUFFIXES = {
    "contracts": "contracts.yaml",
    "canonical": "canonical.sysml",
    "overlay": "review_overlay.sysml",
    "guide": "cameo_display_guide.md",
    "projection_manifest": "projection_manifest.yaml",
}


def _language_label(path: Path) -> str:
    if path.name.endswith("_en.md"):
        return "en"
    if path.name.endswith("_ja.md"):
        return "ja"
    return "default"


def _preferred_label(results: dict[str, Any]) -> str:
    for label in ("default", "en", "ja"):
        if label in results:
            return label
    return next(iter(results))


def _dump_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _write_optional_text(path: Path, content: str | None) -> bool:
    if content is None:
        if path.exists():
            path.unlink()
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _write_optional_yaml(path: Path, payload: dict[str, Any] | None) -> bool:
    if payload is None:
        if path.exists():
            path.unlink()
        return False
    _dump_yaml(path, payload)
    return True


def _write_generated_outputs(result: Any, output_dir: Path, label: str) -> None:
    prefix = f"generated_{label}"
    _dump_yaml(output_dir / f"{prefix}_{GENERATED_SUFFIXES['contracts']}", result.contracts)
    _write_optional_text(output_dir / f"{prefix}_{GENERATED_SUFFIXES['canonical']}", result.canonical)
    _write_optional_text(output_dir / f"{prefix}_{GENERATED_SUFFIXES['overlay']}", result.overlay)
    _write_optional_text(output_dir / f"{prefix}_{GENERATED_SUFFIXES['guide']}", result.cameo_display_guide)
    _write_optional_yaml(output_dir / f"{prefix}_{GENERATED_SUFFIXES['projection_manifest']}", result.projection_manifest)


def _write_primary_outputs(result: Any, output_dir: Path, case_id: str) -> None:
    _dump_yaml(output_dir / f"{case_id}_{GENERATED_SUFFIXES['contracts']}", result.contracts)
    _write_optional_text(output_dir / f"{case_id}_{GENERATED_SUFFIXES['canonical']}", result.canonical)
    _write_optional_text(output_dir / f"{case_id}_{GENERATED_SUFFIXES['overlay']}", result.overlay)
    _write_optional_text(output_dir / f"{case_id}_{GENERATED_SUFFIXES['guide']}", result.cameo_display_guide)
    _write_optional_yaml(output_dir / f"{case_id}_{GENERATED_SUFFIXES['projection_manifest']}", result.projection_manifest)


def _write_expected_outputs(result: Any, output_dir: Path, label: str, case_name: str) -> None:
    legacy_sysml = output_dir / f"expected_{label}.sysml"
    if legacy_sysml.exists() and result.canonical is not None:
        legacy_sysml.write_text(result.canonical, encoding="utf-8")

    canonical_path = output_dir / f"expected_{label}_{GENERATED_SUFFIXES['canonical']}"
    overlay_path = output_dir / f"expected_{label}_{GENERATED_SUFFIXES['overlay']}"
    contracts_path = output_dir / f"expected_{label}_{GENERATED_SUFFIXES['contracts']}"
    manifest_path = output_dir / f"expected_{label}_{GENERATED_SUFFIXES['projection_manifest']}"

    should_write_expected_bundle = case_name.startswith("case") or contracts_path.exists() or canonical_path.exists() or overlay_path.exists() or manifest_path.exists()

    if not should_write_expected_bundle:
        return

    _dump_yaml(contracts_path, result.contracts)
    _write_optional_text(canonical_path, result.canonical)
    _write_optional_text(overlay_path, result.overlay)
    _write_optional_yaml(manifest_path, result.projection_manifest)


def _validate_output_dir(output_dir: Path, report_path: Path, tool_jar: Path) -> None:
    sysml_files = sorted(output_dir.glob("*.sysml"))
    results: list[dict[str, Any]] = []
    failures = 0
    for sysml_file in sysml_files:
        completed = subprocess.run(
            ["java", "-jar", str(tool_jar), "-nc", "-i", str(sysml_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = (completed.stdout + completed.stderr).strip()
        if completed.returncode != 0:
            failures += 1
        results.append(
            {
                "file": str(sysml_file.relative_to(ROOT)),
                "status": "ok" if completed.returncode == 0 else "error",
                "output": output,
            }
        )
    report = {
        "tool_jar": str(tool_jar.relative_to(ROOT)),
        "root": str(output_dir.relative_to(ROOT)),
        "file_count": len(sysml_files),
        "failure_count": failures,
        "results": results,
    }
    _dump_yaml(report_path, report)


def regenerate_case(case_dir: Path, tool_jar: Path) -> None:
    input_dir = case_dir / "input"
    output_dir = case_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = sorted(input_dir.glob("*.md"))
    results_by_label: dict[str, Any] = {}
    for input_file in input_files:
        label = _language_label(input_file)
        result = transform_markdown(input_file)
        results_by_label[label] = result
        _write_generated_outputs(result, output_dir, label)
        _write_expected_outputs(result, output_dir, label, case_dir.name)

    primary_result = results_by_label[_preferred_label(results_by_label)]
    _write_primary_outputs(primary_result, output_dir, primary_result.case_id)
    _validate_output_dir(output_dir, output_dir / f"{case_dir.name}_syntax.yaml", tool_jar)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate all example outputs and syntax reports.")
    parser.add_argument("--root", type=Path, default=EXAMPLE_ROOT, help="Example root directory")
    parser.add_argument("--tool-jar", type=Path, default=TOOL_JAR, help="Path to MCSysMLv2.jar")
    args = parser.parse_args()

    case_dirs = sorted(path for path in args.root.iterdir() if path.is_dir() and (path / "input").is_dir())
    for case_dir in case_dirs:
        print(f"[regen] {case_dir.name}")
        regenerate_case(case_dir, args.tool_jar)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
