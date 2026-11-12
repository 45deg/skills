# Skills

AIエージェント向けのスキル集です。コードの可読性・テスト・形式検証、UI/カラー設計、日本語文章の推敲を扱います。

[日本語](#日本語) | [English](#english)

## 日本語

### スキル一覧

| スキル | 分野 | 概要 | スキル言語 |
| --- | --- | --- | --- |
| [`human-readable-code`](#human-readable-code) | コード実装 | 可読性の高いコード設計・実装・レビュー | 英語 |
| [`human-readable-code-ja`](#human-readable-code-ja) | コード実装 | コード構造・日本語コメント・冒頭要約マップの設計 | 日本語 |
| [`write-quality-tests`](#write-quality-tests) | テスト | 仕様とリスクに基づくテスト設計・実装・レビュー | 英語 |
| [`verify-with-dafny`](#verify-with-dafny) | 形式検証 | Dafnyを用いたアルゴリズム・状態更新の検証 | 英語 |
| [`verify-with-quint`](#verify-with-quint) | 形式検証 | Quintを用いた既存コード・状態遷移のモデル検証 | 英語 |
| [`design-clear-ui`](#design-clear-ui) | UI設計 | 認知負荷（記憶・探索・判断）を減らすUIの設計・改善 | 英語 |
| [`dads-foundations-core`](#dads-foundations-core) | UI設計 | デジタル庁デザインシステム（DADS）基盤の適用・監査 | 英語 |
| [`ud-color-design`](#ud-color-design) | カラー設計 | カラーユニバーサルデザイン（CUD）配色と視認性チェック | 英語 |
| [`naturalize-japanese-prose`](#naturalize-japanese-prose) | 日本語文章 | 意味や主張の強さを保ったままAI由来の日本語を自然化 | 日本語 |

### インストール

リポジトリに含まれるスキルの一覧を表示します。

```bash
npx skills add 45deg/skills --list
```

特定のスキルをインストールする場合は、各スキルに記載の `--skill <スキル名>` コマンドを実行してください。

```bash
npx skills add 45deg/skills --skill <スキル名>
```

### スキル

#### コード・テスト・形式検証

##### `human-readable-code`

新規実装、機能追加、リファクタリング、レビューで、言語を問わず人が意図を追いやすいコードを書く・改善するためのスキルです。命名、データ表現、制御フロー、インターフェース、状態、失敗の設計に加え、目的や前提を示すコメント、ASCII図表、`index.*` を含むファイル冒頭の要約マップの書き方を扱います。

```bash
npx skills add 45deg/skills --skill human-readable-code
```

- [SKILL.md](skills/human-readable-code/SKILL.md): 判断基準と設計原則
- [具体例](skills/human-readable-code/references/howto.md): 実装時の選択肢とトレードオフ
- [レビュー・リファクタリング](skills/human-readable-code/references/review-and-refactoring.md): 動作を保つための確認点
- [出典](skills/human-readable-code/references/sources.md): 参考資料と適用範囲

##### `human-readable-code-ja`

コードの構造、日本語コメント、ファイル冒頭の要約マップを一体で設計する独立したスキルです（他スキルを追加せず単体で使用可能）。実装、リファクタリング、レビューにおいて、命名、データ表現、制御フロー、契約、状態、失敗を扱い、仕様と実装を根拠にした日本語の説明を最初から書きます。ファイル冒頭の要約マップには役割と主な処理を示し、`index.*` などの入口では公開内容と実装先も案内します。

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

- [SKILL.md](skills/human-readable-code-ja/SKILL.md): 設計・実装・レビューの手順
- [日本語コメント](skills/human-readable-code-ja/references/japanese-comments.md): 日本語コメントと要約マップの書き方
- [具体例](skills/human-readable-code-ja/references/examples.md): 実装例
- [レビュー・リファクタリング](skills/human-readable-code-ja/references/review-and-refactoring.md): 改善時の確認点
- [出典](skills/human-readable-code-ja/references/sources.md): 参考資料

##### `write-quality-tests`

仕様とリスクに基づくテストの設計・実装と、生成されたテストのレビューを支援するスキルです。期待値の根拠、境界条件、認可、途中失敗後の復旧、欠陥を検出できるかの確認を扱います。フロントエンド、バックエンド、DB、API契約、E2E、セキュリティ、性能・信頼性、データパイプラインの8つのサブスキルと、一次資料38件の出典一覧・調査整理を同梱しています。

```bash
npx skills add 45deg/skills --skill write-quality-tests
```

> [!NOTE]
> サブスキルと共有資料を含むディレクトリ全体を使用してください。テストの設計とレビューの判断を支援するガイドであり、引用した研究はそれぞれの手法やツールを評価したものです。本スキルの使用によって欠陥検出率が向上することを保証するものではありません。

- [SKILL.md](skills/write-quality-tests/SKILL.md): 共通ワークフローと各サブスキルへの案内
- [テスト設計ガイド](skills/write-quality-tests/references/test-design.md): 境界値・状態遷移・テストダブルの指針
- [AIテストレビュー](skills/write-quality-tests/references/ai-test-review.md): 偽の安心感を防ぐ確認項目
- [出典](skills/write-quality-tests/references/sources.md): 一次資料38件の一覧

##### `verify-with-dafny`

Quint公式スキルの検証ワークフローを参考に、Dafnyを使ってアルゴリズムや状態更新の正しさを検証するスキルです。事前条件と事後条件、ループ不変条件、停止性、変更可能範囲（フレーム）に加え、仮定や未検証部分の監査を扱います。Dafnyの公式スキルではありません。

```bash
npx skills add 45deg/skills --skill verify-with-dafny
```

- [SKILL.md](skills/verify-with-dafny/SKILL.md): 検証ワークフローと監査基準
- [言語ガイド](skills/verify-with-dafny/references/language-guide.md): Dafnyの要点と公式リファレンスへのリンク
- [証明パターン](skills/verify-with-dafny/references/proof-patterns.md): ループ・可変状態・実装対応の指針
- [実行と証跡](skills/verify-with-dafny/references/execution.md): 検証コマンドと結果の記録方法

##### `verify-with-quint`

公式のQuintスキルを参考に、既存のコード、プロトコル、状態遷移をモデル化して検証する自己完結型のスキルです。ソースコードとの対応、原子性や障害の仮定、不変条件・到達可能性・活性の検証、反例の調査、検証範囲の報告を扱い、モデル検査の成功と実装の正しさを明確に区別します。

```bash
npx skills add 45deg/skills --skill verify-with-quint
```

- [SKILL.md](skills/verify-with-quint/SKILL.md): モデル化から検証・報告までの手順
- [モデリング指針](skills/verify-with-quint/references/modeling.md): 既存システムからのモデル抽出
- [検証指針](skills/verify-with-quint/references/verification.md): 性質の定義と実行手順

#### UI・デザイン

##### `design-clear-ui`

WebやアプリのUIを設計・レビュー・改善し、利用者が覚えること、探すこと、読み直すこと、判断することを減らすためのスキルです。操作の流れ、選択肢の示し方、UI文言、フィードバック、中断後の再開を扱います。既存のデザインシステムとアクセシビリティを保ち、必要な情報や操作が実際に使う場面で揃っているかを確認します。

```bash
npx skills add 45deg/skills --skill design-clear-ui
```

- [SKILL.md](skills/design-clear-ui/SKILL.md): 設計原則と確認フロー
- [継続性・再開設計](skills/design-clear-ui/references/continuity.md): 作業の保持と復旧の指針
- [検証チェック](skills/design-clear-ui/references/verification.md): 状態・失敗・再開パスの検証方法

##### `dads-foundations-core`

日本の行政機関向けWeb UIを設計、レビュー、実装する際に、デジタル庁デザインシステム（DADS）のデザイン基盤（カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、アクセシビリティ、エレベーション、角の形状など）を適用・監査するためのスキルです。

```bash
npx skills add 45deg/skills --skill dads-foundations-core
```

> [!NOTE]
> これはデジタル庁による公式の公開物、パッケージ、推奨表明ではありません。DADSのWebサイトをもとにLLM利用向けに編集・蒸留した派生資料です。利用・再利用時は [README.md](skills/dads-foundations-core/README.md) に記載の出典・利用上の注意事項・コピーライトポリシーを確認してください。

- [README.md](skills/dads-foundations-core/README.md): 出典、ライセンス、収録ファイル一覧
- [SKILL.md](skills/dads-foundations-core/SKILL.md): 適用ルールとリファレンスの参照先

##### `ud-color-design`

カラーユニバーサルデザイン（CUD）とUDカラーの原則を、Web UI、グラフ、地図、インフォグラフィック、スライド、サイン、印刷物・DTPへ適用するスキルです。用途に応じた画面用RGB・印刷用CMYK値の選択、識別しにくい配色ペアの検出、ラベル・アイコン・パターン・線種など色以外の補助表現の追加を行います。

```bash
npx skills add 45deg/skills --skill ud-color-design
```

- [README.md](skills/ud-color-design/README.md): 概要と出典（『カラーユニバーサルデザイン推奨配色セット ガイドブック』第2版）
- [SKILL.md](skills/ud-color-design/SKILL.md): 媒体別の適用ワークフロー
- [CUD配色データ](skills/ud-color-design/references/cud-palette-data.md): 画面用RGB・印刷用CMYKの数値一覧
- [配色組み合わせ指針](skills/ud-color-design/references/cud-combination-guidance.md): 推奨セットと注意が必要なペア
- [UDカラー設計ルール](skills/ud-color-design/references/ud-color-design-rules.md): 冗長表現・ラベル・コントラストの確認項目

#### 日本語文章

##### `naturalize-japanese-prose`

AIが生成または補助した日本語の文章を、意味、事実、論理関係、情報量、書き手の立場、主張の強さを保ちながら自然な日本語へ書き直すスキルです。指示とリファレンスはすべて日本語の構文・句読点・文体・ジャンル慣習に基づいて記述されています。

主な用途：

- 構成の繰り返しや過剰な道案内、機械的な接続表現、均一なリズムの診断・整理
- 曖昧な抽象表現や名詞偏重の構文の解消、タイトル・見出しにおける演出目的の不要な読点の修正
- 用語、限定表現、引用、ジャンル固有の慣習の保持と、根拠のない評価・因果・推測の切り分け
- 書き直し前後の意味の追加・欠落の監査と、自然さ・一読での解析しやすさ・読者理解の分離評価

```bash
npx skills add 45deg/skills --skill naturalize-japanese-prose
```

- [README.md](skills/naturalize-japanese-prose/README.md): スキル概要
- [SKILL.md](skills/naturalize-japanese-prose/SKILL.md): 改稿手順、保存ルール、出力モード
- [詳細分析](skills/naturalize-japanese-prose/references/analysis.md): 文体パターンの分類と編集指針
- [AI文体シグナル](skills/naturalize-japanese-prose/references/ai-writing-signals.md): 日本語向けの判定基準
- [チェックリスト](skills/naturalize-japanese-prose/references/checklist.md): 意味保存と自然さの検査項目
- [解説文の検査](skills/naturalize-japanese-prose/references/explanatory-prose.md): 入門・技術解説向けの理解条件チェック

---

## English

### Skills Overview

| Skill | Category | Summary | Language |
| --- | --- | --- | --- |
| [`human-readable-code`](#human-readable-code-1) | Code | Write, refactor, and review human-readable code across languages | English |
| [`human-readable-code-ja`](#human-readable-code-ja-1) | Code | Design code structure, Japanese comments, and opening maps together | Japanese |
| [`write-quality-tests`](#write-quality-tests-1) | Testing | Risk-based test design, implementation, and review | English |
| [`verify-with-dafny`](#verify-with-dafny-1) | Verification | Verify algorithms and state updates with Dafny contracts and proofs | English |
| [`verify-with-quint`](#verify-with-quint-1) | Verification | Model and verify existing code, protocols, and state transitions in Quint | English |
| [`design-clear-ui`](#design-clear-ui-1) | UI Design | Reduce memory, attention, reading, and decision demands in UI | English |
| [`dads-foundations-core`](#dads-foundations-core-1) | UI Design | Apply and audit Digital Agency Design System (DADS) foundations | English |
| [`ud-color-design`](#ud-color-design-1) | Color Design | Apply Color Universal Design (CUD) palettes and redundant cues | English |
| [`naturalize-japanese-prose`](#naturalize-japanese-prose-1) | Japanese Prose | Revise AI-assisted Japanese while preserving meaning and stance | Japanese |

### Install

List the skills in this repository:

```bash
npx skills add 45deg/skills --list
```

Install any specific skill using the `--skill <skill-name>` command shown in each section below:

```bash
npx skills add 45deg/skills --skill <skill-name>
```

### Skills

#### Code, Testing & Verification

##### `human-readable-code`

An English skill for writing and improving human-readable code across languages during implementation, feature development, refactoring, and review. Covers naming, data representations, control flow, interfaces, state, and failures, plus purpose and invariant comments, useful ASCII tables or diagrams, and opening summary maps for files including `index.*` entry points.

```bash
npx skills add 45deg/skills --skill human-readable-code
```

- [SKILL.md](skills/human-readable-code/SKILL.md): Decision guidance and core principles
- [Construction examples](skills/human-readable-code/references/howto.md): Implementation choices and tradeoffs
- [Review and refactoring](skills/human-readable-code/references/review-and-refactoring.md): Behavior-preserving refactoring checks
- [Sources](skills/human-readable-code/references/sources.md): Provenance and applicability

##### `human-readable-code-ja`

An independent Japanese-language skill for designing code structure, Japanese comments, and opening summary maps together. Covers implementation, refactoring, and review of naming, data representation, control flow, contracts, state, and failures, with explanations drafted directly from verified requirements and implementation. Opening maps identify file responsibilities and processing stages, including public responsibilities and implementation paths in `index.*` entry points.

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

- [SKILL.md](skills/human-readable-code-ja/SKILL.md): Self-contained workflow and guidance
- [Japanese comments](skills/human-readable-code-ja/references/japanese-comments.md): Comment and opening-map conventions
- [Examples](skills/human-readable-code-ja/references/examples.md): Concrete examples
- [Review and refactoring](skills/human-readable-code-ja/references/review-and-refactoring.md): Review and refactoring cases
- [Sources](skills/human-readable-code-ja/references/sources.md): Reference sources

##### `write-quality-tests`

An English skill for risk-based test design, implementation, and review of generated tests. Covers grounded expectations, boundary cases, authorization, recovery after partial failure, and evidence of defect detection. It bundles eight subskills (frontend, backend, database, contracts, E2E, security, performance and reliability, and data pipelines) alongside a research synthesis and source register covering 38 primary sources.

```bash
npx skills add 45deg/skills --skill write-quality-tests
```

> [!NOTE]
> Keep the entire bundle, including its subskills and shared references, together. This is guidance for test-design and review decisions; the cited studies evaluate their own methods and tools and do not establish a defect-detection advantage from using this skill.

- [SKILL.md](skills/write-quality-tests/SKILL.md): Common workflow and subskill routing
- [Test design](skills/write-quality-tests/references/test-design.md): Boundary, state-transition, and test-double guidance
- [AI test review](skills/write-quality-tests/references/ai-test-review.md): Checks against false confidence
- [Sources](skills/write-quality-tests/references/sources.md): Register of 38 primary sources

##### `verify-with-dafny`

An English skill for verifying algorithms and state updates with Dafny, informed by the official Quint modeling workflow. Covers contracts, loop invariants, termination, frames, and auditing assumptions and unverified boundaries. This is not an official Dafny skill.

```bash
npx skills add 45deg/skills --skill verify-with-dafny
```

- [SKILL.md](skills/verify-with-dafny/SKILL.md): Verification workflow and audit rules
- [Language guide](skills/verify-with-dafny/references/language-guide.md): Concise Dafny summaries and official documentation links
- [Proof patterns](skills/verify-with-dafny/references/proof-patterns.md): Loops, mutable state, and implementation correspondence
- [Execution](skills/verify-with-dafny/references/execution.md): Running the verifier and recording evidence

##### `verify-with-quint`

An English, self-contained skill informed by the official Quint skills for modeling and verifying existing code, protocols, and state transitions. Covers source correspondence, atomicity and failure assumptions, safety, reachability, liveness, counterexample investigation, and scoped verification evidence, distinguishing model-checking results from implementation correctness.

```bash
npx skills add 45deg/skills --skill verify-with-quint
```

- [SKILL.md](skills/verify-with-quint/SKILL.md): End-to-end modeling and verification workflow
- [Modeling](skills/verify-with-quint/references/modeling.md): Extracting models from existing systems
- [Verification](skills/verify-with-quint/references/verification.md): Defining properties and running checks

#### UI & Design

##### `design-clear-ui`

An English skill for designing, reviewing, and improving web and app UI to reduce memory, attention, reading, and decision demands. Covers task flows, choices, UI copy, feedback, and recovery after interruption while preserving existing design systems and accessibility.

```bash
npx skills add 45deg/skills --skill design-clear-ui
```

- [SKILL.md](skills/design-clear-ui/SKILL.md): Core UI clarity workflow
- [Continuity](skills/design-clear-ui/references/continuity.md): Retention and recovery guidance
- [Verification](skills/design-clear-ui/references/verification.md): Checking populated, failure, and return states

##### `dads-foundations-core`

An English skill that applies Japanese government-style Digital Agency Design System (DADS) core design foundations—color, typography, layout, spacing, icons, links, elevation, corner shapes, and accessibility—when designing, reviewing, or implementing web UI.

```bash
npx skills add 45deg/skills --skill dads-foundations-core
```

> [!NOTE]
> This is not an official Digital Agency publication, package, or endorsement. It is an edited and distilled derivative for LLM use. See [README.md](skills/dads-foundations-core/README.md) for source, usage notice, and copyright policy details.

- [README.md](skills/dads-foundations-core/README.md): Source, license notice, and file index
- [SKILL.md](skills/dads-foundations-core/SKILL.md): Operating rules and reference routing

##### `ud-color-design`

An English skill for applying Color Universal Design (CUD) palette data and UD color-design checks to web UI, charts, maps, infographics, slides, signage, and print/DTP artifacts. Covers screen RGB and print CMYK selection, hard-to-distinguish color pairs, and redundant non-color cues such as labels, icons, patterns, line styles, and marker shapes.

```bash
npx skills add 45deg/skills --skill ud-color-design
```

- [README.md](skills/ud-color-design/README.md): Overview and CUD guidebook citation
- [SKILL.md](skills/ud-color-design/SKILL.md): Medium-specific workflow and output checks
- [CUD palette data](skills/ud-color-design/references/cud-palette-data.md): Screen RGB and print CMYK values
- [Combination guidance](skills/ud-color-design/references/cud-combination-guidance.md): Starter sets and risk pairs
- [Design rules](skills/ud-color-design/references/ud-color-design-rules.md): Redundant cues, labeling, and contrast checks

#### Japanese Prose

##### `naturalize-japanese-prose`

Revises AI-generated or AI-assisted Japanese while preserving meaning, facts, logical relations, stance, and claim strength. Its instructions and references are written in Japanese because the editing criteria depend on Japanese syntax, punctuation, register, and genre conventions.

Use it for:

- Diagnosing repetitive structures, excessive signposting, mechanical connectives, and uniform sentence rhythms
- Replacing vague abstractions and noun-heavy phrasing, and removing unnecessary dramatic punctuation in titles and headings
- Preserving terminology, qualifications, quotations, and genre conventions while flagging unsupported claims instead of polishing them
- Auditing rewrites in both directions for semantic additions or omissions, and separating naturalness, parseability, and reader comprehension

```bash
npx skills add 45deg/skills --skill naturalize-japanese-prose
```

- [README.md](skills/naturalize-japanese-prose/README.md): Skill overview
- [SKILL.md](skills/naturalize-japanese-prose/SKILL.md): Workflow, preservation rules, and output modes
- [Analysis](skills/naturalize-japanese-prose/references/analysis.md): Taxonomy of prose patterns and editing guidance
- [AI writing signals](skills/naturalize-japanese-prose/references/ai-writing-signals.md): Japanese editing criteria
- [Checklist](skills/naturalize-japanese-prose/references/checklist.md): Semantic-preservation and naturalness checks
- [Explanatory prose](skills/naturalize-japanese-prose/references/explanatory-prose.md): Comprehension checks for tutorials and technical explanations

---

## 参考文献 / References

### 日本語の文章とコードコメント

一般財団法人日本特許情報機構 特許情報研究所『特許ライティングマニュアル（第2版）「産業日本語」』、一般財団法人日本特許情報機構、2018年3月26日第2版第1刷発行、2019年3月22日第2版第2刷発行。
