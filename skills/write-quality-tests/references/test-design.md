# Test design and evidence

Use this reference when selecting cases or reviewing whether a generated test can detect a meaningful defect. Apply the common workflow in [the entrypoint](../SKILL.md).

## Derive the oracle independently

An oracle is the rule that decides whether the observed result is correct. Start with explicit acceptance criteria, supported protocol semantics, domain invariants, and confirmed incident behavior. Existing tests and implementation describe local conventions, but can encode bugs.

When sources disagree, identify the conflict. Do not silently promote a comment, snapshot, generated schema, or current result to product authority. A characterization test may deliberately preserve legacy behavior; label its purpose and keep unresolved correctness questions visible.

Prefer independently calculated literal examples, trusted reference implementations with known limits, or justified algebraic properties. Round-trip checks alone can pass when encoder and decoder share the same defect. Pair them with independently specified examples. Cross-implementation agreement is supporting evidence, not proof that either implementation is correct.

## Contract precision without implementation coupling

An exact assertion is useful when the contract fixes the value. An amount of 125 cents, an owner of `alice`, or a documented error payload can have literal expectations. A generated record ID need not equal `1` merely because the current implementation starts there. Capture the returned ID for subsequent reads and replay assertions; check distinctness across new records if required. Continue to assert the amount and owner independently rather than treating the whole returned object as its own oracle.

Apply the same distinction to timestamps, collection order, and internal storage layout: assert the supported range or relationship when specified, and exact values or ordering when promised. A diagnostic snapshot can establish that rejected operations leave state unchanged without making its internal key structure a product requirement. Keep implementation-specific assertions only when that implementation detail is itself an explicit supported contract or a labeled characterization target.

During review, ask whether a different correct implementation could fail the test. If a concrete coupling risk appears, use one bounded, disposable variant that preserves the requirements, such as a different generated ID starting value. The suite should still pass. This complements a fault mutation, which should fail; do not count a valid variant as a detected defect. Do not require alternative-implementation execution for every test or relax an assertion protecting a specified business rule.

## Select cases by the shape of the risk

| Risk shape | Useful design | Important caveat |
| --- | --- | --- |
| Numeric, size, or time threshold | Below, exactly at, and above each meaningful boundary | Use the domain's units and precision, not arbitrary floating-point tolerances |
| Multiple conditions | Decision table and cases that independently exercise each condition | A covered branch may leave short-circuited conditions untested |
| Lifecycle or workflow | Allowed and forbidden state transitions | Assert the destination state and effects that must not happen |
| Many equivalent inputs | Equivalence classes plus representative examples | Empty, missing, null, malformed, and zero may have different semantics |
| Combinatorial configuration | Risk-based combinations; pairwise sampling when justified | Add higher-order interactions known to matter; pairwise is not exhaustive |
| Repeated or concurrent actions | Model, controlled interleavings, replay and idempotency cases | Concurrent task creation alone does not guarantee the intended overlap |
| Parser or large input domain | Properties or fuzzing with resource bounds | No crash is often necessary but insufficient for semantic correctness |
| Migration or compatibility | Old data, new code, and supported version combinations | A clean install does not test upgrading existing state |

Choose cases from actual product behavior. Do not mechanically apply every row to every function.

## Interaction and failure sequences

A fixture can accidentally protect the behavior under test. When probing a boundary, keep the other relevant conditions equal so that another predicate cannot mask its removal. For a tenant-scoped cache, reuse the same user, object ID, version, and permission epoch in two tenants, provide independently different content, warm one tenant's cache, then read the other. Pair this with valid access in both tenants. Distinct users or versions alone can hide a missing tenant key. Use the same reasoning for scoped idempotency keys, partition offsets, or role checks; do not force equality where the contract requires a difference.

For partial-failure recovery, start from a successful prefix: commit or acknowledge one item, fail a later item, reopen the durable state where restart is part of the contract, and retry. Assert that earlier successes remain durable, failed or pending work remains eligible, and retry processes only what the contract allows. Check final cardinality and business values, not only a callback count. Also retain a before-any-success case when its rollback mechanism differs. An injected exception at a documented seam is not evidence of process-kill or power-loss recovery.

Match adversarial inputs and copy tests to the public boundary. A native-object API promising validation errors should see invalid types that can fail before validation, such as serialization-incompatible values; a JSON-only wire boundary cannot receive those native objects and needs malformed or wrongly typed JSON instead. Do not invent a required exception class when the contract leaves it unspecified. For an isolation promise, return a supported nested dictionary or list, mutate a nested field, and reread the observable state with an independent expected value. Replacing a scalar in the outer container cannot distinguish a shallow copy from a deep copy. When an error reveals a product defect, preserve the justified regression in a tests-only task.

Select a few sequences from the actual risks rather than multiplying all states and inputs. During review ask: what other condition could still make this pass if the boundary were removed; what changes after an earlier item has succeeded; and would a shallow copy or reordered validation still pass? Use bounded isolated sensitivity checks when those questions expose a concrete uncertainty.

## Choose a boundary that preserves the failure mechanism

Use fast in-process tests for pure decisions. Use component or service integration tests when framework wiring matters. Use the actual engine when SQL semantics, transactions, browser layout, or message delivery matter. Add a small number of complete journeys for assembly and product outcomes.

Record dependencies and execution scope instead of arguing about names such as “unit” and “integration.” Test pyramid proportions and historical size budgets are heuristics, not universal gates. See [S01–S03](sources.md#strategy-and-ai-generated-tests).

## Test doubles and fixtures

- Substitute a dependency at an owned seam when its behavior is irrelevant to the assertion or needs controlled failure injection. Keep the subject's decision logic real.
- Prefer observable results over interaction assertions. Call counts or order are useful when the interaction itself is the contract, such as suppressing duplicate effects; they are weak substitutes for verifying a durable result.
- Treat a fake's behavior as an assumption. For material integrations, verify it against a contract or a real adapter test. A mocked database cannot validate database semantics.
- Construct only the state relevant to the case. Make decisive values explicit even when using a fixture builder. Avoid fixtures that silently create administrative users or permissive feature flags.
- Isolate clocks, locale, time zone, random seeds, temporary paths, environment variables, and global state as applicable. Use distinct test namespaces and guaranteed cleanup for persistent resources.
- For eventual consistency, poll a meaningful observable condition with a deadline. Check invariant violations during the interval when they matter. Arbitrary sleeps and repeated whole-test retries hide causes.

See [S08](sources.md#strategy-and-ai-generated-tests) for flaky-test causes and [S17–S19](sources.md#backend-and-contracts) for contract limitations.

## Property-based, model-based, and fuzz testing

State why the property should hold and its valid domain before writing a generator. Examples include conservation, monotonicity, idempotence, ordering plus element preservation, and equivalence under a semantics-preserving transformation. These are candidates, not assumptions: discounts need not be monotone and message order need not be irrelevant.

Generate structured valid data directly; use a separate strategy for invalid inputs. Excessive filtering can leave a supposedly broad test nearly empty. Retain readable example tests for product-critical boundaries.

For stateful behavior, maintain a simpler independent model of allowed operations and state. Generate action sequences and compare observable results after each step. Do not port the production algorithm into the model. Capture the shrunk counterexample, replay seed or path, and relevant tool version. Promote a meaningful discovered bug to a stable regression case.

Fuzz only scoped targets with time, input-size, memory, and side-effect limits. Preserve failure corpora. Use the language's existing sanitizer or runtime diagnostics where relevant. See [S09–S12](sources.md#generative-techniques).

## Targeted mutation and red/green evidence

Choose a plausible fault connected to a requirement: changing an inclusive threshold, removing an authorization predicate, dropping a rollback, or duplicating a durable write. Prefer the existing mutation tool. Otherwise use a disposable copy containing the current relevant changes; do not reset the working tree or lose uncommitted work.

1. Establish that the relevant baseline passes, or isolate documented pre-existing failures.
2. Apply one understood fault in the isolated environment and run the intended test.
3. Check that the test fails for the intended behavioral reason, not an import, syntax, discovery, or unrelated fixture error.
4. Restore the original isolated implementation and verify the test passes again. Keep mutant code out of the deliverable.

Investigate surviving mutants: missing case, weak assertion, unreachable behavior, equivalent change, or insufficient harness. Report scope, tool definitions, and exclusions. Some tools count timeouts as detected; a timeout is not equivalent to a checked semantic assertion. Compilation failures do not establish behavioral sensitivity. Mutation scores compare a tool's chosen fault model, not all possible defects. See [S06–S07](sources.md#strategy-and-ai-generated-tests).

For a justified test that reveals an existing bug, a red result is useful evidence. Do not demand a green baseline by encoding the bug as correct. State whether the task includes the production fix.
