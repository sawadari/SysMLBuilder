# Example Layout

このフォルダは、SysMLBuilder のユーザー向けサンプルをまとめたものです。

## 配置ルール

- `example/<model>/input`
  入力ファイルを置く
- `example/<model>/output`
  ツールの出力結果と参照用ファイルを置く

基本的には、1 つのモデル対象ごとに 1 つのフォルダがあります。
英語版と日本語版がある場合は、同じ `input` / `output` の中に `*_en.*` と `*_ja.*` を分けて置きます。

## 入力の考え方

新しいサンプルでは、次の形を標準とします。

- `requirements_*.md`
  人がそのまま読んでレビューできる自然な要求仕様書
- `case.yaml`
  そのケース専用のローカル rule/profile

つまり、Markdown には「何を作りたいか」を書き、`case.yaml` には「そのケースでどの要素名や view 定義を使うか」を置きます。
グローバル `profiles/` に hidden な例外を増やすより、この形の方がサンプル単位で理解しやすく、保守もしやすいです。

Markdown の標準セクションは次です。

- `## Context` / `## 背景`
- `## Requirements` / `## 要求`
- `## Use Cases` / `## ユースケース`
- `## Structure Hints` / `## 構造ヒント`
- `## Interface Hints` / `## インタフェースヒント`
- `## Metadata` / `## メタデータ`
- `## Authoring Notes` / `## 記述方針`

要求部は、次のような読みやすい形を標準とします。

- `- CASE-ID: ...`
- `- [CASE-ID] ...`
- `1. [CASE-ID] ...`

特に新しいサンプルでは、長い SysML キーワード列を Markdown に埋め込むより、
「このモデルで何を見たいか」「どんな package / view 群が必要か」を自然文で書く方を優先します。

詳細な書式は
[docs/standard_requirement_spec_format.md](../docs/standard_requirement_spec_format.md)
を参照してください。

## 標準 View セット

example の canonical `.sysml` には、原則として次の View を含めます。

- `Requirements View`
- `Structural Context View`
- `Internal Structure View`
- `Behavior Activity View`
- `Behavior State View`

モデル固有の view を追加してもよいですが、この 5 つは共通入口として揃えます。

## サンプルの種類

- ローカル `case.yaml` + 自然文 Markdown
  `C01` から `C20`、`legacy_auto_backdoor_*`、`vehicle_practice_expression_views`
- グローバル benchmark profile + 自然文 Markdown
  `case01` から `case06`
- 公開サンプルの roundtrip / 派生表示サンプル
  `dont_panic_batmobile`、`dont_panic_batmobile_displayable`

## output の見方

- `expected_*`
  参照用の期待出力です。手元で確認したい完成例として使います。
- `generated_*`
  実際に SysMLBuilder を実行して生成した結果です。
- `<case_id>_*`
  そのケースの代表出力です。複数入力がある場合は `default -> en -> ja` の優先順で代表版を置きます。
- `*_contracts.yaml`
  requirement contract の抽出結果です。
- `*_projection_manifest.yaml`
  SysML v1 / XMI などの派生出力に関するメタ情報です。対象ケースにだけあります。
- `*_syntax.yaml`
  `.sysml` を構文検証ツールに通した結果です。
- `*_cameo_display_guide.md`
  Cameo でどの view をどう表示するかの補足ガイドです。全サンプルに 1 つずつあります。

## 一括再生成

example 全体の出力を再生成するときは次を使います。

```powershell
python scripts\regenerate_examples.py
```

## 含まれている主なサンプル

- `dont_panic_batmobile`
  公開 Batmobile `.sysml` の roundtrip
- `dont_panic_batmobile_displayable`
  Batmobile の symbolic view 表示確認向け派生版
- `vehicle_practice_expression_views`
  Cameo 向けの要求・構造・アクション・状態サンプル
- `case01_vehicle_explicit_high` から `case06_mining_usecase_ambiguous_low`
  GFSE 派生 benchmark の英日サンプル
- `C01_power_tailgate_conditions` から `C20_washer_low_fluid_warning`
  20ケースの英日サンプル
- `legacy_auto_backdoor_complete_ja`
  legacy 自動バックドア完全版の再構成サンプル
- `legacy_auto_backdoor_incomplete_ja`
  legacy 自動バックドア不足情報版の再構成サンプル

## 補足

- ユーザーが見る入口は `example/` を想定しています。
- `legacy_auto_backdoor_*` の `input` Markdown は、元の requirement contract の evidence から再構成した参考入力です。
