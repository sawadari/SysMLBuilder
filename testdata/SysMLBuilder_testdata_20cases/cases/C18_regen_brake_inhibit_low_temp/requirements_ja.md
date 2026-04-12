# C18 低温時回生制動抑制

## 背景
このケースは、バッテリ温度に応じて回生制動制限を切り替える機能を表します。

## 機能要求
- C18-RQ-001: システムは、バッテリ温度が-10℃未満の場合、HIGH回生制動レベルを禁止すること。
- C18-RQ-002: システムは、バッテリ温度が-20℃未満の場合、すべての回生制動レベルを禁止すること。
- C18-RQ-003: システムは、バッテリ温度が-8℃を超えた後にのみHIGH回生制動レベルを再許可すること。

## 想定構成
- RegenBrakeSystem
- RegenBrakeController
- BatteryTemperatureMonitor

## 主な信号・インタフェース
- batteryTemperature (入力, BatteryTemperaturePort, TemperatureValue)
- regenLevelCommand (出力, RegenLevelPort, RegenLevelValue)

## カバレッジタグ
- category: contextual_threshold
- difficulty: advanced
- completeness: high
