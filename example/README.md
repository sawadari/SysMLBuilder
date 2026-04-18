# Example Layout

このフォルダは、SysMLBuilder のユーザー向けサンプルをまとめたものです。

## 配置ルール

- `example/<model>/input`
  入力ファイルを置く
- `example/<model>/output`
  ツールの出力結果と参照用ファイルを置く

基本的には、1 つのモデル対象ごとに 1 つのフォルダがあります。
英語版と日本語版がある場合は、同じ `input` / `output` の中に `*_en.*` と `*_ja.*` を分けて置きます。

## output の見方

- `expected_*`
  参照用の期待出力です。手元で確認したい完成例として使います。
- `generated_*`
  実際に SysMLBuilder を実行して生成した結果です。
- `*_contracts.yaml`
  requirement contract の抽出結果です。
- `*_projection_manifest.yaml`
  SysML v1 / XMI などの派生出力に関するメタ情報です。対象ケースにだけあります。
- `*_syntax.yaml`
  `.sysml` を構文検証ツールに通した結果です。
- `*_cameo_display_guide.md`
  Cameo でどの view をどう表示するかの補足ガイドです。全サンプルに 1 つずつあります。

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
