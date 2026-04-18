# case06_mining_usecase_ambiguous_low Cameo Display Guide

このケースでは、標準 View セットを canonical `.sysml` に含めています。
まず `*_canonical.sysml` を読み込み、`Display > Display Exposed Elements` を起点に確認してください。

## 基本操作

- Textual Editor で `.sysml` を読み込んだ後、`Synchronize` を実行する。
- まず各 view で `Display > Display Exposed Elements` を実行する。
- 線や接続が足りない場合は `Display > Display Connectors` を追加実行する。
- ポートが不足する場合は `Display > Display Ports` を使う。
- 状態や内部要素が足りない場合は対象シンボルに対して `Display > Display Features` を使う。

## View ごとの使い分け

### Requirements View

- 向いている用途: requirement 階層を最短で確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- 補足: `RequirementsTreeView` が解決しない build では `RequirementTreeView` へ置き換えます。

### Structural Context View

- 向いている用途: システム全体と主要 part 階層を軽く確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`

### Internal Structure View

- 向いている用途: part / port / interface を内部構造寄りに確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 必要なら `Display > Display Ports`
- Cameo 操作: 線が不足する場合は `Display > Display Connectors`

### Behavior Activity View

- 向いている用途: action の入れ子や簡易 activity を確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: flow 線が不足する場合は `Display > Display Connectors`

### Behavior State View

- 向いている用途: state machine や状態階層を確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 必要なら `Display > Display Features`

## 公式リンク

- [Exposing elements for views](https://docs.nomagic.com/SYSML2P/2026x/exposing-elements-for-views-254423168.html)
- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)
- [Filtering elements for views](https://docs.nomagic.com/SYSML2P/2026x/filtering-elements-for-views-254423172.html)
- [Rendering views](https://docs.nomagic.com/SYSML2P/2026x/rendering-views-254422759.html)
- [2026x Hot Fix 1](https://docs.nomagic.com/VN/latest/2026x-hot-fix-1-278725663.html)
