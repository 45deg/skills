---
name: verify-with-quint
description: Model existing code, protocols, and state transitions in Quint and check safety, reachability, and temporal properties. Use for Quint-based formal verification, concurrency or retry analysis, counterexample investigation, and checking an existing .qnt model against implementation behavior. Produces executable models, source correspondence, and scoped verification evidence; does not establish implementation correctness from model checking alone.
---

# Verify with Quint

Turn the system the user actually has into an executable model, check properties that matter, and relate results back to source behavior. This workflow builds on the official Quint modeling and language skills and is self-contained; it does not require their installation.

## Establish the target

Inspect repository instructions, source, protocol documents, tests, existing models, tool versions, and local changes. Locate state holders, entry points, concurrency boundaries, persistence, messages, retries, cancellation, and recovery relevant to the request. Reuse project tooling and model locations; otherwise choose a small dedicated directory such as `specs/quint/`.

State the component, property, and source revision being checked. For a broad request, start with a consequential stateful boundary and explain the choice. Ask only when missing information materially changes the property or model; continue independent investigation while waiting.

Keep **observed behavior**, **required behavior**, and **model assumptions** distinct. Model current behavior, including suspected defects; derive expected properties from documented contracts or confirmed requirements. Do not silently replace source behavior with an ideal algorithm or invent requirements from current outputs. Record discrepancies between source and documentation. Verification-only scope does not automatically authorize production fixes.

## Build correspondence before abstraction

Read [modeling existing systems](references/modeling.md) when extracting source or protocols. Keep a compact map inline for a small task, or beside a substantial model:

| Source symbol / location | Model state or action | Atomic boundary | Omitted behavior / justification |
| --- | --- | --- | --- |
| Actual file and symbol | Corresponding definition | Lock, transaction, await, message, or justified abstraction | Effect on the property |

Record participant/data domains, communication ordering and multiplicity, failure and recovery behavior, persistence guarantees, and timing/fairness premises. Separate established guarantees from hypotheses and identify model-only monitor state.

Every Quint action is atomic. Split observable read/check/write, await, transaction, and message boundaries where interleaving matters. Collapsing a check-then-act sequence can erase the race being investigated. A lock or transaction justifies atomicity only across the operations and state it actually protects.

Choose abstractions per property. A message set loses order and duplicate multiplicity. Use lists, counts, or distinct identities when those affect the target. Actor, counter, queue, and request bounds limit the claim; never silently truncate or wrap to obtain a finite model.

## Make an executable model

Check an existing model's correspondence to current source before reusing it. Define types, state, initialization, guards, updates, and a nondeterministic `step` including relevant environment/failure actions. Separate pure computation from updates where useful, without translating irrelevant plumbing.

Assign every variable in `init` and every action, explicitly preserving unchanged values. Initialize or guard map keys and partial collection operations. Bind every `const` in a concrete analysis module; `assume` does not initialize constants. Validate parameter conditions with executable tests or validated instance constraints instead of assuming uniform enforcement of `assume` across backends.

Typecheck and run a small simulation as soon as initialization and a transition exist; grow incrementally. Keep required properties independent of transition guards: enforcing the invariant inside `step` can exclude every violating transition and create a vacuous success.

Read the original [check-then-act fixture](assets/check-then-act.qnt) only when that pattern helps. It separates observation and commit, compares stale-check and rechecked behavior, and is not evidence about the user's system.

## Define properties and check non-vacuity

Give each property a source and rationale:

- **Safety:** forbidden states such as duplicate ownership, lost value, or commit without prerequisites. Use state predicates and explicit history/monitor state where needed.
- **Reachability:** meaningful work, contention, rejection, or recovery can occur. Use positive witnesses false at initialization when testing transitions. A witness establishes an existential path, not progress on every execution.
- **Liveness:** a required outcome eventually happens under explicit scheduling, delivery, and recovery assumptions. Use temporal properties with a compatible checker; simulation cannot establish them.

Check initialization, relevant actions in `step`, enabled work, terminal states, and premises. Zero sampled witness hits do not prove unreachability. An invariant counterexample refutes the modeled property, but may expose a modeling error rather than a source defect.

Distinguish disabled actions, observable rejection, termination, deadlock, and stuttering. Do not add unconditional no-ops to hide deadlock or invent fairness to exclude inconvenient executions.

For systems with repeated operations, reusable resources, or progress requirements, read [coverage and evidence integrity](references/verification.md#coverage-and-evidence-integrity). Record which behaviors the chosen bounds exclude; safety success does not discharge progress requirements.

## Execute the appropriate check

Read [execution and evidence](references/verification.md) before running or interpreting checks. Inspect installed CLI help/version, use project commands, and preserve commands, selected module/init/step, parameters, seed, checker versions, logs, and traces.

1. Parse/typecheck and run focused scenario tests where present. Record the executed test names and a nonzero test count, not just exit status. A module heading without test results is not a pass; select the intended definitions explicitly and rerun (see the execution reference).
2. Use `quint run` with explicit safety properties, witnesses, and sample/depth budgets to find model errors and counterexamples quickly.
3. For a request to formally verify or model-check, proceed to `quint verify` after the model executes. Use Apalache for bounded checks or justified induction; use TLC for tractable finite-state exploration and supported temporal checks. Modeling-only requests do not automatically need model checking.

Choose practical time/memory budgets and small justified domains. Inspect progress before expanding. Stop stalled checks at the budget, retain artifacts, and report incomplete verification. Errors and timeouts are not passes. `--random-transitions` is symbolic sampling, not exhaustive bounded checking.

For temporal properties or induction, consult the relevant execution-reference section and current official backend documentation. Check the effective specification, fairness, and proof prerequisites. If tools are unavailable, finish the model and reproducible commands and mark execution unverified.

## Investigate counterexamples

Preserve the failing model and exact parameters/seed. Find the first property-breaking transition, preceding state, action and inputs, and corresponding source operations. Minimize traces/domains without removing the failure mechanism.

Classify as a source defect supported by feasible source execution, a translation error, a disputed requirement, or an abstraction/environment artifact. Check locks, transactions, delivery, retries, and persistence against the trace. Do not weaken justified properties or remove plausible failures just to get green output.

For a plausible source defect, provide a concrete sequence and affected symbols. Add or propose an implementation regression or model-based replay within authorized scope. When a fix is authorized, preserve the failing case and rerun the same property and relevant implementation checks after fixing. A corrected model alone does not demonstrate a corrected implementation.

When the task includes implementation, a diagnosed defect is an intermediate result: use the counterexample to revise the design and check the repair while the task budget permits. If unresolved, deliver the failing evidence and the unmet requirement; do not present the defective implementation as completed work.

## Deliver evidence

Tie final claims to the delivered source and model, using file hashes or an immutable revision that includes local changes. After a relevant edit, rerun affected checks and update correspondence; results from a previous artifact do not validate its replacement. Reconcile the final report with these exact artifacts before delivery.

Provide model/source correspondence, properties, assumptions, executed commands, results, and gaps. Label each result using observed evidence: violated, no counterexample in samples, checked through depth, fully explored finite instance, proved by specified induction obligations, incomplete, or not executed. Separate results by property/method.

A successful check establishes a property of the model under its assumptions and scope. It does not automatically verify the implementation, all parameter sizes, or omitted failures. State whether implementation conformance or refinement was checked, and which source/protocol changes require model updates and reruns.

See [official sources and adaptation decisions](references/sources.md) for provenance and maintenance.
