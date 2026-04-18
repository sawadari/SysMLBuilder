# 自動バックドア制御 要求仕様書（完全版サンプル）

この入力は、元の Markdown が残っていなかったため、`auto_backdoor_requirement_contracts.yaml` の evidence から再構成した参考入力です。

## Requirements

- ABD-REQ-001: ShiftPos が P であり、VehSpd が 3 km/h 未満の場合にのみ、BackDoorOpenReq を開要求として受け付けなければならない。
- ABD-REQ-003: 開要求を受け付けた場合、100 ms 以内に駆動モータへ開方向駆動を指示しなければならない。
- ABD-REQ-004: BackDoorPos が 95 % 以上となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。
- ABD-REQ-007: 閉動作中に PinchDetected = true を検知した場合、50 ms 以内に閉方向駆動を停止し、200 ms 以内に開方向へ反転しなければならない。
- ABD-REQ-009: 異常停止状態へ遷移した場合、1 s 以内に BuzzerReq を true にしなければならない。
- ABD-REQ-010: 開度センサ値が 500 ms 以上更新されない場合、異常停止状態へ遷移しなければならない。
- ABD-REQ-012: 全閉状態で開要求を受け付けた場合、開動作中へ遷移しなければならない。
- ABD-REQ-015: 閉動作中で挟み込み検知した場合、反転開へ遷移しなければならない。
- ABD-VER-001: ShiftPos=P, VehSpd=0 km/h, BackDoorOpenReq=true のとき、100 ms 以内に開方向駆動が開始されることを確認する。
