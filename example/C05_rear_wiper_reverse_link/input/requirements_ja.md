# C05 後ワイパリバース連動

## 背景
このケースは、前ワイパ動作中にリバースへ入れたとき、後ワイパを1回作動させる機能を表します。

## 要求
- C05-RQ-001: システムは、前ワイパ動作中にリバースギヤへ入った場合、1 s以内に後ワイパ1回作動を指令すること。
- C05-RQ-002: システムは、10 s以内にリバース連動後ワイパ1回作動を複数回発行しないこと。
- C05-RQ-003: システムは、後ワイパサービスモードが有効な間、リバース連動作動を禁止すること。

## 構造ヒント
- RearWiperLinkSystem
- RearWiperController
- RearWiperMotor

## インタフェースヒント
- frontWiperActive (入力, WiperStatusPort, WiperStatusValue)
- shiftPosition (入力, ShiftPositionPort, ShiftPositionValue)
- rearWiperCommand (出力, WiperCommandPort, WiperCommandValue)

## メタデータ
- category: contextual_trigger
- difficulty: basic
- completeness: high
