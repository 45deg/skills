---
name: human-readable-code
description: Write human-readable code across languages, primarily for new implementations and feature additions. Use when choosing names, data representations, expressions, control flow, interfaces, state, errors, comments, and tests. Also applies to targeted improvements; not for formatting-only work or architecture-wide redesign.
---

# Human Readable Code

Write for a maintainer familiar with the language and project. Reduce the assumptions they must remember and the definitions they must navigate. Optimize for understanding, not line count.

Apply shared principles through each language's idioms. Do not impose one syntax, paradigm, type system, or error model across languages.

## Start from use

Read the request, project instructions, nearby code, callers, and relevant tests. Establish inputs, outputs, effects, failures, and compatibility constraints. Sketch a representative call and meaningful normal, boundary, and failure cases; small tasks do not need a separate design document.

Choose data and interfaces from those uses. Start with a direct implementation, using existing facilities before introducing new machinery.

## Name concepts consistently

- Use domain vocabulary. Give the same concept the same name; distinguish different concepts.
- Match detail to scope. Local idioms such as `i` and `err` can suffice; distant uses need more context. Distinguish roles when nested scopes make indices easy to confuse.
- Name operations for their actions, values for their meaning, and booleans for what true asserts. Avoid ambiguous predicates such as `check`.
- Expose consequential distinctions: units, inclusive/exclusive bounds, encoding, and validation state. Use names or types without repeating information already clear from context.
- Prefer informative names over long names. Follow established abbreviations and naming conventions.

## Let data express meaning

Group values that belong together. Prefer explicit relationships over parallel arrays whose indices must stay aligned, unless performance or external formats justify that representation.

Choose structures by required semantics: order, uniqueness, lookup, missing values, and scale. Represent exclusive states with named alternatives and associated data when practical; avoid independent flags that permit contradictory combinations. Use enums, sum types, tagged records, or validated construction as appropriate, without creating a type for every scalar.

Distinguish absence, emptiness, zero, and failure where callers need the distinction. Validate external data at the boundary that establishes internal assumptions. Names and type assertions do not validate values.

## Write expressions in meaningful units

Name intermediate results when they express a concept or spare readers from decoding a dense expression. Do not introduce temporaries merely to shorten lines.

Keep comparisons natural and range boundaries explicit. Use parentheses where precedence invites misreading. Avoid embedding effects whose behavior depends on operand or argument evaluation order. Preserve short-circuit guards; do not confuse missing-value checks with truthiness.

Name constants that encode policy. Keep independent policies separate even when their values match. Leave obvious arithmetic and indices uncluttered.

## Make control flow recognizable

Expose admission, normal processing, and termination. Use guards for independent exceptional cases; use symmetric branches or pattern matching to compare alternatives. Preserve case priority and required cleanup on every exit.

Express iteration as transformation, filtering, aggregation, search, or traversal. Choose idiomatic loops, standard operations, or queries. Show intermediate stages when chains or effectful folds require mental simulation. Check ordering, laziness, early termination, and memory behavior.

Use tables for simple mappings and explicit decisions when precedence matters. Do not build a rule engine for a few conditions.

## Design interfaces from the caller

Give each function one coherent operation, which may coordinate several steps. Make its name, inputs, and result explain how to use it.

When positional arguments are easy to swap or boolean literals are opaque, consider named arguments, meaningful records, or named alternatives. Do not bundle unrelated values merely to reduce parameter count.

Expose relevant preconditions, mutation, ownership, results, and failures. Pass needed dependencies instead of quietly relying on mutable globals; a simple function does not need a dependency-injection framework.

Keep internal representations behind useful module boundaries. Place code with the concept it serves. Introduce helpers, wrappers, and extension points only when they remove real caller burden or establish a needed contract. Similar code need not share an abstraction if its policies change independently.

## Keep state and effects accountable

Initialize values near use. Do not reuse a variable for unrelated purposes. Prefer stable bindings and narrowly scoped mutation; a stable binding may still reference shared mutable data.

Retain intermediate collections only when they support reuse, a meaningful phase boundary, or required guarantees. Per-item processing can keep related work together; batch validation may be needed before observable effects. Choose by contract and comprehension, not a universal one-pass or two-pass rule.

Separate calculation from I/O where that enables independent reasoning, while preserving atomic operations. Do not hide writes, sends, or deletes behind read-like or predicate names.

Assign responsibility for resource acquisition and release, and for work initiation and completion. Use native cleanup mechanisms. For asynchronous work, make ordering, shared updates, cancellation, and partial failure understandable.

## Treat failure as part of the contract

Distinguish expected absence from operational failure. Use idiomatic exceptions, error values, or result types; do not wrap every failure in a custom abstraction. Make caller-visible error categories deliberate and consistent across implementation, documentation, and tests.

Recover where meaningful recovery is possible; otherwise preserve the cause and useful operation context without exposing secrets. Avoid empty catches, unjustified defaults, and unconditional retries.

Define partial effects and repeatability where relevant. Add transaction or retry machinery only for an actual requirement.

## Arrange code for reading

Keep related declarations, calculations, and uses close. Separate meaningful stages with whitespace. Use consistent ordering and shapes for corresponding cases without changing evaluation dependencies. Follow project layout and formatters.

## Write comments that orient the reader

Use comments proactively to accelerate understanding, not only to preserve facts absent from code. For multi-stage or unfamiliar logic, give readers a brief map before the details and explain the purpose of important stages. A fact being derivable from code is not sufficient reason to omit a useful explanation.

Choose the explanation that answers the reader's next question:

- **Purpose:** what the operation or stage achieves, for whom or for what downstream step, and which property it protects. Connect the mechanism to a concrete outcome and, where useful, explain what would fail or become harder without the step; avoid vague claims such as "for robustness." Ground purpose in requirements or established behavior, not invented author intent.
- **Contracts:** relevant units, bounds, ownership, effects, failure behavior, and ordering guarantees not evident from the signature. Use the language's documentation convention for caller-facing contracts. Keep them discoverable at the entry point; internal invariant comments serve a different reader need.
- **Rationale:** why a constraint, workaround, algorithm, or unusual value is necessary. State the consequence of removing it; link to a verified issue or specification when useful, with enough local context to understand the constraint.
- **Mechanism:** invariants, phases, or a small example that makes a non-obvious algorithm, expression, or data representation understandable. At a consequential phase boundary, state what has been established and what the next phase may assume. Comments may explain how, not only why.

Choose a compact ASCII representation by the reader's question: a decision table for interacting conditions, a transition diagram for states, a flow diagram for handoffs, or a range/layout sketch for boundaries. Use it when comparing relationships spatially saves the reader from reconstructing them across branches or statements. Label nodes, columns, arrows, and boundaries so their meaning is unambiguous. Explain the abstraction shown; a conceptual flow must not imply execution order, atomicity, or synchronization the code does not guarantee. Keep diagrams readable in a normal source view and follow the language's comment syntax. Prefer a sentence when there is no useful relationship to visualize.

Place explanations beside the code they qualify; keep shared contracts in one authoritative location. Use precise statements and established project language. Do not infer thread safety, performance, or guarantees that have not been established.

Use clear names and structure together with helpful explanations. A short overview or purpose comment can save effort even when each individual statement is readable. Avoid syntax narration, decorative banners, mandatory comments on every function, and commented-out code kept as history. Make TODOs actionable by identifying the remaining work and relevant trigger or issue.

Update comments, tables, and diagrams with the implementation. If code and prose disagree, establish the intended contract before changing either. Remove obsolete explanations; preserve still-relevant constraints.

## Verify and finish

Derive expected results independently from requirements. Select cases that distinguish plausible mistakes, including relevant boundaries, duplicates, absence, and failure. Keep setup, action, and expectation visible; do not copy production logic into expected-value calculations.

Verify unfamiliar APIs against the version in use. Use project checks proportionate to impact. Do not suppress type errors or weaken assertions to obtain a pass. A low-risk edit does not justify a new test framework.

Read the complete operation from its caller. Ask: what is this for, why are these steps ordered this way, and what becomes true between stages? Add an overview, purpose, invariant, or diagram where answering requires unnecessary tracing. Judge each explanation by the misunderstanding it prevents, not its length or presence. Confirm that meaning, decisions, effects, and failures remain traceable. Do not impose arbitrary limits on lines, parameters, nesting, or abstractions. Stop when further structure costs more understanding than it saves.

## References and scope

Read [howto.md](references/howto.md) only for a matching design tradeoff or example. Read [sources.md](references/sources.md) for provenance and applicability. No other skill or routine web lookup is required.

For existing code, preserve public contracts and unrelated user changes. Review requests authorize findings, not unsolicited edits; separate defects and material comprehension risks from preferences. Report the result, checks actually performed, and consequential gaps.
