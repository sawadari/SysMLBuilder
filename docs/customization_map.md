# どこを変えれば何が変わるか

| 変えたいもの | 主に触るファイル | 補足 |
|---|---|---|
| Requirement Contract の必須 slot | `profiles/requirement_contract.yaml` | context / actor / flow / IF slot を調整する |
| pattern の分け方 | `profiles/requirement_patterns.yaml` | detect / required_slots / projectors を変える |
| use case を canonical に出すか | `profiles/projection_profiles.yaml` | `use_cases` projector を調整する |
| strict benchmark の採点対象 | `profiles/gfse_reference_benchmark_profile.yaml` | strict case 一覧と trace quality policy を変える |
| 充足性レベルの意味 | `profiles/satisfiability_model.yaml` | high / medium / low の期待 artifact を変える |
| strict lint の厳しさ | `profiles/benchmark_lints.yaml` と `profiles/model_lints.yaml` | fail-fast 条件を変える |
| GfSE 由来の example retrieval | `profiles/example_retrieval.yaml` | 参照例のランキングや優先度を変える |
| 採点基準 | `testdata/gfse_derived/scoring_rubric.yaml` | case ごとの重みを変える |
| validator の具体的な検査 | `scripts/validate_pack.py` | regex / schema / file existence の検査を追加する |

## 開発優先順位
1. `requirement_patterns.yaml`
2. `projection_profiles.yaml`
3. `requirement_contract.yaml`
4. `scoring_rubric.yaml`
5. `benchmark_lints.yaml`
6. `scripts/validate_pack.py`

## よくある誤り
- use case narrative を全部 requirement へ潰す
- context 別 threshold を 1 本に潰す
- typed port を省略する
- low case でも canonical を無理に出す
- direct trace が弱いケースを strict 採点へ入れる
