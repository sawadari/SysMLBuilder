# C17_ota_update_preconditions Cameo Display Guide

このファイルは、Cameo / CATIA Magic でこのサンプルを開くときに、どの `.sysml` を開き、どの Display 操作を選ぶとよいかをまとめたものです。

## まず見るファイル

- 推奨: `generated_en_canonical.sysml`

## output にあるファイル

### `.sysml`
- `expected_en.sysml`
- `expected_ja.sysml`
- `generated_en_canonical.sysml`
- `generated_ja_canonical.sysml`

### `.yaml`
- `C17_ota_update_preconditions_syntax.yaml`
- `generated_en_contracts.yaml`
- `generated_ja_contracts.yaml`

## このサンプルの見方

- このサンプルの主目的は contract / canonicalization / review overlay の確認です。
- `.sysml` は読み込めますが、最初から表示用 `view` が入っている前提ではありません。
- そのため、Cameo では Textual Editor で内容を確認し、必要なら手動で diagram または symbolic view を作る使い方になります。

## どのファイルを読むか

- `*_canonical.sysml`: 正規化済み SysML を確認する
- `generated_*_contracts.yaml`: Markdown から抽出された requirement contract を確認する
- `*_syntax.yaml`: 構文検証の結果を確認する

## Cameo で確認するときの基本手順

- Textual Editor に貼るか `.sysml` を読み込む
- `Synchronize` を実行する
- モデルブラウザで package / requirement / part / action / state を確認する
- view が無い場合は `Display Exposed Elements` は不要です

## 公式リンク

- [Working with textual editor](https://docs.nomagic.com/SYSML2P/2026x/working-with-textual-editor-254422032.html)
- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)
