from __future__ import annotations

import hashlib
import itertools
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any
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
    type_name: str | None = None


@dataclass
class BlockDefinition:
    name: str
    ports: list[PortUsage]
    parts: list[PartUsage]
    connectors: list["ConnectorDefinition"]
    state_machines: list[StateMachineDefinition]


@dataclass
class CanonicalModel:
    package_name: str
    package_doc: str | None
    items: list[str]
    port_defs: dict[str, PortDefinition]
    requirement_defs: dict[str, RequirementDefinition]
    requirements: list[RequirementDefinition]
    parts: dict[str, BlockDefinition]
    top_parts: list[PartUsage]


@dataclass
class ConnectorDefinition:
    name: str
    type_name: str | None
    from_part: str
    from_port: str
    to_part: str
    to_port: str


def generate_sysml_v1_xmi(canonical_sysml: str, target: str, projection_manifest: dict[str, Any] | None = None) -> str:
    if target not in TOOL_PROFILES:
        supported = ", ".join(sorted(TOOL_PROFILES))
        raise ValueError(f"Unsupported SysML v1 XMI target: {target}. Supported targets: {supported}")
    model = parse_sysml_v2_text(canonical_sysml)
    return _generate_xmi(model, target, projection_manifest)


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
            item_type=_strip_qualified_name(item_type),
        )

    requirement_defs: dict[str, RequirementDefinition] = {}
    for block in _find_named_blocks(text, "requirement def"):
        doc_match = re.search(r"doc\s*/\*(.*?)\*/", block["body"], re.S)
        doc = doc_match.group(1).strip() if doc_match else ""
        id_match = re.search(r"([A-Za-z0-9_-]+)\s*:\s*(.*)", doc, re.S)
        req_id = id_match.group(1).strip() if id_match else block["name"]
        req_text = re.sub(r"\s+", " ", id_match.group(2).strip()) if id_match else doc
        requirement_defs[block["name"]] = RequirementDefinition(
            name=block["name"],
            doc=doc,
            req_id=req_id,
            text=req_text,
        )

    requirements = _collect_requirement_usages(text, requirement_defs) or list(requirement_defs.values())

    parts: dict[str, BlockDefinition] = {}
    for block in _find_named_blocks(text, "part def"):
        body = block["body"]
        nested_parts = [
            PartUsage(name=match.group(1), type_name=_strip_qualified_name(match.group(2)))
            for match in re.finditer(r"^\s*part\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s*;", body, re.M)
        ]
        ports = [
            PortUsage(name=match.group(1), conjugated=bool(match.group(2)), type_name=_strip_qualified_name(match.group(3)))
            for match in re.finditer(r"^\s*port\s+([A-Za-z_]\w*)\s*:\s*(~?)([A-Za-z_][\w:]*)\s*;", body, re.M)
        ]
        connectors = _collect_connectors(body)
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
            connectors=connectors,
            state_machines=state_machines,
        )

    for usage_name, type_name, body in _collect_part_usage_blocks(text):
        connectors = _collect_connectors(body)
        if not connectors:
            continue
        local_type = _strip_qualified_name(type_name)
        if local_type in parts:
            existing = {(c.name, c.from_part, c.from_port, c.to_part, c.to_port) for c in parts[local_type].connectors}
            for connector in connectors:
                key = (connector.name, connector.from_part, connector.from_port, connector.to_part, connector.to_port)
                if key not in existing:
                    parts[local_type].connectors.append(connector)
        elif usage_name in parts:
            parts[usage_name].connectors.extend(connectors)

    top_parts = [
        PartUsage(name=match.group(1), type_name=_strip_qualified_name(match.group(2)))
        for match in re.finditer(r"^\s*part\s+(?!def\b)([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s*(?:;|\{)", text, re.M)
    ]

    return CanonicalModel(
        package_name=package_name,
        package_doc=package_doc,
        items=items,
        port_defs=port_defs,
        requirement_defs=requirement_defs,
        requirements=requirements,
        parts=parts,
        top_parts=top_parts,
    )


def _mkid(prefix: str, name: str, package: str = "") -> str:
    digest = hashlib.md5(f"{package}::{prefix}::{name}".encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _ea_id(prefix: str, name: str, package: str = "") -> str:
    digest = hashlib.md5(f"{package}::{prefix}::{name}".encode("utf-8")).hexdigest().upper()
    guid = f"{digest[:8]}_{digest[8:12]}_{digest[12:16]}_{digest[16:20]}_{digest[20:32]}"
    if prefix == "pkg":
        return f"EAPK_{guid}"
    return f"EAID_{guid}"


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


def _strip_qualified_name(name: str) -> str:
    return name.split("::")[-1]


def _collect_requirement_usages(text: str, requirement_defs: dict[str, RequirementDefinition]) -> list[RequirementDefinition]:
    usages: list[RequirementDefinition] = []
    seen: set[str] = set()
    pattern = re.compile(
        r"^\s*requirement\s+(?!def\b)([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s*(\{|;)",
        re.M,
    )
    for match in pattern.finditer(text):
        usage_name = match.group(1)
        type_name = _strip_qualified_name(match.group(2))
        if usage_name in seen:
            continue
        base = requirement_defs.get(type_name)
        if base is not None:
            doc = base.doc
            req_id = base.req_id
            req_text = base.text
        else:
            doc = ""
            req_id = usage_name
            req_text = ""
        usages.append(
            RequirementDefinition(
                name=usage_name,
                doc=doc,
                req_id=req_id,
                text=req_text,
                type_name=type_name,
            )
        )
        seen.add(usage_name)
    return usages


def _collect_connectors(text: str) -> list[ConnectorDefinition]:
    connectors: list[ConnectorDefinition] = []
    pattern = re.compile(
        r"^\s*interface\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s+connect\s+([A-Za-z_]\w*)::([A-Za-z_]\w*)\s+to\s+([A-Za-z_]\w*)::([A-Za-z_]\w*)\s*;",
        re.M,
    )
    for match in pattern.finditer(text):
        connectors.append(
            ConnectorDefinition(
                name=match.group(1),
                type_name=_strip_qualified_name(match.group(2)),
                from_part=match.group(3),
                from_port=match.group(4),
                to_part=match.group(5),
                to_port=match.group(6),
            )
        )
    return connectors


def _collect_part_usage_blocks(text: str) -> list[tuple[str, str, str]]:
    blocks: list[tuple[str, str, str]] = []
    pattern = re.compile(r"^\s*part\s+(?!def\b)([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w:]*)\s*\{", re.M)
    for match in pattern.finditer(text):
        brace_start = text.find("{", match.end() - 1)
        body, _ = _match_brace_block(text, brace_start)
        blocks.append((match.group(1), match.group(2), body))
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
    if root_block.connectors:
        connectors: list[dict[str, dict[str, str] | str]] = []
        for connector in root_block.connectors:
            left_part = next((part for part in root_block.parts if part.name == connector.from_part), None)
            right_part = next((part for part in root_block.parts if part.name == connector.to_part), None)
            if left_part is None or right_part is None:
                continue
            connectors.append(
                {
                    "from": {
                        "part_property": connector.from_part,
                        "part_type": left_part.type_name,
                        "port_name": connector.from_port,
                        "port_type": "",
                        "direction": "",
                    },
                    "to": {
                        "part_property": connector.to_part,
                        "part_type": right_part.type_name,
                        "port_name": connector.to_port,
                        "port_type": "",
                        "direction": "",
                    },
                    "port_type": connector.type_name or "",
                    "name": connector.name,
                }
            )
        if connectors:
            return connectors
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


def _resolve_requirement_id(model: CanonicalModel, ids: dict[object, str], path: str) -> str | None:
    local_name = _strip_qualified_name(path)
    for requirement in model.requirements:
        if requirement.name == local_name:
            return ids.get(requirement.name)
    base = model.requirement_defs.get(local_name)
    if base is not None:
        return ids.get(base.name)
    return None


def _resolve_structure_element_id(model: CanonicalModel, ids: dict[object, str], path: str) -> str | None:
    local_parts = [_strip_qualified_name(segment) for segment in path.split("::") if segment]
    if not local_parts:
        return None

    current_type: str | None = None
    for part_name in local_parts:
        if current_type is None:
            top_part = next((part for part in model.top_parts if part.name == part_name), None)
            if top_part is not None:
                current_type = top_part.type_name
                continue
            if part_name in model.parts:
                current_type = part_name
                continue
            continue
        if current_type not in model.parts:
            return None
        nested = next((part for part in model.parts[current_type].parts if part.name == part_name), None)
        if nested is None:
            return None
        current_type = nested.type_name

    if current_type is None:
        return None
    return ids.get(current_type)


def _pretty_xml(element: Element) -> str:
    return minidom.parseString(ET.tostring(element, encoding="utf-8")).toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")


def _find_element_by_id(parent: Element, xmi_ns: str, xmi_id: str) -> Element | None:
    key = f"{{{xmi_ns}}}id"
    for element in parent.iter():
        if element.attrib.get(key) == xmi_id:
            return element
    return None


def _add_ea_diagram(
    diagrams_el: Element,
    xmi_ns: str,
    diagram_id: str,
    package_id: str,
    local_id: int,
    name: str,
    diagram_type: str,
    style1: str,
    style2: str,
    persistent_style: str,
    elements: list[dict[str, str | int]],
    parent_id: str | None = None,
) -> None:
    diagram_el = SubElement(diagrams_el, "diagram", {f"{{{xmi_ns}}}id": diagram_id})
    model_attrs = {"package": package_id, "localID": str(local_id), "owner": package_id}
    if parent_id:
        model_attrs["parent"] = parent_id
    SubElement(diagram_el, "model", model_attrs)
    SubElement(diagram_el, "properties", {"name": name, "type": diagram_type})
    SubElement(diagram_el, "project", {"author": "sysml-builder", "version": "1.0"})
    SubElement(diagram_el, "style1", {"value": style1})
    SubElement(diagram_el, "style2", {"value": style2})
    SubElement(
        diagram_el,
        "swimlanes",
        {
            "value": (
                "locked=false;orientation=0;width=0;inbar=false;names=false;color=-1;bold=false;fcol=0;"
                "tcol=-1;ofCol=-1;ufCol=-1;hl=1;ufh=0;hh=0;cls=0;bw=0;hli=0;bro=0;"
            )
        },
    )
    SubElement(
        diagram_el,
        "matrixitems",
        {"value": "locked=false;matrixactive=false;swimlanesactive=true;kanbanactive=false;width=1;clrLine=0;"},
    )
    SubElement(diagram_el, "extendedProperties")
    SubElement(diagram_el, "persistentstyle", {"value": persistent_style})
    SubElement(diagram_el, "xrefs")
    diagram_elements = SubElement(diagram_el, "elements")
    for element in elements:
        attrs = {
            "geometry": str(element["geometry"]),
            "subject": str(element["subject"]),
            "seqno": str(element["seqno"]),
            "style": str(element["style"]),
        }
        SubElement(diagram_elements, "element", attrs)


def _add_ea_extension_elements(extension: Element, xmi_ns: str, model: CanonicalModel, ids: dict[object, str]) -> None:
    elements_el = SubElement(extension, "elements")

    def add_common_metadata(element_el: Element, package_name: str, vertical_swimlanes: str = "1", horizontal_swimlanes: str = "1") -> None:
        SubElement(element_el, "project", {"author": "sysml-builder", "version": "1.0", "phase": "1.0", "complexity": "1", "status": "Draft"})
        SubElement(
            element_el,
            "style",
            {"appearance": f"BackColor=-1;BorderColor=-1;BorderWidth=-1;FontColor=-1;VSwimLanes={vertical_swimlanes};HSwimLanes={horizontal_swimlanes};BorderStyle=0;"},
        )
        if element_el.find("tags") is None:
            SubElement(element_el, "tags")
        SubElement(element_el, "xrefs")
        SubElement(element_el, "extendedProperties", {"tagged": "0", "package_name": package_name})

    package_specs = [
        ("root", model.package_name, ids[("pkg", "root")]),
        ("blocks", "Blocks", ids[("pkg", "blocks")]),
        ("requirements", "Requirements", ids[("pkg", "requirements")]),
    ]
    for key, name, element_id in package_specs:
        element_el = SubElement(
            elements_el,
            "element",
            {"xmi:idref": element_id, "xmi:type": "uml:Package", "name": name, "scope": "public"},
        )
        model_attrs = {"package2": element_id, "tpos": "0", "ea_eleType": "package"}
        if key == "root":
            model_attrs["package"] = ids[("model", "root")]
        else:
            model_attrs["package"] = ids[("pkg", "root")]
        SubElement(element_el, "model", model_attrs)
        SubElement(element_el, "properties", {"isSpecification": "false", "sType": "Package", "nType": "0", "scope": "public"})
        add_common_metadata(element_el, model.package_name if key != "root" else "ModelRoot")

    for block_name in sorted(model.parts):
        element_el = SubElement(
            elements_el,
            "element",
            {"xmi:idref": ids[block_name], "xmi:type": "uml:Class", "name": block_name, "scope": "public"},
        )
        SubElement(element_el, "model", {"package": ids[("pkg", "blocks")], "tpos": "0", "ea_eleType": "element"})
        SubElement(
            element_el,
            "properties",
            {"isSpecification": "false", "sType": "Class", "nType": "0", "scope": "public", "stereotype": "block"},
        )
        add_common_metadata(element_el, "Blocks")

        block = model.parts[block_name]
        for state_machine in block.state_machines:
            sm_id = ids[("sm", block_name, state_machine.name)]
            sm_el = SubElement(
                elements_el,
                "element",
                {"xmi:idref": sm_id, "xmi:type": "uml:StateMachine", "name": state_machine.name, "scope": "public"},
            )
            SubElement(sm_el, "model", {"package": ids[("pkg", "blocks")], "owner": ids[block_name], "tpos": "0", "ea_eleType": "element"})
            SubElement(sm_el, "properties", {"isSpecification": "false", "sType": "StateMachine", "nType": "0", "scope": "public"})
            add_common_metadata(sm_el, "Blocks")

            for state in state_machine.states:
                state_id = ids[(block_name, state_machine.name, state)]
                state_el = SubElement(
                    elements_el,
                    "element",
                    {"xmi:idref": state_id, "xmi:type": "uml:State", "name": state, "scope": "public"},
                )
                SubElement(state_el, "model", {"package": ids[("pkg", "blocks")], "owner": sm_id, "tpos": "0", "ea_eleType": "element"})
                SubElement(state_el, "properties", {"isSpecification": "false", "sType": "State", "nType": "0", "scope": "public"})
                links_el = SubElement(state_el, "links")
                for transition in state_machine.transitions:
                    transition_id = ids[("tr", block_name, state_machine.name, transition.name)]
                    if transition.source == state:
                        SubElement(links_el, "StateFlow", {"xmi:id": transition_id, "start": state_id, "end": ids[(block_name, state_machine.name, transition.target)]})
                    elif transition.target == state:
                        SubElement(links_el, "StateFlow", {"xmi:id": transition_id, "start": ids[(block_name, state_machine.name, transition.source)], "end": state_id})
                add_common_metadata(state_el, "Blocks", "0", "0")

    for requirement in model.requirements:
        element_el = SubElement(
            elements_el,
            "element",
            {"xmi:idref": ids[requirement.name], "xmi:type": "uml:Class", "name": requirement.name, "scope": "public"},
        )
        SubElement(element_el, "model", {"package": ids[("pkg", "requirements")], "tpos": "0", "ea_eleType": "element"})
        SubElement(
            element_el,
            "properties",
            {"isSpecification": "false", "sType": "Class", "nType": "0", "scope": "public", "stereotype": "requirement"},
        )
        tags_el = SubElement(element_el, "tags")
        SubElement(tags_el, "tag", {"xmi:id": _ea_id("tag", f"{requirement.name}.Id", model.package_name), "name": "Id", "value": requirement.req_id, "modelElement": ids[requirement.name]})
        SubElement(tags_el, "tag", {"xmi:id": _ea_id("tag", f"{requirement.name}.Text", model.package_name), "name": "Text", "value": requirement.text, "modelElement": ids[requirement.name]})
        add_common_metadata(element_el, "Requirements")


def _add_ea_diagrams(root: Element, xmi_ns: str, model: CanonicalModel, ids: dict[object, str]) -> None:
    extension = SubElement(root, f"{{{xmi_ns}}}Extension", {"extender": "Enterprise Architect", "extenderID": "6.5"})
    _add_ea_extension_elements(extension, xmi_ns, model, ids)
    diagrams_el = SubElement(extension, "diagrams")

    blocks_pkg_id = ids[("pkg", "blocks")]
    requirements_pkg_id = ids[("pkg", "requirements")]
    local_id = 1

    for block_name in sorted(model.parts):
        block = model.parts[block_name]
        for state_machine in block.state_machines:
            sm_id = ids[("sm", block_name, state_machine.name)]
            sm_elements: list[dict[str, str | int]] = []
            positions = [
                (60, 60),
                (190, 220),
                (358, 106),
                (220, 60),
                (380, 240),
            ]
            duid_by_state: dict[str, str] = {}
            for index, state in enumerate(state_machine.states, start=1):
                left, top = positions[(index - 1) % len(positions)]
                duid = _mkid("duid", f"{state_machine.name}.{state}", model.package_name)[-8:].upper()
                duid_by_state[state] = duid
                sm_elements.append(
                    {
                        "geometry": f"Left={left};Top={top};Right={left + 120};Bottom={top + 60};",
                        "subject": ids[(block_name, state_machine.name, state)],
                        "seqno": index,
                        "style": f"DUID={duid};NSL=0;",
                    }
                )
            sm_elements.append(
                {
                    "geometry": "Left=10;Top=10;Right=515;Bottom=319;",
                    "subject": sm_id,
                    "seqno": len(sm_elements) + 1,
                    "style": f"DUID={_mkid('duid', state_machine.name, model.package_name)[-8:].upper()};NSL=1;",
                }
            )
            for transition in state_machine.transitions:
                sm_elements.append(
                    {
                        "geometry": "EDGE=1;$LLB=;LLT=;LMT=CX=100:CY=16:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMB=;LRT=;LRB=;IRHS=;ILHS=;Path=;",
                        "subject": ids[("tr", block_name, state_machine.name, transition.name)],
                        "seqno": len(sm_elements) + 1,
                        "style": f"Mode=3;EOID={duid_by_state[transition.target]};SOID={duid_by_state[transition.source]};Color=-1;LWidth=0;Hidden=0;",
                    }
                )
            _add_ea_diagram(
                diagrams_el,
                xmi_ns,
                _ea_id("diag", f"{block_name}.{state_machine.name}", model.package_name),
                blocks_pkg_id,
                local_id,
                state_machine.name,
                "Statechart",
                (
                    "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;"
                    "PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;"
                ),
                "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MDGDgm=;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;",
                "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
                sm_elements,
                sm_id,
            )
            local_id += 1

    block_elements: list[dict[str, str | int]] = []
    for index, block_name in enumerate(sorted(model.parts), start=1):
        left = 80 + ((index - 1) % 3) * 180
        top = 70 + ((index - 1) // 3) * 120
        block_elements.append(
            {
                "geometry": f"Left={left};Top={top};Right={left + 130};Bottom={top + 70};",
                "subject": ids[block_name],
                "seqno": index,
                "style": f"DUID={_mkid('duid', block_name, model.package_name)[-8:]};NSL=0;",
            }
        )
    block_elements.append(
        {
            "geometry": "Left=10;Top=10;Right=700;Bottom=520;",
            "subject": blocks_pkg_id,
            "seqno": len(block_elements) + 1,
            "style": f"DUID={_mkid('duid', 'blocks-package', model.package_name)[-8:]};NSL=1;",
        }
    )
    _add_ea_diagram(
        diagrams_el,
        xmi_ns,
        _ea_id("diag", "blocks", model.package_name),
        blocks_pkg_id,
        local_id,
        "Blocks",
        "Logical",
        (
            "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;"
            "PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;"
        ),
        (
            "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;"
            "MDGDgm=SysML1.4::BlockDefinition;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;"
        ),
        "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
        block_elements,
    )
    local_id += 1

    root_block_name = _guess_root_system_block(model)
    if root_block_name is not None and root_block_name in model.parts:
        root_block = model.parts[root_block_name]
        ibd_elements: list[dict[str, str | int]] = []
        for index, part in enumerate(root_block.parts, start=1):
            left = 80 + ((index - 1) % 3) * 180
            top = 80 + ((index - 1) // 3) * 140
            ibd_elements.append(
                {
                    "geometry": f"Left={left};Top={top};Right={left + 140};Bottom={top + 90};",
                    "subject": ids[(root_block_name, part.name)],
                    "seqno": index,
                    "style": f"DUID={_mkid('duid', f'{root_block_name}.{part.name}', model.package_name)[-8:]};NSL=0;",
                }
            )
        for connector_index, connector in enumerate(root_block.connectors, start=1):
            connector_id = ids.get(("conn", root_block_name, connector_index))
            if connector_id is None:
                continue
            ibd_elements.append(
                {
                    "geometry": "EDGE=1;$LLB=;LLT=;LMT=CX=100:CY=16:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMB=;LRT=;LRB=;IRHS=;ILHS=;Path=;",
                    "subject": connector_id,
                    "seqno": len(ibd_elements) + 1,
                    "style": "Color=-1;LWidth=0;Hidden=0;",
                }
            )
        ibd_elements.append(
            {
                "geometry": "Left=10;Top=10;Right=760;Bottom=520;",
                "subject": ids[root_block_name],
                "seqno": len(ibd_elements) + 1,
                "style": f"DUID={_mkid('duid', f'{root_block_name}-ibd', model.package_name)[-8:]};NSL=1;",
            }
        )
        _add_ea_diagram(
            diagrams_el,
            xmi_ns,
            _ea_id("diag", f"ibd.{root_block_name}", model.package_name),
            ids[root_block_name],
            local_id,
            f"{root_block_name} Internal",
            "CompositeStructure",
            (
                "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;"
                "PackageContents=1;Zoom=100;ShowIcons=1;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=0;"
            ),
            (
                "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;"
                "MDGDgm=SysML1.4::InternalBlock;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;"
            ),
            "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
            ibd_elements,
            ids[root_block_name],
        )
        local_id += 1

    requirement_elements: list[dict[str, str | int]] = []
    for index, requirement in enumerate(model.requirements, start=1):
        left = 120
        top = 80 + (index - 1) * 150
        width = max(420, min(900, 140 + len(requirement.text) * 4))
        requirement_elements.append(
            {
                "geometry": f"Left={left};Top={top};Right={left + width};Bottom={top + 100};",
                "subject": ids[requirement.name],
                "seqno": index,
                "style": f"DUID={_mkid('duid', requirement.name, model.package_name)[-8:]};NSL=0;",
            }
        )
    requirement_elements.append(
        {
            "geometry": "Left=10;Top=10;Right=980;Bottom=720;",
            "subject": requirements_pkg_id,
            "seqno": len(requirement_elements) + 1,
            "style": f"DUID={_mkid('duid', 'requirements-package', model.package_name)[-8:]};NSL=1;",
        }
    )
    _add_ea_diagram(
        diagrams_el,
        xmi_ns,
        _ea_id("diag", "requirements", model.package_name),
        requirements_pkg_id,
        local_id,
        "Requirements",
        "Custom",
        (
            "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;"
            "PackageContents=1;Zoom=100;ShowIcons=1;ShowTags=1;HideAtts=1;HideOps=1;HideStereo=0;HideElemStereo=0;"
        ),
        (
            "ExcludeRTF=0;DocAll=0;AttPkg=1;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;"
            "MDGDgm=SysML1.4::Requirement;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;"
        ),
        "DGS=On=0:CNT=8:W=120:H=40:SG=0:SGH=0:AEB=0:;AR=0;DCL=0;",
        requirement_elements,
    )


def _generate_xmi(model: CanonicalModel, target: str, projection_manifest: dict[str, Any] | None = None) -> str:
    profile = TOOL_PROFILES[target]
    xmi_ns = profile["xmi_ns"]
    uml_ns = profile["uml_ns"]
    sysml_ns = profile["sysml_ns"]
    ecore_ns = "http://www.eclipse.org/emf/2002/Ecore"
    make_id = _ea_id if target == "ea" else _mkid

    register_namespace("xmi", xmi_ns)
    register_namespace("uml", uml_ns)
    register_namespace("sysml", sysml_ns)
    register_namespace("ecore", ecore_ns)

    root = Element(f"{{{xmi_ns}}}XMI", {f"{{{xmi_ns}}}version": profile["xmi_version"]})
    if target == "ea":
        SubElement(root, f"{{{xmi_ns}}}Documentation", {"exporter": "Enterprise Architect", "exporterVersion": "6.5", "exporterID": "1628"})
    model_id = make_id("model", model.package_name, model.package_name)
    uml_model = SubElement(
        root,
        f"{{{uml_ns}}}Model",
        {f"{{{xmi_ns}}}id": model_id, "name": "EA_Model" if target == "ea" else model.package_name},
    )

    package_container = uml_model
    if target == "ea":
        root_package_id = make_id("pkg", model.package_name, model.package_name)
        package_container = SubElement(
            uml_model,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": root_package_id, "name": model.package_name},
        )

    if model.package_doc:
        owned_comment = SubElement(package_container, "ownedComment", {f"{{{xmi_ns}}}id": make_id("comment", model.package_name, model.package_name)})
        body = SubElement(owned_comment, "body")
        body.text = model.package_doc

    profile_application = SubElement(
        uml_model,
        "profileApplication",
        {
            f"{{{xmi_ns}}}type": "uml:ProfileApplication",
            f"{{{xmi_ns}}}id": make_id("pa", "sysml", model.package_name),
            "applyingPackage": model_id,
        },
    )
    extension = SubElement(profile_application, f"{{{xmi_ns}}}Extension", {"extender": "http://www.eclipse.org/emf/2002/Ecore"})
    annotation = SubElement(
        extension,
        f"{{{ecore_ns}}}EAnnotation",
        {
            f"{{{xmi_ns}}}id": make_id("eann", "sysml", model.package_name),
            "source": "http://www.eclipse.org/uml2/2.0.0/UML",
        },
    )
    SubElement(annotation, "references", {f"{{{xmi_ns}}}type": "ecore:EPackage", "href": profile["profile_href"]})
    SubElement(profile_application, "appliedProfile", {f"{{{xmi_ns}}}type": "uml:Profile", "href": profile["profile_href"]})

    data_types_pkg = SubElement(
        package_container,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": make_id("pkg", "datatypes", model.package_name), "name": "DataTypes"},
    )
    ports_pkg = SubElement(
        package_container,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": make_id("pkg", "ports", model.package_name), "name": "Ports"},
    )
    requirements_pkg = SubElement(
        package_container,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": make_id("pkg", "requirements", model.package_name), "name": "Requirements"},
    )
    blocks_pkg = SubElement(
        package_container,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": make_id("pkg", "blocks", model.package_name), "name": "Blocks"},
    )
    relationships_pkg = SubElement(
        package_container,
        "packagedElement",
        {f"{{{xmi_ns}}}type": "uml:Package", f"{{{xmi_ns}}}id": make_id("pkg", "relationships", model.package_name), "name": "Relationships"},
    )

    ids: dict[object, str] = {}
    ids[("model", "root")] = model_id
    if target == "ea":
        ids[("pkg", "root")] = root_package_id
    ids[("pkg", "datatypes")] = data_types_pkg.attrib[f"{{{xmi_ns}}}id"]
    ids[("pkg", "ports")] = ports_pkg.attrib[f"{{{xmi_ns}}}id"]
    ids[("pkg", "requirements")] = requirements_pkg.attrib[f"{{{xmi_ns}}}id"]
    ids[("pkg", "blocks")] = blocks_pkg.attrib[f"{{{xmi_ns}}}id"]
    ids[("pkg", "relationships")] = relationships_pkg.attrib[f"{{{xmi_ns}}}id"]

    for item in model.items:
        item_id = make_id("dt", item, model.package_name)
        ids[item] = item_id
        SubElement(data_types_pkg, "packagedElement", {f"{{{xmi_ns}}}type": "uml:DataType", f"{{{xmi_ns}}}id": item_id, "name": item})

    for port_name, port_def in model.port_defs.items():
        interface_block_id = make_id("ifb", port_name, model.package_name)
        ids[port_name] = interface_block_id
        interface_block = SubElement(
            ports_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": interface_block_id, "name": port_name},
        )
        flow_id = make_id("flow", f"{port_name}.{port_def.item_name}", model.package_name)
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
        requirement_id = make_id("req", requirement.name, model.package_name)
        ids[requirement.name] = requirement_id
        requirement_class = SubElement(
            requirements_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": requirement_id, "name": requirement.name},
        )
        comment = SubElement(requirement_class, "ownedComment", {f"{{{xmi_ns}}}id": make_id("comment", requirement.name, model.package_name)})
        body = SubElement(comment, "body")
        body.text = requirement.doc

    for block_name, block in model.parts.items():
        block_id = make_id("blk", block_name, model.package_name)
        ids[block_name] = block_id
        block_class = SubElement(
            blocks_pkg,
            "packagedElement",
            {f"{{{xmi_ns}}}type": "uml:Class", f"{{{xmi_ns}}}id": block_id, "name": block_name},
        )
        for part in block.parts:
            property_id = make_id("prop", f"{block_name}.{part.name}", model.package_name)
            ids[(block_name, part.name)] = property_id
            SubElement(
                block_class,
                "ownedAttribute",
                {
                    f"{{{xmi_ns}}}type": "uml:Property",
                    f"{{{xmi_ns}}}id": property_id,
                    "name": part.name,
                    "type": make_id("blk", part.type_name, model.package_name),
                    "aggregation": "composite",
                },
            )
        for port in block.ports:
            port_id = make_id("port", f"{block_name}.{port.name}", model.package_name)
            ids[(block_name, port.name)] = port_id
            SubElement(
                block_class,
                "ownedAttribute",
                {
                    f"{{{xmi_ns}}}type": "uml:Port",
                    f"{{{xmi_ns}}}id": port_id,
                    "name": port.name,
                    "type": make_id("ifb", port.type_name, model.package_name),
                },
            )
        for state_machine in block.state_machines:
            state_machine_id = make_id("sm", f"{block_name}.{state_machine.name}", model.package_name)
            ids[("sm", block_name, state_machine.name)] = state_machine_id
            state_machine_el = SubElement(
                block_class,
                "ownedBehavior",
                {f"{{{xmi_ns}}}type": "uml:StateMachine", f"{{{xmi_ns}}}id": state_machine_id, "name": state_machine.name},
            )
            region = SubElement(
                state_machine_el,
                "region",
                {f"{{{xmi_ns}}}id": make_id("region", f"{block_name}.{state_machine.name}", model.package_name)},
            )
            for state in state_machine.states:
                state_id = make_id("state", f"{block_name}.{state_machine.name}.{state}", model.package_name)
                ids[(block_name, state_machine.name, state)] = state_id
                SubElement(region, "subvertex", {f"{{{xmi_ns}}}type": "uml:State", f"{{{xmi_ns}}}id": state_id, "name": state})
            for transition in state_machine.transitions:
                transition_id = make_id("tr", f"{block_name}.{state_machine.name}.{transition.name}", model.package_name)
                ids[("tr", block_name, state_machine.name, transition.name)] = transition_id
                SubElement(
                    region,
                    "transition",
                    {
                        f"{{{xmi_ns}}}id": transition_id,
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
                connector_name = connector.get("name") or f"{from_end['part_property']}_{from_end['port_name']}_to_{to_end['part_property']}_{to_end['port_name']}"
                connector_id = make_id(
                    "conn",
                    f"{root_block_name}.{index}.{connector_name}",
                    model.package_name,
                )
                connector_el = SubElement(
                    root_block_el,
                    "ownedConnector",
                    {
                        f"{{{xmi_ns}}}type": "uml:Connector",
                        f"{{{xmi_ns}}}id": connector_id,
                        "name": str(connector_name),
                    },
                )
                SubElement(
                    connector_el,
                    "end",
                    {
                        f"{{{xmi_ns}}}id": make_id("ce", f"{connector_id}.1", model.package_name),
                        "role": ids[(from_end["part_type"], from_end["port_name"])],
                        "partWithPort": ids[(root_block_name, from_end["part_property"])],
                    },
                )
                SubElement(
                    connector_el,
                    "end",
                    {
                        f"{{{xmi_ns}}}id": make_id("ce", f"{connector_id}.2", model.package_name),
                        "role": ids[(to_end["part_type"], to_end["port_name"])],
                        "partWithPort": ids[(root_block_name, to_end["part_property"])],
                    },
                )

    satisfy_relationships: list[tuple[str, str, str]] = []
    if projection_manifest:
        for claim in projection_manifest.get("satisfy_claims", []):
            requirement_id = _resolve_requirement_id(model, ids, claim.get("requirement", ""))
            structure_id = _resolve_structure_element_id(model, ids, claim.get("by", ""))
            if requirement_id and structure_id:
                satisfy_relationships.append((claim.get("requirement", ""), structure_id, requirement_id))
    if not satisfy_relationships and root_block_name:
        for requirement in model.requirements:
            satisfy_relationships.append((requirement.name, ids[root_block_name], ids[requirement.name]))

    for index, (name_hint, client_id, supplier_id) in enumerate(satisfy_relationships, start=1):
        dependency_id = make_id("dep", f"satisfy.{index}.{name_hint}", model.package_name)
        ids[("sat", index)] = dependency_id
        SubElement(
            relationships_pkg,
            "packagedElement",
            {
                f"{{{xmi_ns}}}type": "uml:Dependency",
                f"{{{xmi_ns}}}id": dependency_id,
                "name": f"satisfy_{_strip_qualified_name(name_hint)}",
                "client": client_id,
                "supplier": supplier_id,
            },
        )

    allocation_relationships: list[tuple[str, str, str]] = []
    if projection_manifest:
        contract_to_requirement_id = {
            entry["source_contract"]: ids[entry["sysml_name"]]
            for entry in projection_manifest.get("requirements", [])
            if entry.get("source_contract") and entry.get("sysml_name") in ids
        }
        for allocation in projection_manifest.get("allocations", []):
            client_id = contract_to_requirement_id.get(allocation.get("contract", ""))
            supplier_id = _resolve_structure_element_id(model, ids, allocation.get("allocated_to", ""))
            if client_id and supplier_id:
                allocation_relationships.append((allocation.get("id", ""), client_id, supplier_id))

    for index, (allocation_name, client_id, supplier_id) in enumerate(allocation_relationships, start=1):
        dependency_id = make_id("dep", f"allocate.{index}.{allocation_name}", model.package_name)
        ids[("alloc", index)] = dependency_id
        SubElement(
            relationships_pkg,
            "packagedElement",
            {
                f"{{{xmi_ns}}}type": "uml:Dependency",
                f"{{{xmi_ns}}}id": dependency_id,
                "name": allocation_name or f"allocate_{index}",
                "client": client_id,
                "supplier": supplier_id,
            },
        )

    for item in model.items:
        SubElement(root, f"{{{sysml_ns}}}ValueType", {f"{{{xmi_ns}}}id": make_id("stvt", item, model.package_name), "base_DataType": ids[item]})
    for port_name, port_def in model.port_defs.items():
        SubElement(root, f"{{{sysml_ns}}}InterfaceBlock", {f"{{{xmi_ns}}}id": make_id("stifb", port_name, model.package_name), "base_Class": ids[port_name]})
        SubElement(
            root,
            f"{{{sysml_ns}}}FlowProperty",
            {
                f"{{{xmi_ns}}}id": make_id("stflow", f"{port_name}.{port_def.item_name}", model.package_name),
                "base_Property": ids[(port_name, port_def.item_name)],
                "direction": port_def.direction,
            },
        )
    for requirement in model.requirements:
        SubElement(
            root,
            f"{{{sysml_ns}}}Requirement",
            {
                f"{{{xmi_ns}}}id": make_id("streq", requirement.name, model.package_name),
                "base_Class": ids[requirement.name],
                "Id": requirement.req_id,
                "Text": requirement.text,
            },
        )
    for block_name, block in model.parts.items():
        SubElement(root, f"{{{sysml_ns}}}Block", {f"{{{xmi_ns}}}id": make_id("stblk", block_name, model.package_name), "base_Class": ids[block_name]})
        for part in block.parts:
            SubElement(
                root,
                f"{{{sysml_ns}}}PartProperty",
                {
                    f"{{{xmi_ns}}}id": make_id("stpart", f"{block_name}.{part.name}", model.package_name),
                    "base_Property": ids[(block_name, part.name)],
                },
            )
        for port in block.ports:
            SubElement(
                root,
                f"{{{sysml_ns}}}ProxyPort",
                {
                    f"{{{xmi_ns}}}id": make_id("stproxy", f"{block_name}.{port.name}", model.package_name),
                    "base_Port": ids[(block_name, port.name)],
                },
            )
    for index, _ in enumerate(satisfy_relationships, start=1):
        SubElement(
            root,
            f"{{{sysml_ns}}}Satisfy",
            {
                f"{{{xmi_ns}}}id": make_id("stsat", str(index), model.package_name),
                "base_Dependency": ids[("sat", index)],
            },
        )
    for index, _ in enumerate(allocation_relationships, start=1):
        SubElement(
            root,
            f"{{{sysml_ns}}}Allocate",
            {
                f"{{{xmi_ns}}}id": make_id("stalloc", str(index), model.package_name),
                "base_Dependency": ids[("alloc", index)],
            },
        )

    if target == "ea":
        _add_ea_diagrams(root, xmi_ns, model, ids)

    return _pretty_xml(root)
