# GfSE 参照モデルから学んだこと

## この文書の目的

この文書は、GfSE の公開 SysML v2 モデルを見ながらベンチマークを作った結果、SysMLBuilder の設計で何を強く意識するようになったかをまとめたものです。  
専門的な背景よりも、「どんな気づきがあり、何を変えたのか」を分かりやすく整理しています。

## 大きな学び

GfSE のモデルを確認して分かったのは、次の 4 点がとても大事だということです。

- 数値条件だけでなく、使う場面ごとの差も残すこと
- Interface や port を省略しないこと
- use case は普通の要求文と分けて扱うこと
- どのファイルを根拠にしたかを明確にすること

## 1. VehicleModel から学んだこと

見えてきたこと:

- requirement の定義と使用が分かれている
- `satisfy` の関係がはっきり書かれている
- interface や port が独立した要素として出てくる

SysMLBuilder への反映:

- 数値つき要求をしっかり扱うようにした
- interface 要求を主要パターンとして扱うようにした
- 要求と satisfy の対応を追いやすくした

## 2. MiningFrigateRequirementsDef から学んだこと

見えてきたこと:

- 同じ要求でも、場面によって閾値が変わる
- たとえば通常時と特定条件下で、別の値を持つことがある

SysMLBuilder への反映:

- 文脈ごとの条件を別々に持てるようにした
- 1 本の単純な数値に無理やりまとめない方針にした

## 3. standardPortsAndInterfaces から学んだこと

見えてきたこと:

- port には型があり、interface には端点や flow がある
- 接続の意味は、名前だけでなく型や flow で決まる

SysMLBuilder への反映:

- typed port を重視するようにした
- `interface_ends` や `flows` を中間データで持つようにした
- interface の定義まで含めて確認しやすくした

## 4. UseCasesFrigate から学んだこと

見えてきたこと:

- use case には actor、目的、Main Flow、Exception Flow がある
- これを普通の requirement に押し込むと情報が減る

SysMLBuilder への反映:

- use case を独立したパターンとして扱うようにした
- actor や flow を残せるようにした
- canonical と overlay の両方を使う中間的なケースを認めた

## 5. strict benchmark で分かったこと

見えてきたこと:

- あいまいな説明文だけでは、期待出力を厳密に決めにくい
- 厳密比較には、元になった `.sysml` ファイルが明確である方がよい

SysMLBuilder への反映:

- strict benchmark では、根拠が明確なケースを優先するようにした
- 参照元ファイルをたどれることを重視するようにした

## まとめ

GfSE のモデルから学んで、特に大切だと分かったのは次の 4 つです。

- 文脈
- typed interface
- use case の構造
- 根拠の追跡性

そのため、SysMLBuilder では「何を根拠に、どこまで確定したのか」を分けて扱う設計を強めています。
