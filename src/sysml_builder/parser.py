from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .models import ParsedDocument, RequirementEntry, UseCaseEntry
from .profile_runtime import load_case_profiles


def infer_case_id(path: Path, text: str) -> str:
    stem = path.stem
    case_profiles = load_case_profiles()
    for case_id in sorted(case_profiles, key=len, reverse=True):
        if stem.startswith(case_id):
            return case_id
    case_metadata_path = path.with_name("case.yaml")
    if case_metadata_path.is_file():
        if path.parent.name in {"input", "output"}:
            return path.parent.parent.name
        return path.parent.name
    for case_id, profile in case_profiles.items():
        meta = profile["document"]
        if meta["document_name"] in text or meta["document_name_ja"] in text:
            return case_id
    raise ValueError(f"Unsupported input document: {path}")


def _parse_requirement_bullets(text: str, section: str) -> list[RequirementEntry]:
    entries: list[RequirementEntry] = []
    pattern = re.compile(
        r"^\s*(?:-|\d+\.)\s+(?:\[(?P<bracket>[A-Z0-9\-]+)\]|(?P<plain>[A-Z0-9\-]+):)\s+(?P<body>.+?)\s*$",
        re.M,
    )
    for match in pattern.finditer(text):
        entries.append(
            RequirementEntry(
                identifier=(match.group("bracket") or match.group("plain")).strip(),
                text=match.group("body").strip(),
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


def _extract_section_text(text: str, headings: tuple[str, ...]) -> str:
    pattern = r"^##\s+(?P<heading>" + "|".join(re.escape(heading) for heading in headings) + r")\s*$"
    match = re.search(pattern, text, re.M | re.I)
    if not match:
        return ""
    section_start = match.end()
    next_heading = re.search(r"^##\s+.+$", text[section_start:], re.M | re.I)
    section_end = section_start + next_heading.start() if next_heading else len(text)
    return text[section_start:section_end].strip()


def _first_present_section(text: str, section_groups: tuple[tuple[str, ...], ...]) -> str:
    for headings in section_groups:
        section_text = _extract_section_text(text, headings)
        if section_text:
            return section_text
    return ""


def _load_case_metadata(path: Path) -> dict[str, Any] | None:
    case_metadata_path = path.with_name("case.yaml")
    if not case_metadata_path.is_file():
        return None
    payload = yaml.safe_load(case_metadata_path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _parse_structured_model_case(path: Path, text: str, case_id: str, metadata: dict[str, Any]) -> ParsedDocument:
    language = "ja" if path.name.endswith("_ja.md") else "en"
    title = metadata["title_ja"] if language == "ja" else metadata["title_en"]
    section_name = "要求" if language == "ja" else "Requirements"
    requirements_text = _extract_section_text(text, ("Requirements", "要求"))
    requirements = _parse_requirement_bullets(requirements_text, section_name)
    return ParsedDocument(
        path=path,
        case_id=case_id,
        title=title,
        document={
            "document_id": metadata["id"],
            "document_name": title,
            "language": language,
            "domain": metadata["category"],
        },
        requirements=requirements,
        metadata={"structured_model": metadata["structured_model"]},
    )


def _parse_generic_case(path: Path, text: str, case_id: str, metadata: dict[str, Any]) -> ParsedDocument:
    language = "ja" if path.name.endswith("_ja.md") else "en"
    title = metadata["title_ja"] if language == "ja" else metadata["title_en"]
    context = _extract_section_text(text, ("Context", "背景")).strip()
    section_name = "要求" if language == "ja" else "Requirements"
    requirements_text = _first_present_section(
        text,
        (
            ("Requirements", "要求"),
            ("Functional Requirements", "機能要求"),
        ),
    )
    requirements = _parse_requirement_bullets(requirements_text, section_name)

    document: dict[str, Any] = {
        "document_id": metadata["id"],
        "document_name": title,
        "language": language,
        "domain": metadata["category"],
    }

    return ParsedDocument(
        path=path,
        case_id=case_id,
        title=title,
        document=document,
        requirements=requirements,
        metadata={
            "generic_case": {
                "package": metadata["package"],
                "context": context,
                "requirements_count": metadata["requirements_count"],
                "structure": metadata["structure_ja"] if language == "ja" else metadata["structure_en"],
                "interfaces": metadata["interfaces"],
                "part_ports": metadata["part_ports"],
                "subparts": metadata["subparts"],
                "interfaces_defs": metadata["interfaces_defs"],
                "state_machine": metadata.get("state_machine"),
            }
        },
    )


def parse_markdown(path: Path) -> ParsedDocument:
    text = path.read_text(encoding="utf-8")
    case_id = infer_case_id(path, text)
    case_metadata = _load_case_metadata(path)
    if case_metadata and case_metadata.get("profile_type") == "structured_model_v1":
        return _parse_structured_model_case(path, text, case_id, case_metadata)
    case_profiles = load_case_profiles()
    if case_id not in case_profiles:
        if case_metadata:
            return _parse_generic_case(path, text, case_id, case_metadata)
        raise ValueError(f"Unsupported input document: {path}")
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_match.group(1).strip() if title_match else case_id
    meta = case_profiles[case_id]["document"]
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
    requirements_text = _first_present_section(
        text,
        (
            ("Requirements", "要求"),
            ("Functional Requirements", "機能要求"),
            ("Narrative requirements", "記述要求"),
        ),
    )
    if requirements_text:
        section_name = "要求" if document["language"] == "ja" else "Requirements"
        requirements = _parse_requirement_bullets(requirements_text, section_name)
    elif _first_present_section(text, (("Use Cases", "ユースケース"), ("Operational objectives", "運用目的"))):
        use_cases = _parse_use_cases(text)
    return ParsedDocument(
        path=path,
        case_id=case_id,
        title=title,
        document=document,
        requirements=requirements,
        use_cases=use_cases,
    )
