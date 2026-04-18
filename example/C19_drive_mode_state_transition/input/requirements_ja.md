# C19 ドライブモード状態遷移

## 背景
このケースは、Eco、Normal、Sportの各ドライブモードと、遷移ガードおよび故障時フォールバックを表します。

## 機能要求
- C19-RQ-001: システムは、ECO、NORMAL、およびSPORTの各ドライブモードをサポートすること。
- C19-RQ-002: システムは、アクセル開度が20%未満の場合にのみドライブモード変更要求を受け付けること。
- C19-RQ-003: システムは、ドライブモード故障を検知した場合、100 ms以内にNORMALモードへ戻ること。

## 想定構成
- DriveModeSystem
- DriveModeController

## 主な信号・インタフェース
- acceleratorOpening (入力, AcceleratorPort, AcceleratorValue)
- driveModeRequest (入力, DriveModeRequestPort, DriveModeRequestValue)
- driveModeStatus (出力, DriveModeStatusPort, DriveModeStatusValue)

## カバレッジタグ
- category: state_machine
- difficulty: advanced
- completeness: high
