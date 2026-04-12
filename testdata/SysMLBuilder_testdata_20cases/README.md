# SysMLBuilder test data pack (20 bilingual cases)

このパックは、要求仕様から SysML v2 テキストを生成するツールのための自己完結型テストデータ集です。
英語・日本語の要求仕様書と、対応する英語・日本語の `.sysml` を 20 ケース収録しています。

## 構成
- `cases/<case-id>_<slug>/requirements_en.md`
- `cases/<case-id>_<slug>/requirements_ja.md`
- `cases/<case-id>_<slug>/expected_en.sysml`
- `cases/<case-id>_<slug>/expected_ja.sysml`
- `cases/<case-id>_<slug>/case.yaml`

## ケースの狙い
- timed response
- fault reaction
- threshold monitoring
- typed ports / interfaces
- state-machine flavored behavior
- automotive control logic

## リポジトリへの置き方
この環境では `https://github.com/sawadari/SysMLBuilder` のディレクトリ構成を直接読めなかったため、
`testdata/` にそのまま置ける自己完結型の構成にしています。
必要なら `cases/` 以下をリポジトリ側の好みのパスへ移動してください。

## 注意
- `.sysml` は SysML v2 テキスト表記を意識して作っていますが、この環境では正式パーサによる完全構文検証はしていません。
- 代わりに、ファイル整合性と基本的な静的チェックを `scripts/validate_testdata.py` で行っています。
