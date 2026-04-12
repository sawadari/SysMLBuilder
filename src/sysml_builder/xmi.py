from __future__ import annotations

import hashlib
import itertools
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, register_namespace


TOOL_PROFILES = {
    "cameo": {
        "xmi_version": "2.5",
        "xmi_ns": "http://www.omg.org/spec/XMI/20131001",
        "uml_ns": "http://www.omg.org/spec/UML/20161101",
        "sysml_ns": "http://www.omg.org/spec/SysML/20161101/SysML.xmi",
        "profile_href": "http://www.omg.org/spec/SysML/20161101/SysML.xmi#SysML",
    },
    "ea": {
        "xmi_version": "2.1",
        "xmi_ns": "http://schema.omg.org/spec/XMI/2.1",
        "uml_ns": "http://schema.omg.org/spec/UML/2.1",
        "sysml_ns": "http://www.omg.org/spec/SysML/20161101/SysML.xmi",
        "profile_href": "http://www.omg.org/spec/SysML/20161101/SysML.xmi#SysML",
    },
}


@dataclass
class PortDefinition:
    name: str
    direction: str
    item_name: str
    item_type: str


@dataclass
class PortUsage:
    name: str
    type_name: str
    conjugated: bool


@dataclass
class PartUsage:
    name: str
    type_name: str


@dataclass
class Transition:
    name: str
    source: str
    target: str


@dataclass
class StateMachineDefinition:
    name: str
    states: list[str]
    transitions: list[Transition]


@dataclass
class RequirementDefinition:
    name: str
    doc: str
    req_id: str
    text: str


@dataclass
class BlockDefinition:
    name: str
    ports: list[PortUsage]
    parts: list[PartUsage]
    state_machines: list[StateMachineDefinition]


@dataclass
class CanonicalModel:
    package_name: str
    package_doc: str | None
    items: list[str]
    port_defs: dict[str, PortDefinition]
    requirements: list[RequirementDefinition]
    parts: dict[str, BlockDefinition]
    top_parts: list[PartUsage]


def generate_sysml_v1_xmi(canonical_sysml: str, target: str) -> str:
    if target not in TOOL_PROFILES:
        supported = ", ".join(sorted(TOOL_PROFILES))
        raise ValueError(f"Unsupported SysML v1 XMI target: {target}. Supported targets: {supported}")
    model = parse_sysml_v2_text(canonical_sysml)
    return _generate_xmi(model, target)


def parse_sysml_v2_text(text: str) -> CanonicalModel:
    package_match = re.search(r"package\s+([A-Za-z_]\w*)\s*\{", text)
    package_name = package_match.group(1) if package_match else "Model"
    package_doc = None
    package_doc_match = re.search(r"package\s+[A-Za-z_]\w*\s*\{\s*doc\s*/\*(.*?)\*/", text, re.S)
    if package_doc_match:
        package_doc = package_doc_match.group(1).strip()

    items = re.findall(r"item def\s+([A-Za-z_]\w*)\s*;", text)

    port_defs: dict[str, PortDefinition] = {}
    for block in _find_named_blocks(text, "port def"):
        match = re.search(r"\b(in|out)\s+item\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*;", block["body"])
        if not match:
            continue
        direction, item_name, item_type = match.groups()
        port_defs[block["name"]] = PortDefinition(
            name=block["name"],
            direction=direction,
            item_name=item_name,
            item_type=item_type,
        )

    requirements: list[RequirementDefinition] = []
    for block in _find_named_blocks(text, "requirement def"):
        doc_match = re.search(r"doc\s*/\*(.*?)\*/", block["body"], re.S)
        doc = doc_match.group(1).strip() if doc_match else ""
        id_match = re.search(r"([A-Za-z0-9_-]+)\s*:\s*(.*)", doc, re.S)
        req_id = id_match.group(1).strip() if id_match else block["name"]
        req_text = re.sub(r"\s+", " ", id_match.group(2).strip()) if id_match else doc
        requirements.append(
            RequirementDefinition(
                name=block["name"],
                doc=doc,
                req_id=req_id,
                text=req_text,
            )
        )

    parts: dict[str, BlockDefinition] = {}
    for block in _find_named_blocks(text, "part def"):
        body = block["body"]
        nested_parts = [
            PartUsage(name=match.group(1), type_name=match.group(2))
            for match in re.finditer(r"^\s*part\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*;", body, re.M)
        ]
        ports = [
            PortUsage(name=match.group(1), conjugated=bool(match.group(2)), type_name=match.group(3))
            for match in re.finditer(r"^\s*port\s+([A-Za-z_]\w*)\s*:\s*(~?)([A-Za-z_]\w*)\s*;", body, re.M)
        ]
        state_machines = []
        for sm_block in _find_named_blocks(body, "state def"):
            transitions = [
                Transition(name=match.group(1), source=match.group(2), target=match.group(3))
                for match in re.finditer(
                    r"transition\s+([A-Za-z_]\w*)\s+first\s+([A-Za-z_]\w*)\s+then\s+([A-Za-z_]\w*)\s*;",
                    sm_block["body"],
                    re.S,
                )
            ]
            state_machines.append(
                StateMachineDefinition(
                    name=sm_block["name"],
                    states=re.findall(r"^\s*state\s+([A-Za-z_]\w*)\s*;", sm_block["body"], re.M),
                    transitions=transitions,
                )
            )
        parts[block["name"]] = BlockDefinition(
            name=block["name"],
            ports=ports,
            parts=nested_parts,
            state_machines=state_machines,
        )

    top_parts = [
        PartUsage(name=match.group(1), type_name=match.group(2))
        for match in re.finditer(r"^\s*part\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*;", text, re.M)
    ]

    return CanonicalModel(
        package_name=package_name,
        package_doc=package_doc,
        items=items,
        port_defs=port_defs,
        requirements=requirements,
        parts=parts,
        top_parts=top_parts,
    )


def _mkid(prefix: str, name: str, package: str = "") -> str:
    digest = hashlib.md5(f"{package}::{prefix}::{name}".encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _match_brace_block(text: str, start_idx: int) -> tuple[str, int]:
    depth = 0
    for index in range(start_idx, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start_idx + 1 : index], index
    raise ValueError("No matching brace found in SysML text")


def _find_named_blocks(text: str, keyword: str) -> list[dict[str, str | int]]:
    blocks: list[dict[str, str | int]] = []
    pattern = re.compile(rf"{re.escape(keyword)}\s+([A-Za-z_]\w*)\s*\{{", re.M)
    for match in pattern.finditer(text):
        brace_start = text.find("{", match.end() - 1)
        body, end = _match_brace_block(text, brace_start)
        blocks.append({"name": match.group(1), "body": body, "start": match.start(), "end": end + 1})
    return blocks


def _effective_direction(port_usage: PortUsage, port_defs: dict[str, PortDefinition]) -> str | None:
    port_def = port_defs.get(port_usage.type_name)
    if port_def is None:
        return None
    if not port_usage.conjugated:
        return port_def.direction
    return "out" if port_def.direction == "in" else "in"


def _guess_root_system_block(model: CanonicalModel) -> str | None:
    for top_part in model.top_parts:
        if top_part.name == "systemUnderTest" and top_part.type_name in model.parts:
            return top_part.type_name
    with_children = [block.name for block in model.parts.values() if block.parts]
    for name in with_children:
        if name.endswith("System"):
            return name
    if with_children:
        return with_children[-1]
    return next(iter(model.parts), None)


def _build_connector_candidates(model: CanonicalModel, root_block_name: str) -> list[dict[str, dict[str, str] | str]]:
    if root_block_name not in model.parts:
        return []
    root_block = model.parts[root_block_name]
    entries: list[dict[str, str]] = []
    for part in root_block.parts:
        block = model.parts.get(part.type_name)
        if block is None:
            continue
        for port in block.ports:
            entries.append(
                {
                    "part_property": part.name,
                    "part_type": part.type_name,
                    "port_name": port.name,
                    "port_type": port.type_name,
                    "direction": _effective_direction(port, model.port_defs) or "",
                }
            )

    by_type: dict[str, list[dict[str, str]]] = {}
    for entry in entries:
        by_type.setdefault(entry["port_type"], []).append(entry)

    connectors: list[dict[str, dict[str, str] | str]] = []
    used: set[tuple[tuple[str, str], tuple[str, str]]] = set()
    for port_type, elements in by_type.items():
        outs = [entry for entry in elements if entry["direction"] == "out"]
        ins = [entry for entry in elements if entry["direction"] == "in"]
        if outs and ins:
            for out_entry in outs:
                candidates = [in_entry for in_entry in ins if in_entry["part_property"] != out_entry["part_property"]]
                for in_entry in candidates:
                    key = tuple(sorted(((out_entry["part_property"], out_entry["port_name"]), (in_entry["part_property"], in_entry["port_name"]))))
                    if key in used:
                        continue
                    connectors.append({"from": out_entry, "to": in_entry, "port_type": port_type})
                    used.add(key)
                    break
            continue
        for left, right in itertools.combinations(elements, 2):
            if left["part_property"] == right["part_property"]:
                continue
            left_name = left["port_name"].lower()
            right_name = right["port_name"].lower()
            if ("out" in left_name and "in" in right_name) or ("out" in right_name and "in" in left_name) or len(elements) == 2:
                key = tuple(sorted(((left["part_property"], left["port_name"]), (right["part_property"], right["port_name"]))))
                if key in used:
                    continue
                connectors.append({"from": left, "to": right, "port_type": port_type})
                used.add(key)
    return connectors


def _pretty_xml(element: Element) -> str:
    return minidom.parseString(ET.tostring(element, encoding="utf-8")).toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")


def _find_element_by_id(parent: Element, xmi_ns: str, xmi_id: str) -> Element | None:
    key = f"{{{xmi_ns}}}id"
    for element in parent.iter():
        if element.attrib.get(key) == xmi_id:
            return element
    return None


def _generate_xmi(model: CanonicalModel, target: str) -> str:
    profile = TOOL_PROFILES[target]
    xmi_ns = profile["xmi_ns"]
    uml_ns = profile["uml_ns"]
    sysml_ns = profile["sysml_ns"]
    ecore_ns = "http://www.eclipse.org/emf/2002/Ecore"

    register_namespace("xmi", xmi_ns)
    register_namespace("uml", uml_ns)
    register_namespace("sysml", sysml_ns)
    register_namespace("ecore", ecore_ns)

    root = Element(f"{{{xmi_ns}}}XMI", {f"{{{xmi_ns}}}version": profile["xmi_version"]})
    model_id = _mkid("model", model.package_name, model.package_name)
    uml_model = SubElement(root, f"{{{uml_ns}}}Model", {f"{{{xmi_ns}}}id": model_id, "name": model.package_name})

    if model.package_doc:
        owned_comment = SubElement(uml_model, "ownedComment", {f"{{{xmi_ns}}}id": _mkid("comment", model.package_name, model.package_name)})
        body = SubElement(owned_comment, "body")
        body.text = model.package_doc

    profile_application = SubElement(
        uml_model,
        "profileApplication",
        {
            f"{{{xmi_ns}}}type": "uml:ProfileApplication",
            f"{{{xmi_ns}}}id": _mkid("pa", "sysml", model.package_name),
            "applyingPackage": model_id,
        },
    )
    extension = SubElement(profile_application, f"{{{xmi_ns}}}Extension", {"extender": "http://www.eclipse.org/emf/2002/Ecore"})
    annotation = SubElement(
        extension,
        f"{{{ecore_ns}}}EAnnotation",
        {
            f"{{{xmi_ns}}}id": _mkid("eann", "sysml", model.package_name),
            "source": "http://www.eclipse.org/uml2/2.0.0/UML",
        },
    )
    SubElement(annotation, "references", {f"{{{xmi_ns}}}type": "ecore:EPackage", "href": profile["profile_href"]})
    SubElement(profile_application, "appliedProfile", {f"{{{xmi_ns}}}type": "uml:Profile", "href": profile["profile_href"]})

    data_types_pkg = SubElement(
        uml_model,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": _mkid("pkg", "datatypes", model.package_name), "name": "DataTypes"},
    )
    ports_pkg = SubElement(
        uml_model,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": _mkid("pkg", "ports", model.package_name), "name": "Ports"},
    )
    requirements_pkg = SubElement(
        uml_model,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": _mkid("pkg", "requirements", model.package_name), "name": "Requirements"},
    )
    blocks_pkg = SubElement(
        uml_model,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": _mkid("pkg", "blocks", model.package_name), "name": "Blocks"},
    )
    relationships_pkg = SubElement(
        uml_model,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": _mkid("pkg", "relationships", model.package_name), "name": "Relationships"},
    )

    ids: dict[object, str] = {}

    for item in model.items:
        item_id = _mkid("dt", item, model.package_name)
        ids[item] = item_id
        SubElement(data_types_pkg, "packagedElement", {f"{{{xmi_ns}}}type": "uml:DataType", f"{{{xmi_ns}}}id": item_id, "name": item})

    for port_name, port_def in model.port_defs.items():
        interface_block_id = _mkid("ifb", port_name, model.package_name)
        ids[port_name] = interface_block_id
        interface_block = SubElement(
            ports_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": interface_block_id, "name": port_name},
        )
        flow_id = _mkid("flow", f"{port_name}.{port_def.item_name}", model.package_name)
        ids[(port_name, port_def.item_name)] = flow_id
        SubElement(
            interface_block,
            "ownedAttribute",
            {
                f"{{{xmi_ns}}}type": "uml:Property",
                f"{{{xmi_ns}}}id": flow_id,
                "name": port_def.item_name,
                "type": ids[port_def.item_type],
            },
        )

    for requirement in model.requirements:
        requirement_id = _mkid("req", requirement.name, model.package_name)
        ids[requirement.name] = requirement_id
        requirement_class = SubElement(
            requirements_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": requirement_id, "name": requirement.name},
        )
        comment = SubElement(requirement_class, "ownedComment", {f"{{{xmi_ns}}}id": _mkid("comment", requirement.name, model.package_name)})
        body = SubElement(comment, "body")
        body.text = requirement.doc

    for block_name, block in model.parts.items():
        block_id = _mkid("blk", block_name, model.package_name)
        ids[block_name] = block_id
        block_class = SubElement(
            blocks_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": block_id, "name": block_name},
        )
        for part in block.parts:
            property_id = _mkid("prop", f"{block_name}.{part.name}", model.package_name)
            ids[(block_name, part.name)] = property_id
            SubElement(
                block_class,
                "ownedAttribute",
                {
                    f"{{{xmi_ns}}}type": "uml:Property",
                    f"{{{xmi_ns}}}id": property_id,
                    "name": part.name,
                    "type": _mkid("blk", part.type_name, model.package_name),
                    "aggregation": "composite",
                },
            )
        for port in block.ports:
            port_id = _mkid("port", f"{block_name}.{port.name}", model.package_name)
            ids[(block_name, port.name)] = port_id
            SubElement(
                block_class,
                "ownedAttribute",
                {
                    f"{{{xmi_ns}}}type": "uml:Port",
                    f"{{{xmi_ns}}}id": port_id,
                    "name": port.name,
                    "type": _mkid("ifb", port.type_name, model.package_name),
                },
            )
        for state_machine in block.state_machines:
            state_machine_id = _mkid("sm", f"{block_name}.{state_machine.name}", model.package_name)
            state_machine_el = SubElement(
                block_class,
                "ownedBehavior",
                {f"{{{xmi_ns}}}type": "uml:StateMachine", f"{{{xmi_ns}}}id": state_machine_id, "name": state_machine.name},
            )
            region = SubElement(
                state_machine_el,
                "region",
                {f"{{{xmi_ns}}}id": _mkid("region", f"{block_name}.{state_machine.name}", model.package_name)},
            )
            for state in state_machine.states:
                state_id = _mkid("state", f"{block_name}.{state_machine.name}.{state}", model.package_name)
                ids[(block_name, state_machine.name, state)] = state_id
                SubElement(region, "subvertex", {f"{{{xmi_ns}}}type": "uml:State", f"{{{xmi_ns}}}id": state_id, "name": state})
            for transition in state_machine.transitions:
                SubElement(
                    region,
                    "transition",
                    {
                        f"{{{xmi_ns}}}id": _mkid("tr", f"{block_name}.{state_machine.name}.{transition.name}", model.package_name),
                        "name": transition.name,
                        "source": ids[(block_name, state_machine.name, transition.source)],
                        "target": ids[(block_name, state_machine.name, transition.target)],
                    },
                )

    root_block_name = _guess_root_system_block(model)
    if root_block_name and root_block_name in model.parts:
        root_block_el = _find_element_by_id(blocks_pkg, xmi_ns, ids[root_block_name])
        if root_block_el is not None:
            for index, connector in enumerate(_build_connector_candidates(model, root_block_name), start=1):
                from_end = connector["from"]
                to_end = connector["to"]
                connector_id = _mkid(
                    "conn",
                    f"{root_block_name}.{index}.{from_end['part_property']}.{from_end['port_name']}.{to_end['part_property']}.{to_end['port_name']}",
                    model.package_name,
                )
                connector_el = SubElement(
                    root_block_el,
                    "ownedConnector",
                    {
                        f"{{{xmi_ns}}}type": "uml:Connector",
                        f"{{{xmi_ns}}}id": connector_id,
                        "name": f"{from_end['part_property']}_{from_end['port_name']}_to_{to_end['part_property']}_{to_end['port_name']}",
                    },
                )
                SubElement(
                    connector_el,
                    "end",
                    {
                        f"{{{xmi_ns}}}id": _mkid("ce", f"{connector_id}.1", model.package_name),
                        "role": ids[(from_end["part_type"], from_end["port_name"])],
                        "partWithPort": ids[(root_block_name, from_end["part_property"])],
                    },
                )
                SubElement(
                    connector_el,
                    "end",
                    {
                        f"{{{xmi_ns}}}id": _mkid("ce", f"{connector_id}.2", model.package_name),
                        "role": ids[(to_end["part_type"], to_end["port_name"])],
                        "partWithPort": ids[(root_block_name, to_end["part_property"])],
                    },
                )

    if root_block_name:
        for requirement in model.requirements:
            abstraction_id = _mkid("abs", f"{root_block_name}->{requirement.name}", model.package_name)
            ids[("sat", requirement.name)] = abstraction_id
            SubElement(
                relationships_pkg,
                "packagedElement",
                {
                    f"{{{xmi_ns}}}type": "uml:Abstraction",
                    f"{{{xmi_ns}}}id": abstraction_id,
                    "name": f"satisfy_{requirement.name}",
                    "client": ids[root_block_name],
                    "supplier": ids[requirement.name],
                },
            )

    for item in model.items:
        SubElement(root, f"{{{sysml_ns}}}ValueType", {f"{{{xmi_ns}}}id": _mkid("stvt", item, model.package_name), "base_DataType": ids[item]})
    for port_name, port_def in model.port_defs.items():
        SubElement(root, f"{{{sysml_ns}}}InterfaceBlock", {f"{{{xmi_ns}}}id": _mkid("stifb", port_name, model.package_name), "base_Class": ids[port_name]})
        SubElement(
            root,
            f"{{{sysml_ns}}}FlowProperty",
            {
                f"{{{xmi_ns}}}id": _mkid("stflow", f"{port_name}.{port_def.item_name}", model.package_name),
                "base_Property": ids[(port_name, port_def.item_name)],
                "direction": port_def.direction,
            },
        )
    for requirement in model.requirements:
        SubElement(
            root,
            f"{{{sysml_ns}}}Requirement",
            {
                f"{{{xmi_ns}}}id": _mkid("streq", requirement.name, model.package_name),
                "base_Class": ids[requirement.name],
                "Id": requirement.req_id,
                "Text": requirement.text,
            },
        )
    for block_name, block in model.parts.items():
        SubElement(root, f"{{{sysml_ns}}}Block", {f"{{{xmi_ns}}}id": _mkid("stblk", block_name, model.package_name), "base_Class": ids[block_name]})
        for part in block.parts:
            SubElement(
                root,
                f"{{{sysml_ns}}}PartProperty",
                {
                    f"{{{xmi_ns}}}id": _mkid("stpart", f"{block_name}.{part.name}", model.package_name),
                    "base_Property": ids[(block_name, part.name)],
                },
            )
        for port in block.ports:
            SubElement(
                root,
                f"{{{sysml_ns}}}ProxyPort",
                {
                    f"{{{xmi_ns}}}id": _mkid("stproxy", f"{block_name}.{port.name}", model.package_name),
                    "base_Port": ids[(block_name, port.name)],
                },
            )
    if root_block_name:
        for requirement in model.requirements:
            SubElement(
                root,
                f"{{{sysml_ns}}}Satisfy",
                {
                    f"{{{xmi_ns}}}id": _mkid("stsat", requirement.name, model.package_name),
                    "base_Abstraction": ids[("sat", requirement.name)],
                },
            )

    return _pretty_xml(root)
