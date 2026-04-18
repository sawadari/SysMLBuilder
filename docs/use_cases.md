# 想定ユースケース

## この文書の目的

この文書は、SysMLBuilder をどんな場面で使うことを想定しているかを定義します。
同時に、「向いている使い方」と「向いていない使い方」も明確にします。

## 想定する利用者

主な利用者は次の 4 種類です。

- 要求分析者
  Markdown 要求を整理して SysML へ写したい
- モデルベース開発の実務者
  Cameo で確認できる `.sysml` サンプルや view を使いたい
- ツール開発者
  変換ルールや profile を追加したい
- ベンチマーク管理者
  サンプルや比較ケースを増やしたい

## 主要ユースケース

### 1. Markdown 要求から SysML 成果物を作る

もっとも基本的な使い方です。

入力:

- Markdown 形式の要求仕様

出力:

- `contracts.yaml`
- `canonical.sysml`
- 必要に応じて `review_overlay.sysml`
- `projection_manifest.yaml`

このユースケースでは、「自動で図を完成させること」より、
「根拠を残して成果物を分けて出すこと」を重視します。

### 2. 公開サンプル `.sysml` を再生成する

公開されている `.sysml` を、Markdown から再現できるようにするユースケースです。

対象サンプル:

- `dont_panic_batmobile`

向いている場面:

- roundtrip の基準を作りたい
- 公開サンプルをツール入力へ落とし込みたい
- 生成の差分確認をしたい

### 3. Cameo で確認しやすい sample view を出す

text-first で書いた SysML v2 を Cameo で確認しやすくしたい場合です。

対象サンプル:

- `dont_panic_batmobile_displayable`
- `vehicle_practice_expression_views`

向いている場面:

- 要求 view を確認したい
- 構造 view を確認したい
- action / state の symbolic view を試したい
- View ごとの `Display Exposed Elements` / `Display Connectors` の使い分けを残したい

### 4. SysML v1 系ツール向けの連携データを出す

SysML v2 だけでなく、SysML v1 系資産やツールとつなぎたい場合です。

出力:

- SysML v1 projection
- Cameo / EA 向け XMI
- sidecar request

向いている場面:

- 既存の SysML v1 ベース運用へ橋渡ししたい
- JVM sidecar を使って後段処理につなぎたい

### 5. サンプル pack と benchmark を保守する

これは利用というより、ツール運用のユースケースです。

対象:

- `example`

向いている場面:

- サンプルを追加したい
- roundtrip テストを増やしたい
- 日本語版と英語版の整合性を見たい

このときの推奨入力形式は、`requirements_*.md + input/case.yaml` です。
Markdown は人間が読む要求仕様書に保ち、ケース固有の要素名や view 定義はローカル profile に置きます。

## 今回のサンプル群の位置づけ

### `dont_panic_batmobile`

用途:

- 公開 Batmobile `.sysml` の忠実再生成

見るべき点:

- canonical `.sysml` の一致
- roundtrip の安定性

### `dont_panic_batmobile_displayable`

用途:

- Batmobile ベースの symbolic view 表示確認

見るべき点:

- `filter` と `expose` を加えたときの見え方
- 元サンプルとの役割差

### `vehicle_practice_expression_views`

用途:

- Cameo 向けの実行例
- 要求・構造・アクション・状態を含む practice モデル

見るべき点:

- 自然な要求仕様書とローカル `case.yaml` の分担
- expression-based view の使い分け
- `*_cameo_display_guide.md` の案内
- 構造と振る舞いをどの view で確認するか

## SysMLBuilder が向いていること

- ケース定義済み Markdown を安定して SysML 成果物へ変換すること
- 自然な Markdown と小さなローカル profile を組み合わせてサンプルを増やすこと
- サンプルや benchmark の expected output を維持すること
- 曖昧さを overlay 側へ分離すること
- text-first の SysML v2 サンプルを整理すること
- Cameo で確認しやすい補助ガイドを付けること

## SysMLBuilder が向いていないこと

- 任意の自然文を自由入力して高精度に一般化変換すること
- 完全自動で図レイアウト済みのモデルを出すこと
- Cameo の GUI 操作をテキストだけで完全代替すること
- 汎用 SysML v2 モデリング IDE として使うこと

## ユースケースごとのおすすめ入口

- とにかく 1 回動かしたい:
  [user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
- サンプルを見たい:
  [example/README.md](example/README.md)
- 内部設計を変えたい:
  [developer_design_rationale.md](docs/developer_design_rationale.md)
