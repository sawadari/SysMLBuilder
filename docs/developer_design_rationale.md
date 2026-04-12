# 開発者向け設計意図

## この文書の目的
この文書は、**なぜこの変換設計にしたか**を開発者へ短時間で伝えるための説明書です。
今回の版は、以前の改善版をさらに見直し、**GfSE の公開 SysML v2 モデルを使って厳密な expected output を持つ benchmark** を作る過程で更新した設計です。

---

## まず結論
この版の中核は次の 6 点です。

1. **中間表現の主役を Requirement Contract に固定した**
2. **要求パターンと projector を別設定にした**
3. **canonical model と review overlay を分離した**
4. **strict benchmark の採点対象を direct_file_grounded ケースだけに限定した**
5. **operational use case を pattern と projector の両方で第一級にした**
6. **contextual thresholds / typed interface / main-exception flow を first-class slot にした**

---

## なぜ汎用 KG を主役にしないのか
### 採用した設計
中間表現の主役を **Requirement Contract** にしました。
KG は provenance と cross-reference の補助にだけ残します。

### 理由
要求変換では、汎用 triple よりも次の情報が重要です。

- subject は誰か
- 条件は何か
- 閾値はいくつか
- 単位は何か
- どこが不足情報か
- どこまでが根拠でどこからが仮案か

汎用 KG を主役にすると、これらを後段で復元する必要があり、精度が落ちます。
GfSE の `VehicleModel.sysml` や `MiningFrigateRequirementsDef.sysml` を見ると、`requirement def` は subject と属性と constraint を持っています。
したがって、中間表現もその形へ寄せた方が安定します。

---

## なぜ要求パターンを別設定にしたのか
### 採用した設計
`profiles/requirement_patterns.yaml` で、要求の分け方を外出ししました。

### 理由
利用者が最も変えたいのは、**同じ要求文をどの artifact へ落とすか**です。
例えば、

- 定量性能なら requirement usage を出したい
- IF 文なら port / interface を出したい
- use case narrative なら use case def と overlay を両方出したい

この差をコード本体で持つと壊れます。
だから pattern と projector を分けています。

---

## なぜ canonical model と review overlay を分けたのか
### 採用した設計
正式モデルは `*_expected_canonical.sysml`、
不足や仮案は `*_expected_review_overlay.sysml` に分けています。

### 理由
LLM 仮案を正式モデルへ混ぜると、
**原文根拠と仮説の境界が消えます。**
strict benchmark を作るとき、この混在は採点不能の原因になります。
したがって、正式モデルと review 用モデルは必ず分けます。

---

## なぜ strict benchmark の採点対象を direct_file_grounded ケースだけにしたのか
### 採用した設計
今回の strict benchmark は、
**GitHub 上で直接確認できた GfSE の `.sysml` ファイルから推測できるケースだけ**を採点対象にしています。

### 理由
以前は README 抽象説明に基づくケースも含めていました。
しかし、それでは expected `.sysml` を厳密に固定できません。
厳密な採点には、

- 参照元がどの `.sysml` か
- どの構文・要素を根拠にしたか
- どこまでが直接観察でどこからが推測か

を明確に分ける必要があります。
そのため、今回の strict suite では abstract-only ケースを外しました。

### 効果
- 採点基準を明確にできる
- expected output を強く固定できる
- 「参考用の抽象ケース」と「厳密比較ケース」を分離できる

---

## なぜ operational use case を第一級にしたのか
### 採用した設計
`operational_use_case_objective` pattern と `use_cases` projector を追加しました。

### 理由
GfSE の `UseCasesFrigate.sysml` では、
`use case def` に `subject`、`actor`、`objective` があり、
objective 内に Main Flow / Exception Flows が保持されています。
この構造は、通常の shall 文 requirement と別です。

従来の requirement projector だけでは、
運用目的を単一 requirement へ潰してしまい、
actors や flow が失われます。
そのため use case を第一級にしました。

---

## なぜ contextual thresholds / typed interface / main-exception flow を first-class slot にしたのか
### 採用した設計
Requirement Contract に次の slot を追加しました。

- `contextual_thresholds`
- `operating_contexts`
- `interface_ends`
- `flows`
- `actors`
- `main_flow_steps`
- `exception_flow_steps`

### 理由
GfSE の参照モデルを見ると、次の差が大きかったためです。

- `MiningFrigateRequirementsDef.sysml` は文脈別の閾値を持つ
- `standardPortsAndInterfaces.sysml` は型付き port と flow を持つ
- `UseCasesFrigate.sysml` は main / exception flow を持つ

この差を generic slot で吸収すると、採点しづらくなります。
そのため、明示的な slot にしました。

---

## なぜ behavior は既定で candidate only なのか
### 採用した設計
behavior は review overlay へ候補として出し、canonical へは自動確定しません。

### 理由
構造や IF より、behavior の誤りの方が破壊力が大きいからです。
特に use case narrative から state / transition を起こすときは、guards や timing の不足が多いです。
よって、strict benchmark でも behavior は控えめに扱います。

---

## 実装者への指示
変更優先順位は次です。

1. `requirement_patterns.yaml`
2. `projection_profiles.yaml`
3. `requirement_contract.yaml`
4. `benchmark_lints.yaml`
5. `scripts/validate_pack.py`

コード本体より先に profile を直してください。
