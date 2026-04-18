# C07 低電圧警告

## 背景
このケースは、バッテリ電圧を監視し、デバウンス後に警告表示とメッセージ送信を行う機能を表します。

## 要求
- C07-RQ-001: システムは、バッテリ電圧が11.5 V未満の状態が5 s継続した場合、低電圧警告灯を点灯すること。
- C07-RQ-002: システムは、警告灯点灯後100 ms以内に車載ネットワークへ低電圧状態メッセージを送信すること。
- C07-RQ-003: システムは、バッテリ電圧が12.1 Vを超える状態が10 s継続した場合、警告を解除すること。

## 構造ヒント
- BatteryWarningSystem
- BatteryMonitor
- WarningLamp
- NetworkPublisher

## インタフェースヒント
- batteryVoltage (入力, VoltageInputPort, VoltageValue)
- lampCommand (出力, LampCommandPort, LampCommandValue)
- statusMessage (出力, NetworkStatusPort, NetworkStatusValue)

## メタデータ
- category: threshold_monitoring
- difficulty: intermediate
- completeness: high
