# Proof patterns

## Implementation correspondence

For a translated implementation, establish the following before choosing proof obligations:

| Required property | Source steps and return paths | Dafny state and transitions | Obligation or uncovered behavior |
| --- | --- | --- | --- |
| Observable result or state relation | Actual symbols and intermediate operations | Concrete representation, including caller-local state where relevant | What the verifier must establish, or why the claim remains unchecked |

An abstract sequence, set, or mathematical function can define the specification. The implementation model must still preserve the source operations that could violate it. For example, replacing a multi-step state change with one atomic update removes interference rather than proving it harmless.

For concurrent code, represent relevant atomic steps separately, including local observations, pending calls, and their success or failure responses. Model another participant running while a call is suspended at those boundaries. A proof of sequential input/output behavior or a method's `decreases` clause does not establish progress of other callers under suspension. State the memory-order assumptions; a sequentially consistent transition model alone does not cover weaker source memory ordering.

For a small scope, a concrete schedule with assertions about the source-shaped state can expose a defect without attempting a whole-program proof. Check that the schedule is feasible in the implementation, and preserve an executable reproduction when practical. A verified assertion that the schedule reaches a bad state proves the modeled witness, not correctness. A failing assertion alone still needs diagnosis. Label ideal specification examples, implementation-model obligations, and source reproductions separately.

Before reporting, ask whether a consequential source change would affect the model or checked obligation. If it would leave both unchanged because the relevant source behavior was never represented, the proof is not evidence about that behavior. Document the missing correspondence instead of counting that proof toward the requested implementation claim.

## Loop contracts

An invariant must be inductive: true before the loop, maintained by each iteration, and sufficient with the negated guard to imply the result. Bounds alone rarely establish functional behavior. Track a prefix/suffix relation or a relation between the evolving state and a ghost snapshot of the input. Handle early returns and break paths explicitly. A termination metric must decrease on every continuing path and be bounded in the relevant ordering.

For half-open search `[lo, hi)`, partition the excluded regions by the actual search predicate; membership alone cannot distinguish first and last duplicate. For copying or filtering, length and multiset equality do not establish order. For in-place permutation, preservation of multiplicity may require a multiset property in addition to ordering. Choose only properties required by the task.

## Heap and frames

Use `requires` for the valid representation, `modifies` for writable objects, and `ensures` for the full operation contract. Functions and predicates that inspect mutable objects need appropriate `reads` clauses. A frame permits writes; it does not require every permitted object or field to change, and it does not replace unchanged-value postconditions within that frame.

Capture arrays as sequences, e.g. `ghost var before := a[..];`. `old(a[..])` refers to entry heap contents, whereas `old(a)` alone does not snapshot array elements. State alias assumptions explicitly and do not add non-aliasing just to suppress a valid failure. For a representation containing several objects, specify ownership and what callers retain permission to observe.

## Arithmetic and abstractions

Dafny `int` is unbounded and `nat` is nonnegative; use range obligations or appropriate bit-vectors when matching machine arithmetic. Establish nonzero divisors, index bounds, and the exact rounding/sign behavior before using division or remainder. Explain why any abstraction preserves the requested property.

For retries or state machines, require a valid starting state and specify the complete next state and result. Proving only conservation or representation validity leaves observable response and rejection behavior unchecked. An idempotence statement needs the relevant identity and payload relation, not merely a repeated identifier.

## Solver difficulty

First inspect the failing obligation and facts in scope. Split reasoning with `assert`, `calc`, or a proved lemma; use induction for recursive structure and explicit intermediate equalities for sequences/maps when useful. Keep opaque definitions hidden until their meaning is needed. Use assertion isolation and resource logs to locate unstable proofs. Treat increasing a timeout as a diagnostic step, not a repair for an incorrect statement. Avoid unmotivated trigger tuning and large unrelated fact contexts.
