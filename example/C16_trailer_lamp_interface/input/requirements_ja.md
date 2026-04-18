# C16 トレーラランプインタフェース

## 背景
このケースは、トレーラコントローラとトレーラランプコネクタ間の型付き信号インタフェースに焦点を当てます。

## 要求
- C16-RQ-001: トレーラランプコントローラは、左方向指示、右方向指示、および制動灯の各指令をトレーラコネクタインタフェースへ出力すること。
- C16-RQ-002: システムは、コネクタ導通が失われた後500 ms以内にトレーラ切断を検知すること。
- C16-RQ-003: システムは、トレーラ未接続時にトレーラランプ指令を抑止すること。

## 構造ヒント
- TrailerLampSystem
- TrailerLampController
- TrailerConnector

## インタフェースヒント
- leftTurnLampCommand (出力, LeftTurnLampPort, LampCommandValue)
- rightTurnLampCommand (出力, RightTurnLampPort, LampCommandValue)
- stopLampCommand (出力, StopLampPort, LampCommandValue)
- trailerDetected (入力, TrailerPresencePort, TrailerPresenceValue)

## メタデータ
- category: interface_contract
- difficulty: intermediate
- completeness: high
