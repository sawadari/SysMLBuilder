from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports" / "sysml_syntax_validation.yaml"


def discover_sysml_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.sysml"))


def validate_file(tool_jar: Path, sysml_file: Path) -> tuple[bool, str]:
    completed = subprocess.run(
        ["java", "-jar", str(tool_jar), "-nc", "-i", str(sysml_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SysML files with the MontiCore SysML v2 parser in parse-only mode.")
    parser.add_argument("--tool-jar", type=Path, required=True, help="Path to MCSysMLv2.jar")
    parser.add_argument("--root", type=Path, default=ROOT / "testdata", help="Root directory to scan for .sysml files")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="YAML report output path")
    parser.add_argument("--jobs", type=int, default=8, help="Number of parallel Java parser processes")
    args = parser.parse_args()

    files = discover_sysml_files(args.root)
    results: list[dict[str, object]] = []
    failures = 0

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as executor:
        future_map = {executor.submit(validate_file, args.tool_jar, sysml_file): sysml_file for sysml_file in files}
        for future in as_completed(future_map):
            sysml_file = future_map[future]
            ok, output = future.result()
            if not ok:
                failures += 1
            results.append(
                {
                    "file": str(sysml_file),
                    "status": "ok" if ok else "error",
                    "output": output,
                }
            )

    results.sort(key=lambda entry: str(entry["file"]))

    report = {
        "tool_jar": str(args.tool_jar),
        "root": str(args.root),
        "file_count": len(files),
        "failure_count": failures,
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"file_count: {len(files)}")
    print(f"failure_count: {failures}")
    print(f"report: {args.report}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
