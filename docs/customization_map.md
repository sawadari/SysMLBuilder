# 設定変更の早見表

## この文書の使い方

「何を変えたいときに、どのファイルを見ればよいか」をすぐ分かるようにした一覧です。  
細かい実装に入る前の入口として使ってください。

## まず見る表

| 変えたいこと | 主に触るファイル | ひとことで言うと |
|---|---|---|
| Requirement Contract の項目を増やしたい | `profiles/requirement_contract.yaml` | 中間データの形を決める |
| 要求の分類方法を変えたい | `profiles/requirement_patterns.yaml` | どの要求を何として読むかを決める |
| canonical と overlay の出し分けを変えたい | `profiles/projection_profiles.yaml` | どの出力へ送るかを決める |
| strict benchmark の対象を変えたい | `profiles/gfse_reference_benchmark_profile.yaml` | 厳密比較するケースを決める |
| high / medium / low の考え方を変えたい | `profiles/satisfiability_model.yaml` | 期待する成果物のレベルを決める |
| lint の厳しさを変えたい | `profiles/benchmark_lints.yaml` と `profiles/model_lints.yaml` | エラー判定の条件を決める |
| 参考例の出し方を変えたい | `profiles/example_retrieval.yaml` | 参照例の優先度を決める |
| 採点基準を変えたい | `example/scoring_rubric.yaml` | 何を重く評価するかを決める |
| 検証スクリプトを変えたい | `scripts/validate_pack.py` | 実際のチェック内容を変える |

## よくある変更パターン

### 新しい要求タイプを追加したい

主に見るファイル:

- `profiles/requirement_patterns.yaml`
- `profiles/requirement_contract.yaml`
- `profiles/projection_profiles.yaml`

考える順番:

1. その要求をどう見分けるか
2. 中間データに何を持たせるか
3. canonical に出すか overlay に出すか

### use case の扱いを変えたい

主に見るファイル:

- `profiles/requirement_patterns.yaml`
- `profiles/projection_profiles.yaml`

確認したい点:

- use case として扱う条件
- actor や flow をどこまで残すか
- canonical にどこまで入れるか

### 厳密比較をもっと厳しくしたい

主に見るファイル:

- `profiles/benchmark_lints.yaml`
- `profiles/model_lints.yaml`
- `example/scoring_rubric.yaml`

## 迷ったときの優先順

何から触るか迷ったら、次の順で確認すると分かりやすいです。

1. `profiles/requirement_patterns.yaml`
2. `profiles/projection_profiles.yaml`
3. `profiles/requirement_contract.yaml`
4. `example/scoring_rubric.yaml`
5. `profiles/benchmark_lints.yaml`
6. `scripts/validate_pack.py`

## よくあるミス

- 項目を追加したのに、要求分類側でその項目を使っていない
- canonical に出したいのに、出力方針では overlay のままになっている
- lint だけ厳しくして、期待出力や採点基準を見直していない
- use case を普通の requirement と同じように扱って情報を落としてしまう

## 関連文書

- 設計意図:
  [developer_design_rationale.md](docs/developer_design_rationale.md)
- 利用ガイド:
  [user_input_to_sysml_flow.md](docs/user_input_to_sysml_flow.md)
