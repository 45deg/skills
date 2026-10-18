---
name: verify-with-dafny
description: Verify algorithmic and stateful logic with Dafny contracts, loop invariants, frame conditions, and termination proofs. Use for Dafny verification, proving functional correctness, investigating failed proof obligations, or modeling existing implementation logic in Dafny. Distinguishes verified Dafny code from unproved correspondence to another implementation.
---

# Verify with Dafny

Establish what the implementation must do, express that contract, and produce checked proof obligations with an explicit trust boundary. A green verifier result is useful only if the contract captures the required behavior.

## Fix the claim before proving it

Inspect the source, requirements, existing proofs, tool versions, and repository instructions. Identify the actual entry points and allowed inputs. Keep required behavior, current behavior, and additional assumptions separate. Derive postconditions from requirements rather than copying the algorithm's result into its specification.

For native Dafny, annotate the actual implementation. For another language, record source-symbol-to-model correspondence, integer/overflow semantics, mutation and aliasing, exceptions, and atomicity assumptions. Dafny mathematical integers do not reproduce fixed-width overflow. A sequential model does not prove concurrent code correct; model interleavings explicitly or limit the claim. Preserve the original algorithm before proposing a repair. Do not silently substitute a known-correct algorithm for the code under review.

Before proving a foreign-language model, map the requirement to source steps, their Dafny representation, and the obligation that checks them. Keep the desired abstract behavior separate from the implementation model. Proving an ideal operation that directly performs its specified effect only checks that specification example; it does not check an implementation with different intermediate states. Read [implementation correspondence](references/proof-patterns.md#implementation-correspondence) when concurrency or translation is involved. If the decisive source behavior is omitted, prioritize modeling or reproducing it instead of spending the proof budget on an unrelated sequential success.

Translate each requirement into an independently reviewable obligation, including rejection and unchanged-state behavior. Preconditions describe the promised caller domain: adding a precondition to exclude a failing permitted input changes the problem. Record ambiguities rather than silently resolving them in favor of a proof.

## Develop the proof

Use the [Dafny language guide](references/language-guide.md) for concise language summaries and official documentation links. Read [proof patterns](references/proof-patterns.md) for loops, mutable state, arithmetic, or difficult solver obligations.

For a small complete example, see the [first-index fixture](assets/first-index.dfy) and [replay instructions](references/execution.md#replay-the-bundled-fixture). It proves a first-match search contract and includes an intentionally failing mutation with the same contract.

Start with a small executable unit and its contract. State functional properties, not only bounds or absence of runtime errors. For collections, decide whether order, multiplicity, stability, and exact contents matter. For state transitions, describe all affected and preserved state and distinguish successful work, repeated work, conflict, and rejection where the contract does.

Add loop invariants that relate processed and unprocessed regions to the original input, and a well-founded `decreases` measure. Prove initialization, preservation, and the postcondition on exit. Capture heap contents with ghost snapshots when needed; `old` changes heap lookup, not the value of ordinary local variables. Declare frames and account for aliases. Use small lemmas and explicit intermediate facts when they explain a missing mathematical step.

A failure can be a defect, insufficient invariant, missing lemma, invalid assumption, or solver limitation. Classify it before changing code. A solver's inability to prove an obligation is not itself a concrete counterexample. Validate a suspected defect with a feasible input and trace or executable reproduction. Preserve failing evidence and verify authorized repairs against the same requirements.

When the task includes implementation, a diagnosed defect is an intermediate result: revise the design and check the repair while the task budget permits. If unresolved, retain the failing evidence and name the unmet requirement rather than treating a separate passing specification model as completion.

For repeated or concurrent transitions, read [coverage and evidence integrity](references/execution.md#coverage-and-evidence-integrity). Distinguish obligations establishing required behavior from lemmas establishing a failing execution.

## Run and audit

Read [execution and evidence](references/execution.md) before interpreting results. Inspect local `dafny --version` and `dafny verify --help`; prefer the repository's pinned toolchain. Run the actual verifier and save commands, exits, versions, and logs. A parse, resolve, compile, or sample execution alone is not a proof. During iteration use focused checks; before delivery verify the complete intended target and its included dependencies.

Review the trusted surface: `assume`, `expect`, axioms, external/bodyless declarations, disabled verification, skipped dependencies, and nontermination escapes. Do not introduce them to make a failed obligation green. `expect` supplies an assumption to the verifier; a runtime check is not its proof. Legitimate external contracts remain explicit trust assumptions.

Check that the input domain is inhabited and important branches are possible. Supply concrete admissible calls or witnesses for empty/boundary/ordinary cases. Audit specifications for contradictions and accidental omissions. Where useful, mutate one consequential operation and confirm that the unchanged contract rejects it; passing this check supports contract sensitivity, not completeness. Never weaken a required contract to accommodate a mutation.

## Report the result

Tie final claims to the delivered source and model, using file hashes or an immutable revision that includes local changes. After a relevant edit, rerun affected checks and update correspondence; results from a previous artifact do not validate its replacement. Reconcile the final report with these exact artifacts before delivery.

List the required properties, checked symbols, assumptions, and unresolved obligations. Separate original failures, proved repairs, and executable examples. Label timeouts and unavailable execution as incomplete, not successful. Distinguish proof over all admitted inputs from bounded exploration or sample testing.

State whether the verified artifact is the production Dafny code or a model, whether source correspondence was proved or reviewed, and whether generated/runtime integration was tested. Do not claim correctness of omitted components, foreign-language code, concurrency, or runtime dependencies from the Dafny proof alone.

See [provenance and adaptation](references/sources.md) for the official-skill search and Quint workflow basis.
