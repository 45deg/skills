# Sources and applicability

Reviewed 2026-11-03. This skill synthesizes the sources below for new implementation. Cross-language adaptations and examples are this skill's own synthesis, not universal claims made by each source.

## Foundation

Local `good-code/SKILL.md` and `good-code/references/decision-cases.md`, originally read under `/Users/zkr/.codex/skills/`: comprehension cost, contracts, state and effects, abstraction tradeoffs, and independent verification. These are provenance, not runtime dependencies.

## Construction guidance

| Source | Adopted guidance | Limits |
| --- | --- | --- |
| [Rob Pike: Notes on Programming in C](https://www.cs.tufts.edu/~nr/cs257/archive/rob-pike/notes-on-c.pdf) | Context-sensitive names, unambiguous predicates, data representation, table-driven choices | Do not generalize C pointer idioms, abbreviation preferences, or historical performance claims. |
| [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), P.3, I.4, F.1/F.2, E.6 | Express intent, meaningful interfaces, coherent operations, paired resource acquisition/release | Adapt to native language facilities; do not require C++ types or RAII elsewhere. |
| [Effective Go](https://go.dev/doc/effective_go) | Use language idioms and standard formatting | The document dates from 2009 and is not actively updated; not a reference for newer features. |
| [PEP 8](https://peps.python.org/pep-0008/) | Local consistency, readability, and compatibility over mechanical style compliance | Python syntax and formatting rules remain Python-specific. |

## Supporting guidance

| Source | Adopted guidance | Limits |
| --- | --- | --- |
| [Google: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Avoid speculative generality; keep tests readable; distinguish comments from API documentation | Supports implementation checks, not a review-first workflow. |
| [Fowler: Decompose Conditional](https://refactoring.com/catalog/decomposeConditional.html) | Name meaningful conditions and calculations | Does not imply extracting every expression into a function. |
| [Fowler: Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html) | Resolve independent special cases early | One control-flow option; priority and cleanup remain constraints. |

The skill applies these ideas while choosing names, data, processing steps, and interfaces from the outset. Shared goals do not imply uniform syntax, paradigms, or error handling.
