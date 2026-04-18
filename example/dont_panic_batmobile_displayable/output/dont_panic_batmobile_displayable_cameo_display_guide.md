# dont_panic_batmobile_displayable Cameo Display Guide

このファイルは、Cameo / CATIA Magic でこのサンプルを開くときに、どの `.sysml` を開き、どの Display 操作を選ぶとよいかをまとめたものです。

## まず見るファイル

- 推奨: `generated_default_canonical.sysml`

## output にあるファイル

### `.sysml`
- `dont_panic_batmobile_displayable_canonical.sysml`
- `generated_default_canonical.sysml`

### `.yaml`
- `dont_panic_batmobile_displayable_contracts.yaml`
- `dont_panic_batmobile_displayable_syntax.yaml`
- `generated_default_contracts.yaml`

## このサンプルの見方

- このサンプルは `view` と `expose` を含むので、Cameo 上で symbolic view を開いて表示できます。
- まず Textual Editor で読み込み、`Synchronize` を実行します。
- その後、対象の `view` を開いて `Display > Display Exposed Elements` を実行します。
- 線や関係が不足する場合は `Display > Display Connectors` を追加で実行します。

## どの操作を選ぶか

- 要素の箱をまず出したいとき: `Display > Display Exposed Elements`
- 部品間の接続や flow や bind を出したいとき: `Display > Display Connectors`
- ポートが不足するとき: `Display > Display Ports`
- state や action の内側が不足するとき: `Display > Display Features` または `Display > Display Actions`

## こういう用途のときに使う

- 要求を階層で見たい: tree 系 view を開いて `Display Exposed Elements`
- 構造を見たい: parts / parts&ports / interconnection 系 view を開いて `Display Exposed Elements`
- 振る舞いを見たい: actions / states 系 view を開いて `Display Exposed Elements`
- 線が足りない: 同じ view で `Display Connectors`

## 公式リンク

- [Working with textual editor](https://docs.nomagic.com/SYSML2P/2026x/working-with-textual-editor-254422032.html)
- [Exposing elements for views](https://docs.nomagic.com/SYSML2P/2026x/exposing-elements-for-views-254423168.html)
- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)
- [Filtering elements for views](https://docs.nomagic.com/SYSML2P/2026x/filtering-elements-for-views-254423172.html)
- [Rendering views](https://docs.nomagic.com/SYSML2P/2026x/rendering-views-254422759.html)
