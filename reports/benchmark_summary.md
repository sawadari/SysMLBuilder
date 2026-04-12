# GfSE strict benchmark 要約

## strict cases
- case01_vehicle_explicit_high
- case02_vehicle_ambiguous_low
- case03_mining_contextual_performance_high
- case04_mining_modular_interface_high
- case05_mining_usecase_medium
- case06_mining_usecase_ambiguous_low

## この版の設計更新
- strict scoring を direct_file_grounded ケースのみに限定
- use case projector を追加
- context 別 threshold を first-class slot 化
- typed IF を benchmark の主要採点軸へ昇格
- medium case で canonical + overlay の二系統期待を明示

## ケース構成
- high: 3 ケース
- medium: 1 ケース
- low: 2 ケース

## 期待する使い方
1. Markdown から Requirement Contract を作る
2. expected contracts と比較する
3. expected `.sysml` と比較する
4. scoring rubric で採点する
5. lint fail-fast に引っかからないか確認する
