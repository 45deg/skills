# Dafny language and documentation guide

A compact, unofficial guide to Dafny 4.11.0: language semantics, specifications, proof construction, and tooling. Each entry summarizes a topic and links to its official source.

Consult the relevant topic when writing or reviewing Dafny. Read the linked section for details rather than guessing syntax. Links are pinned to 4.11.0; check the project's Dafny version before applying them. Summaries are selective, not a replacement for the manual.

## Language and contracts

- [Getting started: methods, variables, and expressions](https://dafny.org/v4.11.0/OnlineTutorial/guide): Declare imperative procedures with `method` and named outputs with `returns`. Use `:=` for assignment and `==` for equality. Assign output parameters or return values explicitly. Input parameters cannot be reassigned. A `function` describes an expression; a `predicate` describes a Boolean property.
- [Getting started: preconditions and postconditions](https://dafny.org/v4.11.0/OnlineTutorial/guide): `requires` states what callers must establish; `ensures` states what the implementation must prove at every return. A method call exposes its contract to the caller, so an underspecified postcondition can prevent client proofs even when the method body is correct. Express the actual result, not merely a loose bound.
- [Getting started: assertions and loops](https://dafny.org/v4.11.0/OnlineTutorial/guide): `assert` asks the verifier to establish a fact at a program point. Loop invariants must hold on entry and after each iteration. At exit, combine the invariant with the negated guard to derive the postcondition. Index bounds and functional relationships usually require different facts. A failed obligation can indicate incorrect code or missing proof information.
- [Reference manual: numeric types](https://dafny.org/v4.11.0/DafnyRef/DafnyRef): `int` is unbounded; `nat` restricts it to nonnegative values. Bit-vectors model fixed-width operations. Subset types and newtypes express additional constraints. Do not silently identify mathematical arithmetic with machine overflow.
- [Reference manual: datatypes and modules](https://dafny.org/v4.11.0/DafnyRef/DafnyRef): Datatypes define constructor alternatives, inspected with `match`. Modules, imports, and export sets control names and visibility. Check exported specifications when proofs cross module boundaries.

## Collections and state

- [Collection types: sequences](https://dafny.org/v4.11.0/OnlineTutorial/ValueTypes): `seq<T>` is an immutable ordered value. Use `|s|`, `s[i]`, half-open slices `s[i..j]`, concatenation, and value-producing updates. Preserve order explicitly when it matters; a membership property does not capture position or multiplicity.
- [Collection types: sets and multisets](https://dafny.org/v4.11.0/OnlineTutorial/ValueTypes): Sets express membership without duplicates; multisets preserve occurrence counts. Multiset equality is useful for permutation properties but does not imply ordering. Collection values do not themselves require heap read permissions.
- [Collection types: maps](https://dafny.org/v4.11.0/OnlineTutorial/ValueTypes): Maps associate keys with values. Establish key membership before lookup. An update produces a new map. Specifications should describe both changed entries and preserved mappings.
- [Reference manual: arrays, frames, and old state](https://dafny.org/v4.11.0/DafnyRef/DafnyRef): Arrays and objects live on the mutable heap. `reads` declares dependencies; `modifies` permits writes without specifying their results. `old` evaluates heap accesses in a previous state, not ordinary local variables. Use `a[..]` for a sequence snapshot and account for aliases.

## Proof construction

- [Termination](https://dafny.org/v4.11.0/OnlineTutorial/Termination): `decreases` supplies a well-founded measure for loops and recursion. Dafny can infer some measures, such as a difference for a simple increasing loop. Measures also include sequences, sets, and lexicographic tuples. Show strict progress on every continuing iteration or recursive call. `decreases *` opts out of a termination proof where permitted; it does not prove termination.
- [Lemmas and induction](https://dafny.org/v4.11.0/OnlineTutorial/Lemmas): A lemma packages a proof with preconditions and postconditions. Prove its body before relying on it; declaring a desired conclusion alone is not enough. A recursive lemma can follow the structure of a recursive function, supplying an induction hypothesis through a smaller recursive call. Intermediate assertions help expose the missing step to the solver.
- [Reference manual: ghost code and proof statements](https://dafny.org/v4.11.0/DafnyRef/DafnyRef): Ghost declarations support proofs without runtime effects. In Dafny 4, `function` is compiled and `ghost function` is proof-only. `calc` structures relational arguments; `reveal` exposes hidden definitions. Quantifiers need appropriate domains.
- [Reference manual: assumptions](https://dafny.org/v4.11.0/DafnyRef/DafnyRef): `assume` introduces unproved facts. `expect` also assumes its condition during verification, adding a runtime check. External or bodyless declarations can leave contracts trusted rather than proved.
- [Verification optimization](https://dafny.org/v4.11.0/VerificationOptimization/VerificationOptimization): More facts are not always better for an SMT proof. Keep relevant facts local, use intermediate assertions or small lemmas, and reveal definitions when needed. Isolate assertion batches to locate expensive obligations; inspect resource counts as well as elapsed time. Solver sensitivity or timeout is not evidence that a claim is false.

## Tools and further reading

- [Local command and evidence guide](execution.md): Start with `dafny --version` and `dafny verify --help`. Run `dafny verify` for proofs; compilation and sample execution answer different questions. Check selected files, included dependencies, exit status, and verification summary. A per-batch timeout is not a process-wide time limit.
- [Official installation instructions](https://dafny.org/latest/Installation): Choose the distribution for the host platform. Verification and compilation to a target language have different prerequisites; check the selected backend before assuming it can run.
- [Dafny 4.11.0 release](https://github.com/dafny-lang/dafny/releases/tag/v4.11.0): Pinned tool distribution and release notes corresponding to this guide.
- [Local proof patterns](proof-patterns.md): Task-oriented guidance for loop relationships, heap snapshots, arithmetic correspondence, state transitions, and solver diagnosis.
- [Local verification workflow](../SKILL.md): Establish required behavior, construct and audit proofs, investigate failures, and state the limits of the result.
