# C15 チャイルドロックシフト連動

## 背景
このケースは、安全な車両条件下でのみチャイルドロック状態変更を許可する機能を表します。

## 機能要求
- C15-RQ-001: システムは、シフト位置がPかつ車速0 km/hの場合にのみチャイルドロック有効化を許可すること。
- C15-RQ-002: システムは、いずれかの後席ドアが開いている間、チャイルドロック有効化を拒否すること。
- C15-RQ-003: システムは、有効なチャイルドロック無効化要求を受信した場合、500 ms以内に無効化を完了すること。

## 想定構成
- ChildLockSystem
- ChildLockController
- RearDoorLockActuator

## 主な信号・インタフェース
- shiftPosition (入力, ShiftPositionPort, ShiftPositionValue)
- vehicleSpeed (入力, VehicleSpeedPort, VehicleSpeedValue)
- rearDoorOpen (入力, DoorStatusPort, DoorStatusValue)
- childLockCommand (出力, LockCommandPort, LockCommandValue)

## カバレッジタグ
- category: gated_capability
- difficulty: basic
- completeness: high
