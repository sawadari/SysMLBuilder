# C02 オートウインドウ挟み込み防止

## 背景
このケースは、挟み込み防止機能とドア開時の禁止条件を持つオートウインドウ機能を表します。

## 要求
- C02-RQ-001: オートウインドウシステムは、閉スイッチが300 ms以上押下された場合に自動閉動作を開始すること。
- C02-RQ-002: システムは、対応するドアが開いている間、自動閉動作を禁止すること。
- C02-RQ-003: システムは、自動閉動作中に挟み込みを検知した場合、30 ms以内に停止し、ガラスを少なくとも100 mm下降させること。

## 構造ヒント
- AutoWindowSystem
- WindowController
- WindowMotor
- PinchSensor

## インタフェースヒント
- closeRequest (入力, WindowSwitchPort, WindowSwitchValue)
- doorOpen (入力, DoorStatusPort, DoorStatusValue)
- pinchDetected (入力, PinchSignalPort, PinchSignalValue)
- windowCommand (出力, WindowMotorCommandPort, WindowMotorCommandValue)

## メタデータ
- category: fault_reaction
- difficulty: intermediate
- completeness: high
