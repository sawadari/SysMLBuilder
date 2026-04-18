# 内部設計

## この文書の目的

この文書は、SysMLBuilder の内部構造を把握したい開発者向けの説明です。
対象は次の人です。

- 新しいケースを追加したい
- 既存の変換ルールを変えたい
- 出力ファイルがどこで生成されているか知りたい
- SysML v1 変換や sidecar 連携まで追いたい

## 設計の基本方針

SysMLBuilder は、次の考え方で作っています。

1. 入力 Markdown をそのまま SysML にしない
2. まず Requirement Contract に整理する
3. 正式出力とレビュー出力を分ける
4. 追跡可能な中間データを残す
5. ケース差分はできるだけ `profiles/` で吸収する

このため、実装は「自然文を直接描画するツール」ではなく、
「ケース定義済みの Markdown を、追跡可能な変換パイプラインへ通すツール」という位置づけです。

## 全体アーキテクチャ

処理の大きな流れは次のとおりです。

1. `parser.py`
   Markdown を読み、`ParsedDocument` にする
2. `transformer.py`
   `ParsedDocument` を Requirement Contract 群へ変換する
3. `renderer.py`
   canonical SysML、overlay、projection manifest、Cameo ガイドを描画する
4. `common_ir.py`
   契約群と manifest から共通意味表現 `CommonIrModel` を組み立てる
5. `v1_projector.py`
   共通意味表現から SysML v1 用の安全な投影モデルを作る
6. `xmi.py`
   SysML v1 XMI を出す
7. `pipeline.py`
   上記を束ね、`TransformResult` として返す
8. `cli.py`
   ファイル出力を行う

## 主要モジュールと責務

### `src/sysml_builder/cli.py`

利用者がもっとも直接触る CLI です。

- 入力 Markdown を受け取る
- `transform_markdown()` を呼ぶ
- `write_result()` で出力ファイルを書く

### `src/sysml_builder/parser.py`

入力 Markdown を `ParsedDocument` にします。

主な役割:

- `case_id` の推定
- 要求箇条書きの抽出
- use case 形式の抽出
- 汎用ケース向け `case.yaml` 参照

この層では、まだ SysML は作りません。
「文書を構造化して読む」ことだけに責務を絞っています。

### `src/sysml_builder/transformer.py`

`ParsedDocument` から Requirement Contract を構築します。

主な役割:

- `case_profiles.yaml` の抽出ルールを読む
- 正規表現で必要スロットを抽出する
- `contract_id`、`pattern_id`、`subject`、`evidence` を付ける
- 汎用ケースなら generic profile ベースで簡易 contract を作る

この層が「入力解釈の中心」です。

### `src/sysml_builder/renderer.py`

契約や case profile に基づいて、最終ファイルを描画します。

主な役割:

- canonical SysML の出力
- review overlay の出力
- projection manifest の出力
- Cameo display guide の出力
- generic case の簡易 SysML 生成

今回のサンプル系では、`raw_sysml` を返す canonical profile もここを通ります。

### `src/sysml_builder/common_ir.py`

canonical 文字列とは別に、意味的に扱いやすい共通 IR を作ります。

主なデータ:

- `RequirementIR`
- `BlockIR`
- `PortTypeIR`
- `ConnectorIR`
- `StateMachineIR`
- `AllocationIR`
- `SatisfyIR`

使いどころ:

- SysML v1 投影
- sidecar 連携
- 将来の別出力先追加

### `src/sysml_builder/v1_projector.py`

`CommonIrModel` を SysML v1 の安全な部分集合へ写像します。

主な役割:

- requirement 投影
- block / port / connector 投影
- satisfy / allocate 関係の投影
- state machine 情報の保持

ここでは `PROJECTION_PROFILE = "safe_subset_v1_5"` を使っています。

### `src/sysml_builder/xmi.py`

SysML v1 XMI を生成します。

対象:

- Cameo
- Enterprise Architect

### `src/sysml_builder/pipeline.py`

変換全体のオーケストレーションです。

`TransformResult` に含まれる主なもの:

- `contracts`
- `canonical`
- `overlay`
- `cameo_display_guide`
- `projection_manifest`
- `common_ir`
- `v1_projection`
- `sysml_v1_xmi`

### `src/sysml_builder/sidecar_cli.py`

JVM sidecar と連携するための payload を出します。

流れ:

1. Markdown を読む
2. contract を作る
3. common IR を作る
4. SysML v1 projection を作る
5. sidecar 用 YAML / JSON を出す

## 主要なデータ構造

### `ParsedDocument`

入力文書の構造化結果です。

主な内容:

- 文書メタデータ
- 要求一覧
- use case 一覧
- generic case 用メタデータ

### Requirement Contract

現在は dataclass ではなく辞書ベースです。
この層が「自然文の意味づけ結果」です。

典型的な項目:

- `contract_id`
- `source_requirement_id`
- `classification.pattern_id`
- `subject`
- `evidence.quote`
- 抽出スロット
- `gaps`

### `CommonIrModel`

出力依存性を下げるための意味表現です。
SysML v2 文字列と SysML v1 XMI の間をつなぐ役割を持ちます。

### `V1ProjectionModel`

SysML v1 側で扱いやすい形へ落とした投影結果です。

## `profiles/` の役割

SysMLBuilder の振る舞いは、かなりの部分を `profiles/` で決めています。

重要なファイル:

- `profiles/case_profiles.yaml`
  ケースごとの抽出ルール、canonical profile 参照、追加ガイド
- `profiles/canonical_profiles.yaml`
  canonical SysML の出力内容
- `profiles/review_overlay.yaml`
  overlay の共通パッケージ名や文言方針
- `profiles/generic_case_profile.yaml`
  汎用ケースの描画方針
- `profiles/projection_profiles.yaml`
  投影設計に関する profile 群
- `profiles/requirement_patterns.yaml`
  要求分類パターンの定義
- `profiles/requirement_contract.yaml`
  contract スキーマ観点の定義

実装上、読み込みに直接使っているのは主に
`case_profiles.yaml`、`canonical_profiles.yaml`、`review_overlay.yaml`、`generic_case_profile.yaml` です。
他の profile 群は設計ルールや周辺検証の根拠として使います。

## ファイル出力規約

`write_result()` は、ケース ID を接頭辞にして出力を書きます。

典型的な出力:

- `<case_id>_contracts.yaml`
- `<case_id>_canonical.sysml`
- `<case_id>_review_overlay.sysml`
- `<case_id>_cameo_display_guide.md`
- `<case_id>_projection_manifest.yaml`
- `<case_id>_cameo_v1.xmi`
- `<case_id>_ea_v1.xmi`

この命名規約により、`example/<case>/output` にそのまま配置しやすくしています。

## 新しいケースを追加する手順

最小手順は次です。

1. `example/<case>/input` に Markdown を置く
2. `profiles/case_profiles.yaml` に case を追加する
3. 必要なら `profiles/canonical_profiles.yaml` に canonical profile を追加する
4. 必要なら Cameo guide を case profile に追加する
5. `tests/` に roundtrip テストを追加する
6. `python -m sysml_builder.cli ...` で `output` を生成する
7. `validate_sysml_syntax.py` で構文確認する

## サンプル設計の考え方

現在の `example/` は次の役割で整理しています。

- `dont_panic_batmobile`
  公開 `.sysml` の忠実 roundtrip
- `dont_panic_batmobile_displayable`
  表示確認向けの派生サンプル
- `vehicle_practice_expression_views`
  Cameo で view と display 操作を試すサンプル

サンプルを 1 か所に集めた理由は、
「入力 Markdown」と「期待出力一式」を同じモデル単位で見られるようにするためです。

## 拡張ポイント

拡張しやすい場所は次です。

- 新しい case 追加:
  `profiles/case_profiles.yaml`
- 新しい canonical 出力:
  `profiles/canonical_profiles.yaml`
- generic case の出力方針変更:
  `profiles/generic_case_profile.yaml`
- overlay 文言の変更:
  `profiles/review_overlay.yaml`
- 新しい補助出力追加:
  `renderer.py` と `pipeline.py`

## 非目標

現時点で SysMLBuilder が目指していないものも明確にしておきます。

- 任意の自然文を高精度に自由解釈すること
- GUI モデラの代わりに完全な図編集を行うこと
- Cameo の表示操作をテキストだけで完全自動化すること
- SysML v2 全文法を汎用的に生成すること

## 読み進める順番

内部を追うときは次の順が分かりやすいです。

1. `src/sysml_builder/cli.py`
2. `src/sysml_builder/pipeline.py`
3. `src/sysml_builder/parser.py`
4. `src/sysml_builder/transformer.py`
5. `src/sysml_builder/renderer.py`
6. `src/sysml_builder/common_ir.py`
7. `src/sysml_builder/v1_projector.py`
8. `src/sysml_builder/xmi.py`

## 関連文書

- 初心者向けの実行手順:
  [user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
- 想定ユースケース:
  [use_cases.md](docs/use_cases.md)
- サンプル配置:
  [example/README.md](example/README.md)
