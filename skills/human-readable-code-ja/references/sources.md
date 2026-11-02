# 出典と適用範囲

`human-readable-code-ja` は、コードの構造と日本語の説明を一緒に設計する独立したスキルである。判断基準は本スキル内で管理し、参照元スキルとの同期を前提にしない。

作成時には、同じリポジトリの `human-readable-code/SKILL.md` と `references/howto.md` を参考にした。命名、データ、制御フロー、契約、状態、副作用、失敗、独立した検証に関する考え方を採用し、日本語コメントと要約マップを含む実装の指針として構成した。

日本語コメントでは `naturalize-japanese-prose/SKILL.md` と、その `references/checklist.md`、`references/ai-writing-signals.md`、`references/explanatory-prose.md` を参考にした。採用したのは、具体的な主体と動詞、条件・確実性の維持、用語の一貫性、自然さと理解可能性の区別、内容のない予告や重複の削減である。

元の文章を保存する推敲手順は、そのまま適用していない。新規コメントでは、仕様と実装を根拠に必要な定義、前提、具体例を追加する。既存コメントでは根拠を再確認しながら意味を保つ。AI判定、禁止語リスト、原文にない情報の一律禁止は採用しない。参照したスキルは由来を示すもので、実行時の依存ではない。

## コード設計の参考資料

以下は、作成時に `human-readable-code` の出典記録を通じて参照した資料と、ここで採用した観点である。外部資料を再調査したものではない。

| 資料 | 採用した観点 | 適用上の限界 |
| --- | --- | --- |
| ローカルの `good-code` | 理解の負担、契約、状態と副作用、抽象化の判断、独立した検証 | レビュー専用の手順として扱わない。 |
| [Rob Pike: Notes on Programming in C](https://www.cs.tufts.edu/~nr/cs257/archive/rob-pike/notes-on-c.pdf) | 文脈に応じた命名、明確な述語、データ表現、表による対応 | C固有のポインター表現、略語の好み、過去の性能上の主張を一般化しない。 |
| [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | 意図、意味のあるインターフェース、一貫した操作、取得と解放の対応 | 他言語にC++の型やRAIIを要求しない。 |
| [Effective Go](https://go.dev/doc/effective_go) | 言語の慣用表現と標準書式 | 新しい言語機能の確認には使用中の版の資料を使う。 |
| [PEP 8](https://peps.python.org/pep-0008/) | 局所的な一貫性、読みやすさ、互換性 | Python固有の書式は他言語へ持ち込まない。 |
| [Google: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | 先回りした汎用化の抑制、読めるテスト、コメントとAPI文書の区別 | 実装時の確認に使い、レビュー中心の進め方を必須にしない。 |
| [Fowler: Decompose Conditional](https://refactoring.com/catalog/decomposeConditional.html) | 意味のある条件と計算に名前を付ける | すべての式を関数へ抽出する要求ではない。 |
| [Fowler: Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html) | 独立した特殊ケースの早期処理 | 優先順位と後始末を保ち、ガード節を一律に選ばない。 |

言語をまたぐ適用、模式例、要約マップ、日本語コメントの指針は、このスキルの編集上の判断を含む。各資料が同じ規則を直接要求しているという意味ではない。
