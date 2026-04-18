# Don't Panic バットモービル公開サンプル

## 背景
この Markdown 文書は、「Don't Panic - The Absolute Beginners Guide to SysML v2」に掲載されている公開 SysML v2 バットモービルサンプルを逆起こしした要求仕様書です。
このケースの目的は元のモデルを単純化することではなく、同じ公開 `.sysml` サンプルテキストを再生成できる決定的な Markdown 入力を用意することです。

## ソース対応
- 書籍サンプル package: `Dont_Panic_Batmobile`
- 公開モデルのテーマ: structural modeling, behavioral modeling, use cases modelling, requirements modelling

## 要求
- REQ-BAT-001: Vehicle、Wheel、BatmobileEngine、PowerInterface、PowerIP、Power、EngineCommand を含む中核的な車両ドメインを定義すること。
- REQ-BAT-002: seat、body、wheel、battery、engine、および `bat2eng` power interface 接続を含む Batmobile システムを定義すること。
- REQ-BAT-003: BatmobileNG、EngineChoices、WheelChoices、BatmobileConfigurations、XBatmobile を含む特殊化要素とバリアビリティ要素を定義すること。
- REQ-BAT-004: Batman および Hero 関連の item と、走行および充電 timeslice を持つ `bm1` system occurrence を定義すること。
- REQ-BAT-005: `Drive Batmobile`、`Activate rocket booster`、`ActivateRocketBooster` を含む運用振る舞いを定義すること。
- REQ-BAT-006: VehicleMaxSpeed requirement、batmobileSpecification requirements package、および `batmobileDesignV23` 上の satisfy 関係を定義すること。
- REQ-BAT-007: concern、viewpoint、tabular view、および非標準ライブラリ要素にフィルタされた `batmobileParts` exposed view を定義すること。
- REQ-BAT-008: `definition and usage`、`subclassification`、`subsetting`、`redefinition`、`structural Modeling`、`default value`、`timeslice modelling`、`behavioral modelling`、`use cases modelling`、`requirements modelling`、および最上位 `index` を含む汎用 symbolic view を定義すること。
