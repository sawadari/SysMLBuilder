# SysMLBuilder

SysMLBuilder は、Markdown で書かれた要求仕様をそのまま直接 SysML に変換するのではなく、
まず **Requirement Contract** に正規化し、その後で SysML v2 の成果物へ射影するためのリポジトリです。

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
- 何をどこで変えるかの早見表
  - [docs/customization_map.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/customization_map.md)

### 新しいプロファイルを作る基本手順

1. 既存 YAML をコピーして、新しい `profile_id` を付ける
2. 追加したい要求タイプに対応する slot を `requirement_contract.yaml` で定義する
3. その要求タイプを `requirement_patterns.yaml` に pattern として追加する
4. 生成したい成果物に応じて `projection_profiles.yaml` を調整する
5. 必要なら lint と benchmark ルールを更新する
6. 入力例と expected 出力を `testdata/` に追加して検証する

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

### 最小の作成例

たとえば「安全余裕要求」を追加したい場合は、次の順で作るのが自然です。

1. `requirement_contract.yaml` に `safety_margin` を追加する
2. `requirement_patterns.yaml` に `safety_margin_constraint` を追加する
3. `required_slots` に `subject`, `measured_property`, `safety_margin` を入れる
4. `projectors.requirements` を新しい requirement 形式へ向ける
5. `projection_profiles.yaml` で canonical 側に出すか overlay 側に出すかを決める

### 注意

現状の Python 実装は、まだ完全に profile-driven ではありません。
つまり `profiles/` だけを書き換えても、必ずしも実装が自動で追従するわけではありません。

今の段階では:

- profile は設計の正本
- `src/sysml_builder/` は strict suite を通すための実装

という位置づけです。

そのため、新しいプロファイルを本当に有効化したい場合は、通常は次も必要です。

- [src/sysml_builder/parser.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/parser.py)
- [src/sysml_builder/transformer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/transformer.py)
- [src/sysml_builder/renderer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/renderer.py)

## 現状の制約

- 実装は strict suite を通すためのルールベース実装
- 任意の自由文要求を汎用的に解釈する段階にはまだない
- pattern 判定や proposal 生成は、まだ LLM 呼び出しに置き換わっていない
- renderer は suite の期待形に強く寄せてある

## 今後の拡張ポイント

- pattern 分類を profile 駆動にする
- Contract 抽出をケース固定から汎化する
- review overlay の proposal を LLM で生成する
- canonical renderer をテンプレート固定から構造生成へ移す
- CLI を複数ファイル一括処理に対応させる

## 最初に読む順番

1. [README.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/README.md)
2. [docs/user_input_to_sysml_flow.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/user_input_to_sysml_flow.md)
3. [docs/developer_design_rationale.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/developer_design_rationale.md)
4. [profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml)
5. [testdata/gfse_derived/case_manifest.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case_manifest.yaml)
