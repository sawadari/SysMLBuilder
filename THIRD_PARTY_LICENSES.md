# Third-Party Materials

このファイルは、SysMLBuilder を公開するときに注意すべき第三者由来物を整理したものです。
このリポジトリ自身のコードと文書のライセンスは [Apache License 2.0](LICENSE) ですが、同梱物や参照サンプルの権利関係は別です。

## 基本方針

- このリポジトリ自身のコード、設定、独自文書は `LICENSE` の条件に従います。
- 第三者由来のツール、JAR、公開サンプル、書籍由来サンプルは、それぞれの配布条件に従います。
- 公開前に、実際に同梱しているファイル単位で再配布可否を確認してください。

## 同梱または参照している主な第三者由来物

### 1. MontiCore SysML v2 parser / validator

- 対象ファイル:
  - `tools/MCSysMLv2.jar`
- 由来:
  - MontiCore の SysML v2 関連成果物
- 公開時の注意:
  - この JAR をそのまま同梱して配布する場合は、取得元リポジトリまたは配布ページのライセンスと notice を確認してください。
  - バージョンごとに配布条件や notice の置き方が変わる可能性があるため、公開時点の upstream 表記を再確認してください。

### 2. Systems Modeling / OMG 系の公開 SysML v2 サンプル

- 対象:
  - `example/` 配下のうち、公開 SysML v2 サンプルを参照または派生元としているもの
- 由来:
  - SysML v2 Release / Pilot Implementation / 公開 example model
- 公開時の注意:
  - 元の公開リポジトリに書かれているライセンス条件に従ってください。
  - 派生サンプルを含める場合は、元の出典とライセンスを README などに明示してください。

### 3. Batmobile サンプル

- 対象:
  - `example/dont_panic_batmobile/`
  - `example/dont_panic_batmobile_displayable/`
- 由来:
  - 「Don't Panic - The Absolute Beginners Guide to SysML v2」で紹介される Batmobile 例に基づくサンプル
- 公開時の注意:
  - 書籍・ツール内サンプル由来の内容は、コードと違って転載条件が別扱いになることがあります。
  - このサンプルを公開物に含める場合は、書籍本文やツール配布物からの転載に該当しないかを確認してください。
  - 必要なら、完全転載ではなく「参考にして再構成した独自サンプル」であることを明示してください。

### 4. Cameo / CATIA Magic 連携用スクリプト

- 対象:
  - `scripts/run_cameo_import_smoke.py`
  - `tools/cameo_smoke_action/`
- 公開時の注意:
  - これらは Cameo / CATIA Magic のインストール先やプラグイン API を利用する補助コードです。
  - ここには Cameo 本体や No Magic / Dassault 製 JAR は同梱していません。
  - 商用製品本体、製品付属 JAR、製品ログなどはこのリポジトリに含めないでください。

## 公開前チェックリスト

- `tools/` にある第三者配布物の再配布可否を確認した
- `example/` にあるサンプルの出典を把握し、必要な表記を README か文書に書いた
- 商用ツール本体、商用ツール付属 JAR、ログ、ライセンスファイルを誤って同梱していない
- ローカル絶対パス、ユーザー名、環境依存ログを含む生成物を除去または匿名化した

## 免責

この文書は公開判断を補助するための整理であり、法的助言ではありません。
最終的な再配布可否は、実際に公開するファイル、取得元、ライセンス本文に基づいて確認してください.
