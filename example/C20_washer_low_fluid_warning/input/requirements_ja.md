# C20 ウォッシャ液残量低下警告

## 背景
このケースは、ウォッシャ液残量低下をデバウンス付きで検知し、補充後に警告を解除する機能を表します。

## 要求
- C20-RQ-001: システムは、ウォッシャ液残量低下が2 s継続した場合、500 ms以内に残量低下警告を表示すること。
- C20-RQ-002: システムは、2 s未満の一時的な低レベル検知に対して警告を表示しないこと。
- C20-RQ-003: システムは、液量が正常状態で5 s継続した場合、警告を解除すること。

## 構造ヒント
- WasherFluidWarningSystem
- FluidLevelMonitor
- ClusterDisplay

## インタフェースヒント
- fluidLow (入力, FluidLevelPort, FluidLevelValue)
- displayCommand (出力, DisplayCommandPort, DisplayCommandValue)

## メタデータ
- category: threshold_monitoring
- difficulty: basic
- completeness: high
