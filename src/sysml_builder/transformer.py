from __future__ import annotations

import re
from typing import Any

from .models import ParsedDocument, RequirementEntry, UseCaseEntry


def _match(text: str, *patterns: str) -> re.Match[str]:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match
    raise ValueError(f"Unsupported requirement text: {text}")


def _base_document_metadata(parsed: ParsedDocument) -> dict[str, Any]:
    return {"document": parsed.document.copy(), "contracts": []}


def _is_japanese(parsed: ParsedDocument) -> bool:
    return parsed.document.get("language") == "ja"


def _vehicle_explicit_contracts(reqs: list[RequirementEntry]) -> list[dict[str, Any]]:
    contracts = []
    for index, req in enumerate(reqs, start=1):
        if req.identifier == "REQ-VEH-001":
            match = _match(req.text, r"equal to (\d+)\s+kg", r"(\d+)\s*kg以下")
            contracts.append(
                {
                    "contract_id": "C-VEH-001",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE01", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "quantified_property_constraint", "confidence": 0.97},
                    "subject": {"kind": "system", "canonical_name": "Vehicle"},
                    "measured_property": "mass",
                    "comparator": "<=",
                    "threshold_value": int(match.group(1)),
                    "threshold_unit": "kg",
                    "responsible_module": "Vehicle",
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier in {"REQ-VEH-002", "REQ-VEH-003"}:
            match = _match(
                req.text,
                r"at least (\d+)\s+mpg.*cargo mass of at least (\d+)\s+kg",
                r"少なくとも(\d+)\s*mpg.*貨物質量が少なくとも(\d+)\s*kg",
                r"貨物質量が少なくとも(\d+)\s*kg.*少なくとも(\d+)\s*mpg",
            )
            mpg = int(match.group(1))
            cargo = int(match.group(2))
            if match.re.pattern.startswith("貨物質量"):
                cargo = int(match.group(1))
                mpg = int(match.group(2))
            context = "CityNominal" if req.identifier == "REQ-VEH-002" else "HighwayNominal"
            contracts.append(
                {
                    "contract_id": "C-VEH-002" if req.identifier == "REQ-VEH-002" else "C-VEH-003",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE01", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "contextual_quantified_performance", "confidence": 0.96},
                    "subject": {"kind": "system", "canonical_name": "Vehicle"},
                    "measured_property": "fuelEconomy",
                    "operating_contexts": [context],
                    "contextual_thresholds": [{"context": context, "comparator": ">=", "value": mpg, "unit": "mpg"}],
                    "assumption_constraints": [{"lhs": "assumedCargoMass", "operator": ">=", "rhs": cargo, "unit": "kg"}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-VEH-004":
            contracts.append(
                {
                    "contract_id": "C-VEH-004",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE01", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "interface_transfer", "confidence": 0.95},
                    "subject": {"kind": "module", "canonical_name": "Engine"},
                    "interface_name": "EngineToTransmissionInterface",
                    "interface_ends": [{"role": "p1", "port_type": "DrivePwrPort"}, {"role": "p2", "port_type": "ClutchPort"}],
                    "flows": [{"item": "Torque", "from": "p1", "to": "p2"}],
                    "evidence": {"quote": req.text},
                }
            )
    return contracts


def _vehicle_ambiguous_contracts(reqs: list[RequirementEntry], japanese: bool) -> list[dict[str, Any]]:
    rationale_threshold = "Mass requirement in VehicleModel uses a 2000 kg style threshold." if not japanese else "VehicleModel では 2000 kg 級の質量閾値が使われている。"
    rationale_mass = "The phrase lightweight most likely maps to vehicle mass." if not japanese else "軽量という表現は車両質量を指す可能性が高い。"
    rationale_contexts = "VehicleModel separates city and highway fuel economy requirements." if not japanese else "VehicleModel では市街地と高速の燃費要求が分離されている。"
    rationale_interface = "VehicleModel defines an EngineToTransmissionInterface between engine and transmission." if not japanese else "VehicleModel ではエンジンとトランスミッション間に EngineToTransmissionInterface が定義されている。"

    contracts = []
    for index, req in enumerate(reqs, start=1):
        if req.identifier == "REQ-VEH-L-001":
            contracts.append(
                {
                    "contract_id": "C-VEH-L-001",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE02", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "ambiguous_quality_claim", "confidence": 0.91},
                    "subject": {"kind": "system", "canonical_name": "Vehicle"},
                    "gaps": ["threshold_value", "threshold_unit", "measured_property"],
                    "llm_proposals": [
                        {"proposal_id": "P-VEH-L-001", "missing_slot": "threshold_value", "proposed_value": "2000", "confidence": 0.56, "rationale": rationale_threshold},
                        {"proposal_id": "P-VEH-L-002", "missing_slot": "measured_property", "proposed_value": "mass", "confidence": 0.79, "rationale": rationale_mass},
                    ],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-VEH-L-002":
            contracts.append(
                {
                    "contract_id": "C-VEH-L-002",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE02", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "ambiguous_quality_claim", "confidence": 0.9},
                    "subject": {"kind": "system", "canonical_name": "Vehicle"},
                    "gaps": ["operating_contexts", "threshold_value", "threshold_unit"],
                    "llm_proposals": [{"proposal_id": "P-VEH-L-003", "missing_slot": "operating_contexts", "proposed_value": "CityNominal and HighwayNominal", "confidence": 0.58, "rationale": rationale_contexts}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-VEH-L-003":
            contracts.append(
                {
                    "contract_id": "C-VEH-L-003",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE02", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "interface_transfer", "confidence": 0.74},
                    "subject": {"kind": "module", "canonical_name": "Engine"},
                    "gaps": ["interface_name", "interface_ends", "flows"],
                    "llm_proposals": [{"proposal_id": "P-VEH-L-004", "missing_slot": "interface_name", "proposed_value": "EngineToTransmissionInterface", "confidence": 0.68, "rationale": rationale_interface}],
                    "evidence": {"quote": req.text},
                }
            )
    return contracts


def _mining_contextual_contracts(reqs: list[RequirementEntry]) -> list[dict[str, Any]]:
    contracts = []
    for index, req in enumerate(reqs, start=1):
        if req.identifier == "REQ-MF-001":
            value = int(_match(req.text, r"at least (\d+)\s+m3", r"少なくとも(\d+)\s*m3").group(1))
            contracts.append(
                {
                    "contract_id": "C-MF-001",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE03", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "quantified_property_constraint", "confidence": 0.98},
                    "subject": {"kind": "system", "canonical_name": "MiningFrigate"},
                    "measured_property": "cargoCapacity",
                    "comparator": ">=",
                    "threshold_value": value,
                    "threshold_unit": "m3",
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-MF-002":
            value = int(_match(req.text, r"at least (\d+)\s+DPS", r"少なくとも(\d+)\s*DPS").group(1))
            contracts.append(
                {
                    "contract_id": "C-MF-002",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE03", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "contextual_quantified_performance", "confidence": 0.97},
                    "subject": {"kind": "system", "canonical_name": "MiningFrigate"},
                    "measured_property": "shieldStrength",
                    "operating_contexts": ["HighSec"],
                    "contextual_thresholds": [{"context": "HighSec", "comparator": ">=", "value": value, "unit": "DPS"}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-MF-003":
            value = int(_match(req.text, r"at least (\d+)\s+DPS", r"少なくとも(\d+)\s*DPS").group(1))
            contracts.append(
                {
                    "contract_id": "C-MF-003",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE03", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "contextual_quantified_performance", "confidence": 0.97},
                    "subject": {"kind": "system", "canonical_name": "MiningFrigate"},
                    "measured_property": "shieldStrength",
                    "operating_contexts": ["LowSec", "NullSec", "Wormhole"],
                    "contextual_thresholds": [{"context": "LowSec|NullSec|Wormhole", "comparator": ">=", "value": value, "unit": "DPS"}],
                    "evidence": {"quote": req.text},
                }
            )
    return contracts


def _modular_interface_contracts(reqs: list[RequirementEntry]) -> list[dict[str, Any]]:
    contracts = []
    for index, req in enumerate(reqs, start=1):
        if req.identifier == "REQ-MFI-001":
            contracts.append(
                {
                    "contract_id": "C-MFI-001",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE04", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "modular_slot_interface", "confidence": 0.97},
                    "subject": {"kind": "module", "canonical_name": "MiningFrigateHull"},
                    "slot_type": "HighSlot",
                    "interface_name": "HighSlotInterface",
                    "interface_ends": [{"role": "hullPort", "port_type": "HighSlotPort"}, {"role": "modulePort", "port_type": "~HighSlotPort"}],
                    "module_bindings": ["MiningLaserModule"],
                    "flows": [{"item": "PowerSupply", "from": "hullPort.power", "to": "modulePort.power"}, {"item": "HighSlotCommand", "from": "hullPort.control", "to": "modulePort.control"}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-MFI-002":
            contracts.append(
                {
                    "contract_id": "C-MFI-002",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE04", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "interface_transfer", "confidence": 0.98},
                    "subject": {"kind": "interface", "canonical_name": "HighSlotInterface"},
                    "interface_name": "HighSlotInterface",
                    "interface_ends": [{"role": "hullPort", "port_type": "HighSlotPort"}, {"role": "modulePort", "port_type": "~HighSlotPort"}],
                    "flows": [{"item": "PowerSupply", "from": "hullPort.power", "to": "modulePort.power"}, {"item": "HighSlotCommand", "from": "hullPort.control", "to": "modulePort.control"}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-MFI-003":
            contracts.append(
                {
                    "contract_id": "C-MFI-003",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE04", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "modular_slot_interface", "confidence": 0.97},
                    "subject": {"kind": "module", "canonical_name": "MiningFrigateHull"},
                    "slot_type": "MediumSlot",
                    "interface_name": "MediumSlotInterface",
                    "interface_ends": [{"role": "hullPort", "port_type": "MediumSlotPort"}, {"role": "modulePort", "port_type": "~MediumSlotPort"}],
                    "module_bindings": ["ShieldHardenerModule"],
                    "flows": [{"item": "PowerSupply", "from": "hullPort.power", "to": "modulePort.power"}, {"item": "MediumSlotCommand", "from": "hullPort.control", "to": "modulePort.control"}],
                    "evidence": {"quote": req.text},
                }
            )
        elif req.identifier == "REQ-MFI-004":
            contracts.append(
                {
                    "contract_id": "C-MFI-004",
                    "source_requirement_id": req.identifier,
                    "source_anchor": {"document_id": "GFSE-CASE04", "section": req.section, "sentence_index": index},
                    "trace_quality": "direct_file_grounded",
                    "classification": {"pattern_id": "interface_transfer", "confidence": 0.98},
                    "subject": {"kind": "interface", "canonical_name": "MediumSlotInterface"},
                    "interface_name": "MediumSlotInterface",
                    "interface_ends": [{"role": "hullPort", "port_type": "MediumSlotPort"}, {"role": "modulePort", "port_type": "~MediumSlotPort"}],
                    "flows": [{"item": "PowerSupply", "from": "hullPort.power", "to": "modulePort.power"}, {"item": "MediumSlotCommand", "from": "hullPort.control", "to": "modulePort.control"}],
                    "evidence": {"quote": req.text},
                }
            )
    return contracts


def _usecase_medium_contracts(use_cases: list[UseCaseEntry], japanese: bool) -> list[dict[str, Any]]:
    mapping = {
        "UC-MF-001": {
            "contract_id": "C-UC-001",
            "confidence": 0.95,
            "actors": ["PilotPod", "AsteroidBelt"],
            "objective_text": "Mine asteroids and manage cargo." if not japanese else "小惑星を採掘し貨物を管理する。",
            "gaps": ["success_thresholds", "time_limits", "trigger_conditions"],
            "evidence": "Main Flow: Identify an asteroid target, activate the mining laser, extract ore, and suspend mining when the cargo hold becomes full." if not japanese else "メインフロー: 小惑星ターゲットを特定し、採掘レーザーを起動し、鉱石を採取し、貨物倉が満杯になったら採掘を中断する。",
        },
        "UC-MF-002": {
            "contract_id": "C-UC-002",
            "confidence": 0.94,
            "actors": ["Station"],
            "objective_text": "Offload ore and resupply essential systems." if not japanese else "鉱石を荷下ろしし重要システムを補給する。",
            "gaps": ["success_thresholds", "completion_conditions"],
            "evidence": "Main Flow: Establish a docking connection with a station, transfer ore, and resupply essential systems." if not japanese else "メインフロー: ステーションとのドッキング接続を確立し、鉱石を移送し、重要システムを補給する。",
        },
    }
    results = []
    for uc in use_cases:
        info = mapping[uc.identifier]
        results.append(
            {
                "contract_id": info["contract_id"],
                "source_requirement_id": uc.identifier,
                "source_anchor": {"document_id": "GFSE-CASE05", "section": uc.identifier, "sentence_index": 1},
                "trace_quality": "direct_file_grounded",
                "classification": {"pattern_id": "operational_use_case_objective", "confidence": info["confidence"]},
                "subject": {"kind": "system", "canonical_name": "MiningFrigate"},
                "actors": info["actors"],
                "objective_text": info["objective_text"],
                "main_flow_steps": uc.main_flow_steps,
                "exception_flow_steps": uc.exception_flow_steps,
                "gaps": info["gaps"],
                "evidence": {"quote": info["evidence"]},
            }
        )
    return results


def _usecase_ambiguous_contracts(reqs: list[RequirementEntry], japanese: bool) -> list[dict[str, Any]]:
    mapping = {
        "REQ-UC-L-001": {"contract_id": "C-UCL-001", "confidence": 0.88, "gaps": ["actors", "objective_text", "main_flow_steps", "success_thresholds"], "proposal_id": "P-UCL-001", "proposed_value": "PilotPod and AsteroidBelt", "proposal_confidence": 0.72, "rationale": "UseCasesFrigate pairs mining with pilot and asteroid belt actors." if not japanese else "UseCasesFrigate の採掘ユースケースではパイロットと小惑星帯が組みになっている。"},
        "REQ-UC-L-002": {"contract_id": "C-UCL-002", "confidence": 0.87, "gaps": ["actors", "trigger_conditions", "exception_flow_steps"], "proposal_id": "P-UCL-002", "proposed_value": "HostileShip and PilotPod", "proposal_confidence": 0.71, "rationale": "Threat engagement use case involves hostile ship and pilot." if not japanese else "脅威対処ユースケースには敵対艦船とパイロットが含まれる。"},
        "REQ-UC-L-003": {"contract_id": "C-UCL-003", "confidence": 0.86, "gaps": ["actors", "trigger_conditions", "completion_conditions"], "proposal_id": "P-UCL-003", "proposed_value": "Station", "proposal_confidence": 0.70, "rationale": "Offload and resupply use cases involve a station actor." if not japanese else "荷下ろしと補給のユースケースにはステーションアクターが含まれる。"},
    }
    results = []
    for index, req in enumerate(reqs, start=1):
        info = mapping[req.identifier]
        results.append(
            {
                "contract_id": info["contract_id"],
                "source_requirement_id": req.identifier,
                "source_anchor": {"document_id": "GFSE-CASE06", "section": req.section, "sentence_index": index},
                "trace_quality": "direct_file_grounded",
                "classification": {"pattern_id": "ambiguous_quality_claim", "confidence": info["confidence"]},
                "subject": {"kind": "system", "canonical_name": "MiningFrigate"},
                "gaps": info["gaps"],
                "llm_proposals": [{"proposal_id": info["proposal_id"], "missing_slot": "actors", "proposed_value": info["proposed_value"], "confidence": info["proposal_confidence"], "rationale": info["rationale"]}],
                "evidence": {"quote": req.text},
            }
        )
    return results


def build_contracts(parsed: ParsedDocument) -> dict[str, Any]:
    payload = _base_document_metadata(parsed)
    if parsed.metadata.get("generic_case"):
        payload["contracts"] = [
            {
                "contract_id": requirement.identifier,
                "source_requirement_id": requirement.identifier,
                "source_anchor": {"document_id": parsed.document["document_id"], "section": requirement.section},
                "trace_quality": "direct_file_grounded",
                "classification": {"pattern_id": "generic_requirement_doc", "confidence": 1.0},
                "subject": {"kind": "system", "canonical_name": parsed.metadata["generic_case"]["structure"][0]},
                "evidence": {"quote": requirement.text},
            }
            for requirement in parsed.requirements
        ]
        payload["generic_case"] = parsed.metadata["generic_case"]
        return payload
    japanese = _is_japanese(parsed)
    if parsed.case_id == "case01_vehicle_explicit_high":
        payload["contracts"] = _vehicle_explicit_contracts(parsed.requirements)
    elif parsed.case_id == "case02_vehicle_ambiguous_low":
        payload["contracts"] = _vehicle_ambiguous_contracts(parsed.requirements, japanese)
    elif parsed.case_id == "case03_mining_contextual_performance_high":
        payload["contracts"] = _mining_contextual_contracts(parsed.requirements)
    elif parsed.case_id == "case04_mining_modular_interface_high":
        payload["contracts"] = _modular_interface_contracts(parsed.requirements)
    elif parsed.case_id == "case05_mining_usecase_medium":
        payload["contracts"] = _usecase_medium_contracts(parsed.use_cases, japanese)
    elif parsed.case_id == "case06_mining_usecase_ambiguous_low":
        payload["contracts"] = _usecase_ambiguous_contracts(parsed.requirements, japanese)
    else:
        raise ValueError(f"Unsupported case: {parsed.case_id}")
    return payload
