from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import generate_japanese_suite
from sysml_builder.pipeline import transform_markdown
from sysml_builder.renderer import JA_RENDER_REPLACEMENTS


def _replacement_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for replacements in generate_japanese_suite.FILE_REPLACEMENTS.values():
        pairs.extend((target, source) for source, target in replacements)
    pairs.extend((target, source) for source, target in generate_japanese_suite.GLOBAL_REPLACEMENTS)
    pairs.extend((target, source) for source, target in JA_RENDER_REPLACEMENTS)
    return pairs


def _normalize_text(text: str) -> str:
    for source, target in _replacement_pairs():
        text = text.replace(source, target)
    return text.replace("\r\n", "\n").strip()


def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        normalized = {}
        for key, item in value.items():
            if key == "language":
                normalized[key] = "en"
            elif key in {"objective_text", "rationale"}:
                normalized[key] = "<localized-text>"
            elif key == "evidence" and isinstance(item, dict):
                normalized[key] = {"quote": "<localized-text>"}
            elif key in {"main_flow_steps", "exception_flow_steps"} and isinstance(item, list):
                normalized[key] = {"count": len(item)}
            elif key == "document_name":
                normalized[key] = _normalize_text(str(item))
            else:
                normalized[key] = _normalize_value(item)
        return normalized
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, str):
        return _normalize_text(value)
    return value


def main() -> int:
    generate_japanese_suite.main()
    en_root = ROOT / "testdata" / "gfse_derived"
    ja_root = ROOT / "testdata" / "gfse_derived_ja"
    case_ids = sorted(path.name.replace("_requirements.md", "") for path in en_root.glob("*_requirements.md"))
    failures = 0

    for case_id in case_ids:
        en_result = transform_markdown(en_root / f"{case_id}_requirements.md")
        ja_result = transform_markdown(ja_root / f"{case_id}_requirements.md")

        if _normalize_value(ja_result.contracts) != _normalize_value(en_result.contracts):
            print(f"FAIL contracts: {case_id}")
            failures += 1

        if _normalize_value(ja_result.projection_manifest) != _normalize_value(en_result.projection_manifest):
            print(f"FAIL projection manifest: {case_id}")
            failures += 1

        if _normalize_text(ja_result.canonical or "") != _normalize_text(en_result.canonical or ""):
            print(f"FAIL canonical: {case_id}")
            failures += 1

        if _normalize_text(ja_result.overlay or "") != _normalize_text(en_result.overlay or ""):
            print(f"FAIL overlay: {case_id}")
            failures += 1

    print("ok" if failures == 0 else "error")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
