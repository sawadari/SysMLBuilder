# C13 充電フラップロック制御

## 背景
このケースは、走行状態と充電状態に応じて充電フラップを施錠・解錠する機能を表します。

## 機能要求
- C13-RQ-001: システムは、車両走行中に充電フラップを施錠すること。
- C13-RQ-002: システムは、充電中に充電フラップを施錠すること。
- C13-RQ-003: システムは、車両が駐車状態で充電完了時、または有効なユーザー解錠要求を受信した場合、充電フラップを解錠すること。

## 想定構成
- ChargeFlapLockSystem
- ChargeFlapController
- ChargeFlapActuator

## 主な信号・インタフェース
- vehicleMoving (入力, VehicleMotionPort, VehicleMotionValue)
- chargingActive (入力, ChargingStatusPort, ChargingStatusValue)
- lockCommand (出力, LockCommandPort, LockCommandValue)

## カバレッジタグ
- category: contextual_locking
- difficulty: intermediate
- completeness: high
