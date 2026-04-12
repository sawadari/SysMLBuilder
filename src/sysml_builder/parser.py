from __future__ import annotations

import re
from pathlib import Path

from .models import ParsedDocument, RequirementEntry, UseCaseEntry


CASE_METADATA = {
    "case01_vehicle_explicit_high": {
        "document_id": "GFSE-CASE01",
        "document_name": "Vehicle quantitative and interface requirements",
        "document_name_ja": "車両の定量性能およびインタフェース要求",
        "language": "en",
        "domain": "vehicle_system",
    },
    "case02_vehicle_ambiguous_low": {
        "document_id": "GFSE-CASE02",
        "document_name": "Vehicle ambiguous performance requirements",
        "document_name_ja": "車両の曖昧な性能要求",
        "language": "en",
        "domain": "vehicle_system",
    },
    "case03_mining_contextual_performance_high": {
        "document_id": "GFSE-CASE03",
        "document_name": "Mining frigate contextual performance requirements",
        "document_name_ja": "採掘フリゲートの文脈別性能要求",
        "language": "en",
        "domain": "space_system",
    },
    "case04_mining_modular_interface_high": {
        "document_id": "GFSE-CASE04",
        "document_name": "Mining frigate modular interface requirements",
        "document_name_ja": "採掘フリゲートのモジュラーインタフェース要求",
        "language": "en",
        "domain": "space_system",
    },
    "case05_mining_usecase_medium": {
        "document_id": "GFSE-CASE05",
        "document_name": "Mining frigate operational use cases",
        "document_name_ja": "採掘フリゲートの運用ユースケース",
        "language": "en",
        "domain": "space_system",
    },
    "case06_mining_usecase_ambiguous_low": {
        "document_id": "GFSE-CASE06",
        "document_name": "Mining frigate ambiguous operational narrative",
        "document_name_ja": "採掘フリゲートの曖昧な運用記述",
        "language": "en",
        "domain": "space_system",
    },
}


def infer_case_id(path: Path, text: str) -> str:
    stem = path.stem
    for case_id in CASE_METADATA:
        if stem.startswith(case_id):
            return case_id
    for case_id, meta in CASE_METADATA.items():
        if meta["document_name"] in text or meta["document_name_ja"] in text:
            return case_id
    raise ValueError(f"Unsupported input document: {path}")


def _parse_requirement_bullets(text: str, section: str) -> list[RequirementEntry]:
    entries: list[RequirementEntry] = []
    for match in re.finditer(r"^- ([A-Z0-9\-]+): (.+)$", text, re.M):
        entries.append(
            RequirementEntry(
                identifier=match.group(1).strip(),
                text=match.group(2).strip(),
                section=section,
            )
        )
    return entries


def _parse_use_cases(text: str) -> list[UseCaseEntry]:
    use_cases: list[UseCaseEntry] = []
    pattern = re.compile(
        r"^###\s+(?P<identifier>[A-Z0-9\-]+)\s+(?P<title>.+?)\n"
        r"(?:Main Flow|メインフロー):\n(?P<main>(?:\d+\.\s+.+\n)+)\n"
        r"(?:Exception Flows|例外フロー):\n(?P<exception>(?:- .+\n)+)",
        re.M,
    )
    for match in pattern.finditer(text):
        main_steps = [
            re.sub(r"^\d+\.\s+", "", line).strip()
            for line in match.group("main").strip().splitlines()
        ]
        exception_steps = [
            re.sub(r"^- ", "", line).strip()
            for line in match.group("exception").strip().splitlines()
        ]
        use_cases.append(
            UseCaseEntry(
                identifier=match.group("identifier").strip(),
                title=match.group("title").strip(),
                main_flow_steps=main_steps,
                exception_flow_steps=exception_steps,
            )
        )
    return use_cases


def parse_markdown(path: Path) -> ParsedDocument:
    text = path.read_text(encoding="utf-8")
    case_id = infer_case_id(path, text)
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_match.group(1).strip() if title_match else case_id
    meta = CASE_METADATA[case_id]
    document = {
        "document_id": meta["document_id"],
        "document_name": meta["document_name"],
        "language": meta["language"],
        "domain": meta["domain"],
    }
    if path.as_posix().endswith("_ja.md") or meta["document_name_ja"] in text:
        document["document_name"] = meta["document_name_ja"]
        document["language"] = "ja"
    requirements = []
    use_cases = []
    if "## Requirements" in text or "## 要求" in text:
        requirements = _parse_requirement_bullets(text, "Requirements")
    elif "## Narrative requirements" in text or "## 記述要求" in text:
        requirements = _parse_requirement_bullets(text, "Narrative requirements")
    elif "## Operational objectives" in text or "## 運用目的" in text:
        use_cases = _parse_use_cases(text)
    return ParsedDocument(
        path=path,
        case_id=case_id,
        title=title,
        document=document,
        requirements=requirements,
        use_cases=use_cases,
    )
