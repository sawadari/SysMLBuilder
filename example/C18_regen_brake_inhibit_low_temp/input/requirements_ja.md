# C18 低温時回生制動抑制

## 背景
このケースは、バッテリ温度に応じて回生制動制限を切り替える機能を表します。

## 要求
- C18-RQ-001: システムは、バッテリ温度が-10℃未満の場合、HIGH回生制動レベルを禁止すること。
- C18-RQ-002: システムは、バッテリ温度が-20℃未満の場合、すべての回生制動レベルを禁止すること。
- C18-RQ-003: システムは、バッテリ温度が-8℃を超えた後にのみHIGH回生制動レベルを再許可すること。

## 構造ヒント
- RegenBrakeSystem
- RegenBrakeController
- BatteryTemperatureMonitor

## インタフェースヒント
- batteryTemperature (入力, BatteryTemperaturePort, TemperatureValue)
- regenLevelCommand (出力, RegenLevelPort, RegenLevelValue)

## メタデータ
- category: contextual_threshold
- difficulty: advanced
- completeness: high
