# C09 シートヒータ自動オフ

## 背景
このケースは、時間経過に応じて段下げとOFFを行うシートヒータを表します。

## 要求
- C09-RQ-001: シートヒータは、ユーザー起動直後にHIGHレベルを許可すること。
- C09-RQ-002: システムは、HIGHレベル連続動作が30 min継続した場合、HIGHからMEDIUMへ変更すること。
- C09-RQ-003: システムは、加熱動作が合計60 min継続した場合、シートヒータをOFFにすること。

## 構造ヒント
- SeatHeaterSystem
- SeatHeaterController
- SeatHeaterElement

## インタフェースヒント
- heaterRequest (入力, HeatingRequestPort, HeatingRequestValue)
- heatingLevelCommand (出力, HeatingLevelPort, HeatingLevelValue)

## メタデータ
- category: timed_state_change
- difficulty: basic
- completeness: high
