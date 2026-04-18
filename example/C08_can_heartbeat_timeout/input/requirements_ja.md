# C08 CANハートビートタイムアウト反応

## 背景
このケースは、ブレーキコントローラからのハートビート消失に対して、依存機能を停止し故障を記録する機能を表します。

## 機能要求
- C08-RQ-001: システムは、ブレーキコントローラのハートビートが100 ms欠落した場合、通信タイムアウト故障を設定すること。
- C08-RQ-002: システムは、通信タイムアウト故障設定後50 ms以内にクルーズコントロールを無効化すること。
- C08-RQ-003: システムは、100 ms以内に故障診断コードを保存し、故障状態メッセージを送信すること。

## 想定構成
- CommunicationMonitoringSystem
- HeartbeatMonitor
- CruiseControlGate
- DiagnosticManager

## 主な信号・インタフェース
- heartbeat (入力, HeartbeatPort, HeartbeatValue)
- cruiseEnable (出力, FunctionControlPort, FunctionControlValue)
- diagnosticStatus (出力, DiagnosticStatusPort, DiagnosticStatusValue)

## カバレッジタグ
- category: fault_reaction
- difficulty: advanced
- completeness: high
