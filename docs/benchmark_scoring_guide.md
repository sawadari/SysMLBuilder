# GfSE strict benchmark 採点ガイド

## この文書の目的
この文書は、`testdata/gfse_derived/` にあるケースをどう採点するかを説明するものです。

## 採点の原則
### 1. strict benchmark は direct_file_grounded のみ
厳密採点の対象は、参照元 `.sysml` ファイルを直接確認して作成したケースだけです。

### 2. case ごとに採点軸を変える
Vehicle の定量 requirement と、UseCase の narrative では、成功条件が違います。
そのため、1本の万能 rubric ではなく、case ごとに重みを持ちます。

### 3. canonical と overlay は別採点
- canonical は **正式モデルとしての整合**
- overlay は **不足の見つけ方と仮案の透明性**

を見ます。

## 主要な採点観点
- Requirement Contract の slot 充足
- pattern 分類の正しさ
- requirement usage への parameterization
- typed port / interface def / flow の保持
- satisfy / allocation / view target の分離
- use case actor / objective / main-exception flow の保持
- missing slot / open question / llm proposal の overlay 分離
- provenance と traceability

## 充足性レベルごとの期待
### high
- canonical model を主成果物にする
- overlay は不要か最小
- threshold や IF は具体的に出るべき

### medium
- canonical と overlay の両方を許可
- narrative の保持と gap 可視化の両立が必要

### low
- canonical を無理に作らない
- overlay 側で missing slot と review action を明示する

## 採点の使い方
1. `case_manifest.yaml` で case の期待 artifact を確認する
2. `scoring_rubric.yaml` で case ごとの重みを読む
3. expected contracts / expected `.sysml` と比較する
4. strict lint を満たしているかを見る
5. 総合点と fail-fast 条件を判定する

## fail-fast 条件
次のいずれかが起きたら、その case は自動 fail にする方がよいです。

- canonical に draft / missing slot が混入している
- requirement def に subject がない
- untyped port がある
- use case def に subject または objective がない
- low case なのに overlay を出さずに canonical へ確定している
- source trace が direct_file_grounded でないのに strict 採点へ入っている
