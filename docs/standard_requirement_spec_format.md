# 標準要求仕様フォーマット

## 目的

この文書は、SysMLBuilder に入力する Markdown 要求仕様の標準フォーマットを定義するものです。

目標は次の 3 つです。

- 人がそのまま読める自然な要求仕様書にする
- 変換ルールは単純で再現可能にする
- 出力される SysML View を全ケースで揃える

## 基本方針

入力は 2 層に分けます。

- `requirements_*.md`
  人が書く要求仕様書
- `input/case.yaml`
  そのケースだけで使う補助ルール、package 名、要素名、追加 View 定義

Markdown には「何をしたいか」を書き、`case.yaml` には「どういう SysML 名へ写すか」を書きます。
大きな SysML 断片や巨大な YAML を Markdown へ埋め込むことは標準としません。

## 必須セクション

最低限、次のどちらかを含めます。

- `## Requirements`
- `## Use Cases`

加えて、文書の前半に状況説明を 1 つ置きます。

- `## Context`

日本語版では次を使います。

- `## 背景`
- `## 要求`
- `## ユースケース`

## 推奨セクション

必要に応じて、次のセクションを追加します。

- `## Goal`
- `## Structure Hints`
- `## Interface Hints`
- `## Metadata`
- `## Authoring Notes`

日本語版では次を使います。

- `## 目標`
- `## 構造ヒント`
- `## インタフェースヒント`
- `## メタデータ`
- `## 記述方針`

## 要求の書き方

要求行は、次のいずれかを標準として受け付けます。

```md
- CASE-ID: The system shall ...
- [CASE-ID] The system shall ...
1. [CASE-ID] The system shall ...
```

日本語でも識別子の書式は同じにし、本文だけを日本語にします。

```md
- CASE-ID: システムは...
- [CASE-ID] システムは...
1. [CASE-ID] システムは...
```

## 推奨テンプレート

```md
# Model Title

## Context
Describe the product, operating situation, and modeling intent in plain language.

## Goal
State what the generated SysML should help the reader confirm.

## Requirements
- REQ-001: The system shall ...
- REQ-002: The subsystem shall ...

## Structure Hints
- MainSystem
- SubsystemA
- SubsystemB

## Interface Hints
- signalName (input, SignalPort, SignalValue)

## Metadata
- category: example_category
- completeness: high

## Authoring Notes
- Keep the wording natural and reviewable.
```

## 標準 SysML View セット

canonical `.sysml` には、原則として次の View を含めます。

- `Requirements View`
- `Structural Context View`
- `Internal Structure View`
- `Behavior Activity View`
- `Behavior State View`

意味は次のとおりです。

- `Requirements View`
  requirement 系要素を確認する
- `Structural Context View`
  システム全体と主要 part 階層を確認する
- `Internal Structure View`
  part / port / interface / connector を確認する
- `Behavior Activity View`
  action と flow を確認する
- `Behavior State View`
  state machine や状態遷移を確認する

入力に十分な情報がない場合でも、この View セット自体は標準として出力します。
ただし、表示される要素の密度は入力の具体性に依存します。

## 設計上の割り切り

- SysML の完成度より、入力仕様書の分かりやすさを優先する
- 複雑な推論より、単純なルールベース変換を優先する
- 曖昧な内容は review overlay に残してよい
- View は標準化するが、表示要素の豊かさはケース差があってよい

## 参照先

- [初心者向け実行ガイド](user_input_to_sysml_flow.md)
- [内部設計](developer_design_rationale.md)
- [example 配置ルール](../example/README.md)
