# C11 車線逸脱警報

## 背景
このケースは、有効条件下で車線逸脱が発生したときに可聴警報を出す機能を表します。

## 機能要求
- C11-RQ-001: システムは、車速60 km/h以上かつ方向指示器OFFの状態で車線逸脱を検知した場合、150 ms以内に可聴警報を生成すること。
- C11-RQ-002: システムは、方向指示器が有効な間、警報を抑止すること。
- C11-RQ-003: システムは、車線逸脱条件が解消された後300 ms以内に可聴警報を停止すること。

## 想定構成
- LaneDepartureWarningSystem
- LaneMonitor
- Buzzer

## 主な信号・インタフェース
- vehicleSpeed (入力, VehicleSpeedPort, VehicleSpeedValue)
- turnSignalActive (入力, TurnSignalPort, TurnSignalValue)
- laneDepartureDetected (入力, LaneDeparturePort, LaneDepartureValue)
- buzzerCommand (出力, BuzzerCommandPort, BuzzerCommandValue)

## カバレッジタグ
- category: multi_condition_alert
- difficulty: intermediate
- completeness: high
