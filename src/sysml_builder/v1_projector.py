from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .common_ir import CommonIrModel


PROJECTION_PROFILE = "safe_subset_v1_5"


@dataclass
class RequirementProjection:
    name: str
    subject: str
    text: str
    source_contract: str


@dataclass
class InterfaceBlockProjection:
    name: str
    flow_properties: list[dict[str, str]] = field(default_factory=list)


@dataclass
class BlockProjection:
    name: str
    ports: list[dict[str, Any]] = field(default_factory=list)
    parts: list[dict[str, str]] = field(default_factory=list)
    state_machines: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ConnectorProjection:
    name: str
    type_name: str | None
    source: str
    target: str


@dataclass
class RelationshipProjection:
    kind: str
    name: str
    client: str
    supplier: str


@dataclass
class V1ProjectionModel:
    schema_version: str
    projection_profile: str
    package_name: str
    source_document: dict[str, Any]
    value_types: list[str] = field(default_factory=list)
    interface_blocks: list[InterfaceBlockProjection] = field(default_factory=list)
    requirements: list[RequirementProjection] = field(default_factory=list)
    blocks: list[BlockProjection] = field(default_factory=list)
    connectors: list[ConnectorProjection] = field(default_factory=list)
    relationships: list[RelationshipProjection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def project_to_sysml_v1(common_ir: CommonIrModel, target_profile: str = PROJECTION_PROFILE) -> V1ProjectionModel:
    requirement_by_contract = {requirement.source_contract: requirement.id for requirement in common_ir.requirements}
    relationships = [
        RelationshipProjection(kind="satisfy", name=_relationship_name("satisfy", relation.requirement), client=relation.by, supplier=relation.requirement)
        for relation in common_ir.satisfies
    ]
    relationships.extend(
        RelationshipProjection(
            kind="allocate",
            name=allocation.id,
            client=requirement_by_contract.get(allocation.source_contract, allocation.source_contract),
            supplier=allocation.target,
        )
        for allocation in common_ir.allocations
    )

    return V1ProjectionModel(
        schema_version="v1_projection_model_v1alpha1",
        projection_profile=target_profile,
        package_name=common_ir.package_name,
        source_document=common_ir.source_document,
        value_types=[value_type.name for value_type in common_ir.value_types],
        interface_blocks=[
            InterfaceBlockProjection(
                name=port_type.name,
                flow_properties=[
                    {"name": flow_property.name, "direction": flow_property.direction, "item_type": flow_property.item_type}
                    for flow_property in port_type.flow_properties
                ],
            )
            for port_type in common_ir.port_types
        ],
        requirements=[
            RequirementProjection(
                name=requirement.id,
                subject=requirement.subject,
                text=requirement.text,
                source_contract=requirement.source_contract,
            )
            for requirement in common_ir.requirements
            if not requirement.gaps
        ],
        blocks=[
            BlockProjection(
                name=block.name,
                ports=[{"name": port.name, "type": port.type, "conjugated": port.conjugated} for port in block.ports],
                parts=[{"name": part.name, "type": part.type} for part in block.parts],
                state_machines=[
                    {
                        "name": state_machine.name,
                        "states": list(state_machine.states),
                        "transitions": [{"source": transition.source, "target": transition.target} for transition in state_machine.transitions],
                    }
                    for state_machine in block.state_machines
                ],
            )
            for block in common_ir.blocks
        ],
        connectors=[
            ConnectorProjection(name=connector.name, type_name=connector.type, source=connector.source, target=connector.target)
            for connector in common_ir.connectors
        ],
        relationships=relationships,
        metadata={"source_schema_version": common_ir.schema_version},
    )


def _relationship_name(prefix: str, path: str) -> str:
    return f"{prefix}_{path.split('::')[-1]}"
