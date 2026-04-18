from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .pipeline import transform_markdown


def _normalized_text(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def _compare_yaml(actual_path: Path, expected_path: Path) -> bool:
    return yaml.safe_load(actual_path.read_text(encoding="utf-8")) == yaml.safe_load(expected_path.read_text(encoding="utf-8"))


def run_suite(root: Path, suite_dir: Path | None = None) -> int:
    cases_root = suite_dir or (root / "example")
    manifest = yaml.safe_load((cases_root / "case_manifest.yaml").read_text(encoding="utf-8"))
    failures = 0
    out_root = root / f".generated_{cases_root.name}"
    out_root.mkdir(exist_ok=True)

    for case in manifest["cases"]:
        case_id = case["case_id"]
        result = transform_markdown(cases_root / case_id / "input" / "requirements_en.md")
        case_out = out_root / case_id
        case_out.mkdir(parents=True, exist_ok=True)

        actual_contracts = case_out / "contracts.yaml"
        actual_contracts.write_text(yaml.safe_dump(result.contracts, sort_keys=False, allow_unicode=True), encoding="utf-8")
        if not _compare_yaml(actual_contracts, cases_root / case_id / "output" / "expected_en_contracts.yaml"):
            print(f"FAIL contracts: {case_id}")
            failures += 1

        if result.canonical:
            actual_canonical = case_out / "canonical.sysml"
            actual_canonical.write_text(result.canonical, encoding="utf-8")
            if _normalized_text(actual_canonical.read_text(encoding="utf-8")) != _normalized_text((cases_root / case_id / "output" / "expected_en_canonical.sysml").read_text(encoding="utf-8")):
                print(f"FAIL canonical: {case_id}")
                failures += 1

        if result.overlay:
            actual_overlay = case_out / "review_overlay.sysml"
            actual_overlay.write_text(result.overlay, encoding="utf-8")
            if _normalized_text(actual_overlay.read_text(encoding="utf-8")) != _normalized_text((cases_root / case_id / "output" / "expected_en_review_overlay.sysml").read_text(encoding="utf-8")):
                print(f"FAIL overlay: {case_id}")
                failures += 1

        if result.projection_manifest:
            actual_projection = case_out / "projection_manifest.yaml"
            actual_projection.write_text(yaml.safe_dump(result.projection_manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
            if not _compare_yaml(actual_projection, cases_root / case_id / "output" / "expected_en_projection_manifest.yaml"):
                print(f"FAIL projection manifest: {case_id}")
                failures += 1

    print("ok" if failures == 0 else "error")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the GFSE strict suite against the local transformer.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--suite-dir", type=Path, default=None, help="Suite directory to execute")
    args = parser.parse_args()
    return run_suite(args.root, args.suite_dir)


if __name__ == "__main__":
    raise SystemExit(main())
