# C01 パワーバックドア開条件

## 背景
このケースは、開動作前に車両条件を確認し、閉動作中の障害物にも反応するパワーバックドアを表します。

## 機能要求
- C01-RQ-001: パワーバックドアシステムは、車速が3 km/h未満かつシフト位置がPの場合にのみ開要求を受け付けること。
- C01-RQ-002: システムは、有効な閉要求の後、200 ms以内に閉動作を開始すること。
- C01-RQ-003: システムは、閉動作中に障害物を検知した場合、50 ms以内に停止し、少なくとも200 msは反転動作すること。

## 想定構成
- PowerTailgateSystem
- TailgateController
- TailgateActuator
- ObstacleSensor

## 主な信号・インタフェース
- vehicleSpeed (入力, VehicleSpeedPort, VehicleSpeedValue)
- shiftPosition (入力, ShiftPositionPort, ShiftPositionValue)
- tailgateCommand (出力, TailgateCommandPort, TailgateCommandValue)
- obstacleDetected (入力, ObstacleSignalPort, ObstacleSignalValue)

## カバレッジタグ
- category: timed_response
- difficulty: intermediate
- completeness: high
