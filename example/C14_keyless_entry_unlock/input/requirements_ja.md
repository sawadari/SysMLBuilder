# C14 キーレスエントリ解錠

## 背景
このケースは、有効キー検知、解錠タイミング、および無効試行連続時のロックアウトを表します。

## 要求
- C14-RQ-001: システムは、有効キーが1 m以内にあり運転席ドアハンドルがタッチされた場合、300 ms以内に運転席ドアを解錠すること。
- C14-RQ-002: システムは、無効キーからの解錠要求を拒否すること。
- C14-RQ-003: システムは、60 s以内に無効キー試行が5回発生した場合、その後5 min間キーレス解錠処理を禁止すること。

## 構造ヒント
- KeylessEntrySystem
- AccessController
- RfReceiver
- DoorLockActuator

## インタフェースヒント
- validKeyPresent (入力, KeyPresencePort, KeyPresenceValue)
- handleTouched (入力, HandleTouchPort, HandleTouchValue)
- doorUnlockCommand (出力, DoorLockCommandPort, DoorLockCommandValue)

## メタデータ
- category: timed_secure_access
- difficulty: advanced
- completeness: high
