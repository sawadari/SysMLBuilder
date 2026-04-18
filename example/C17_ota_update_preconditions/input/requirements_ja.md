# C17 OTA更新事前条件

## 背景
このケースは、OTAソフトウェア更新中の開始条件と中断条件を表します。

## 要求
- C17-RQ-001: OTA更新システムは、車両が駐車状態でドアが施錠され、かつバッテリ残量が40%以上の場合にのみ更新を開始すること。
- C17-RQ-002: システムは、更新中にイグニッションがONになった場合、1 s以内に更新を中断すること。
- C17-RQ-003: システムは、更新中にいずれかのドアが解錠された場合、1 s以内に更新を中断すること。

## 構造ヒント
- OtaUpdateSystem
- UpdateManager
- VehicleConditionMonitor

## インタフェースヒント
- vehicleParked (入力, VehicleParkPort, VehicleParkValue)
- doorsLocked (入力, DoorLockStatusPort, DoorLockStatusValue)
- batterySoc (入力, BatterySocPort, BatterySocValue)
- updateControl (出力, UpdateControlPort, UpdateControlValue)

## メタデータ
- category: multi_precondition
- difficulty: advanced
- completeness: high
