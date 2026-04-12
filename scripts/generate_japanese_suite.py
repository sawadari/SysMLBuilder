from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "testdata" / "gfse_derived"
DST = ROOT / "testdata" / "gfse_derived_ja"


FILE_REPLACEMENTS = {
    "case01_vehicle_explicit_high_requirements.md": [
        ("# Case 01: Vehicle quantitative and interface requirements", "# ケース01: 車両の定量性能およびインタフェース要求"),
        ("## Scope", "## 範囲"),
        ("This requirement specification is a bottom-up reconstruction derived from the structure and requirement style seen in `VehicleModel.sysml`.", "`VehicleModel.sysml` に見られる構造と要求記法からボトムアップに再構成した要求仕様である。"),
        ("## Requirements", "## 要求"),
        ("The vehicle shall have a total mass less than or equal to 2000 kg.", "車両の総質量は2000 kg以下でなければならない。"),
        ("The vehicle shall maintain an average city fuel economy of at least 25 mpg in the nominal city driving scenario with an assumed cargo mass of at least 500 kg.", "車両は、想定貨物質量が少なくとも500 kgの通常市街地走行シナリオにおいて、平均市街地燃費を少なくとも25 mpg維持しなければならない。"),
        ("The vehicle shall maintain an average highway fuel economy of at least 30 mpg in the nominal highway driving scenario with an assumed cargo mass of at least 500 kg.", "車両は、想定貨物質量が少なくとも500 kgの通常高速走行シナリオにおいて、平均高速燃費を少なくとも30 mpg維持しなければならない。"),
        ("The engine shall transfer generated torque to the transmission through the clutch interface.", "エンジンはクラッチインタフェースを介して生成トルクをトランスミッションへ伝達しなければならない。"),
        ("## Design context", "## 設計コンテキスト"),
        ("The system includes a vehicle, an engine, and a transmission.", "システムは車両、エンジン、トランスミッションで構成される。"),
    ],
    "case02_vehicle_ambiguous_low_requirements.md": [
        ("# Case 02: Vehicle ambiguous performance requirements", "# ケース02: 車両の曖昧な性能要求"),
        ("## Scope", "## 範囲"),
        ("This requirement specification intentionally under-specifies quantitative information while staying loosely grounded in `VehicleModel.sysml`.", "`VehicleModel.sysml` に緩く根拠を置きつつ、定量情報を意図的に不足させた要求仕様である。"),
        ("## Requirements", "## 要求"),
        ("The vehicle shall be lightweight.", "車両は軽量でなければならない。"),
        ("The vehicle shall be fuel efficient.", "車両は燃費が良くなければならない。"),
        ("The engine shall provide drive power to the transmission reliably.", "エンジンはトランスミッションへ駆動力を確実に供給しなければならない。"),
        ("## Note", "## 注記"),
        ("Thresholds, operating contexts, and interface details are intentionally omitted to test gap detection and review overlay generation.", "ギャップ検出とレビューオーバーレイ生成を試験するため、閾値、運用コンテキスト、インタフェース詳細は意図的に省略している。"),
    ],
    "case03_mining_contextual_performance_high_requirements.md": [
        ("# Case 03: Mining frigate contextual performance requirements", "# ケース03: 採掘フリゲートの文脈別性能要求"),
        ("## Scope", "## 範囲"),
        ("This requirement specification is a bottom-up reconstruction derived from `MiningFrigateRequirementsDef.sysml`.", "`MiningFrigateRequirementsDef.sysml` からボトムアップに再構成した要求仕様である。"),
        ("## Requirements", "## 要求"),
        ("The mining frigate shall have a cargo capacity of at least 5000 m3.", "採掘フリゲートの貨物容量は少なくとも5000 m3でなければならない。"),
        ("The mining frigate shall withstand at least 200 DPS in High Sec operations.", "採掘フリゲートはHigh Sec運用において少なくとも200 DPSに耐えなければならない。"),
        ("The mining frigate shall withstand at least 400 DPS in Low Sec, Null Sec, and Wormhole operations.", "採掘フリゲートはLow Sec、Null Sec、およびWormhole運用において少なくとも400 DPSに耐えなければならない。"),
        ("## Design context", "## 設計コンテキスト"),
        ("The subject is a mining frigate considered across multiple operating contexts.", "対象は複数の運用コンテキストで評価される採掘フリゲートである。"),
    ],
    "case04_mining_modular_interface_high_requirements.md": [
        ("# Case 04: Mining frigate modular interface requirements", "# ケース04: 採掘フリゲートのモジュラーインタフェース要求"),
        ("## Scope", "## 範囲"),
        ("This requirement specification is a bottom-up reconstruction derived from `standardPortsAndInterfaces.sysml`.", "`standardPortsAndInterfaces.sysml` からボトムアップに再構成した要求仕様である。"),
        ("## Requirements", "## 要求"),
        ("The hull shall provide a typed HighSlot interface to a mining laser module.", "船体は採掘レーザーモジュールに対して型付きHighSlotインタフェースを提供しなければならない。"),
        ("The HighSlot interface shall transfer power and activation command from the hull to the mining laser module.", "HighSlotインタフェースは船体から採掘レーザーモジュールへ電力と起動コマンドを伝達しなければならない。"),
        ("The hull shall provide a typed MediumSlot interface to a shield hardener module.", "船体はシールドハードナーモジュールに対して型付きMediumSlotインタフェースを提供しなければならない。"),
        ("The MediumSlot interface shall transfer power and activation command from the hull to the shield hardener module.", "MediumSlotインタフェースは船体からシールドハードナーモジュールへ電力と起動コマンドを伝達しなければならない。"),
        ("## Design context", "## 設計コンテキスト"),
        ("The architecture includes a hull, a mining laser module, and a shield hardener module.", "アーキテクチャは船体、採掘レーザーモジュール、シールドハードナーモジュールを含む。"),
    ],
    "case05_mining_usecase_medium_requirements.md": [
        ("# Case 05: Mining frigate operational use cases", "# ケース05: 採掘フリゲートの運用ユースケース"),
        ("## Scope", "## 範囲"),
        ("This requirement specification is a bottom-up reconstruction derived from `UseCasesFrigate.sysml`.", "`UseCasesFrigate.sysml` からボトムアップに再構成した要求仕様である。"),
        ("## Operational objectives", "## 運用目的"),
        ("Main Flow:", "メインフロー:"),
        ("Exception Flows:", "例外フロー:"),
        ("Mine Asteroids", "小惑星を採掘する"),
        ("Identify an asteroid target.", "小惑星ターゲットを特定する。"),
        ("Activate the mining laser.", "採掘レーザーを起動する。"),
        ("Extract ore and store it in the cargo hold.", "鉱石を採取し貨物倉へ格納する。"),
        ("Suspend mining when the cargo hold becomes full.", "貨物倉が満杯になったら採掘を中断する。"),
        ("If the mining laser fails, halt mining and alert the pilot.", "採掘レーザーが故障した場合、採掘を停止してパイロットへ通知する。"),
        ("If the target asteroid is depleted, reacquire a target.", "対象小惑星が枯渇した場合、ターゲットを再取得する。"),
        ("Offload Ore and Resupply", "鉱石を荷下ろしして補給する"),
        ("Establish a docking connection with a station.", "ステーションとのドッキング接続を確立する。"),
        ("Transfer ore to the station.", "鉱石をステーションへ移送する。"),
        ("Resupply essential systems.", "重要システムを補給する。"),
        ("If docking fails, notify the pilot and abort the offload sequence.", "ドッキングに失敗した場合、パイロットへ通知して荷下ろし手順を中止する。"),
        ("If cargo transfer fails, suspend operations and keep the ore on board.", "貨物移送に失敗した場合、運用を中断して鉱石を船内に保持する。"),
        ("## Note", "## 注記"),
        ("This input intentionally leaves quantitative success thresholds unspecified.", "この入力では定量的な成功閾値を意図的に未指定としている。"),
    ],
    "case06_mining_usecase_ambiguous_low_requirements.md": [
        ("# Case 06: Mining frigate ambiguous operational narrative", "# ケース06: 採掘フリゲートの曖昧な運用記述"),
        ("## Scope", "## 範囲"),
        ("This requirement specification intentionally keeps the operational narrative vague while remaining grounded in the themes of `UseCasesFrigate.sysml`.", "`UseCasesFrigate.sysml` の主題に根拠を置きつつ、運用記述を意図的に曖昧に保った要求仕様である。"),
        ("## Narrative requirements", "## 記述要求"),
        ("The mining frigate should mine asteroids efficiently.", "採掘フリゲートは小惑星を効率的に採掘できるべきである。"),
        ("The mining frigate should defend itself when threatened.", "採掘フリゲートは脅威を受けたとき自己防衛できるべきである。"),
        ("The mining frigate should resupply when needed.", "採掘フリゲートは必要時に補給できるべきである。"),
        ("## Note", "## 注記"),
        ("Actors, triggers, success criteria, and exception handling thresholds are intentionally omitted.", "アクター、トリガ、成功基準、例外処理の閾値は意図的に省略している。"),
    ],
}


GLOBAL_REPLACEMENTS = [
    ("Vehicle quantitative and interface requirements", "車両の定量性能およびインタフェース要求"),
    ("Vehicle ambiguous performance requirements", "車両の曖昧な性能要求"),
    ("Mining frigate contextual performance requirements", "採掘フリゲートの文脈別性能要求"),
    ("Mining frigate modular interface requirements", "採掘フリゲートのモジュラーインタフェース要求"),
    ("Mining frigate operational use cases", "採掘フリゲートの運用ユースケース"),
    ("Mining frigate ambiguous operational narrative", "採掘フリゲートの曖昧な運用記述"),
    ("The engine shall transfer generated torque to the transmission through the clutch interface.", "エンジンはクラッチインタフェースを介して生成トルクをトランスミッションへ伝達しなければならない。"),
    ("The hull shall provide a typed HighSlot interface to a mining laser module.", "船体は採掘レーザーモジュールに対して型付きHighSlotインタフェースを提供しなければならない。"),
    ("The hull shall provide a typed MediumSlot interface to a shield hardener module.", "船体はシールドハードナーモジュールに対して型付きMediumSlotインタフェースを提供しなければならない。"),
    ("The HighSlot interface shall transfer power and activation command from the hull to the mining laser module.", "HighSlotインタフェースは船体から採掘レーザーモジュールへ電力と起動コマンドを伝達しなければならない。"),
    ("The MediumSlot interface shall transfer power and activation command from the hull to the shield hardener module.", "MediumSlotインタフェースは船体からシールドハードナーモジュールへ電力と起動コマンドを伝達しなければならない。"),
    ("Main Flow:", "メインフロー:"),
    ("Exception Flows:", "例外フロー:"),
    ("Main Flow: Identify an asteroid target, activate the mining laser, extract ore, and suspend mining when the cargo hold becomes full.", "メインフロー: 小惑星ターゲットを特定し、採掘レーザーを起動し、鉱石を採取し、貨物倉が満杯になったら採掘を中断する。"),
    ("Main Flow: Establish a docking connection with a station, transfer ore, and resupply essential systems.", "メインフロー: ステーションとのドッキング接続を確立し、鉱石を移送し、重要システムを補給する。"),
    ("Mine asteroids and manage cargo.", "小惑星を採掘し貨物を管理する。"),
    ("Offload ore and resupply essential systems.", "鉱石を荷下ろしし重要システムを補給する。"),
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
    ("Mass requirement in VehicleModel uses a 2000 kg style threshold.", "VehicleModel では 2000 kg 級の質量閾値が使われている。"),
    ("The phrase lightweight most likely maps to vehicle mass.", "軽量という表現は車両質量を指す可能性が高い。"),
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
    ("Canonical use cases are acceptable, but quantitative success criteria remain unresolved.", "canonical なユースケース自体は受容可能だが、定量的な成功基準は未解決のままである。"),
    ("Mining use cases in the reference model use a pilot and an asteroid belt.", "参照モデルの採掘ユースケースではパイロットと小惑星帯を用いている。"),
    ("Threat engagement use case involves hostile ship and pilot.", "脅威対処ユースケースには敵対艦船とパイロットが含まれる。"),
    ("Threat engagement use cases in the reference model use hostile ships and the pilot.", "参照モデルの脅威対処ユースケースでは敵対艦船とパイロットを用いている。"),
    ("Resupply use cases in the reference model involve a station actor.", "参照モデルの補給ユースケースにはステーションアクターが含まれる。"),
    ("What is the concrete success definition for efficient mining?", "効率的な採掘の具体的な成功定義は何か。"),
    ("What specific trigger makes a threat actionable?", "どの具体的なトリガが脅威を対処対象にするのか。"),
    ("When exactly is resupply considered necessary and complete?", "補給はどの時点で必要かつ完了と見なされるのか。"),
    ("This case is intentionally vague.", "このケースは意図的に曖昧である。"),
    ("It is grounded in the same source file as case05, but the input narrative omits most operational structure.", "case05 と同じソースファイルを根拠にしているが、入力記述では運用構造の大半を省略している。"),
    ("Do not emit canonical use cases until actors, objective text, and flow structure are accepted.", "アクター、目的テキスト、フロー構造が受理されるまで canonical なユースケースを出力してはならない。"),
]


def apply_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    for source, target in replacements:
        text = text.replace(source, target)
    return text


def main() -> int:
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    for file_name, replacements in FILE_REPLACEMENTS.items():
        path = DST / file_name
        text = path.read_text(encoding="utf-8")
        path.write_text(apply_replacements(text, replacements), encoding="utf-8")

    for path in DST.iterdir():
        if path.name in FILE_REPLACEMENTS or path.name in {"case_manifest.yaml", "scoring_rubric.yaml"}:
            continue
        if path.suffix.lower() in {".yaml", ".sysml"}:
            text = path.read_text(encoding="utf-8")
            path.write_text(apply_replacements(text, GLOBAL_REPLACEMENTS), encoding="utf-8")

    print(DST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
