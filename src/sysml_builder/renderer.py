from __future__ import annotations

import re
from typing import Any

from .profile_runtime import get_canonical_profile, get_case_profile, load_generic_case_profile, load_review_overlay_profile


JA_RENDER_REPLACEMENTS = [
    ("The engine shall transfer generated torque to the transmission through the clutch interface.", "エンジンはクラッチインタフェースを介して生成トルクをトランスミッションへ伝達しなければならない。"),
    ("The hull shall provide a typed HighSlot interface to a mining laser module.", "船体は採掘レーザーモジュールに対して型付きHighSlotインタフェースを提供しなければならない。"),
    ("The hull shall provide a typed MediumSlot interface to a shield hardener module.", "船体はシールドハードナーモジュールに対して型付きMediumSlotインタフェースを提供しなければならない。"),
    ("Main Flow:", "メインフロー:"),
    ("Exception Flows:", "例外フロー:"),
    ("Identify an asteroid target.", "小惑星ターゲットを特定する。"),
    ("Activate the mining laser.", "採掘レーザーを起動する。"),
    ("Extract ore and store it in the cargo hold.", "鉱石を採取し貨物倉へ格納する。"),
    ("Suspend mining when the cargo hold becomes full.", "貨物倉が満杯になったら採掘を中断する。"),
    ("If the mining laser fails, halt mining and alert the pilot.", "採掘レーザーが故障した場合、採掘を停止してパイロットへ通知する。"),
    ("If the target asteroid is depleted, reacquire a target.", "対象小惑星が枯渇した場合、ターゲットを再取得する。"),
    ("Establish a docking connection with a station.", "ステーションとのドッキング接続を確立する。"),
    ("Transfer ore to the station.", "鉱石をステーションへ移送する。"),
    ("Resupply essential systems.", "重要システムを補給する。"),
    ("If docking fails, notify the pilot and abort the offload sequence.", "ドッキングに失敗した場合、パイロットへ通知して荷下ろし手順を中止する。"),
    ("If cargo transfer fails, suspend operations and keep the ore on board.", "貨物移送に失敗した場合、運用を中断して鉱石を船内に保持する。"),
    ("Derived from operational use case objectives. Quantitative completion thresholds are intentionally left unresolved.", "運用ユースケースの目的から導出した。定量的な完了閾値は意図的に未解決のままとしている。"),
    ("VehicleModel uses explicit quantitative mass requirements.", "VehicleModel では明示的な定量質量要求が使われている。"),
    ("VehicleModel separates city and highway fuel economy requirements.", "VehicleModel では市街地と高速の燃費要求が分離されている。"),
    ("VehicleModel defines an EngineToTransmissionInterface between engine and transmission.", "VehicleModel ではエンジンとトランスミッションの間に EngineToTransmissionInterface が定義されている。"),
    ("Is lightweight a mass threshold or an acceleration/performance surrogate?", "軽量とは質量閾値なのか、それとも加速性能の代用なのか。"),
    ("Should fuel efficiency be split into city and highway contexts?", "燃費は市街地と高速の文脈に分割すべきか。"),
    ("Does reliable drive power imply an interface requirement, a performance requirement, or both?", "確実な駆動力供給はインタフェース要求を意味するのか、性能要求を意味するのか、それとも両方か。"),
    ("Assumption A1: lightweight most likely maps to mass.", "Assumption A1: 軽量は質量を指す可能性が高い。"),
    ("Assumption A2: fuel efficient most likely maps to city/highway fuel economy.", "Assumption A2: 燃費が良いとは市街地/高速燃費を指す可能性が高い。"),
    ("Assumption A3: drive power transfer most likely maps to a named interface.", "Assumption A3: 駆動力伝達は名前付きインタフェースを指す可能性が高い。"),
    ("The input is intentionally ambiguous.", "この入力は意図的に曖昧にしてある。"),
    ("The review overlay should remain the source of truth until the missing quantitative slots are accepted.", "不足している定量スロットが受理されるまでは、レビューオーバーレイを正とすべきである。"),
    ("Do not promote any draft to canonical until all missing quantitative slots are resolved.", "不足している定量スロットがすべて解決するまで、いかなるドラフトも canonical へ昇格させてはならない。"),
    ("define ore extraction completion criteria and cargo-full threshold", "鉱石採取の完了基準と貨物満杯閾値を定義する"),
    ("The use case contains main and exception flows but does not define measurable success limits.", "このユースケースはメインフローと例外フローを含むが、測定可能な成功限界を定義していない。"),
    ("define successful docking, cargo transfer completion, and resupply completion criteria", "成功したドッキング、貨物移送完了、補給完了の基準を定義する"),
    ("The narrative preserves flow but not completion metrics.", "この記述はフローを保持しているが完了指標は保持していない。"),
    ("Should mining completion be measured by ore quantity, time, or cargo fill percentage?", "採掘完了は鉱石量、時間、貨物充填率のどれで測るべきか。"),
    ("Should offload success be measured by all cargo transferred, minimum cargo transferred, or docking completion?", "荷下ろし成功は全貨物移送、最小貨物移送、ドッキング完了のどれで測るべきか。"),
    ("Candidate behavior decomposition:", "候補となる振る舞い分解:"),
    ("MineAsteroids -> target selection / mining activation / ore transfer / suspend on full cargo", "MineAsteroids -> ターゲット選択 / 採掘起動 / 鉱石移送 / 貨物満杯で中断"),
    ("OffloadOreAndResupply -> docking / cargo transfer / resupply / abort on failure", "OffloadOreAndResupply -> ドッキング / 貨物移送 / 補給 / 失敗時中止"),
    ("Canonical use cases are acceptable, but quantitative success criteria remain unresolved.", "canonical なユースケース自体は受容可能だが、定量的な成功基準は未解決のままである。"),
    ("Mining use cases in the reference model use a pilot and an asteroid belt.", "参照モデルの採掘ユースケースではパイロットと小惑星帯を用いている。"),
    ("Threat engagement use cases in the reference model use hostile ships and the pilot.", "参照モデルの脅威対処ユースケースでは敵対艦船とパイロットを用いている。"),
    ("Resupply use cases in the reference model involve a station actor.", "参照モデルの補給ユースケースにはステーションアクターが含まれる。"),
    ("What is the concrete success definition for efficient mining?", "効率的な採掘の具体的な成功定義は何か。"),
    ("What specific trigger makes a threat actionable?", "どの具体的なトリガが脅威を対処対象にするのか。"),
    ("When exactly is resupply considered necessary and complete?", "補給はどの時点で必要かつ完了と見なされるのか。"),
    ("This case is intentionally vague.", "このケースは意図的に曖昧である。"),
    ("It is grounded in the same source file as case05, but the input narrative omits most operational structure.", "case05 と同じソースファイルを根拠にしているが、入力記述では運用構造の大半を省略している。"),
    ("Do not emit canonical use cases until actors, objective text, and flow structure are accepted.", "アクター、目的テキスト、フロー構造が受理されるまで canonical なユースケースを出力してはならない。"),
]


def _localize(text: str, contracts: dict[str, Any]) -> str:
    if contracts.get("document", {}).get("language") != "ja":
        return text
    for source, target in JA_RENDER_REPLACEMENTS:
        text = text.replace(source, target)
    return text


def _indent(block: str, level: int = 1) -> str:
    prefix = "    " * level
    return "\n".join(prefix + line if line else "" for line in block.splitlines())


def _render_view_package(
    viewpoint_name: str,
    view_name: str,
    expose_paths: list[str],
    frame_name: str,
    package_name: str = "ViewDefinitions",
    imports: list[str] | None = None,
    rendering_type: str = "DS_Views::SymbolicViews::gv",
) -> list[str]:
    imports = imports or ["Views::*", "DS_Views::*"]
    lines = [f"    package {package_name} {{"]
    for import_name in imports:
        lines.append(f"        private import {import_name};")
    lines.extend(
        [
            "",
            f"        view {view_name} : {rendering_type} {{",
        ]
    )
    for expose_path in expose_paths:
        lines.append(f"            expose {expose_path};")
    lines.extend(
        [
            "        }",
            "    }",
        ]
    )
    return lines


def _render_state_machine(definition: dict[str, Any]) -> str:
    states = definition["states"]
    transitions = definition["transitions"]
    lines = [f"state def {definition['name']} {{", f"    entry; then {states[0]};", ""]
    for index, state in enumerate(states):
        lines.append(f"    state {state};")
        lines.append("")
        outgoing = [transition for transition in transitions if transition[0] == state]
        for source, target in outgoing:
            lines.append(f"    transition {source}_to_{target}")
            lines.append(f"        first {source}")
            lines.append(f"        then {target};")
            lines.append("")
    lines.append("}")
    return "\n".join(lines)


def _join_blocks(blocks: list[str]) -> str:
    return "\n\n".join(block for block in blocks if block)


def _sysml_name(name: str) -> str:
    if name.startswith("'") and name.endswith("'"):
        return name
    if name and (name[0].isalpha() or name[0] == "_") and all(char.isalnum() or char == "_" for char in name[1:]):
        return name
    return f"'{name}'"


def _structured_literal(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _render_doc_statement(doc: str, indent_level: int = 1) -> str:
    indent = "    " * indent_level
    return f"{indent}doc /* {doc} */"


def _render_structured_requirement_def(definition: dict[str, Any]) -> str:
    lines = [f"requirement def {_sysml_name(definition['name'])} {{"]
    if definition.get("doc"):
        lines.append(_render_doc_statement(definition["doc"]))
    for attribute in definition.get("attributes", []):
        lines.append(f"    attribute {attribute['name']} : {attribute['type']};")
    if definition.get("constraint"):
        lines.append(f"    require constraint {{ {definition['constraint']} }}")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_requirement_group(group: dict[str, Any]) -> str:
    lines = [f"requirement {_sysml_name(group['name'])} {{"]
    nested = group.get("nested_requirements", [])
    for index, requirement in enumerate(nested):
        lines.append(f"    requirement {_sysml_name(requirement['name'])} : {requirement['type']} {{")
        for attribute in requirement.get("attributes", []):
            lines.append(f"        attribute :>> {attribute['name']} = {_structured_literal(attribute['value'])};")
        lines.append("    }")
        if index != len(nested) - 1:
            lines.append("")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_item_def(definition: dict[str, Any]) -> str:
    attributes = definition.get("attributes", [])
    if not attributes:
        return f"item def {_sysml_name(definition['name'])};"
    lines = [f"item def {_sysml_name(definition['name'])} {{"]
    for attribute in attributes:
        lines.append(f"    attribute {attribute['name']} : {attribute['type']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_attribute_def(definition: dict[str, Any]) -> str:
    if isinstance(definition, str):
        return f"attribute def {definition};"
    return f"attribute def {definition['name']};"


def _render_structured_port_def(definition: dict[str, Any]) -> str:
    lines = [f"port def {_sysml_name(definition['name'])} {{"]
    for item in definition.get("items", []):
        lines.append(f"    {item['direction']} item {item['name']} : {item['type']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_interface_def(definition: dict[str, Any]) -> str:
    lines = [f"interface def {_sysml_name(definition['name'])} {{"]
    for end in definition.get("ends", []):
        lines.append(f"    end {end['name']} : {end['type']};")
    if definition.get("ends") and definition.get("flows"):
        lines.append("")
    for flow in definition.get("flows", []):
        lines.append(f"    flow of {flow['item_type']} from {flow['source']} to {flow['target']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_state_machine(machine: dict[str, Any]) -> str:
    modifier = f" {machine['modifier']}" if machine.get("modifier") else ""
    lines = [f"exhibit state {_sysml_name(machine['name'])}{modifier} {{"]
    composites = machine.get("composites", [])
    for composite_index, composite in enumerate(composites):
        lines.append(f"    state {_sysml_name(composite['name'])} {{")
        if composite.get("entry_action"):
            lines.append(f"        entry action {composite['entry_action']};")
            lines.append("")
        for state_name in composite.get("states", []):
            lines.append(f"        state {_sysml_name(state_name)};")
        if composite.get("states"):
            lines.append("")
        transitions = composite.get("transitions", [])
        for transition_index, transition in enumerate(transitions):
            if transition.get("inline"):
                lines.append(f"        transition {transition['name']} then {transition['then']};")
            else:
                lines.append(f"        transition {transition['name']}")
                if transition.get("first"):
                    lines.append(f"            first {transition['first']}")
                if transition.get("accept"):
                    lines.append(f"            accept {transition['accept']}")
                lines.append(f"            then {transition['then']};")
            if transition_index != len(transitions) - 1:
                lines.append("")
        lines.append("    }")
        if composite_index != len(composites) - 1:
            lines.append("")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_part_def(definition: dict[str, Any]) -> str:
    lines = [f"part def {_sysml_name(definition['name'])} {{"]
    for attribute in definition.get("attributes", []):
        lines.append(f"    attribute {attribute['name']} : {attribute['type']};")
    for port in definition.get("ports", []):
        lines.append(f"    port {port['name']} : {port['type']};")
    for part in definition.get("parts", []):
        lines.append(f"    part {part['name']} : {part['type']};")
    for interface in definition.get("interfaces", []):
        lines.append(f"    interface {interface['name']} : {interface['type']}")
        lines.append(f"    connect {interface['from']} to {interface['to']};")
    for machine in definition.get("state_machines", []):
        lines.append(_indent(_render_structured_state_machine(machine), 1))
    lines.append("}")
    return "\n".join(lines)


def _render_structured_part_usage(usage: dict[str, Any]) -> str:
    return f"part {usage['name']} : {usage['type']};"


def _render_structured_action_def(definition: dict[str, Any]) -> str:
    lines = [f"action def {_sysml_name(definition['name'])} {{"]
    for input_item in definition.get("inputs", []):
        lines.append(f"    in item {input_item['name']} : {input_item['type']};")
    for output_item in definition.get("outputs", []):
        lines.append(f"    out item {output_item['name']} : {output_item['type']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_action_usage(usage: dict[str, Any]) -> str:
    header = f"action {_sysml_name(usage['name'])}"
    if usage.get("type"):
        header += f" : {usage['type']}"
    lines = [f"{header} {{"]
    nested_actions = usage.get("nested_actions", [])
    for action in nested_actions:
        lines.append(f"    action {action['name']} : {action['type']};")
    if nested_actions and usage.get("flows"):
        lines.append("")
    for flow in usage.get("flows", []):
        lines.append(f"    flow of {flow['item_type']} from {flow['source']} to {flow['target']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_view(view: dict[str, Any]) -> str:
    lines: list[str] = []
    if view.get("comment"):
        comment = view["comment"]
        if isinstance(comment, list):
            lines.extend(f"// {line}" for line in comment)
        else:
            lines.append(f"// {comment}")
    lines.append(f"view {_sysml_name(view['name'])} : {view['type']} {{")
    for expose_path in view.get("expose", []):
        lines.append(f"    expose {expose_path};")
    if view.get("render"):
        lines.append(f"    render {view['render']};")
    lines.append("}")
    return "\n".join(lines)


def _render_structured_package_body(package: dict[str, Any]) -> str:
    blocks: list[str] = []
    imports = package.get("imports", [])
    if imports:
        blocks.append("\n".join(f"private import {import_name};" for import_name in imports))
    for collection_name, renderer in (
        ("requirement_defs", _render_structured_requirement_def),
        ("requirement_groups", _render_structured_requirement_group),
        ("item_defs", _render_structured_item_def),
        ("attribute_defs", _render_structured_attribute_def),
        ("port_defs", _render_structured_port_def),
        ("interface_defs", _render_structured_interface_def),
        ("part_defs", _render_structured_part_def),
        ("part_usages", _render_structured_part_usage),
        ("action_defs", _render_structured_action_def),
        ("action_usages", _render_structured_action_usage),
        ("views", _render_structured_view),
    ):
        for definition in package.get(collection_name, []):
            blocks.append(renderer(definition))
    return _join_blocks(blocks)


def _render_structured_model(structured_model: dict[str, Any]) -> str:
    package_blocks: list[str] = []
    for package in structured_model.get("packages", []):
        body = _render_structured_package_body(package)
        package_blocks.append(
            "\n".join(
                [
                    f"    package {package['name']} {{",
                    _indent(body, 2),
                    "    }",
                ]
            )
        )
    return "\n".join(
        [
            f"package {structured_model['package_name']} {{",
            "",
            "\n\n".join(package_blocks),
            "}",
            "",
        ]
    )


def _extract_root_package_name(sysml_text: str) -> str | None:
    match = re.search(r"^\s*package\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{", sysml_text, re.M)
    return match.group(1) if match else None


def _render_standard_views_package(root_package: str) -> str:
    package_name = f"{root_package}StandardViews"
    return "\n".join(
        [
            f"package {package_name} {{",
            "    private import DS_Views::*;",
            "",
            "    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.",
            "    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {",
            f"        expose {root_package}::**;",
            "    }",
            "",
            "    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {",
            f"        expose {root_package}::**;",
            "    }",
            "",
            "    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {",
            f"        expose {root_package}::**;",
            "    }",
            "",
            "    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {",
            f"        expose {root_package}::**;",
            "    }",
            "",
            "    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {",
            f"        expose {root_package}::**;",
            "    }",
            "}",
        ]
    )


def _append_standard_views(sysml_text: str) -> str:
    if "view 'Requirements View'" in sysml_text:
        return sysml_text if sysml_text.endswith("\n") else sysml_text + "\n"
    root_package = _extract_root_package_name(sysml_text)
    if not root_package:
        return sysml_text if sysml_text.endswith("\n") else sysml_text + "\n"
    stripped = sysml_text.rstrip()
    return stripped + "\n\n" + _render_standard_views_package(root_package) + "\n"


def _render_generic_activity(requirements: list[dict[str, Any]]) -> str:
    lines = [
        "item def ActivityToken;",
        "",
        "action def RequirementActivityStep {",
        "    in item inToken : ActivityToken;",
        "    out item outToken : ActivityToken;",
        "}",
        "",
        "action systemActivity {",
    ]
    for index, requirement in enumerate(requirements, start=1):
        lines.append(f"    action requirementStep{index:03d} : RequirementActivityStep;")
        lines.append(f"    doc /* {requirement['source_requirement_id']}: {requirement['evidence']['quote']} */")
    if requirements:
        lines.append("")
    for index in range(1, len(requirements)):
        lines.append(
            f"    flow of ActivityToken from requirementStep{index:03d}.outToken to requirementStep{index + 1:03d}.inToken;"
        )
    lines.append("}")
    return "\n".join(lines)


def _pascal_case(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    return "".join(part[:1].upper() + part[1:] for part in parts if part)


def _safe_identifier(value: str, suffix: str = "") -> str:
    candidate = re.sub(r"[^A-Za-z0-9_]", "_", value).strip("_")
    if not candidate:
        candidate = "GeneratedElement"
    if candidate[0].isdigit():
        candidate = f"_{candidate}"
    return candidate + suffix


def _render_contract_backed_case(case_id: str, contracts: dict[str, Any]) -> str:
    package_name = f"{_pascal_case(case_id)}Expected"
    document = contracts["document"]
    contract_items = contracts["contracts"]
    subject_names: list[str] = []
    for contract in contract_items:
        canonical_name = contract.get("subject", {}).get("canonical_name")
        if canonical_name and canonical_name not in subject_names:
            subject_names.append(canonical_name)
    if not subject_names:
        subject_names = ["SystemUnderStudy"]

    context_parts = []
    needs_interaction = len(subject_names) >= 2 or any(
        contract.get("classification", {}).get("pattern_id") == "interface_transfer" for contract in contract_items
    )

    lines = [
        f"package {package_name} {{",
        f"    doc /* Generated canonical model for {document['document_name']}. */",
        "",
    ]

    if needs_interaction:
        lines.extend(
            [
                "    item def InteractionToken;",
                "",
                "    port def InteractionPort {",
                "        out item token : InteractionToken;",
                "    }",
                "",
                "    interface def InteractionLink {",
                "        end source : InteractionPort;",
                "        end target : ~InteractionPort;",
                "        flow source.token to target.token;",
                "    }",
                "",
            ]
        )

    for subject_name in subject_names:
        subject_identifier = _safe_identifier(subject_name)
        lines.append(f"    part def {subject_identifier} {{")
        if needs_interaction:
            lines.append("        port interactionPort : InteractionPort;")
        lines.append("    }")
        lines.append("")
        context_parts.append((subject_identifier[:1].lower() + subject_identifier[1:], subject_identifier))

    for index, contract in enumerate(contract_items, start=1):
        requirement_def = _safe_identifier(contract["source_requirement_id"], "Requirement")
        subject_type = _safe_identifier(contract.get("subject", {}).get("canonical_name", subject_names[0]))
        lines.extend(
            [
                f"    requirement def {requirement_def} {{",
                f"        subject subjectRef : {subject_type};",
                "        doc /*",
                f"        {contract['source_requirement_id']}: {contract['evidence']['quote']}",
                "        */",
                "    }",
                "",
            ]
        )

    lines.extend([_indent(_render_generic_activity(contract_items), 1), ""])

    lines.append("    part def SystemContext {")
    for child_name, child_type in context_parts:
        lines.append(f"        part {child_name} : {child_type};")
    if needs_interaction and len(context_parts) >= 2:
        lines.append("        interface subjectInteraction : InteractionLink")
        lines.append(f"        connect {context_parts[0][0]}::interactionPort to {context_parts[1][0]}::interactionPort;")
    lines.append("    }")
    lines.append("")
    lines.append("    part systemContext : SystemContext;")
    lines.append("")
    lines.append("    requirement extractedRequirements {")
    for index, contract in enumerate(contract_items, start=1):
        requirement_def = _safe_identifier(contract["source_requirement_id"], "Requirement")
        requirement_usage = _safe_identifier(contract["source_requirement_id"].lower(), "")
        lines.append(f"        requirement {requirement_usage} : {requirement_def};")
    lines.append("    }")
    lines.append("")
    lines.append("}")
    return _append_standard_views("\n".join(lines) + "\n")


def _generic_state_machine_owners(case_id: str, generic_case: dict[str, Any], rendering_profile: dict[str, Any]) -> set[str]:
    if not generic_case.get("state_machine"):
        return set()
    part_ports = generic_case["part_ports"]
    top_level_parts = set(generic_case["subparts"])
    owner_policy = rendering_profile["state_machine_owner_policy"]
    candidates = [name for name, ports in part_ports.items() if name not in top_level_parts and ports]
    if not candidates:
        return set()
    owners = {max(candidates, key=lambda name: len(part_ports[name]))}
    if case_id in owner_policy.get("include_top_level_case_ids", []):
        owners.add(generic_case["structure"][0])
    return owners


def _render_generic_case(case_id: str, contracts: dict[str, Any]) -> str:
    generic_profile = load_generic_case_profile()
    rendering = generic_profile["renderer"]
    generic_case = contracts["generic_case"]
    document = contracts["document"]
    state_machine_owners = _generic_state_machine_owners(case_id, generic_case, rendering)
    top_level = generic_case["structure"][0]

    package_doc_lines = [
        line.format(document_id=document["document_id"], document_name=document["document_name"], context=generic_case["context"])
        for line in rendering["package_doc_lines"]
    ]
    lines = [f"package {generic_case['package']} {{", "    doc /*", *[f"    {line}" for line in package_doc_lines], "    */", ""]

    seen_items: set[str] = set()
    for port_name, _, item_name, _ in generic_case["interfaces"]:
        if item_name in seen_items:
            continue
        seen_items.add(item_name)
        lines.append(f"    item def {item_name};")
    lines.append("")

    for port_name, signal_name, item_name, direction in generic_case["interfaces"]:
        lines.extend(
            [
                f"    port def {port_name} {{",
                f"        {direction} item {signal_name} : {item_name};",
                "    }",
                "",
            ]
        )

    for interface_name, source_port, target_port, signal_name in generic_case["interfaces_defs"]:
        lines.extend(
            [
                f"    interface def {interface_name} {{",
                f"        end source : {source_port};",
                f"        end target : ~{target_port};",
                f"        flow source.{signal_name} to target.{signal_name};",
                "    }",
                "",
            ]
        )

    for index, requirement in enumerate(contracts["contracts"], start=1):
        lines.extend(
            [
                f"    requirement def {rendering['requirement_definition_prefix']}{index:03d} {{",
                "        doc /*",
                f"        {requirement['source_requirement_id']}: {requirement['evidence']['quote']}",
                "        */",
                "    }",
                "",
            ]
        )

    lines.extend([_indent(_render_generic_activity(contracts["contracts"]), 1), ""])

    subparts = generic_case["subparts"]
    part_ports = generic_case["part_ports"]
    part_order = [name for name in generic_case["structure"] if name != top_level] + [top_level]

    for part_name in part_order:
        lines.append(f"    part def {part_name} {{")
        if part_name in state_machine_owners:
            lines.append(_indent(_render_state_machine(generic_case["state_machine"]), 2))
            lines.append("")
        for port_name, port_type in part_ports.get(part_name, []):
            lines.append(f"        port {port_name} : {port_type};")
        if part_name in subparts:
            for child_name, child_type in subparts[part_name]:
                lines.append(f"        part {child_name} : {child_type};")
        lines.extend(["    }", ""])

    lines.extend([f"    part {rendering['system_under_test_name']} : {top_level};", ""])
    for index in range(1, len(contracts["contracts"]) + 1):
        lines.append(
            f"    requirement {rendering['requirement_usage_prefix']}{index:0{rendering['requirement_usage_digits']}d} : "
            f"{rendering['requirement_definition_prefix']}{index:03d};"
        )
    lines.append("")
    lines.append("}")
    return _append_standard_views("\n".join(lines) + "\n")


def render_canonical(case_id: str, contracts: dict[str, Any]) -> str | None:
    structured_model = contracts.get("structured_model")
    if structured_model:
        canonical_sysml = structured_model.get("canonical_sysml")
        if canonical_sysml:
            return _append_standard_views(canonical_sysml if canonical_sysml.endswith("\n") else canonical_sysml + "\n")
        return _append_standard_views(_render_structured_model(structured_model))
    if contracts.get("generic_case"):
        return _render_generic_case(case_id, contracts)
    case_profile = get_case_profile(case_id)
    if not case_profile:
        return None
    canonical_profile_id = case_profile.get("canonical_profile_id")
    if not canonical_profile_id:
        return _render_contract_backed_case(case_id, contracts)
    canonical_profile = get_canonical_profile(canonical_profile_id)
    if not canonical_profile:
        return _render_contract_backed_case(case_id, contracts)
    return _append_standard_views(_localize(_render_canonical_profile(canonical_profile), contracts))


def _render_canonical_profile(canonical_profile: dict[str, Any]) -> str:
    raw_sysml = canonical_profile.get("raw_sysml")
    if raw_sysml is not None:
        return raw_sysml if raw_sysml.endswith("\n") else raw_sysml + "\n"
    lines = [f"package {canonical_profile['package_name']} {{", ""]
    packages = canonical_profile["packages"]
    for index, package in enumerate(packages):
        lines.append(f"package {package['name']} {{")
        if package.get("leading_blank"):
            lines.append("")
        body = package["body"].rstrip("\n")
        if body:
            lines.extend(f"  {line}" if line else "" for line in body.splitlines())
        lines.append("}")
        if index != len(packages) - 1:
            lines.append("")
    lines.append("")
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_overlay(case_id: str, contracts: dict[str, Any]) -> str | None:
    case_profile = get_case_profile(case_id)
    if case_profile and case_profile.get("overlay"):
        return _render_profile_overlay(case_profile["overlay"], contracts)
    templates = {
        "case02_vehicle_ambiguous_low": """package Case02VehicleAmbiguousLowExpectedReview {

package DomainDefinitions {
  part def Vehicle;
  part def Engine;
}

package DraftRequirementContracts {

  requirement def DraftVehicleMassRequirement {
    subject vehicle : DomainDefinitions::Vehicle;
    doc /* [proposal-id] P-VEH-L-001
           [source-contract] C-VEH-L-001
           [source-requirement] REQ-VEH-L-001
           [missing-slot] threshold_value
           [proposed-value] 2000
           [rationale] VehicleModel uses explicit quantitative mass requirements.
           [trace-quality] direct_file_grounded
           [confidence] 0.56
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftVehicleFuelEconomyContext {
    subject vehicle : DomainDefinitions::Vehicle;
    doc /* [proposal-id] P-VEH-L-003
           [source-contract] C-VEH-L-002
           [source-requirement] REQ-VEH-L-002
           [missing-slot] operating_contexts
           [proposed-value] CityNominal and HighwayNominal
           [rationale] VehicleModel separates city and highway fuel economy requirements.
           [trace-quality] direct_file_grounded
           [confidence] 0.58
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftVehicleDrivePowerInterface {
    subject engine : DomainDefinitions::Engine;
    doc /* [proposal-id] P-VEH-L-004
           [source-contract] C-VEH-L-003
           [source-requirement] REQ-VEH-L-003
           [missing-slot] interface_name
           [proposed-value] EngineToTransmissionInterface
           [rationale] VehicleModel defines an EngineToTransmissionInterface between engine and transmission.
           [trace-quality] direct_file_grounded
           [confidence] 0.68
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* REQ-VEH-L-001 missing: measured_property, threshold_value, threshold_unit
         REQ-VEH-L-002 missing: operating_contexts, threshold_value, threshold_unit
         REQ-VEH-L-003 missing: interface_name, interface_ends, flows */
}

package OpenQuestions {
  doc /* Is lightweight a mass threshold or an acceleration/performance surrogate?
         Should fuel efficiency be split into city and highway contexts?
         Does reliable drive power imply an interface requirement, a performance requirement, or both? */
}

package Assumptions {
  doc /* Assumption A1: lightweight most likely maps to mass.
         Assumption A2: fuel efficient most likely maps to city/highway fuel economy.
         Assumption A3: drive power transfer most likely maps to a named interface. */
}

package TraceWeaknesses {
  doc /* The input is intentionally ambiguous.
         The review overlay should remain the source of truth until the missing quantitative slots are accepted. */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Do not promote any draft to canonical until all missing quantitative slots are resolved. */
}

}
""",
        "case05_mining_usecase_medium": """package Case05MiningUseCaseMediumExpectedReview {

package DomainDefinitions {
  part def MiningFrigate;
}

package DraftRequirementContracts {

  requirement def DraftMineAsteroidsCompletionCriteria {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UC-001
           [source-contract] C-UC-001
           [source-requirement] UC-MF-001
           [missing-slot] success_thresholds
           [proposed-value] define ore extraction completion criteria and cargo-full threshold
           [rationale] The use case contains main and exception flows but does not define measurable success limits.
           [trace-quality] direct_file_grounded
           [confidence] 0.61
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftOffloadCompletionCriteria {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UC-002
           [source-contract] C-UC-002
           [source-requirement] UC-MF-002
           [missing-slot] completion_conditions
           [proposed-value] define successful docking, cargo transfer completion, and resupply completion criteria
           [rationale] The narrative preserves flow but not completion metrics.
           [trace-quality] direct_file_grounded
           [confidence] 0.60
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* UC-MF-001 missing: success_thresholds, time_limits, trigger_conditions
         UC-MF-002 missing: success_thresholds, completion_conditions */
}

package OpenQuestions {
  doc /* Should mining completion be measured by ore quantity, time, or cargo fill percentage?
         Should offload success be measured by all cargo transferred, minimum cargo transferred, or docking completion? */
}

package BehaviorCandidates {
  doc /* Candidate behavior decomposition:
         MineAsteroids -> target selection / mining activation / ore transfer / suspend on full cargo
         OffloadOreAndResupply -> docking / cargo transfer / resupply / abort on failure */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Canonical use cases are acceptable, but quantitative success criteria remain unresolved. */
}

}
""",
        "case06_mining_usecase_ambiguous_low": """package Case06MiningUseCaseAmbiguousLowExpectedReview {

package DomainDefinitions {
  part def MiningFrigate;
}

package DraftRequirementContracts {

  requirement def DraftMineAsteroidsUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-001
           [source-contract] C-UCL-001
           [source-requirement] REQ-UC-L-001
           [missing-slot] actors
           [proposed-value] PilotPod and AsteroidBelt
           [rationale] Mining use cases in the reference model use a pilot and an asteroid belt.
           [trace-quality] direct_file_grounded
           [confidence] 0.72
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftDefenseUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-002
           [source-contract] C-UCL-002
           [source-requirement] REQ-UC-L-002
           [missing-slot] actors
           [proposed-value] HostileShip and PilotPod
           [rationale] Threat engagement use cases in the reference model use hostile ships and the pilot.
           [trace-quality] direct_file_grounded
           [confidence] 0.71
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftResupplyUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-003
           [source-contract] C-UCL-003
           [source-requirement] REQ-UC-L-003
           [missing-slot] actors
           [proposed-value] Station
           [rationale] Resupply use cases in the reference model involve a station actor.
           [trace-quality] direct_file_grounded
           [confidence] 0.70
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* REQ-UC-L-001 missing: objective_text, actors, main_flow_steps, success_thresholds
         REQ-UC-L-002 missing: objective_text, actors, trigger_conditions, exception_flow_steps
         REQ-UC-L-003 missing: objective_text, actors, trigger_conditions, completion_conditions */
}

package OpenQuestions {
  doc /* What is the concrete success definition for efficient mining?
         What specific trigger makes a threat actionable?
         When exactly is resupply considered necessary and complete? */
}

package TraceWeaknesses {
  doc /* This case is intentionally vague.
         It is grounded in the same source file as case05, but the input narrative omits most operational structure. */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Do not emit canonical use cases until actors, objective text, and flow structure are accepted. */
}

}
""",
    }
    template = templates.get(case_id)
    return _localize(template, contracts) if template else None


def render_projection_manifest(case_id: str, contracts: dict[str, Any] | None = None) -> dict[str, Any] | None:
    structured_model = (contracts or {}).get("structured_model")
    if structured_model:
        return structured_model.get("projection_manifest")
    case_profile = get_case_profile(case_id)
    if case_profile:
        return case_profile.get("projection_manifest")
    manifests: dict[str, dict[str, Any]] = {
        "case01_vehicle_explicit_high": {
            "requirements": [
                {"sysml_name": "vehicleMassRequirement", "source_contract": "C-VEH-001", "pattern": "MassRequirement"},
                {"sysml_name": "cityFuelEconomyRequirement", "source_contract": "C-VEH-002", "pattern": "FuelEconomyRequirement"},
                {"sysml_name": "highwayFuelEconomyRequirement", "source_contract": "C-VEH-003", "pattern": "FuelEconomyRequirement"},
                {"sysml_name": "drivePowerInterface", "source_contract": "C-VEH-004", "pattern": "DrivePowerInterfaceRequirement"},
            ],
            "interfaces": [{"id": "IF-VEH-001", "name": "engineToTransmissionInterface", "type": "EngineToTransmissionInterface", "from": "vehicle_b.engine.drivePwrPort", "to": "vehicle_b.transmission.clutchPort"}],
            "allocations": [{"id": "ALLOC-VEH-001", "contract": "C-VEH-001", "allocated_to": "Structure::vehicle_b"}, {"id": "ALLOC-VEH-004", "contract": "C-VEH-004", "allocated_to": "Structure::vehicle_b::engine"}],
            "satisfy_claims": [{"requirement": "Requirements::vehicleSpecification::vehicleMassRequirement", "by": "Structure::vehicle_b"}, {"requirement": "Requirements::engineSpecification::drivePowerInterface", "by": "Structure::vehicle_b::engine"}],
            "views": [{"id": "VIEW-VEH-001", "target": "Structure::vehicle_b", "rendering": "structural_context"}],
        },
        "case03_mining_contextual_performance_high": {
            "requirements": [{"sysml_name": "cargoCapacityRequirement", "source_contract": "C-MF-001", "pattern": "CargoCapacityRequirement"}, {"sysml_name": "survivabilityRequirement", "source_contract": "C-MF-002|C-MF-003", "pattern": "SurvivabilityRequirement"}],
            "allocations": [{"id": "ALLOC-MF-001", "contract": "C-MF-001", "allocated_to": "Structure::miningFrigate_ref"}, {"id": "ALLOC-MF-002", "contract": "C-MF-002", "allocated_to": "Structure::miningFrigate_ref"}, {"id": "ALLOC-MF-003", "contract": "C-MF-003", "allocated_to": "Structure::miningFrigate_ref"}],
            "satisfy_claims": [{"requirement": "Requirements::miningFrigateSpecification::cargoCapacityRequirement", "by": "Structure::miningFrigate_ref"}, {"requirement": "Requirements::miningFrigateSpecification::survivabilityRequirement", "by": "Structure::miningFrigate_ref"}],
            "views": [{"id": "VIEW-MF-001", "target": "Structure::miningFrigate_ref", "rendering": "structural_context"}],
        },
        "case04_mining_modular_interface_high": {
            "requirements": [{"sysml_name": "highSlotInterfaceRequirement", "source_contract": "C-MFI-001|C-MFI-002", "pattern": "HighSlotInterfaceRequirement"}, {"sysml_name": "mediumSlotInterfaceRequirement", "source_contract": "C-MFI-003|C-MFI-004", "pattern": "MediumSlotInterfaceRequirement"}],
            "interfaces": [{"id": "IF-MFI-001", "name": "miningLaserIf", "type": "HighSlotInterface", "from": "frigate_ref.hull.highSlot1", "to": "frigate_ref.miningLaser.modulePort"}, {"id": "IF-MFI-002", "name": "shieldIf", "type": "MediumSlotInterface", "from": "frigate_ref.hull.mediumSlot1", "to": "frigate_ref.shieldHardener.modulePort"}],
            "allocations": [{"id": "ALLOC-MFI-001", "contract": "C-MFI-001", "allocated_to": "Structure::frigate_ref::hull"}, {"id": "ALLOC-MFI-003", "contract": "C-MFI-003", "allocated_to": "Structure::frigate_ref::hull"}],
            "satisfy_claims": [{"requirement": "Requirements::architectureSpecification::highSlotInterfaceRequirement", "by": "Structure::frigate_ref::hull"}, {"requirement": "Requirements::architectureSpecification::mediumSlotInterfaceRequirement", "by": "Structure::frigate_ref::hull"}],
            "views": [{"id": "VIEW-MFI-001", "target": "Structure::frigate_ref", "rendering": "interconnection"}],
        },
        "case05_mining_usecase_medium": {
            "use_cases": [{"sysml_name": "MineAsteroids", "source_contract": "C-UC-001", "subject_type": "MiningFrigate", "actors": ["PilotPod", "AsteroidBelt"]}, {"sysml_name": "OffloadOreAndResupply", "source_contract": "C-UC-002", "subject_type": "MiningFrigate", "actors": ["Station"]}],
            "derived_requirements": [{"sysml_name": "operationalObjectives", "source_contract": "C-UC-001|C-UC-002"}],
            "views": [{"id": "VIEW-UC-001", "target": "UseCases::MineAsteroids", "rendering": "textual_objective"}, {"id": "VIEW-UC-002", "target": "UseCases::OffloadOreAndResupply", "rendering": "textual_objective"}],
        },
    }
    return manifests.get(case_id)


def render_cameo_display_guide(case_id: str, contracts: dict[str, Any] | None = None) -> str | None:
    structured_model = (contracts or {}).get("structured_model")
    if structured_model:
        guide = structured_model.get("cameo_display_guide")
        if isinstance(guide, dict):
            return _render_cameo_guide_payload(guide)
        if guide:
            return guide if guide.endswith("\n") else guide + "\n"
        return _render_standard_cameo_guide(case_id, contracts, canonical_expected=True)
    if (contracts or {}).get("generic_case"):
        return _render_standard_cameo_guide(case_id, contracts, canonical_expected=True)
    case_profile = get_case_profile(case_id)
    if not case_profile:
        return _render_standard_cameo_guide(case_id, contracts, canonical_expected=True)
    guide = case_profile.get("cameo_display_guide")
    if not guide:
        return _render_standard_cameo_guide(case_id, contracts, canonical_expected=True)
    if isinstance(guide, str):
        return guide if guide.endswith("\n") else guide + "\n"
    return _render_cameo_guide_payload(guide)


def _render_standard_cameo_guide(case_id: str, contracts: dict[str, Any] | None, canonical_expected: bool) -> str:
    lines = [f"# {case_id} Cameo Display Guide", ""]
    if canonical_expected:
        lines.extend(
            [
                "このケースでは、標準 View セットを canonical `.sysml` に含めています。",
                "まず `*_canonical.sysml` を読み込み、`Display > Display Exposed Elements` を起点に確認してください。",
                "",
                "## 基本操作",
                "",
                "- Textual Editor で `.sysml` を読み込んだ後、`Synchronize` を実行する。",
                "- まず各 view で `Display > Display Exposed Elements` を実行する。",
                "- 線や接続が足りない場合は `Display > Display Connectors` を追加実行する。",
                "- ポートが不足する場合は `Display > Display Ports` を使う。",
                "- 状態や内部要素が足りない場合は対象シンボルに対して `Display > Display Features` を使う。",
                "",
                "## View ごとの使い分け",
                "",
                "### Requirements View",
                "",
                "- 向いている用途: requirement 階層を最短で確認したいとき",
                "- Cameo 操作: `Display > Display Exposed Elements`",
                "- 補足: `RequirementsTreeView` が解決しない build では `RequirementTreeView` へ置き換えます。",
                "",
                "### Structural Context View",
                "",
                "- 向いている用途: システム全体と主要 part 階層を軽く確認したいとき",
                "- Cameo 操作: `Display > Display Exposed Elements`",
                "",
                "### Internal Structure View",
                "",
                "- 向いている用途: part / port / interface を内部構造寄りに確認したいとき",
                "- Cameo 操作: `Display > Display Exposed Elements`",
                "- Cameo 操作: 必要なら `Display > Display Ports`",
                "- Cameo 操作: 線が不足する場合は `Display > Display Connectors`",
                "",
                "### Behavior Activity View",
                "",
                "- 向いている用途: action の入れ子や簡易 activity を確認したいとき",
                "- Cameo 操作: `Display > Display Exposed Elements`",
                "- Cameo 操作: flow 線が不足する場合は `Display > Display Connectors`",
                "",
                "### Behavior State View",
                "",
                "- 向いている用途: state machine や状態階層を確認したいとき",
                "- Cameo 操作: `Display > Display Exposed Elements`",
                "- Cameo 操作: 必要なら `Display > Display Features`",
                "",
                "## 公式リンク",
                "",
                "- [Exposing elements for views](https://docs.nomagic.com/SYSML2P/2026x/exposing-elements-for-views-254423168.html)",
                "- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)",
                "- [Filtering elements for views](https://docs.nomagic.com/SYSML2P/2026x/filtering-elements-for-views-254423172.html)",
                "- [Rendering views](https://docs.nomagic.com/SYSML2P/2026x/rendering-views-254422759.html)",
                "- [2026x Hot Fix 1](https://docs.nomagic.com/VN/latest/2026x-hot-fix-1-278725663.html)",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    lines.extend(
        [
            "このケースでは canonical `.sysml` は出さず、review overlay を主に確認します。",
            "まず `*_review_overlay.sysml` を開き、未解決スロットやレビュー方針を確認してください。",
            "",
            "## 基本操作",
            "",
            "- Textual Editor で `.sysml` を読み込んだ後、`Synchronize` を実行する。",
            "- モデルブラウザで package、requirement、doc を確認する。",
            "- review overlay は diagram よりもレビュー用テキストとして読む前提です。",
            "",
            "## 公式リンク",
            "",
            "- [Working with textual editor](https://docs.nomagic.com/SYSML2P/2026x/working-with-textual-editor-254422032.html)",
            "- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_cameo_guide_payload(guide: dict[str, Any]) -> str:
    lines: list[str] = [f"# {guide['title']}", ""]

    intro = guide.get("intro", [])
    if intro:
        lines.extend(intro)
        lines.append("")

    basics = guide.get("basics", [])
    if basics:
        lines.append("## 基本操作")
        lines.append("")
        for item in basics:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## View ごとの使い分け")
    lines.append("")
    for view in guide.get("views", []):
        lines.append(f"### {view['view_name']}")
        lines.append("")

        for element in view.get("model_elements", []):
            lines.append(f"- 対象要素: {element}")
        for use_case in view.get("use_when", []):
            lines.append(f"- 向いている用途: {use_case}")
        for step in view.get("display_steps", []):
            lines.append(f"- Cameo 操作: {step}")
        for note in view.get("notes", []):
            lines.append(f"- 補足: {note}")
        lines.append("")

    links = guide.get("links", [])
    if links:
        lines.append("## 公式リンク")
        lines.append("")
        for link in links:
            lines.append(f"- [{link['label']}]({link['url']})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _overlay_language(contracts: dict[str, Any]) -> str:
    return contracts.get("document", {}).get("language", "en")


def _overlay_lines(payload: dict[str, Any], field: str, language: str) -> list[str]:
    value = payload.get(field, {})
    if isinstance(value, dict):
        return value.get(language, value.get("en", []))
    return value or []


def _find_contract(contracts: dict[str, Any], contract_id: str) -> dict[str, Any]:
    for contract in contracts["contracts"]:
        if contract["contract_id"] == contract_id:
            return contract
    raise KeyError(contract_id)


def _find_proposal(contracts: dict[str, Any], proposal_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for contract in contracts["contracts"]:
        for proposal in contract.get("llm_proposals", []):
            if proposal["proposal_id"] == proposal_id:
                return contract, proposal
    raise KeyError(proposal_id)


def _indent_lines(lines: list[str], level: int = 1) -> list[str]:
    prefix = "  " * level
    return [f"{prefix}{line}" if line else "" for line in lines]


def _render_doc_block(lines: list[str], level: int = 0) -> list[str]:
    indent = "  " * level
    if len(lines) == 1:
        return [f"{indent}doc /* {lines[0]} */"]
    rendered = [f"{indent}doc /* {lines[0]}"]
    rendered.extend(f"{indent}       {line}" for line in lines[1:-1])
    rendered.append(f"{indent}       {lines[-1]} */")
    return rendered


def _proposal_payload(draft: dict[str, Any], contracts: dict[str, Any], language: str) -> dict[str, Any]:
    if "proposal" in draft:
        proposal = draft["proposal"].copy()
        proposed_value = proposal.get("proposed_value")
        rationale = proposal.get("rationale")
        if isinstance(proposed_value, dict):
            proposal["proposed_value"] = proposed_value.get(language, proposed_value.get("en"))
        if isinstance(rationale, dict):
            proposal["rationale"] = rationale.get(language, rationale.get("en"))
        return proposal

    contract, proposal = _find_proposal(contracts, draft["proposal_id"])
    return {
        "proposal_id": proposal["proposal_id"],
        "source_contract": contract["contract_id"],
        "source_requirement_id": contract["source_requirement_id"],
        "missing_slot": proposal["missing_slot"],
        "proposed_value": proposal["proposed_value"],
        "rationale": proposal["rationale"],
        "trace_quality": contract["trace_quality"],
        "confidence": proposal["confidence"],
    }


def _render_profile_overlay(overlay_profile: dict[str, Any], contracts: dict[str, Any]) -> str:
    review_profile = load_review_overlay_profile()
    language = _overlay_language(contracts)
    package_names = review_profile["packages"]
    lines = [f"package {overlay_profile['package_name']} {{", ""]

    lines.extend(
        [
            "package DomainDefinitions {",
            *[f"  part def {part_name};" for part_name in overlay_profile.get("domain_parts", [])],
            "}",
            "",
        ]
    )

    lines.append(f"package {package_names['draft_requirement_contracts']} {{")
    lines.append("")
    for draft in overlay_profile.get("drafts", []):
        proposal = _proposal_payload(draft, contracts, language)
        lines.append(f"  requirement def {draft['name']} {{")
        lines.append(f"    subject {draft['subject_name']} : DomainDefinitions::{draft['subject_type']};")
        lines.extend(
            _render_doc_block(
                [
                    f"[proposal-id] {proposal['proposal_id']}",
                    f"[source-contract] {proposal['source_contract']}",
                    f"[source-requirement] {proposal['source_requirement_id']}",
                    f"[missing-slot] {proposal['missing_slot']}",
                    f"[proposed-value] {proposal['proposed_value']}",
                    f"[rationale] {proposal['rationale']}",
                    f"[trace-quality] {proposal['trace_quality']}",
                    f"[confidence] {proposal['confidence']:.2f}",
                    "[review-action] accept / modify / reject / defer",
                ],
                level=2,
            )
        )
        lines.append("  }")
        if draft is not overlay_profile["drafts"][-1]:
            lines.append("")
    lines.append("}")
    lines.append("")

    package_field_map = {
        "missing_slots": "missing_slots",
        "open_questions": "open_questions",
        "assumptions": "assumptions",
        "behavior_candidates": "behavior_candidates",
        "trace_weaknesses": "trace_weaknesses",
        "review_guide": "review_guide",
    }
    for profile_key, package_key in package_field_map.items():
        package_name = package_names[package_key]
        package_lines = _overlay_lines(overlay_profile, profile_key, language)
        if not package_lines:
            continue
        lines.append(f"package {package_name} {{")
        lines.extend(_render_doc_block(package_lines, level=1))
        lines.append("}")
        lines.append("")

    lines.append("}")
    return "\n".join(lines) + "\n"
