# 利用者ガイド

## この文書の目的

この文書は、SysMLBuilder を **利用者視点** で理解して使えるようにするためのガイドです。

対象読者:

- 要求仕様を SysML v2 に落としたい人
- strict suite を使って変換品質を確認したい人
- canonical と review overlay の使い分けを知りたい人
- 日本語化した要求仕様でも同じ構造結果を得られるか確認したい人

開発者向け設計背景は [developer_design_rationale.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/developer_design_rationale.md) を参照してください。

## まず結論

このリポジトリは、要求文をいきなり SysML に変換しません。

必ず次の順で進みます。

1. Markdown 要求仕様を読む
2. Requirement Contract に正規化する
3. 正式化できるものだけを canonical SysML に出す
4. 不足情報や曖昧さは review overlay に出す
5. 対応関係を projection manifest に出す

この順番が重要です。
理由は、自然言語要求には必ず「明確な部分」と「不足している部分」が混在するからです。

## 利用者が理解しておくべき 4 つの成果物

### contracts.yaml

これは変換の中心となる中間成果物です。
要求文を機械が扱える構造にしたものです。

見るべき点:

- どの要求がどの `pattern_id` と判定されたか
- `subject` は何か
- 定量要求なら閾値と単位が取れているか
- 不足情報が `gaps` に入っているか
- レビュー案が `llm_proposals` に出ているか

### canonical.sysml

これは正式採用候補の SysML です。

入ってよいもの:

- `part def`
- `requirement def`
- `requirement`
- `interface def`
- `use case def`
- `SatisfactionManifest`
- `AllocationManifest`

入ってはいけないもの:

- Draft 系
- MissingSlots
- OpenQuestions
- Assumptions
- BehaviorCandidates

### review_overlay.sysml

これはレビュー待ち事項の SysML です。

見るべき点:

- 何が不足しているか
- 何が仮案か
- どの review action を想定しているか

review overlay は失敗出力ではありません。
不足を隠さずに分離した成果物です。

### projection_manifest.yaml

これは追跡性のための対応表です。

見るべき点:

- どの contract がどの SysML 名へ写像されたか
- どこへ allocation されたか
- どこで satisfy されたか
- どの view を描画対象にしているか

## 利用者が最初に用意する入力

入力は Markdown です。
最低限、次の形にしてください。

```md
# 文書タイトル

## Requirements
- REQ-001: 要求本文
- REQ-002: 要求本文
```

ユースケース系なら次の形式も扱います。

```md
## Operational objectives
### UC-001 ユースケース名
Main Flow:
1. 手順1
2. 手順2

Exception Flows:
- 例外1
- 例外2
```

現在の実装が前提としている要素:

- 要求 ID
- 箇条書き形式
- セクション見出し
- 対象システムやモジュールを特定できる文

入力例:

- [case01_vehicle_explicit_high_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_requirements.md)
- [case05_mining_usecase_medium_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_requirements.md)

## 変換処理の流れ

### 1. 入力解析

[parser.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/parser.py) が担当します。

役割:

- ケース ID の推定
- 文書メタデータの設定
- 箇条書き要求の抽出
- ユースケースの main flow / exception flow 抽出
- 英語版と日本語版の見出し差異の吸収

### 2. Requirement Contract 化

[transformer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/transformer.py) が担当します。

役割:

- 要求パターンの割当
- subject の決定
- 定量 slot の抽出
- interface slot の抽出
- use case slot の抽出
- gap と proposal の付与

典型的な pattern:

- `quantified_property_constraint`
- `contextual_quantified_performance`
- `interface_transfer`
- `modular_slot_interface`
- `operational_use_case_objective`
- `ambiguous_quality_claim`

### 3. 成果物分岐

[pipeline.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/pipeline.py) が担当します。

役割:

- contracts の保持
- canonical が出るケースの判定
- overlay が出るケースの判定
- projection manifest の付与

### 4. SysML / manifest 生成

[renderer.py](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/src/sysml_builder/renderer.py) が担当します。

役割:

- expected 形式の canonical SysML 生成
- expected 形式の review overlay 生成
- projection manifest 生成
- 日本語版では human-readable 文面の切り替え

## どの出力をどう読めばよいか

### 定量要求が明確な場合

例:

- mass
- cargo capacity
- fuel economy
- DPS threshold

期待されること:

- `threshold_value`
- `threshold_unit`
- `comparator`
- `measured_property`

が contracts に入り、canonical に requirement / constraint が出ること。

### 文脈依存の性能要求がある場合

例:

- city / highway
- High Sec / Low Sec / Wormhole

期待されること:

- `operating_contexts`
- `contextual_thresholds`

が contracts に入り、canonical 側で context を反映した requirement になること。

### interface 要求がある場合

例:

- transfer
- interface
- through
- typed port

期待されること:

- `interface_name`
- `interface_ends`
- `flows`

が contracts に入り、canonical 側で `interface def` や `connect` が出ること。

### 曖昧要求の場合

例:

- lightweight
- fuel efficient
- efficiently
- when needed

期待されること:

- `gaps` が出る
- `llm_proposals` が出る
- canonical ではなく overlay が主成果物になる

## 代表ケースの読み方

### case01

用途:

- もっとも基本的な high 充足性ケース
- 定量要求とインタフェース要求の両方を見るのに向く

先に見るファイル:

- [case01_vehicle_explicit_high_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_requirements.md)
- [case01_vehicle_explicit_high_expected_contracts.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_contracts.yaml)
- [case01_vehicle_explicit_high_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case01_vehicle_explicit_high_expected_canonical.sysml)

### case02

用途:

- 曖昧要求をどう review overlay に落とすかを見る

先に見るファイル:

- [case02_vehicle_ambiguous_low_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case02_vehicle_ambiguous_low_requirements.md)
- [case02_vehicle_ambiguous_low_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case02_vehicle_ambiguous_low_expected_review_overlay.sysml)

### case05

用途:

- use case をどう扱うかを見る
- canonical と overlay の両方が出る medium ケース

先に見るファイル:

- [case05_mining_usecase_medium_requirements.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_requirements.md)
- [case05_mining_usecase_medium_expected_canonical.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_expected_canonical.sysml)
- [case05_mining_usecase_medium_expected_review_overlay.sysml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/testdata/gfse_derived/case05_mining_usecase_medium_expected_review_overlay.sysml)

## 実行手順

### 単一ファイルを変換する

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli testdata\gfse_derived\case01_vehicle_explicit_high_requirements.md -o out
```

### 英語版 strict suite を回す

```powershell
python scripts\run_local_suite.py
```

### 日本語版派生 suite を回す

```powershell
python scripts\run_local_suite_ja.py
```

### pack 全体の静的検査を回す

```powershell
python scripts\validate_pack.py
```

### テストを回す

```powershell
python -m unittest discover -s tests -v
```

### MontiCore で SysML 構文確認を回す

```powershell
python scripts\validate_sysml_syntax.py --tool-jar tools\MCSysMLv2.jar
```

`tools\MCSysMLv2.jar` があるなら、MontiCore を使う unittest も有効になります。

```powershell
$env:SYSML_MONTICORE_JAR = (Resolve-Path "tools\\MCSysMLv2.jar")
python -m unittest tests.test_randomized_input_resilience -v
```

## 日本語版確認の意味

`testdata/gfse_derived_ja/` は、英語版 strict suite を日本語化した派生データです。

ここで確認したいのは「日本語文面でも自然言語記述の差だけに留まり、構造結果が変わらないか」です。

したがって `run_local_suite_ja.py` は、次を見ています。

- contracts の構造は同じか
- projection manifest は同じか
- canonical / overlay の SysML 構造は同じか
- localized な文面差は許容する

つまり、日本語版で完全な文字列一致を取っているわけではなく、**構造同等性** を見ています。

## よくある見方の誤り

### review overlay が出たので失敗

誤りです。
review overlay は、曖昧さを隠さずに分離できたことを示します。

### canonical が出たので十分

不十分です。
projection manifest と contracts を見ないと追跡性が確認できません。

### contracts は中間ファイルだから見なくてよい

誤りです。
このリポジトリでは contracts が中核です。
問題があるときは、まず contracts を見てください。

## 実運用での使い方

実運用で見るなら、次の順が安定です。

1. Markdown 入力を確認する
2. contracts を確認する
3. canonical を確認する
4. overlay を確認する
5. projection manifest を確認する
6. 必要なら review decision を反映して再実行する

## プロファイルの作成方法

新しいドメインや要求タイプを追加したい場合は、`profiles/` 配下を基準に進めます。

最初に見るファイル:

- [profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml)
- [profiles/requirement_patterns.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_patterns.yaml)
- [profiles/projection_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/projection_profiles.yaml)
- [profiles/case_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/case_profiles.yaml)
- [profiles/canonical_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/canonical_profiles.yaml)
- [profiles/generic_case_profile.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/generic_case_profile.yaml)
- [docs/customization_map.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/customization_map.md)

### 手順 1. 何を追加したいかを決める

最初に、追加したいものを 1 つに絞ります。

例:

- 新しい要求 pattern
- 新しい slot
- use case の出力方針
- strict lint
- benchmark 採点条件

ここを曖昧にしたままファイルを触ると、pattern と projector がずれます。

### 手順 2. Contract schema を決める

[profiles/requirement_contract.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_contract.yaml) で中間表現を定義します。

主に触る場所:

- `contract_schema.required_fields`
- `contract_schema.first_class_slots`
- `artifact_hints`

追加の考え方:

- 正式に追跡したい情報なら `first_class_slots` に入れる
- projector が参照するなら `artifact_hints` にも反映する
- gap 扱いにしたいなら `normalization.gap_policy` と整合させる

例:

```yaml
contract_schema:
  first_class_slots:
  - safety_margin
artifact_hints:
  requirements_projector_reads:
  - safety_margin
```

### 手順 3. pattern を追加する

[profiles/requirement_patterns.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/requirement_patterns.yaml) で要求の分類方法を定義します。

主に触る場所:

- `detect.markers`
- `detect.section_bias`
- `required_slots`
- `optional_slots`
- `projectors`
- `review_policy`

最小例:

```yaml
patterns:
  safety_margin_constraint:
    detect:
      markers:
      - margin
      - reserve
      section_bias:
      - Requirements
    required_slots:
    - subject
    - measured_property
    - safety_margin
    projectors:
      requirements: SafetyMarginRequirement
    review_policy:
      llm_propose_missing: true
```

### 手順 4. projection 方針を決める

[profiles/projection_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/projection_profiles.yaml) で出力先を決めます。

判断すること:

- canonical に出すか
- overlay に送るか
- use case として出すか
- requirement として出すか
- behavior を自動で出すか

ここで決めるときの原則:

- 根拠が弱いものは overlay
- 不足 slot があるものも overlay
- formal に閉じるものだけ canonical

### 手順 5. ケースごとの抽出と canonical を定義する

benchmark ケースを追加する場合は、次も必要です。

- [profiles/case_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/case_profiles.yaml)
- [profiles/canonical_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/canonical_profiles.yaml)

`case_profiles.yaml` で決めること:

- case metadata
- contract extraction の regex / captures
- contract ごとの slot
- overlay draft
- projection manifest

`canonical_profiles.yaml` で決めること:

- canonical package 名
- package ごとの SysML body

generic 20 case pack の共通描画ルールを変えるなら:

- [profiles/generic_case_profile.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/generic_case_profile.yaml)

### 手順 6. lint と benchmark を必要に応じて更新する

関係ファイル:

- [profiles/benchmark_lints.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/benchmark_lints.yaml)
- [profiles/model_lints.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/model_lints.yaml)
- [profiles/gfse_reference_benchmark_profile.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/gfse_reference_benchmark_profile.yaml)

更新が必要になる例:

- 新しい artifact を canonical に追加した
- strict suite で禁止する package を増やした
- trace quality の条件を変えた

### 手順 7. テストデータを作る

新しい profile を入れたら、必ず入力例と expected 出力をセットで作ります。

追加候補:

- `*_requirements.md`
- `*_expected_contracts.yaml`
- `*_expected_canonical.sysml`
- `*_expected_review_overlay.sysml`
- `*_expected_projection_manifest.yaml`

実務上は、high / medium / low を分けて作ると確認しやすいです。

### 手順 8. 実装が追従しているか確認する

重要:

benchmark 6ケースと generic 20 case pack の描画規則については、現在の実装は profile-driven です。

つまり、次は `profiles/` を更新すればそのまま挙動に反映されます。

- [case_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/case_profiles.yaml)
- [canonical_profiles.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/canonical_profiles.yaml)
- [review_overlay.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/review_overlay.yaml)
- [generic_case_profile.yaml](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/profiles/generic_case_profile.yaml)

ただし benchmark 外の新しい投影方式や、`case.yaml` 自体のスキーマ拡張は必要に応じて実装側の拡張が要ります。

### 手順 9. 検証する

最低限、次を実行します。

```powershell
python scripts\run_local_suite.py
python scripts\run_local_suite_ja.py
python scripts\validate_pack.py
python -m unittest discover -s tests -v
python scripts\validate_sysml_syntax.py --tool-jar tools\MCSysMLv2.jar
```

### よくある失敗

- slot を schema に追加したが pattern の `required_slots` に入れていない
- pattern を追加したが projector が未定義
- canonical に出したいのに projection 側で overlay 扱いのまま
- lint だけ厳しくして expected を更新していない
- YAML は更新したが Python 実装が追従していない

## 現状の限界

- 任意自由文への汎用対応はまだ弱い
- suite 外の要求文ではケース固有ロジックに依存する部分がある
- proposal は本物の AI 推論ではなく、現時点では静的に与えている

## 次に読むべき文書

- [README.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/README.md)
- [developer_design_rationale.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/developer_design_rationale.md)
- [benchmark_scoring_guide.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/benchmark_scoring_guide.md)
- [customization_map.md](C:/Users/sawad/OneDrive/ドキュメント/dev/SysMLBuilder/docs/customization_map.md)
