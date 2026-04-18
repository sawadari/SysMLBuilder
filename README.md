# SysMLBuilder

SysMLBuilder は、Markdown で書いた要求仕様を、追跡しやすい SysML 成果物へ変換するためのツールです。  
文章をそのまま 1 つのモデルへ押し込むのではなく、まず Requirement Contract として整理し、そこから SysML や補助ファイルを出します。

ライセンスは [Apache License 2.0](LICENSE) です。

第三者由来の JAR、公開サンプル、Cameo 連携コードの扱いは別です。公開前に
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)
を確認してください。

## 何ができるか

- Markdown 要求を `contracts.yaml`、`canonical.sysml`、`projection manifest` へ変換できる
- 曖昧な内容を `review_overlay.sysml` として分離できる
- SysML v1 XMI や sidecar payload を追加生成できる
- Cameo 向けの `.sysml` サンプルと表示ガイドを一緒に管理できる
- サンプルと expected output を `example/` で一元管理できる

## 処理の流れ

SysMLBuilder は、入力した Markdown をいきなり SysML に変換しません。  
まず **Requirement Contract** という中間データに整理し、そのあと必要に応じて複数の成果物へ分けて出力します。

流れは次のとおりです。

1. Markdown の要求仕様を読む
2. 要求の内容を Requirement Contract に整理する
3. 十分に明確な内容だけを canonical SysML にする
4. 曖昧な内容や不足情報は review overlay に分ける
5. 要求と出力の対応表を projection manifest に残す

この流れにより、「正式に採用してよい内容」と「まだ確認が必要な内容」を分けて扱えます。

## 主な出力

- `*_contracts.yaml`
  要求文を整理した中間データ
- `*_canonical.sysml`
  正式モデルとして扱いやすい SysML
- `*_review_overlay.sysml`
  曖昧さや不足情報をレビュー用に分けた SysML
- `*_projection_manifest.yaml`
  要求と SysML 要素の対応表

必要に応じて SysML v1 XMI、sidecar payload、Cameo 表示ガイドも出力できます。

## 想定ユースケース

- 要求仕様から SysML への変換ルールを揃えたい
- 曖昧な要求を隠さず、レビューしやすい形で残したい
- Cameo で確認できる text-first な SysML v2 サンプルを管理したい
- 公開 `.sysml` サンプルの roundtrip ケースを持ちたい
- ベンチマーク付きで変換品質を確かめたい

## リポジトリの見取り図

- `src/sysml_builder/`
  変換処理の本体
- `example/`
  ユーザー向けに整理したサンプル一式
- `docs/`
  使い方、設計意図、採点方法、設定変更ガイド
- `profiles/`
  変換ルールや出力方針を定義する YAML
- `scripts/`
  実行補助、検証、ベンチマーク用スクリプト
- `reports/`
  検証結果の出力先

## 公開時の注意

- このリポジトリ自身のコードは Apache 2.0 ですが、`tools/` や `example/` の一部は第三者由来物を含みます。
- `tools/MCSysMLv2.jar` を再配布する場合は、取得元のライセンスと notice を確認してください。
- `example/dont_panic_batmobile*` のような書籍・ツール由来サンプルは、転載条件を確認してください。
- Cameo / CATIA Magic 本体や製品付属 JAR は、このリポジトリに含めない前提です。
- 詳細は [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) を参照してください。

## 最短ではじめる

前提:

- Python 3.10 以上

セットアップ:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

最初の実行例:

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\vehicle_practice_expression_views\input\vehicle_practice_expression_views_requirements.md `
  -o example\vehicle_practice_expression_views\output
```

出力結果は `example\vehicle_practice_expression_views\output\` に作られます。

主な出力:

- `vehicle_practice_expression_views_contracts.yaml`
- `vehicle_practice_expression_views_canonical.sysml`
- `vehicle_practice_expression_views_cameo_display_guide.md`

より詳しい手順は
[docs/user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
を参照してください。

## SysML v1 XMI も出したい場合

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli example\C01_power_tailgate_conditions\input\requirements_en.md -o example\C01_power_tailgate_conditions\output --sysml-v1-xmi cameo ea
```

追加で次のようなファイルが出ます。

- `*_cameo_v1.xmi`
- `*_ea_v1.xmi`

## sidecar 用データを作る場合

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.sidecar_cli example\C01_power_tailgate_conditions\input\requirements_en.md --target cameo -o example\C01_power_tailgate_conditions\output\C01_cameo_sidecar.yaml
```

JVM sidecar を使って XMI へ変換する最小手順:

```powershell
mvn -q package -f sidecar\pom.xml
java -jar sidecar\target\sysml-v1-sidecar-0.1.0-SNAPSHOT-jar-with-dependencies.jar `
  --input example\C01_power_tailgate_conditions\output\C01_cameo_sidecar.yaml `
  --output example\C01_power_tailgate_conditions\output\C01_cameo_sidecar.xmi
```

## 品質確認のコマンド

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

## どの文書から読めばよいか

- はじめて触る人:
  [docs/user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
- 想定ユースケースを先に知りたい人:
  [docs/use_cases.md](docs/use_cases.md)
- ツールの内部設計を知りたい人:
  [docs/developer_design_rationale.md](docs/developer_design_rationale.md)
- Batmobile の公開 `.sysml` を roundtrip したい人:
  [docs/dont_panic_batmobile_roundtrip.md](docs/dont_panic_batmobile_roundtrip.md)
- Batmobile の symbolic view を表示確認用に派生させたい人:
  [docs/dont_panic_batmobile_displayable_roundtrip.md](docs/dont_panic_batmobile_displayable_roundtrip.md)
- Cameo 向けに要求・構造・アクション・状態遷移の expression-based view を試したい人:
  [docs/vehicle_practice_expression_views_roundtrip.md](docs/vehicle_practice_expression_views_roundtrip.md)
- サンプルデータの配置ルールを見たい人:
  [example/README.md](example/README.md)
- 採点や比較の考え方を知りたい人:
  [docs/benchmark_scoring_guide.md](docs/benchmark_scoring_guide.md)
- 設定をどこで変えるか知りたい人:
  [docs/customization_map.md](docs/customization_map.md)

## 現在の前提と制約

- 現状は生成 AI ではなく、決定論的なルールベース実装です
- strict suite を再現しやすいように、出力形式をかなり明確に決めています
- 自由度の高い自然文を何でも自動で高精度に解釈する段階ではありません
- 曖昧な要求は、無理に canonical へ入れず review overlay に出します

## 参考ファイル

- 初心者向けガイド:
  [docs/user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
- 想定ユースケース:
  [docs/use_cases.md](docs/use_cases.md)
- 内部設計:
  [docs/developer_design_rationale.md](docs/developer_design_rationale.md)
- 設定変更ガイド:
  [docs/customization_map.md](docs/customization_map.md)
- 20ケースの説明:
  [example/README.md](example/README.md)
