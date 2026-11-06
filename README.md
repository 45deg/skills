# Skills

エージェント向けスキル

## 日本語

### インストール

このリポジトリに含まれるスキルの一覧を表示します。

```bash
npx skills add 45deg/skills --list
```

特定のスキルをインストールします。

```bash
npx skills add 45deg/skills --skill naturalize-japanese-prose
```

```bash
npx skills add 45deg/skills --skill dads-foundations-core
```

```bash
npx skills add 45deg/skills --skill ud-color-design
```

```bash
npx skills add 45deg/skills --skill human-readable-code
```

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

### スキル

#### `human-readable-code`

新規実装、機能追加、リファクタリング、レビューで、言語を問わず、人が意図を追いやすいコードを書く・改善するための英語スキルです。命名、データ表現、制御フロー、インターフェース、状態、失敗の設計を扱います。あわせて、目的や前提を説明するコメント、ASCII図表、`index.*` を含むファイル冒頭の要約マップの書き方も説明します。

```bash
npx skills add 45deg/skills --skill human-readable-code
```

[SKILL.md](skills/human-readable-code/SKILL.md) に判断基準を、[具体例](skills/human-readable-code/references/howto.md) に実装時の選択肢を、[レビュー・リファクタリング](skills/human-readable-code/references/review-and-refactoring.md) に動作を保つための確認点を、[出典](skills/human-readable-code/references/sources.md) に参考資料と適用範囲をまとめています。

#### `human-readable-code-ja`

コードの構造、日本語コメント、ファイル冒頭の要約マップを一緒に設計する独立したスキルです。実装、リファクタリング、レビューにおいて、命名、データ表現、制御フロー、契約、状態、失敗を扱い、仕様と実装を根拠にした日本語の説明を最初から書きます。ファイル冒頭の要約マップには役割と主な処理を示し、`index.*` などの入口では公開内容と実装先も案内します。

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

[SKILL.md](skills/human-readable-code-ja/SKILL.md)、[日本語コメント](skills/human-readable-code-ja/references/japanese-comments.md)、[具体例](skills/human-readable-code-ja/references/examples.md)、[レビュー・リファクタリング](skills/human-readable-code-ja/references/review-and-refactoring.md) を参照してください。他のスキルを追加せずに単体で使えます。

#### `verify-with-dafny`

Quint公式スキルの検証ワークフローを参考に、Dafnyを使ってアルゴリズムや状態更新の正しさを検証します。事前条件と事後条件、ループ不変条件、停止性、変更可能範囲に加え、仮定や未検証部分の監査を扱います。Dafnyの公式スキルではありません。

```bash
npx skills add 45deg/skills --skill verify-with-dafny
```

[SKILL.md](skills/verify-with-dafny/SKILL.md) に検証手順を、[言語ガイド](skills/verify-with-dafny/references/language-guide.md) にDafnyの要点と公式リファレンスへのリンクをまとめています。

#### `verify-with-quint`

公式のQuintスキルを参考に、既存のコード、プロトコル、状態遷移をモデル化して検証します。ソースコードとの対応、原子性や障害の仮定、不変条件・到達可能性・活性の検証、反例の調査、検証範囲の報告を扱います。モデル検査の成功と実装の正しさを区別します。

```bash
npx skills add 45deg/skills --skill verify-with-quint
```

詳しくは [SKILL.md](skills/verify-with-quint/SKILL.md) を参照してください。検証手順、公式出典、実行可能な競合状態の例を同梱しています。

#### `write-quality-tests`

仕様とリスクに基づくテストの設計・実装と、生成されたテストのレビューを支援します。期待値の根拠、境界条件、認可、途中失敗後の復旧、欠陥を検出できるかの確認を扱います。フロントエンド、バックエンド、DB、API契約、E2E、セキュリティ、性能・信頼性、データパイプラインの8つのサブスキルと、一次資料38件の出典一覧および調査整理を同梱しています。

```bash
npx skills add 45deg/skills --skill write-quality-tests
```

サブスキルと共有資料を含むディレクトリ全体を使用してください。詳しくは [SKILL.md](skills/write-quality-tests/SKILL.md) を参照してください。

テストの設計とレビューの判断を支援するガイドです。引用した研究はそれぞれの手法やツールを評価したものであり、このスキルの使用によって欠陥検出率が向上することを保証するものではありません。

#### `naturalize-japanese-prose`

AIが生成または補助した日本語を、意味、事実、論理関係、書き手の立場、主張の強さを保ちながら書き直します。

次の用途に使用できます。

- 構成の繰り返しや過剰な道案内の診断
- 重複した表現、曖昧な抽象表現、機械的な接続表現の整理
- タイトルや見出しにある、演出目的の不要な読点の修正
- 用語、限定表現、引用、ジャンル固有の慣習の保持
- 書き直しによる意味の追加や欠落の確認

#### `dads-foundations-core`

日本の行政機関向けWeb UIを設計、レビュー、実装する際に、デジタル庁デザインシステム（DADS）のデザイン基盤を適用します。対象は、カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、アクセシビリティです。

次の用途に使用できます。

- カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、エレベーション、角の形状などのデザイン基盤
- 日本の行政機関向けWeb UIにおけるデザイン判断の検証と監査

#### `ud-color-design`

カラーユニバーサルデザインとUDカラーの原則をビジュアル制作物に適用します。

次の用途に使用できます。

- Web UIのカラー、デザイントークン、状態スタイル
- グラフ、地図、インフォグラフィック、スライドのビジュアル
- RGB/CMYKへの対応が必要な印刷物やDTPのカラーパレット
- 色だけで情報を伝えている箇所の監査

## English

Agent skills

### Install

List the skills in this repository:

```bash
npx skills add 45deg/skills --list
```

Install a specific skill:

```bash
npx skills add 45deg/skills --skill naturalize-japanese-prose
```

```bash
npx skills add 45deg/skills --skill dads-foundations-core
```

```bash
npx skills add 45deg/skills --skill ud-color-design
```

```bash
npx skills add 45deg/skills --skill human-readable-code
```

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

### Skills

#### `human-readable-code`

An English skill for writing and improving human-readable code across languages during implementation, feature development, refactoring, and review. Covers naming, data, control flow, interfaces, state, and failures, plus purpose and invariant comments, useful ASCII tables or diagrams, and opening summary maps for files including `index.*` entry points.

```bash
npx skills add 45deg/skills --skill human-readable-code
```

See [SKILL.md](skills/human-readable-code/SKILL.md) for decision guidance, [construction examples](skills/human-readable-code/references/howto.md) for tradeoffs, [review and refactoring cases](skills/human-readable-code/references/review-and-refactoring.md) for behavior-preserving changes, and [sources](skills/human-readable-code/references/sources.md) for provenance and applicability.

#### `human-readable-code-ja`

An independent skill for designing code structure, Japanese comments, and opening summary maps together. Covers implementation, refactoring, and review of naming, data representation, control flow, contracts, state, and failures, with explanations drafted directly from verified requirements and implementation. Opening maps identify file responsibilities and processing stages, including public responsibilities and implementation paths in `index.*` entry points.

```bash
npx skills add 45deg/skills --skill human-readable-code-ja
```

See [SKILL.md](skills/human-readable-code-ja/SKILL.md), [Japanese comments](skills/human-readable-code-ja/references/japanese-comments.md), [examples](skills/human-readable-code-ja/references/examples.md), and [review and refactoring cases](skills/human-readable-code-ja/references/review-and-refactoring.md). All guidance needed to use the skill is included in its own bundle.

#### `verify-with-dafny`

An English skill for verifying algorithms and state updates with Dafny, informed by the official Quint modeling workflow. Covers contracts, loop invariants, termination, frames, and auditing assumptions and unverified boundaries. This is not an official Dafny skill.

```bash
npx skills add 45deg/skills --skill verify-with-dafny
```

See [SKILL.md](skills/verify-with-dafny/SKILL.md) for the workflow and [language guide](skills/verify-with-dafny/references/language-guide.md) for concise Dafny summaries and official reference links.

#### `verify-with-quint`

An English skill informed by the official Quint skills for modeling and verifying existing code, protocols, and state transitions. Covers source correspondence, atomicity and failure assumptions, safety, reachability, liveness, counterexample investigation, and scoped verification evidence. Distinguishes model-checking results from implementation correctness.

```bash
npx skills add 45deg/skills --skill verify-with-quint
```

Start with [SKILL.md](skills/verify-with-quint/SKILL.md). The bundle includes execution guidance, official sources, and a runnable race-condition example.

#### `write-quality-tests`

An English skill for risk-based test design, implementation, and review of generated tests. Covers grounded expectations, boundary cases, authorization, recovery after partial failure, and evidence of defect detection. It bundles eight subskills: frontend, backend, database, contracts, E2E, security, performance and reliability, and data pipelines. The research synthesis and source register cover 38 primary sources.

```bash
npx skills add 45deg/skills --skill write-quality-tests
```

Keep the entire bundle, including its subskills and shared references, together. Start with [SKILL.md](skills/write-quality-tests/SKILL.md); it routes to the relevant layers without loading every module.

This is guidance for test-design and review decisions. The cited studies evaluate their own methods and tools; they do not establish a defect-detection advantage from using this skill.

#### `naturalize-japanese-prose`

Revises AI-generated or AI-assisted Japanese while preserving meaning, facts, logical relations, stance, and claim strength.

Use it for:

- Diagnosing repetitive structures and excessive signposting
- Removing redundant wording, vague abstractions, and mechanical connective patterns
- Correcting unnecessary dramatic punctuation in titles and headings
- Preserving terminology, qualifications, quotations, and genre-specific conventions
- Checking rewrites for semantic additions or omissions

#### `dads-foundations-core`

Applies Japanese government style Digital Agency Design System (DADS) core design foundations (color, typography, layout, spacing, icons, links, and accessibility) when designing, reviewing, or implementing web UI.

Use it for:

- Design foundations such as color, typography, layout, spacing, icons, links, elevation, and corner shapes
- Verification and audit of Japanese government-style web UI design decisions

#### `ud-color-design`

Applies Color Universal Design and UD color principles to visual artifacts.

Use it for:

- Web UI colors, design tokens, and state styles
- Charts, maps, infographics, and slide visuals
- Print and DTP palettes that need RGB/CMYK handling
- Audits where information is communicated by color alone

## 参考文献 / References

### 日本語の文章とコードコメント

一般財団法人日本特許情報機構 特許情報研究所『特許ライティングマニュアル（第2版）「産業日本語」』、一般財団法人日本特許情報機構、2018年3月26日第2版第1刷発行、2019年3月22日第2版第2刷発行。