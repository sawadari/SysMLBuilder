# C03 ドアロック車速連動

## 背景
このケースは、車速、シフト位置、ドア状態に基づく自動ロック・自動アンロックを表します。

## 要求
- C03-RQ-001: ドアロックシステムは、車速が20 km/h以上の状態が3 s継続した場合、全ドアを施錠すること。
- C03-RQ-002: システムは、いずれかのドアが半ドアの間、自動施錠を実行しないこと。
- C03-RQ-003: システムは、イグニッションがOFFでシフト位置がPに変化した場合、500 ms以内に運転席ドアを解錠すること。

## 構造ヒント
- DoorLockSystem
- DoorLockController
- DoorLockActuator

## インタフェースヒント
- vehicleSpeed (入力, VehicleSpeedPort, VehicleSpeedValue)
- doorAjar (入力, DoorStatusPort, DoorStatusValue)
- shiftPosition (入力, ShiftPositionPort, ShiftPositionValue)
- lockCommand (出力, DoorLockCommandPort, DoorLockCommandValue)

## メタデータ
- category: timed_gated_capability
- difficulty: basic
- completeness: high
