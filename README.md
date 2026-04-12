# SysML v2 変換方法 改善版パック（GfSE 参照の厳密テストスイート付き）

このパックは、要求仕様から SysML v2 へ変換する方法を **Requirement Contract 中心** に再設計し、
GfSE の公開 SysML v2 モデルを直接参照して作成した **厳密テストスイート** を追加したものです。

## この版で増えたもの
- GfSE 参照モデルを元にボトムアップで作成した Markdown 要求仕様テストデータ
- high / medium / low 充足性を分けた expected Requirement Contract
- 以前より厳密化した expected `.sysml`
- テストケースごとの採点基準表
- 「なぜこう設計したか」を開発者向けに説明する文書
- strict benchmark 用の静的検査スクリプト

## 最初に読むファイル
1. `docs/developer_design_rationale.md`
2. `docs/gfse_testdata_design_feedback.md`
3. `docs/benchmark_scoring_guide.md`
4. `profiles/automotive_control_profile_v3.yaml`
5. `profiles/requirement_patterns.yaml`
6. `profiles/projection_profiles.yaml`
7. `testdata/gfse_derived/case_manifest.yaml`
8. `testdata/gfse_derived/scoring_rubric.yaml`

## この版の重要な設計更新
- 厳密採点の対象は **direct_file_grounded** のケースだけに限定
- README 抽象説明だけに依存するケースは strict benchmark から外した
- `operational_use_case_objective` を新しい pattern として追加
- `use_cases` projector を追加
- 文脈別閾値、型付き IF、main/exception flow を first-class slot として追加
- strict benchmark は canonical / review overlay の期待形をケース別に持つ

## ディレクトリ構成
- `docs/`
  - 開発者向け設計意図、GfSE 参照からの設計更新、採点ガイド
- `profiles/`
  - 変換プロファイル、pattern、projection、lint、benchmark ルール
- `testdata/gfse_derived/`
  - GfSE 参照モデルから逆生成した Markdown 要求仕様、expected contracts、expected `.sysml`、rubric
- `testdata/legacy_auto_backdoor/`
  - 以前の自動バックドア例
- `scripts/`
  - 静的検査スクリプト
- `reports/`
  - 検査結果とベンチマーク要約

## 使い方
1. 入力 Markdown を Requirement Contract へ正規化する
2. pattern を分類する
3. projector で expected artifact を出す
4. strict benchmark なら scoring rubric で採点する
5. review decision を反映して再実行する

## 注意
- strict benchmark は **直接確認できた GfSE の `.sysml` ファイル** に基づくケースのみを採点対象にしています。
- `.sysml` はできる限り GfSE の書き方へ寄せていますが、ここでは **期待出力の見本** として使ってください。
- allocation / satisfy の厳密構文は、ツール差を避けるため manifest と doc block で併用しています。
