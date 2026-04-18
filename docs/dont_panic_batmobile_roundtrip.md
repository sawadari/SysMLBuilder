# Don't Panic Batmobile Roundtrip

この文書は、`Dont_Panic_Batmobile` の公開 `.sysml` サンプルを、Markdown 要求仕様から再生成する roundtrip ケースを説明します。

## 追加したファイル

- 入力 Markdown:
  [dont_panic_batmobile_requirements.md](example/dont_panic_batmobile/input/dont_panic_batmobile_requirements.md)
- サンプル出力 `.sysml`:
  [dont_panic_batmobile_canonical.sysml](example/dont_panic_batmobile/output/dont_panic_batmobile_canonical.sysml)

## 目的

このケースの目的は、公開されている Batmobile サンプルを唯一の参照モデルとして扱い、その `.sysml` を再現できる Markdown 入力を SysMLBuilder に持たせることです。

ここでは diagram の自動再構成よりも、公開 `.sysml` テキスト自体を忠実に再出力できることを優先しています。

## 実行例

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\dont_panic_batmobile\input\dont_panic_batmobile_requirements.md `
  -o example\dont_panic_batmobile\output
```

出力:

- `example\dont_panic_batmobile\output\dont_panic_batmobile_canonical.sysml`
- `example\dont_panic_batmobile\output\dont_panic_batmobile_contracts.yaml`
- `example\dont_panic_batmobile\output\dont_panic_batmobile_syntax.yaml`

サンプルデータとして固定している入出力は次です。

- `example\dont_panic_batmobile\input`
- `example\dont_panic_batmobile\output`

## 方針

- サンプルは Batmobile だけを扱う
- Markdown は roundtrip 用の要求仕様書として保持する
- canonical 出力は公開 `.sysml` のテキストをそのまま返す
- `structural Modeling`、`behavioral modelling`、`use cases modelling`、`requirements modelling` を含む
