# SysMLBuilder

SysMLBuilder は、Markdown で書かれた要求仕様を SysML のv1およびv2に変換するツールです。
現状は生成系AIを利用せず、完全に決定論的なツールです。

SysMLBuilder は、Markdown で書かれた要求仕様をそのまま直接 SysML に変換するのではなく、
まず **Requirement Contract** に正規化し、その後で SysML の成果物へ射影します。

ライセンスは [Apache License 2.0](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/LICENSE) です。

このリポジトリには 2 つの役割があります。

- 変換方式そのものの実装
- GfSE 参照モデルを根拠にした strict benchmark スイート

現状の実装は、付属の strict suite を確実に再現するための **決定的なルールベース実装** です。
実際の LLM 推論はまだ入っていません。

## 何ができるか

- Markdown 要求仕様から Requirement Contract を生成する
- Contract から canonical SysML を生成する
- 不足情報や曖昧さを review overlay SysML に分離する
- Contract と SysML 要素の対応を projection manifest として出力する
- Common Semantic IR と SysML v1 sidecar payload の土台を生成する
- 英語版 strict suite と、日本語化した派生 suite の両方で同等性を確認する

## 変換の考え方

このリポジトリの中心は **Requirement Contract** です。

変換は次の流れで進みます。

1. Markdown 要求仕様を読む
2. 要求を構造化して Contract にする
3. 十分に確定できる内容だけを canonical SysML に出す
4. 不足情報やレビュー待ち事項を review overlay に出す
5. Contract と成果物の対応関係を manifest に残す

この方式により、次の境界を明確に保てます。

- 原文根拠と推測
- 正式モデルとレビュー用ドラフト
- 要求本文と SysML 要素の対応

## リポジトリ構成

- `src/sysml_builder/`
  - 変換実装本体
- `scripts/`
  - suite 実行、検証、日本語版データ生成
- `profiles/`
  - Contract schema、pattern、projection、lint 定義
- `testdata/gfse_derived/`
  - 英語版 strict suite
- `testdata/gfse_derived_ja/`
  - 日本語化した派生 suite
- `testdata/legacy_auto_backdoor/`
  - 旧来のサンプル
- `docs/`
  - 設計意図、採点ガイド、利用者向け文書
- `reports/`
  - 検証結果の出力先

## 主要ファイル

- 利用者ガイド: [docs/user_input_to_sysml_flow.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/user_input_to_sysml_flow.md)
- 設計意図: [docs/developer_design_rationale.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/developer_design_rationale.md)
- 採点ガイド: [docs/benchmark_scoring_guide.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/benchmark_scoring_guide.md)
- Contract schema: [profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml)
- pattern 定義: [profiles/requirement_patterns.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_patterns.yaml)
- projection 定義: [profiles/projection_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/projection_profiles.yaml)

## セットアップ

前提:

- Python 3.10 以上

最小セットアップ:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

依存は軽く、基本的には `PyYAML` が中心です。

## 変換の実行

単一の Markdown ファイルを変換する場合:

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli testdata\gfse_derived\case01_vehicle_explicit_high_requirements.md -o out
```

出力されるファイル:

- `*_contracts.yaml`
- `*_canonical.sysml`
- `*_review_overlay.sysml`
- `*_projection_manifest.yaml`

low 充足性ケースのように canonical が出ない場合もあります。
その場合は review overlay が主成果物です。

SysML v1 XMI も必要な場合:

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli testdata\SysMLBuilder_testdata_20cases\cases\C01_power_tailgate_conditions\requirements_en.md -o out --sysml-v1-xmi cameo ea
```

追加で出力されるファイル:

- `*_cameo_v1.xmi`
- `*_ea_v1.xmi`

`ea` 向け XMI には、要求図、ブロック定義図、内部ブロック図、ステートマシン図の diagram 定義も含めます。
モデル要素だけでなく diagram まで含めて確認したい場合は、まず `*_ea_v1.xmi` を使います。

Common IR から SysML v1 sidecar 向け payload を作る場合:

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.sidecar_cli testdata\SysMLBuilder_testdata_20cases\cases\C01_power_tailgate_conditions\requirements_en.md --target cameo -o out\C01_cameo_sidecar.yaml
```

この payload は、設計書で想定している JVM sidecar の入力契約です。
現状のリポジトリでは、`Common IR -> v1 projection -> sidecar request` までを Python 側で生成します。

JVM sidecar をビルドして XMI を生成する最小 smoke 手順:

```powershell
mvn -q package -f sidecar\pom.xml
java -jar sidecar\target\sysml-v1-sidecar-0.1.0-SNAPSHOT-jar-with-dependencies.jar `
  --input out\C01_cameo_sidecar.yaml `
  --output out\C01_cameo_sidecar.xmi
```

現在の sidecar は Eclipse UML2 を使って SysML v1 向け XMI を生成します。
sidecar の `ea` 向け XMI も同様に、要求図、ブロック定義図、内部ブロック図、ステートマシン図の diagram 定義を含みます。

ツール固有の import smoke は補助用途です。Cameo / EA が使える環境でだけ任意に実行します:

```powershell
python scripts\run_cameo_import_smoke.py
```

通常の既定フローは `XMI` 出力のみです。`sidecar` の標準出力は `*.xmi` だけを生成します。
`cameo` と `ea` では target shim で XMI wrapper を分けています。
SysML profile 適用と OMG SysML.xmi 連携はまだ未実装です。

## 検証コマンド

英語版 strict suite:

```powershell
python scripts\run_local_suite.py
```

日本語版派生 suite:

```powershell
python scripts\run_local_suite_ja.py
```

pack の静的検査:

```powershell
python scripts\validate_pack.py
```

ユニットテスト:

```powershell
python -m unittest discover -s tests -v
```

MontiCore による SysML 構文検証:

```powershell
python scripts\validate_sysml_syntax.py --tool-jar tools\MCSysMLv2.jar
```

`tools\MCSysMLv2.jar` がある場合は、次も実行できます。

```powershell
$env:SYSML_MONTICORE_JAR = (Resolve-Path "tools\\MCSysMLv2.jar")
python -m unittest tests.test_randomized_input_resilience -v
```

## 生成される成果物

### 1. Requirement Contract

自然言語要求を構造化した中間表現です。

代表的な項目:

- `contract_id`
- `source_requirement_id`
- `source_anchor`
- `classification.pattern_id`
- `subject`
- `evidence`
- `gaps`
- `llm_proposals`

例:

- [case01_vehicle_explicit_high_expected_contracts.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_contracts.yaml)

### 2. canonical SysML

正式採用する SysML 成果物です。
仮説やレビュー待ち情報は入れません。

例:

- [case01_vehicle_explicit_high_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_canonical.sysml)
- [case04_mining_modular_interface_high_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case04_mining_modular_interface_high_expected_canonical.sysml)

### 3. review overlay SysML

不足情報、曖昧性、仮案、レビュー指示を持つ SysML 成果物です。

例:

- [case02_vehicle_ambiguous_low_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case02_vehicle_ambiguous_low_expected_review_overlay.sysml)
- [case06_mining_usecase_ambiguous_low_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case06_mining_usecase_ambiguous_low_expected_review_overlay.sysml)

### 4. projection manifest

Contract と SysML 要素の対応表です。
追跡性確認、監査、ビュー構築の基礎になります。

例:

- [case01_vehicle_explicit_high_expected_projection_manifest.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_projection_manifest.yaml)

## どのケースが何を表しているか

- `case01`
  - 定量性能とインタフェースが十分に明示された high ケース
- `case02`
  - 曖昧な性能要求を review overlay へ逃がす low ケース
- `case03`
  - 文脈別閾値を含む contextual performance の high ケース
- `case04`
  - 型付きポートとモジュラー IF を含む high ケース
- `case05`
  - use case を canonical と overlay に分ける medium ケース
- `case06`
  - 曖昧な運用記述を review overlay に残す low ケース

## 日本語版について

`testdata/gfse_derived_ja/` は英語版 strict suite を「構文に影響しない範囲」で日本語化した派生データです。

確認方針:

- localized な文言は日本語になっていてよい
- ただし構造結果は英語版と同等であるべき
- `scripts/run_local_suite_ja.py` は、その同等性を正規化比較で確認する

## プロファイルの作成と調整

このリポジトリでは、変換方式の考え方を `profiles/` 配下の YAML に分けています。

まず押さえるべきこと:

- Contract の形を決めるファイル
  - [profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml)
- 要求パターンを決めるファイル
  - [profiles/requirement_patterns.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_patterns.yaml)
- SysML への射影方針を決めるファイル
- [profiles/projection_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/projection_profiles.yaml)
- [profiles/common_semantic_ir_schema.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/common_semantic_ir_schema.yaml)
projection_profiles.yaml)
- benchmark ケースごとの抽出と投影を決めるファイル
  - [profiles/case_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/case_profiles.yaml)
- canonical SysML の package 構造を決めるファイル
  - [profiles/canonical_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/canonical_profiles.yaml)
- generic case の描画規則を決めるファイル
  - [profiles/generic_case_profile.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/generic_case_profile.yaml)
- 何をどこで変えるかの早見表
  - [docs/customization_map.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/customization_map.md)

### 新しいプロファイルを作る基本手順

1. 既存 YAML をコピーして、新しい `profile_id` を付ける
2. 追加したい要求タイプに対応する slot を `requirement_contract.yaml` で定義する
3. その要求タイプを `requirement_patterns.yaml` に pattern として追加する
4. benchmark ケースなら `case_profiles.yaml` に contract 抽出規則と overlay / projection manifest を追加する
5. canonical SysML を出すなら `canonical_profiles.yaml` に package 構造を追加する
6. generic case 系の共通規則を変えるなら `generic_case_profile.yaml` を更新する
7. 必要なら lint と benchmark ルールを更新する
8. 入力例と expected 出力を `testdata/` に追加して検証する

### どのファイルで何を決めるか

`requirement_contract.yaml`:

- 必須フィールド
- first-class slot
- gap があったときに overlay へ送る方針
- projector が読むべき slot

`requirement_patterns.yaml`:

- どんな文をどの pattern と見るか
- required slot / optional slot
- どの projector に渡すか
- review 必須条件

`projection_profiles.yaml`:

- canonical に入れてよい package
- overlay に入れる package
- requirement / interface / use case の出し方
- allocation / satisfy / behavior の出し方

`case_profiles.yaml`:

- case metadata
- contract extraction の capture regex
- contract ごとの subject / slot / proposal
- overlay に出す draft requirement
- projection manifest

`canonical_profiles.yaml`:

- canonical package 名
- package ごとの SysML body
- benchmark ケースの canonical 出力構造

### 最小の作成例

たとえば「安全余裕要求」を追加したい場合は、次の順で作るのが自然です。

1. `requirement_contract.yaml` に `safety_margin` を追加する
2. `requirement_patterns.yaml` に `safety_margin_constraint` を追加する
3. `required_slots` に `subject`, `measured_property`, `safety_margin` を入れる
4. `projectors.requirements` を新しい requirement 形式へ向ける
5. `projection_profiles.yaml` で canonical 側に出すか overlay 側に出すかを決める

### 注意

benchmark 6ケースについては、現在の実装は profile-driven です。
つまり case metadata / contract extraction / canonical / overlay / projection manifest は `profiles/` の定義から生成されます。

主に使うファイル:

- [profiles/case_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/case_profiles.yaml)
- [profiles/canonical_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/canonical_profiles.yaml)
- [profiles/review_overlay.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/review_overlay.yaml)

generic case 系も、描画規則自体は profile-driven です。
ただし各 `case.yaml` の構造スキーマをどう解釈するかというランタイム自体は Python 実装にあります。

## 現状の制約

- 実装は strict suite を通すためのルールベース実装
- 任意の自由文要求を汎用的に解釈する段階にはまだない
- pattern 判定や proposal 生成は、まだ LLM 呼び出しに置き換わっていない
- renderer は suite の期待形に強く寄せてある

## 今後の拡張ポイント

- pattern 分類を profile 駆動にする
- Contract 抽出をケース固定 regex から汎化する
- review overlay の proposal を LLM で生成する
- canonical renderer を package body から要素レベル生成へ移す
- CLI を複数ファイル一括処理に対応させる

## 最初に読む順番

1. [README.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/README.md)
2. [docs/user_input_to_sysml_flow.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/user_input_to_sysml_flow.md)
3. [docs/developer_design_rationale.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/developer_design_rationale.md)
4. [profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml)
5. [testdata/gfse_derived/case_manifest.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case_manifest.yaml)
