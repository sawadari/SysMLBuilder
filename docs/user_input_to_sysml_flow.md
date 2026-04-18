# 初心者向け実行ガイド

## この文書の目的

この文書は、SysMLBuilder を初めて触る人が、

1. 何をするツールかを理解する
2. サンプルを 1 回動かす
3. 出力ファイルの見方を知る
4. Cameo で確認する

までを迷わず進められるようにするためのガイドです。

## まず 1 分で理解する

SysMLBuilder は、Markdown で書かれた要求やユースケースの記述を、

- 中間整理用の `contracts.yaml`
- 確定側の `canonical.sysml`
- 必要に応じて `review_overlay.sysml`
- 追跡用の `projection_manifest.yaml`

へ変換するツールです。

このツールは、文章をそのまま 1 つの巨大な SysML に押し込むのではなく、
「確定している内容」と「まだレビューが必要な内容」を分けて扱います。

## どのサンプルから始めればよいか

最初に触るなら、次の 3 つのサンプルのどれかを使います。

- `dont_panic_batmobile`
  公開されている Batmobile の `.sysml` を Markdown から再生成する最小サンプル
- `dont_panic_batmobile_displayable`
  Batmobile の symbolic view を表示確認しやすくした派生サンプル
- `vehicle_practice_expression_views`
  Cameo 向けに、要求・構造・アクション・状態を 1 つの `.sysml` にまとめたサンプル

迷ったら `vehicle_practice_expression_views` から始めてください。
出力 `.sysml` に加えて、Cameo 用の表示ガイドも自動生成されます。

## サンプルの配置

サンプルは次のルールで整理されています。

- `example/<モデル名>/input`
  入力 Markdown
- `example/<モデル名>/output`
  期待出力の `.sysml`、`contracts.yaml`、`syntax.yaml` など

たとえば `vehicle_practice_expression_views` は次です。

- 入力:
  `example/vehicle_practice_expression_views/input/vehicle_practice_expression_views_requirements.md`
- 期待出力:
  `example/vehicle_practice_expression_views/output/`

## 事前準備

前提:

- Python 3.10 以上
- PowerShell もしくは同等のシェル

セットアップ:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

補足:

- `pip install -e .[dev]` により、CLI とテスト実行に必要な依存を入れます
- インストール後は `sysml-builder` コマンドも使えますが、最初は `python -m ...` のほうが分かりやすいです

## 最短で 1 回動かす

新しく出力を作りたいだけなら、次を実行します。

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\vehicle_practice_expression_views\input\vehicle_practice_expression_views_requirements.md `
  -o example\vehicle_practice_expression_views\output
```

成功すると、`example\vehicle_practice_expression_views\output\` に次のようなファイルが出ます。

- `vehicle_practice_expression_views_contracts.yaml`
- `vehicle_practice_expression_views_canonical.sysml`
- `vehicle_practice_expression_views_cameo_display_guide.md`

ケースによっては、さらに次も出ます。

- `review_overlay.sysml`
- `projection_manifest.yaml`

## サンプルの期待出力と比べたいとき

既存サンプルの期待出力と照らしたい場合は、まず `example/.../output` を見ます。

例:

- 期待 `.sysml`:
  `example/vehicle_practice_expression_views/output/vehicle_practice_expression_views_canonical.sysml`
- 期待ガイド:
  `example/vehicle_practice_expression_views/output/vehicle_practice_expression_views_cameo_display_guide.md`

サンプルを再生成して期待出力を更新したい場合は、出力先をその `output` フォルダにします。

```powershell
$env:PYTHONPATH='src'
python -m sysml_builder.cli `
  example\vehicle_practice_expression_views\input\vehicle_practice_expression_views_requirements.md `
  -o example\vehicle_practice_expression_views\output
```

## 生成後に何を見ればよいか

おすすめの確認順は次です。

1. 入力 Markdown
2. `contracts.yaml`
3. `canonical.sysml`
4. `review_overlay.sysml`
5. `cameo_display_guide.md`
6. `projection_manifest.yaml`

見るポイント:

- `contracts.yaml`
  要求がどう解釈されたか
- `canonical.sysml`
  正式側として採用された SysML
- `review_overlay.sysml`
  曖昧さや未解決項目の残し方
- `cameo_display_guide.md`
  Cameo でどの view に何を表示すべきか
- `projection_manifest.yaml`
  どの要求がどのモデル要素へ写像されたか

## Cameo で確認する手順

`vehicle_practice_expression_views` を例にすると、次の順で進めると分かりやすいです。

1. `vehicle_practice_expression_views_canonical.sysml` を Cameo / CATIA Magic へ読み込む
2. `Views` パッケージを開く
3. 見たい `view` を開く
4. まず `Display > Display Exposed Elements` を実行する
5. 構造や関係線が足りない場合は `Display > Display Connectors` を実行する
6. 詳しい使い分けは、同じフォルダの `vehicle_practice_expression_views_cameo_display_guide.md` を参照する

重要:

- Cameo 本体と SysML v2 Plugin の Hot Fix 番号は合わせてください
- `RequirementsTreeView` と `RequirementTreeView` は build により表記ゆれがあります

## 何が出るケースなのか

各サンプルの役割は次のとおりです。

- `dont_panic_batmobile`
  「公開 `.sysml` を忠実に再出力できるか」を見る
- `dont_panic_batmobile_displayable`
  「symbolic view を表示確認しやすい形に寄せられるか」を見る
- `vehicle_practice_expression_views`
  「要求・構造・振る舞いを text-first で Cameo に持ち込めるか」を見る

## よくあるつまずき

### `canonical.sysml` は出たが Cameo で何も表示されない

原因の大半は、`view` を開いただけで `Display Exposed Elements` を実行していないことです。

### `review_overlay.sysml` が出たので失敗だと思った

失敗とは限りません。
未解決要件を無理に canonical 側へ入れなかった、という意味です。

### どのファイルを直せば振る舞いが変わるのか分からない

まずは次を見てください。

- `profiles/case_profiles.yaml`
- `profiles/canonical_profiles.yaml`
- `docs/developer_design_rationale.md`

## 便利な確認コマンド

ユニットテスト:

```powershell
python -m unittest discover -s tests -v
```

SysML 構文検証:

```powershell
python scripts\validate_sysml_syntax.py --tool-jar tools\MCSysMLv2.jar
```

## 次に読む文書

- 想定ユースケースを知りたい:
  [use_cases.md](docs/use_cases.md)
- 内部設計を知りたい:
  [developer_design_rationale.md](docs/developer_design_rationale.md)
- サンプルの配置ルールを見たい:
  [example/README.md](example/README.md)
