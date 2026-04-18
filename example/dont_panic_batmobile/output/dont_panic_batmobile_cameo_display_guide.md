# dont_panic_batmobile Cameo Display Guide

このファイルは、Cameo / CATIA Magic でこのサンプルを開くときに、どの `.sysml` を開き、どの Display 操作を選ぶとよいかをまとめたものです。

## まず見るファイル

- 推奨: `generated_default_canonical.sysml`

## output にあるファイル

### `.sysml`
- `dont_panic_batmobile_canonical.sysml`
- `generated_default_canonical.sysml`

### `.yaml`
- `dont_panic_batmobile_contracts.yaml`
- `dont_panic_batmobile_syntax.yaml`
- `generated_default_contracts.yaml`

## このサンプルの見方

- このサンプルには `view` はありますが、表示用の `expose` が弱いか、用途が限定されています。
- まず `Display > Display Exposed Elements` を試し、何も出ない場合はその view は表示確認用ではなく、定義例として見てください。
- 表示目的なら `generated_*` より `expected_*` も合わせて確認すると差分が分かりやすいです。

## こういう用途のときに使う

- テキストとしての `view` 記述例を見たい
- Cameo で minimal な symbolic view を手で調整する出発点にしたい

## 公式リンク

- [Working with textual editor](https://docs.nomagic.com/SYSML2P/2026x/working-with-textual-editor-254422032.html)
- [Exposing elements for views](https://docs.nomagic.com/SYSML2P/2026x/exposing-elements-for-views-254423168.html)
- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)
