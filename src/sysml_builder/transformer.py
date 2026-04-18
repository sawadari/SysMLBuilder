from __future__ import annotations

import re
from typing import Any

from .models import ParsedDocument, RequirementEntry, UseCaseEntry
from .profile_runtime import get_case_profile, load_generic_case_profile


def _base_document_metadata(parsed: ParsedDocument) -> dict[str, Any]:
    return {"document": parsed.document.copy(), "contracts": []}


def _language(parsed: ParsedDocument) -> str:
    return parsed.document.get("language", "en")


def _resolve_language_value(value: Any, language: str) -> Any:
    if isinstance(value, dict) and language in value:
        return value[language]
    return value


def _resolve_capture_regex(capture_spec: dict[str, Any], language: str) -> list[str]:
    regex_spec = _resolve_language_value(capture_spec.get("regex"), language)
    if isinstance(regex_spec, str):
        return [regex_spec]
    return list(regex_spec or [])


def _coerce_capture(value: str, capture_spec: dict[str, Any]) -> Any:
    capture_type = capture_spec.get("type")
    if capture_type == "int":
        return int(value)
    if capture_type == "float":
        return float(value)
    return value


def _extract_captures(text: str, captures_spec: dict[str, Any], language: str) -> dict[str, Any]:
    captures: dict[str, Any] = {}
    pending = dict(captures_spec)

    while pending:
        progressed = False
        for name, spec in list(pending.items()):
            if "from_capture" in spec:
                source_name = spec["from_capture"]
                if source_name not in captures:
                    continue
                source_value = captures[source_name]
                if isinstance(source_value, dict):
                    captures[name] = source_value.get(name)
                else:
                    captures[name] = source_value
                pending.pop(name)
                progressed = True
                continue

            matched = None
            for pattern in _resolve_capture_regex(spec, language):
                match = re.search(pattern, text)
                if match:
                    matched = match
                    break
            if matched is None:
                raise ValueError(f"Could not extract capture '{name}' from: {text}")

            if name in matched.groupdict():
                captures[name] = _coerce_capture(matched.group(name), spec)
            else:
                captures[name] = {group_name: _coerce_capture(group_value, spec) for group_name, group_value in matched.groupdict().items()}
            pending.pop(name)
            progressed = True

        if not progressed:
            unresolved = ", ".join(sorted(pending))
            raise ValueError(f"Unresolved captures: {unresolved}")

    return captures


def _render_template(value: Any, captures: dict[str, Any], language: str) -> Any:
    value = _resolve_language_value(value, language)
    if isinstance(value, str):
        exact = re.fullmatch(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", value)
        if exact:
            return captures[exact.group(1)]
        return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", lambda match: str(captures[match.group(1)]), value)
    if isinstance(value, list):
        return [_render_template(item, captures, language) for item in value]
    if isinstance(value, dict):
        return {key: _render_template(item, captures, language) for key, item in value.items()}
    return value


def _entries_for_profile(parsed: ParsedDocument, extraction_profile: dict[str, Any]) -> tuple[list[RequirementEntry | UseCaseEntry], str]:
    mode = extraction_profile["mode"]
    if mode == "requirements":
        return parsed.requirements, extraction_profile["section"]
    if mode == "use_cases":
        return parsed.use_cases, extraction_profile["section"]
    raise ValueError(f"Unsupported extraction mode: {mode}")


def _build_contract(rule: dict[str, Any], entry: RequirementEntry | UseCaseEntry, parsed: ParsedDocument, sentence_index: int) -> dict[str, Any]:
    language = _language(parsed)
    captures = _extract_captures(getattr(entry, "text", ""), rule.get("captures", {}), language) if rule.get("captures") else {}
    slots = _render_template(rule.get("slots", {}), captures, language)

    section = entry.section if isinstance(entry, RequirementEntry) else entry.identifier
    anchor_sentence_index = sentence_index if isinstance(entry, RequirementEntry) else 1
    contract = {
        "contract_id": rule["contract_id"],
        "source_requirement_id": rule["source_requirement_id"],
        "source_anchor": {
            "document_id": parsed.document["document_id"],
            "section": section,
            "sentence_index": anchor_sentence_index,
        },
        "trace_quality": rule.get("trace_quality", "direct_file_grounded"),
        "classification": {
            "pattern_id": rule["pattern_id"],
            "confidence": rule["confidence"],
        },
        "subject": rule["subject"],
    }

    if isinstance(entry, UseCaseEntry):
        contract["main_flow_steps"] = entry.main_flow_steps
        contract["exception_flow_steps"] = entry.exception_flow_steps
        evidence_quote = slots.pop("evidence_quote", None)
        contract["evidence"] = {"quote": evidence_quote or entry.title}
    else:
        contract["evidence"] = {"quote": entry.text}

    contract.update(slots)
    return contract


def _build_profile_driven_contracts(parsed: ParsedDocument, case_profile: dict[str, Any]) -> list[dict[str, Any]]:
    extraction_profile = case_profile["extraction"]
    entries, _default_section = _entries_for_profile(parsed, extraction_profile)
    by_id = {entry.identifier: entry for entry in entries}

    contracts = []
    for sentence_index, rule in enumerate(extraction_profile["contract_rules"], start=1):
        entry = by_id[rule["source_requirement_id"]]
        contracts.append(_build_contract(rule, entry, parsed, sentence_index))
    return contracts


def build_contracts(parsed: ParsedDocument) -> dict[str, Any]:
    payload = _base_document_metadata(parsed)
    if parsed.metadata.get("structured_model"):
        payload["contracts"] = [
            {
                "contract_id": requirement.identifier,
                "source_requirement_id": requirement.identifier,
                "source_anchor": {"document_id": parsed.document["document_id"], "section": requirement.section},
                "trace_quality": "direct_file_grounded",
                "classification": {"pattern_id": "structured_model_requirement_doc", "confidence": 1.0},
                "subject": {
                    "kind": "system",
                    "canonical_name": parsed.metadata["structured_model"].get("default_subject", parsed.case_id),
                },
                "evidence": {"quote": requirement.text},
            }
            for requirement in parsed.requirements
        ]
        payload["structured_model"] = parsed.metadata["structured_model"]
        return payload
    if parsed.metadata.get("generic_case"):
        generic_profile = load_generic_case_profile()
        classification = generic_profile["contracts"]["classification"]
        subject_profile = generic_profile["contracts"]["subject"]
        payload["contracts"] = [
            {
                "contract_id": requirement.identifier,
                "source_requirement_id": requirement.identifier,
                "source_anchor": {"document_id": parsed.document["document_id"], "section": requirement.section},
                "trace_quality": "direct_file_grounded",
                "classification": {"pattern_id": classification["pattern_id"], "confidence": classification["confidence"]},
                "subject": {"kind": subject_profile["kind"], "canonical_name": parsed.metadata["generic_case"]["structure"][0]},
                "evidence": {"quote": requirement.text},
            }
            for requirement in parsed.requirements
        ]
        payload["generic_case"] = parsed.metadata["generic_case"]
        return payload

    case_profile = get_case_profile(parsed.case_id)
    if not case_profile:
        raise ValueError(f"Unsupported case: {parsed.case_id}")
    payload["contracts"] = _build_profile_driven_contracts(parsed, case_profile)
    return payload
