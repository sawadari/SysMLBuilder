#!/usr/bin/env python3
from pathlib import Path
import yaml, re, sys

ROOT = Path(__file__).resolve().parents[1]
manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
cases = manifest["cases"]

errors = []
warnings = []
for case in cases:
    case_dir = ROOT / case["path"]
    expected = ["requirements_en.md", "requirements_ja.md", "expected_en.sysml", "expected_ja.sysml", "case.yaml"]
    for name in expected:
        if not (case_dir / name).exists():
            errors.append(f"{case['id']}: missing {name}")
    if not (case_dir / "case.yaml").exists():
        continue
    meta = yaml.safe_load((case_dir / "case.yaml").read_text(encoding="utf-8"))
    pkg = meta.get("package")
    req_count = meta.get("requirements_count", 0)
    for sysml_name in ["expected_en.sysml", "expected_ja.sysml"]:
        path = case_dir / sysml_name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if f"package {pkg} " not in text and f"package {pkg}{{" not in text and f"package {pkg} {{" not in text:
            errors.append(f"{case['id']}: package name mismatch in {sysml_name}")
        found_reqs = len(re.findall(r'\brequirement def\b', text))
        if found_reqs != req_count:
            errors.append(f"{case['id']}: requirement count mismatch in {sysml_name} ({found_reqs} != {req_count})")
        if "part systemUnderTest :" not in text:
            errors.append(f"{case['id']}: missing systemUnderTest in {sysml_name}")
        if "doc /*" not in text:
            errors.append(f"{case['id']}: missing doc block in {sysml_name}")
        if "port def" not in text:
            warnings.append(f"{case['id']}: no port def in {sysml_name}")
        # basic brace balance
        if text.count("{") != text.count("}"):
            errors.append(f"{case['id']}: brace mismatch in {sysml_name}")

report = {
    "case_count": len(cases),
    "errors": errors,
    "warnings": warnings,
    "status": "ok" if not errors else "ng",
}
out = ROOT / "reports"
out.mkdir(exist_ok=True)
(out / "validation_report.yaml").write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
print(yaml.safe_dump(report, sort_keys=False, allow_unicode=True))
sys.exit(0 if not errors else 1)
