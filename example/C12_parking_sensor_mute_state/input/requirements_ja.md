# C12 パーキングセンサミュート状態

## 背景
このケースは、パーキングセンサ音声警報のミュート/ミュート解除切替と電源再投入時リセットを表します。

## 機能要求
- C12-RQ-001: システムは、有効なミュートボタン押下ごとに、パーキングセンサ音声警報状態をMUTEDとUNMUTEDの間で切り替えること。
- C12-RQ-002: システムは、電源サイクルごとに音声警報状態をUNMUTEDへリセットすること。
- C12-RQ-003: システムは、音声警報がミュート中でも視覚警報を維持すること。

## 想定構成
- ParkingSensorAlertSystem
- ParkingSensorController
- AudioBuzzer
- VisualDisplay

## 主な信号・インタフェース
- muteButtonPressed (入力, MuteButtonPort, MuteButtonValue)
- audioAlertCommand (出力, AudioAlertPort, AudioAlertValue)
- visualAlertCommand (出力, VisualAlertPort, VisualAlertValue)

## カバレッジタグ
- category: stateful_toggle
- difficulty: basic
- completeness: high
