# 自動バックドア制御 要求仕様書（不足情報ありサンプル）

この入力は、元の Markdown が残っていなかったため、`auto_backdoor_requirement_contracts_incomplete.yaml` の evidence から再構成した参考入力です。

## Requirements

- ABD-REQ-101: ShiftPos が P であり、車両が低速時のみ、BackDoorOpenReq を開要求として受け付けなければならない。
- ABD-REQ-103: 開要求を受け付けた場合、所定時間以内に駆動モータへ開方向駆動を指示しなければならない。
- ABD-REQ-104: バックドアがほぼ全開となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。
- ABD-REQ-105: 短時間で閉方向駆動を停止し、その後に開方向へ反転しなければならない。
- ABD-REQ-106: センサ異常を検知した場合、異常停止状態へ遷移しなければならない。
