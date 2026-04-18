# Don't Panic Batmobile Displayable Roundtrip

この文書は、公開されている `Dont_Panic_Batmobile` サンプルを保持しつつ、空だった symbolic view に `filter` と `expose` を追加した派生ケースを説明します。

## 追加したファイル

- 入力 Markdown:
  [batmobile_displayable_views_requirements.md](example/dont_panic_batmobile_displayable/input/batmobile_displayable_views_requirements.md)
- サンプル出力 `.sysml`:
  [dont_panic_batmobile_displayable_canonical.sysml](example/dont_panic_batmobile_displayable/output/dont_panic_batmobile_displayable_canonical.sysml)

## 目的

元の公開サンプルは `batmobileParts` 以外の symbolic view が空宣言です。

この派生ケースでは、

- 元のモデル要素は維持する
- `batmobileParts` はそのまま残す
- symbolic view に `filter DS_Functions::IsNonStandardLibraryElement();` を付ける
- symbolic view に `expose` を追加して、Cameo で内容を出しやすくする

という方針を取っています。

## 実行例

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\dont_panic_batmobile_displayable\input\batmobile_displayable_views_requirements.md `
  -o example\dont_panic_batmobile_displayable\output
```

出力:

- `example\dont_panic_batmobile_displayable\output\dont_panic_batmobile_displayable_canonical.sysml`
- `example\dont_panic_batmobile_displayable\output\dont_panic_batmobile_displayable_contracts.yaml`
- `example\dont_panic_batmobile_displayable\output\dont_panic_batmobile_displayable_syntax.yaml`

サンプルデータとして固定している入出力は次です。

- `example\dont_panic_batmobile_displayable\input`
- `example\dont_panic_batmobile_displayable\output`

## 注意点

このケースは公開サンプルの忠実複製ではなく、表示確認用の派生版です。
公開サンプルそのものを再現したい場合は、引き続き
[docs/dont_panic_batmobile_roundtrip.md](docs/dont_panic_batmobile_roundtrip.md)
を使ってください。
