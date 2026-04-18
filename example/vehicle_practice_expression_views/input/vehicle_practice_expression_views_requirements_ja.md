# Vehicle Practice Expression Views

## 背景
この文書は、Cameo で確認しやすい小さな SysML v2 練習モデルを、人が読める要求仕様として記述したものです。
目的は大規模で精密なシステム記述ではなく、要求・構造・アクション・状態の view を 1 つの text-first 入力から安定して生成できるサンプルを用意することです。

## 目標
このサンプルでは、初心者が 1 つの `.sysml` を Cameo に取り込み、次の内容を確認できることを目指します。

- 小さな要求階層
- 1 本の明示的な接続を持つ構造モデル
- 小さなアクション flow
- 小さなステートマシン
- それぞれに対応した symbolic view

## 対象範囲
- 要求
  質量確認用の requirement definition を 1 つ用意し、それを車両とエンジンへ適用する requirement 階層を持つこと。
- 構造
  エンジン、トランスミッション、駆動力ポート型、エンジンからトランスミッションへの interface を含む小さな車両構造を持つこと。
- 振る舞い（アクション）
  トルクを生成して渡す action flow を 1 つ持つこと。
- 振る舞い（状態）
  start/off 信号で遷移する簡単な off/on ステートマシンを持つ controller を 1 つ持つこと。

## 記述方針
- package 名や view 名などの厳密な定義は、同じフォルダの `case.yaml` で固定する。
- Markdown 側は、人が読んで意図を理解できる説明を優先する。
- SysML のキーワードをすべて書き下す必要はなく、作りたいモデル内容が自然に伝わればよい。

## 要求
- [REQ-VPV-001] このサンプルは、車両とエンジンの質量を上限値と比較できる小さな要求 package を持つこと。
- [REQ-VPV-002] このサンプルは、車両、エンジン、トランスミッション、駆動力ポート型、およびエンジンからトランスミッションへの明示的な interface を持つ小さな構造 package を持つこと。
- [REQ-VPV-003] 構造 package には、tree view、nested view、interconnection view で表示できるよう、具体的な vehicle part usage も含めること。
- [REQ-VPV-004] このサンプルは、トルクを生成して渡す流れを持つ小さな action package を持つこと。
- [REQ-VPV-005] このサンプルは、start 信号と off 信号に応じて `off` と `on` の間を移る controller の state package を持つこと。
- [REQ-VPV-006] 要求 package に対する requirements tree view を持つこと。
- [REQ-VPV-007] 構造 package に対する parts tree、parts nested、parts and ports nested、system interconnection の各 view を持つこと。
- [REQ-VPV-008] action package に対する actions nested、actions tree、action flow の各 view を持つこと。
- [REQ-VPV-009] state package に対する states nested、state transition の各 view を持つこと。
- [REQ-VPV-010] このサンプルは Cameo で扱いやすいことを重視し、まず `Display > Display Exposed Elements` で意味が分かり、必要に応じて `Display > Display Connectors` で関係線を追加表示できること。
