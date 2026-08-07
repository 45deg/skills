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
npx skills add 45deg/skills --skill dads-design-system
```

```bash
npx skills add 45deg/skills --skill ud-color-design
```

### スキル

#### `naturalize-japanese-prose`

AIが生成または補助した日本語を、意味、事実、論理関係、書き手の立場、主張の強さを保ちながら書き直します。

次の用途に使用できます。

- 構成の繰り返しや過剰な道案内の診断
- 重複した表現、曖昧な抽象表現、機械的な接続表現の整理
- タイトルや見出しにある不要で演出的な句読点の修正
- 用語、限定表現、引用、ジャンル固有の慣習の保持
- 書き直しによる意味の追加や欠落の確認

#### `dads-foundations-core`

日本の行政機関向けWeb UIを設計、レビュー、実装する際に、デジタル庁デザインシステム（DADS）のデザイン基盤（カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、アクセシビリティ）を適用します。

次の用途に使用できます。

- カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、エレベーション、角の形状などのデザイン基盤
- 日本の行政機関向けWeb UIにおけるデザイン判断の検証と監査

#### `dads-design-system`（非推奨）

> [!WARNING]
> このスキルは非推奨です。デザイン基盤のガイダンスには `dads-foundations-core` を使用してください。

デジタル庁デザインシステムのWebサイトから抽出したガイダンスを、日本の行政機関向けWeb UIの設計判断に適用します。

次の用途に使用できます。

- カラー、タイポグラフィ、レイアウト、余白、アイコン、リンク、エレベーション、角の形状などのデザイン基盤
- フォーム、ナビゲーション、フィードバック、コンテンツ、データ表示のパターンに応じたコンポーネントの選択
- DADSに沿った実装やレビューにおけるアクセシビリティの確認

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
npx skills add 45deg/skills --skill dads-design-system
```

```bash
npx skills add 45deg/skills --skill ud-color-design
```

### Skills

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

#### `dads-design-system` (DEPRECATED)

> [!WARNING]
> This skill is deprecated. Please use `dads-foundations-core` for foundations guidance.

Applies distilled guidance from the Digital Agency Design System website to Japanese government-style web UI decisions.

Use it for:

- Design foundations such as color, typography, layout, spacing, icons, links, elevation, and corner shapes
- Component choice for forms, navigation, feedback, content, and data-display patterns
- Accessibility checks for DADS-oriented implementation and review work

#### `ud-color-design`

Applies Color Universal Design and UD color principles to visual artifacts.

Use it for:

- Web UI colors, design tokens, and state styles
- Charts, maps, infographics, and slide visuals
- Print and DTP palettes that need RGB/CMYK handling
- Audits where information is communicated by color alone
