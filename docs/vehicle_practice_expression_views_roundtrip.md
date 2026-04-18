# Vehicle Practice Expression Views Roundtrip

この文書は、Cameo / CATIA Magic の text-first 検証向けに、要求・構造・アクション・状態遷移を 1 つの `.sysml` にまとめて再生成するケースを説明します。

## 追加したファイル

- 入力 Markdown:
  [vehicle_practice_expression_views_requirements.md](example/vehicle_practice_expression_views/input/vehicle_practice_expression_views_requirements.md)
- サンプル出力 `.sysml`:
  [vehicle_practice_expression_views_canonical.sysml](example/vehicle_practice_expression_views/output/vehicle_practice_expression_views_canonical.sysml)
- サンプル出力 Cameo ガイド:
  [vehicle_practice_expression_views_cameo_display_guide.md](example/vehicle_practice_expression_views/output/vehicle_practice_expression_views_cameo_display_guide.md)

## 方針

- 要求は `RequirementsTreeView`
- 構造は `PartsTreeView` / `PartsNestedView` / `'Parts&PortsNestedView'`
- アクションは `ActionsNestedView` / `ActionsTreeView`
- 状態は `StatesNestedView`
- 線を見やすくする補助として `DS_Views::SymbolicViews::iv` / `afv` / `stv`

を同じモデル内に置いています。

## Cameo での使い方

1. Textual Editor に同期する
2. 各 `view` を開く
3. `Display -> Display Exposed Elements` を実行する
4. 構造 view で線を追加したい場合は `Display Connectors` を使う

`Views::asActionFlowDiagram` と `Views::asStateTransitionDiagram` は 2026x の公式 renderer 名として確認できなかったため、このケースでは標準 predefined symbolic view definitions の `afv` と `stv` を使っています。

## 注意点

要求ツリー view 名は、Cameo のドキュメントで `RequirementsTreeView` と `RequirementTreeView` の表記ゆれがあります。
このケースでは `RequirementsTreeView` を採用しています。もし名前解決エラーが出る場合は、生成 `.sysml` 内のその型名だけを `RequirementTreeView` に置き換えてください。

## 実行例

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\vehicle_practice_expression_views\input\vehicle_practice_expression_views_requirements.md `
  -o example\vehicle_practice_expression_views\output
```

出力:

- `example\vehicle_practice_expression_views\output\vehicle_practice_expression_views_canonical.sysml`
- `example\vehicle_practice_expression_views\output\vehicle_practice_expression_views_contracts.yaml`
- `example\vehicle_practice_expression_views\output\vehicle_practice_expression_views_cameo_display_guide.md`
- `example\vehicle_practice_expression_views\output\vehicle_practice_expression_views_syntax.yaml`

サンプルデータとして固定している入出力は次です。

- `example\vehicle_practice_expression_views\input`
- `example\vehicle_practice_expression_views\output`
