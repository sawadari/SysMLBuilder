# C06 空調デフロスト優先制御

## 背景
このケースは、前席デフロスト要求時にブロワ段、コンプレッサ状態、吹出口モードを協調制御する機能を表します。

## 要求
- C06-RQ-001: HVACシステムは、前席デフロストが要求された場合、500 ms以内にブロワ段を5以上に設定すること。
- C06-RQ-002: システムは、前席デフロストが有効な間、吹出口モードをウインドシールドモードに指令すること。
- C06-RQ-003: システムは、コンプレッサ保護が有効でない限り、前席デフロストが有効な間エアコンをONにすること。

## 構造ヒント
- ClimateDefogSystem
- HvacController
- BlowerActuator
- AirMixActuator
- CompressorRelay

## インタフェースヒント
- defogRequest (入力, DefogRequestPort, DefogRequestValue)
- blowerCommand (出力, BlowerCommandPort, BlowerCommandValue)
- outletModeCommand (出力, OutletModePort, OutletModeValue)
- acCommand (出力, AcCommandPort, AcCommandValue)

## メタデータ
- category: multi_action_response
- difficulty: intermediate
- completeness: high
