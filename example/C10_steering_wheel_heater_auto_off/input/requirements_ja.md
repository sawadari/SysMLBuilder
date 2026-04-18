# C10 ステアリングヒータ自動オフ

## 背景
このケースは、周囲温度条件と自動タイムアウトを組み合わせたステアリングヒータを表します。

## 機能要求
- C10-RQ-001: システムは、外気温が20℃を超える場合、ステアリングヒータ要求を拒否すること。
- C10-RQ-002: システムは、加熱が30 min連続した後、ステアリングヒータをOFFにすること。
- C10-RQ-003: システムは、イグニッションサイクルごとにヒータ状態をOFFへ戻すこと。

## 想定構成
- SteeringWheelHeaterSystem
- SteeringWheelHeaterController
- SteeringWheelHeaterElement

## 主な信号・インタフェース
- ambientTemperature (入力, AmbientTemperaturePort, TemperatureValue)
- heaterRequest (入力, HeatingRequestPort, HeatingRequestValue)
- heatingLevelCommand (出力, HeatingLevelPort, HeatingLevelValue)

## カバレッジタグ
- category: contextual_threshold
- difficulty: basic
- completeness: high
