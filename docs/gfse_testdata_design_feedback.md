# GfSE 参照モデルから得た設計フィードバック

この文書は、GfSE の公開 SysML v2 モデルを参照しながら strict benchmark を作成した結果、
設計をどう更新したかを整理したものです。

## 1. VehicleModel.sysml
### 観察
- `requirement def` に subject、attribute、`require constraint` がある
- `requirement` usage 側で `redefines` を使って値を具体化している
- `satisfy ... by ...` がある
- `port def`、`interface def`、`interface ... connect ... to ...` がある

### 設計への影響
- `quantified_property_constraint` を強化
- `interface_transfer` を first-class pattern にした
- strict expected `.sysml` では requirement def / usage の両方を使うようにした
- manifest 側でも satisfy を別軸で採点するようにした

## 2. MiningFrigateRequirementsDef.sysml
### 観察
- cargo capacity と survivability のような定量 requirement がある
- survivability は High Sec と Low Sec 系で閾値が分かれる
- 同じ requirement def の中で context 別制約が表現されている

### 設計への影響
- `contextual_quantified_performance` を追加
- `operating_contexts` と `contextual_thresholds` を contract slot に追加
- context 別 threshold を flatten しすぎない方針に変更した

## 3. standardPortsAndInterfaces.sysml
### 観察
- `port def HighSlotPort` のような型付き port 定義がある
- `interface def HighSlotInterface` で `end` と `flow` が定義されている
- IF の意味は port の型と flow によって固定されている

### 設計への影響
- typed port 必須を benchmark rule に昇格
- `modular_slot_interface` を追加
- `flows` と `interface_ends` を contract slot に追加
- strict expected `.sysml` では interface def まで要求するようにした

## 4. UseCasesFrigate.sysml
### 観察
- `use case def` に subject、actor、objective がある
- objective doc に Main Flow / Exception Flows が書かれている
- use case narrative は requirement へ無理に潰さない方が情報が保てる

### 設計への影響
- `operational_use_case_objective` を追加
- `use_cases` projector を追加
- medium satisfiability ケースでは canonical use case + review overlay の二系統出力を許可
- scoring rubric に actor / flow retention を追加

## 5. strict suite の境界
### 観察
- abstract な README 説明だけでは expected `.sysml` を強く固定できない
- strict benchmark には source file grounded なケースだけが向く

### 設計への影響
- `trace_quality` を profile と case manifest に追加
- strict scoring は `direct_file_grounded` のみ許可
- abstract-only ケースは今回はパックから外した

## まとめ
今回の strict suite で足りなかったのは、
**context、typed IF、use case、trace quality**
の4点でした。
そのため今回の版では、pattern / projector / lint / scoring をこの4点中心に拡張しています。
