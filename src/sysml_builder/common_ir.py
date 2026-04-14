from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .models import ParsedDocument


SCHEMA_VERSION = "common_semantic_ir_v1alpha1"


@dataclass
class RequirementIR:
    id: str
    source_contract: str
    source_requirement_id: str
    subject: str
    pattern: str
    text: str
    attributes: dict[str, Any] = field(default_factory=dict)
    gaps: list[str] = field(default_factory=list)


@dataclass
class ValueTypeIR:
    name: str


@dataclass
class FlowPropertyIR:
    name: str
    direction: str
    item_type: str


@dataclass
class PortTypeIR:
    name: str
    flow_properties: list[FlowPropertyIR] = field(default_factory=list)


@dataclass
class PortIR:
    name: str
    type: str
    conjugated: bool = False


@dataclass
class PartIR:
    name: str
    type: str


@dataclass
class TransitionIR:
    source: str
    target: str


@dataclass
class StateMachineIR:
    name: str
    states: list[str] = field(default_factory=list)
    transitions: list[TransitionIR] = field(default_factory=list)


@dataclass
class BlockIR:
    name: str
    ports: list[PortIR] = field(default_factory=list)
    parts: list[PartIR] = field(default_factory=list)
    state_machines: list[StateMachineIR] = field(default_factory=list)


@dataclass
class ConnectorIR:
    name: str
    type: str | None
    source: str
    target: str


@dataclass
class AllocationIR:
    id: str
    source_contract: str
    target: str


@dataclass
class SatisfyIR:
    requirement: str
    by: str


@dataclass
class CommonIrModel:
    schema_version: str
    case_id: str
    package_name: str
    source_document: dict[str, Any]
    requirements: list[RequirementIR] = field(default_factory=list)
    value_types: list[ValueTypeIR] = field(default_factory=list)
    port_types: list[PortTypeIR] = field(default_factory=list)
    blocks: list[BlockIR] = field(default_factory=list)
    connectors: list[ConnectorIR] = field(default_factory=list)
    allocations: list[AllocationIR] = field(default_factory=list)
    satisfies: list[SatisfyIR] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_common_ir(parsed: ParsedDocument, contracts: dict[str, Any], projection_manifest: dict[str, Any] | None) -> CommonIrModel:
    if parsed.metadata.get("generic_case"):
        return _build_generic_case_ir(parsed, contracts, projection_manifest)
    return _build_profile_case_ir(parsed, contracts, projection_manifest)


def _build_generic_case_ir(parsed: ParsedDocument, contracts: dict[str, Any], projection_manifest: dict[str, Any] | None) -> CommonIrModel:
    generic_case = parsed.metadata["generic_case"]
    contract_entries = contracts.get("contracts", [])
    requirements = [
        RequirementIR(
            id=contract["contract_id"],
            source_contract=contract["contract_id"],
            source_requirement_id=contract["source_requirement_id"],
            subject=contract["subject"]["canonical_name"],
            pattern=contract["classification"]["pattern_id"],
            text=contract["evidence"]["quote"],
            gaps=list(contract.get("gaps", [])),
        )
        for contract in contract_entries
    ]
    value_types = [ValueTypeIR(name=item_name) for _port_name, _signal_name, item_name, _direction in generic_case["interfaces"]]
    port_types = [
        PortTypeIR(
            name=port_name,
            flow_properties=[FlowPropertyIR(name=signal_name, direction=direction, item_type=item_name)],
        )
        for port_name, signal_name, item_name, direction in generic_case["interfaces"]
    ]

    top_level = generic_case["structure"][0]
    state_machine = generic_case.get("state_machine")
    part_ports = generic_case["part_ports"]
    subparts = generic_case["subparts"]
    blocks: list[BlockIR] = []
    for block_name in generic_case["structure"]:
        block = BlockIR(
            name=block_name,
            ports=[
                PortIR(name=port_name, type=port_type.removeprefix("~"), conjugated=port_type.startswith("~"))
                for port_name, port_type in part_ports.get(block_name, [])
            ],
            parts=[PartIR(name=part_name, type=part_type) for part_name, part_type in subparts.get(block_name, [])],
        )
        if state_machine and block_name != top_level and part_ports.get(block_name):
            block.state_machines.append(
                StateMachineIR(
                    name=state_machine["name"],
                    states=list(state_machine["states"]),
                    transitions=[TransitionIR(source=source, target=target) for source, target in state_machine["transitions"]],
                )
            )
            state_machine = None
        blocks.append(block)

    connectors: list[ConnectorIR] = []
    for interface_name, source_port, target_port, _signal_name in generic_case.get("interfaces_defs", []):
        source_owner = _find_part_with_port(top_level, subparts.get(top_level, []), generic_case["part_ports"], source_port, prefer_conjugated=False)
        target_owner = _find_part_with_port(top_level, subparts.get(top_level, []), generic_case["part_ports"], target_port, prefer_conjugated=True)
        if source_owner and target_owner:
            connectors.append(
                ConnectorIR(
                    name=interface_name,
                    type=interface_name,
                    source=f"{top_level}.{source_owner[0]}.{source_owner[1]}",
                    target=f"{top_level}.{target_owner[0]}.{target_owner[1]}",
                )
            )

    return CommonIrModel(
        schema_version=SCHEMA_VERSION,
        case_id=parsed.case_id,
        package_name=generic_case["package"],
        source_document=parsed.document,
        requirements=requirements,
        value_types=_dedupe_by_name(value_types),
        port_types=_dedupe_by_name(port_types),
        blocks=blocks,
        connectors=connectors,
        allocations=[],
        satisfies=[],
        metadata={"completeness": "generic_case", "source": "case.yaml"},
    )


def _build_profile_case_ir(parsed: ParsedDocument, contracts: dict[str, Any], projection_manifest: dict[str, Any] | None) -> CommonIrModel:
    contract_entries = contracts.get("contracts", [])
    manifest_requirements = {
        entry["source_contract"]: entry.get("sysml_name", entry["source_contract"])
        for entry in (projection_manifest or {}).get("requirements", [])
        if entry.get("source_contract")
    }
    requirements = [
        RequirementIR(
            id=manifest_requirements.get(contract["contract_id"], contract["contract_id"]),
            source_contract=contract["contract_id"],
            source_requirement_id=contract["source_requirement_id"],
            subject=contract["subject"]["canonical_name"],
            pattern=contract["classification"]["pattern_id"],
            text=contract["evidence"]["quote"],
            attributes={
                key: value
                for key, value in contract.items()
                if key
                not in {
                    "contract_id",
                    "source_requirement_id",
                    "source_anchor",
                    "trace_quality",
                    "classification",
                    "subject",
                    "evidence",
                    "gaps",
                    "llm_proposals",
                }
            },
            gaps=list(contract.get("gaps", [])),
        )
        for contract in contract_entries
    ]
    value_types: list[ValueTypeIR] = []
    port_types: list[PortTypeIR] = []
    for contract in contract_entries:
        for flow in contract.get("flows", []):
            item_name = flow["item"]
            if item_name:
                value_types.append(ValueTypeIR(name=item_name))
        if contract["classification"]["pattern_id"] == "interface_transfer":
            flow_properties = [
                FlowPropertyIR(name=flow["item"], direction="out", item_type=flow["item"])
                for flow in contract.get("flows", [])
            ]
            if contract.get("interface_name"):
                port_types.append(PortTypeIR(name=contract["interface_name"], flow_properties=flow_properties))

    blocks = _infer_blocks_from_profile_case(requirements, projection_manifest)
    connectors = [
        ConnectorIR(
            name=entry["name"],
            type=entry.get("type"),
            source=entry["from"],
            target=entry["to"],
        )
        for entry in (projection_manifest or {}).get("interfaces", [])
    ]
    allocations = [
        AllocationIR(id=entry["id"], source_contract=entry["contract"], target=entry["allocated_to"])
        for entry in (projection_manifest or {}).get("allocations", [])
    ]
    satisfies = [
        SatisfyIR(requirement=entry["requirement"], by=entry["by"])
        for entry in (projection_manifest or {}).get("satisfy_claims", [])
    ]

    return CommonIrModel(
        schema_version=SCHEMA_VERSION,
        case_id=parsed.case_id,
        package_name=parsed.case_id,
        source_document=parsed.document,
        requirements=requirements,
        value_types=_dedupe_by_name(value_types),
        port_types=_dedupe_by_name(port_types),
        blocks=blocks,
        connectors=connectors,
        allocations=allocations,
        satisfies=satisfies,
        metadata={"completeness": "profile_case", "source": "contracts+projection_manifest"},
    )


def _infer_blocks_from_profile_case(requirements: list[RequirementIR], projection_manifest: dict[str, Any] | None) -> list[BlockIR]:
    block_names = {requirement.subject for requirement in requirements}
    for allocation in (projection_manifest or {}).get("allocations", []):
        for segment in allocation["allocated_to"].split("::"):
            if segment and segment != "Structure":
                block_names.add(segment)
    ordered = sorted(block_names)
    return [BlockIR(name=name) for name in ordered]


def _first_port_name(ports: list[list[str]] | list[tuple[str, str]], port_type: str, prefer_conjugated: bool = False) -> str | None:
    matches = [(name, type_name) for name, type_name in ports if type_name.removeprefix("~") == port_type]
    if prefer_conjugated:
        for name, type_name in matches:
            if type_name.startswith("~"):
                return name
        return None
    return matches[0][0] if matches else None


def _find_part_with_port(
    root_name: str,
    top_level_parts: list[list[str]] | list[tuple[str, str]],
    part_ports: dict[str, list[list[str]]],
    port_type: str,
    prefer_conjugated: bool,
) -> tuple[str, str] | None:
    for part_name, block_type in top_level_parts:
        port_name = _first_port_name(part_ports.get(block_type, []), port_type, prefer_conjugated=prefer_conjugated)
        if port_name is not None:
            return part_name, port_name
    return None


def _dedupe_by_name(items: list[Any]) -> list[Any]:
    seen: set[str] = set()
    deduped: list[Any] = []
    for item in items:
        name = getattr(item, "name", None)
        if name in seen:
            continue
        seen.add(name)
        deduped.append(item)
    return deduped
