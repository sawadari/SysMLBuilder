from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


PACK_ROOT = ROOT / "testdata" / "SysMLBuilder_testdata_20cases"
REPORT_PATH = ROOT / "reports" / "compatibility_20cases.yaml"


def build_report() -> dict:
    manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    cases: list[dict] = []
    supported = 0

    for case in manifest["cases"]:
        case_dir = PACK_ROOT / case["path"]
        checks = []
        case_supported = True

        for language in ("en", "ja"):
            requirement_path = case_dir / f"requirements_{language}.md"
            expected_path = case_dir / f"expected_{language}.sysml"
            try:
                result = transform_markdown(requirement_path)
                expected = expected_path.read_text(encoding="utf-8")
                exact_match = result.canonical == expected
                checks.append(
                    {
                        "language": language,
                        "status": "matched" if exact_match else "mismatch",
                        "detected_case_id": result.case_id,
                        "exact_match": exact_match,
                    }
                )
                case_supported = case_supported and exact_match
            except Exception as exc:  # pragma: no cover - exercised by the compatibility probe itself
                case_supported = False
                checks.append(
                    {
                        "language": language,
                        "status": "unsupported",
                        "error_type": type(exc).__name__,
                        "message": str(exc),
                    }
                )

        if case_supported:
            supported += 1

        cases.append(
            {
                "id": case["id"],
                "slug": case["slug"],
                "category": case["category"],
                "supported_in_current_transformer": case_supported,
                "checks": checks,
            }
        )

    return {
        "pack_name": "SysMLBuilder_testdata_20cases",
        "case_count": manifest["case_count"],
        "supported_cases": supported,
        "unsupported_cases": manifest["case_count"] - supported,
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check current SysMLBuilder compatibility with the 20-case external pack.")
    parser.add_argument("--fail-on-unsupported", action="store_true", help="Exit non-zero when at least one case is unsupported.")
    args = parser.parse_args()

    report = build_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"pack: {report['pack_name']}")
    print(f"cases: {report['case_count']}")
    print(f"supported_cases: {report['supported_cases']}")
    print(f"unsupported_cases: {report['unsupported_cases']}")
    print(f"report: {REPORT_PATH}")

    if args.fail_on_unsupported and report["unsupported_cases"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
