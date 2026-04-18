# C04 ヘッドランプ自動消灯遅延

## 背景
このケースは、イグニッションOFF後のヘッドランプ遅延消灯と、手動操作によるタイマ解除を表します。

## 要求
- C04-RQ-001: システムは、イグニッションがOFFになり運転席ドアが閉じている場合、30 s後にヘッドランプを消灯すること。
- C04-RQ-002: システムは、ユーザーがヘッドランプを再度手動でONした場合、自動消灯タイマを解除すること。
- C04-RQ-003: システムは、運転席ドアが開いている間、ヘッドランプを点灯状態に維持すること。

## 構造ヒント
- HeadlampControlSystem
- HeadlampController
- HeadlampRelay

## インタフェースヒント
- ignitionOn (入力, IgnitionStatusPort, IgnitionStatusValue)
- driverDoorOpen (入力, DoorStatusPort, DoorStatusValue)
- lampCommand (出力, LampCommandPort, LampCommandValue)

## メタデータ
- category: timed_response
- difficulty: basic
- completeness: high
