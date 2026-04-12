# 利用者向け入力と成果物の流れ

## 概要
このリポジトリでは、利用者が用意した Markdown 要求仕様をそのまま直接 `.sysml` にせず、まず Requirement Contract に正規化し、その後に SysML 成果物へ射影します。

流れ:
1. Markdown 要求仕様を入力する
2. 要求を構造化して Requirement Contract にする
3. Contract から canonical SysML を出す
4. 不足情報があれば review overlay SysML を出す
5. 対応表として projection manifest を出す
6. 検証する

## 1. 利用者が最初に用意するもの
最初のインプットは Markdown の要求仕様書です。

最低限必要な内容:
- 要求 ID
- 要求本文
- セクション名
- 対象システムやモジュールが分かる表現

入力例:
```md
# Case 01: Vehicle quantitative and interface requirements

## Requirements
- REQ-VEH-001: The vehicle shall have a total mass less than or equal to 2000 kg.
- REQ-VEH-002: The vehicle shall maintain an average city fuel economy of at least 25 mpg in the nominal city driving scenario with an assumed cargo mass of at least 500 kg.
- REQ-VEH-004: The engine shall transfer generated torque to the transmission through the clutch interface.
```

入力サンプル:
- [case01_vehicle_explicit_high_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_requirements.md)
- [case05_mining_usecase_medium_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_requirements.md)

## 2. 最初の処理: Markdown を読み解く
この段階は [parser.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/parser.py) が担当します。

処理内容:
1. ファイル名やタイトルからケース ID を決める
2. 文書 ID、文書名、ドメイン、言語を付ける
3. 箇条書き要求を抜き出す
4. ユースケース形式なら Main Flow と Exception Flows を抜き出す

ここではまだ SysML は出ません。入力文書を分解して、機械が扱える形にします。

## 3. 中間表現: Requirement Contract
次に [transformer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/transformer.py) が Requirement Contract を作ります。

Contract の基本項目:
- `contract_id`
- `source_requirement_id`
- `source_anchor`
- `trace_quality`
- `classification.pattern_id`
- `subject`
- `evidence`

要求の種類に応じて追加される項目:
- `measured_property`
- `comparator`
- `threshold_value`
- `threshold_unit`
- `operating_contexts`
- `contextual_thresholds`
- `interface_name`
- `interface_ends`
- `flows`
- `actors`
- `objective_text`
- `main_flow_steps`
- `exception_flow_steps`
- `gaps`
- `llm_proposals`

Contract の役割:
- 自然言語要求を構造化する
- どの要求がどの SysML 要素になったか追跡できるようにする
- 正式モデルとレビュー待ち情報を分離する

Contract 出力例:
- [case01_vehicle_explicit_high_expected_contracts.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_contracts.yaml)

## 4. 処理をさらに細かく分けると何が起きるか
1. 要求文を 1 件ずつ読む
2. 要求パターンを判定する
3. 必要 slot を抜き出す
4. 欠けている slot を検出する
5. 正式化できるものを canonical 側へ回す
6. 不足があるものを review overlay 側へ回す

要求パターン定義:
- [requirement_patterns.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_patterns.yaml)

主な pattern:
- `quantified_property_constraint`
- `contextual_quantified_performance`
- `interface_transfer`
- `modular_slot_interface`
- `operational_use_case_objective`
- `ambiguous_quality_claim`

## 5. 最終成果物 1: canonical SysML
canonical SysML は正式モデルです。十分に構造化できた内容だけが入ります。

典型的に入るもの:
- `part def`
- `port def`
- `interface def`
- `requirement def`
- `requirement`
- `use case def`
- `SatisfactionManifest`
- `AllocationManifest`
- `ViewTargets`

代表例:
- [case01_vehicle_explicit_high_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_canonical.sysml)
- [case04_mining_modular_interface_high_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case04_mining_modular_interface_high_expected_canonical.sysml)
- [case05_mining_usecase_medium_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_expected_canonical.sysml)

意味:
- 要求から正式に採用した SysML モデル
- 不足情報や仮説は入れない

## 6. 最終成果物 2: review overlay SysML
review overlay は、曖昧さや不足情報をレビュー用に切り出した SysML です。

主に入るもの:
- `DraftRequirementContracts`
- `MissingSlots`
- `OpenQuestions`
- `Assumptions`
- `BehaviorCandidates`
- `TraceWeaknesses`
- `ReviewGuide`

使う場面:
- 閾値がない
- 単位がない
- actor が不足している
- success criteria が未定義
- interface 詳細が不足している

代表例:
- [case02_vehicle_ambiguous_low_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case02_vehicle_ambiguous_low_expected_review_overlay.sysml)
- [case06_mining_usecase_ambiguous_low_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case06_mining_usecase_ambiguous_low_expected_review_overlay.sysml)

意味:
- 変換を止めずにレビュー待ち事項を明示する成果物
- canonical に昇格させる前の確認対象

## 7. 最終成果物 3: projection manifest
projection manifest は Contract と SysML 要素の対応表です。

書かれる内容:
- どの contract がどの requirement 名になったか
- どの interface がどこを接続するか
- どこへ allocation されたか
- どこで satisfy されたか
- どの view を描画対象にするか

代表例:
- [case01_vehicle_explicit_high_expected_projection_manifest.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_projection_manifest.yaml)
- [case05_mining_usecase_medium_expected_projection_manifest.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_expected_projection_manifest.yaml)

意味:
- 要求と SysML 成果物の対応を追跡するための監査用ファイル

## 8. 利用者から見た最終納品物
利用者目線で見ると、最終的に重要なのは次の 3 つです。

1. canonical `.sysml`
2. review overlay `.sysml`
3. projection manifest `.yaml`

補助的だが重要な中間成果物:
- `contracts.yaml`

## 9. 実装上の担当箇所
- 入力解析: [parser.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/parser.py)
- Contract 化: [transformer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/transformer.py)
- 成果物分岐: [pipeline.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/pipeline.py)
- SysML / manifest 生成: [renderer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/renderer.py)
- 検証: [validate_pack.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/scripts/validate_pack.py), [suite.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/suite.py)

## 10. 実行イメージ
1. Markdown 要求仕様を用意する
2. 変換処理を実行する
3. Contract を確認する
4. canonical と overlay を確認する
5. manifest で対応関係を確認する
6. 検証を通す

実行コマンド:
```powershell
python scripts/run_local_suite.py
python scripts/validate_pack.py
```

## 11. 利用者が押さえるべき点
- 入力は Markdown 要求仕様から始まる
- Requirement Contract が変換の中心である
- 最終成果物は canonical だけではない
- 曖昧な要求は review overlay に分離される
- projection manifest で要求と SysML の対応を追える
