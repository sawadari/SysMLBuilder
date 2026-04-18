# Vehicle Practice Expression Views Cameo Display Guide

このガイドは `vehicle_practice_expression_views_canonical.sysml` を Cameo / CATIA Magic で開いた後、どの view に対してどの Display 操作を選ぶと見たい情報が出やすいかを整理したものです。
expression-based view は built-in filter を持つので、まずはこちらを使い、線や関係を見たいときだけ `iv` / `afv` / `stv` 側へ切り替える運用を前提にしています。

## 基本操作

- Textual Editor で読み込んだ後は `Synchronize` を実行する。
- まず各 view で `Display > Display Exposed Elements` を実行する。これは expose 済み要素を view に出す基本操作です。
- 線が不足する場合は、対象シンボルを選んで `Display > Display Connectors` を追加実行する。
- 2026x Hot Fix 1 以降では `Display Connectors` 周りの不具合修正が入っている。モデリングツール本体と SysML v2 Plugin の Hot Fix 番号は一致させる。

## View ごとの使い分け

### Requirements Tree

- 対象要素: requirement def MassRequirement
- 対象要素: requirement vehicleSpecification
- 対象要素: requirement vehicleMass
- 対象要素: requirement engineMass
- 向いている用途: 要求階層と requirement usage を最短で確認したいとき
- 向いている用途: 標準ライブラリ要素を極力見たくないとき
- Cameo 操作: `Display > Display Exposed Elements`
- 補足: expression-based tree view なので、通常はこれだけで十分です。
- 補足: `RequirementsTreeView` が名前解決できない build では `RequirementTreeView` に置き換えます。

### Parts Tree

- 対象要素: part def Vehicle
- 対象要素: part vehicle1
- 対象要素: engine / transmission の part 階層
- 向いている用途: 部品階層だけを軽く確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- 補足: tree view は線より階層確認向きです。

### Parts Nested

- 対象要素: part def Vehicle
- 対象要素: nested part hierarchy
- 向いている用途: ネストされた containment を箱の入れ子で見たいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 必要なら対象シンボルに対して `Display > Display Parts`
- 補足: nested view なので、部品の内包関係が tree view より視覚的です。

### Parts & Ports Nested

- 対象要素: Vehicle / Engine / Transmission
- 対象要素: drivePwrPort / clutchPort
- 向いている用途: 部品に加えてポートも見たいとき
- 向いている用途: IBD に近い入口が欲しいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: ポートが不足する場合は `Display > Display Ports`
- Cameo 操作: 線が不足する場合は `Display > Display Connectors`
- 補足: expression-based view なのでノイズは少ないですが、線は追加表示が必要なことがあります。

### System Interconnection

- 対象要素: EngineToTransmissionInterface
- 対象要素: engine.drivePwrPort to transmission.clutchPort
- 向いている用途: connection / interface / flow の線を優先して見たいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: `Display > Display Connectors`
- 補足: `iv` は interconnection representation 向けです。構造の線を見るときは最初にこの view を試すのが分かりやすいです。

### Actions Nested

- 対象要素: action providePower
- 対象要素: action generateTorque
- 対象要素: action transferTorque
- 向いている用途: action の入れ子や所有関係を確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 必要なら対象 action に対して `Display > Display Actions`
- 補足: flow 線より action 階層の確認向きです。

### Actions Tree

- 対象要素: action providePower
- 対象要素: action generateTorque
- 対象要素: action transferTorque
- 向いている用途: action の構成を tree で一覧したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- 補足: tree 表示なので軽い確認向きです。

### Action Flow View

- 対象要素: flow of Torque from generateTorque.torque to transferTorque.inTorque
- 対象要素: providePower 配下の action 群
- 向いている用途: action 間の flow を線で見たいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 線が不足する場合は `Display > Display Connectors`
- 補足: `Action Flow View` は renderer 名ではなく標準 predefined symbolic view definition の `DS_Views::SymbolicViews::afv` を使っています。

### States Nested

- 対象要素: part def Controller
- 対象要素: exhibit state controllerStates
- 対象要素: state operatingStates / off / on
- 向いている用途: state の所有構造を確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 内部 state が不足する場合は対象 state machine または state に対して `Display > Display Features`
- 補足: nested view は state hierarchy を追うのに向いています。

### State Transition View

- 対象要素: transition initial
- 対象要素: transition off_to_on
- 対象要素: transition on_to_off
- 向いている用途: 遷移矢印を優先して確認したいとき
- Cameo 操作: `Display > Display Exposed Elements`
- Cameo 操作: 必要なら state / state machine に対して `Display > Display Features`
- 補足: `State Transition View` は標準 predefined symbolic view definition の `DS_Views::SymbolicViews::stv` を使っています。

## 公式リンク

- [Exposing elements for views](https://docs.nomagic.com/SYSML2P/2026x/exposing-elements-for-views-254423168.html)
- [Displaying elements in symbolic views](https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html)
- [Filtering elements for views](https://docs.nomagic.com/SYSML2P/2026x/filtering-elements-for-views-254423172.html)
- [Rendering views](https://docs.nomagic.com/SYSML2P/2026x/rendering-views-254422759.html)
- [2026x Hot Fix 1](https://docs.nomagic.com/VN/latest/2026x-hot-fix-1-278725663.html)
