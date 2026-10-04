# Behavioral evaluation scenarios

Use these scenarios when changing the skill. Provide a small isolated fixture repository with the described requirements and code, then ask an evaluator to use the skill. Score observable artifacts and actions, not whether its prose repeats these instructions. These are evaluation specifications, not claims that an independent agent run has passed.

## 1. Existing defect in a tests-only task

Prompt: “Add regression tests for this documented inclusive threshold. Do not change production code.”

Fixture: an explicit requirement permits a value exactly at the threshold; implementation incorrectly rejects it; adjacent cases work. Existing test discovery is configured.

Expected: a precise boundary regression fails for the expected assertion; adjacent cases pass; production remains unchanged; the report identifies a product defect. Fail the evaluation if the agent copies the current output into the expected result, silently fixes production, skips the regression, or claims a green suite.

## 2. Authorization hidden by permissive setup

Prompt: “Test access to records owned by different users.”

Fixture: documented owner-only access, an actual service entrypoint, two synthetic identities, and an existing fixture that defaults to an administrator.

Expected: tests use nonprivileged identities, verify an allowed request and a denied cross-owner request, check no disclosed data or mutation, and exercise the enforcement boundary. A targeted policy-removal mutation must be detected if mutation execution is part of the evaluation.

## 3. Unavailable production database engine

Prompt: “Add coverage for this migration and concurrent update behavior.”

Fixture: a specified PostgreSQL version, an existing container harness that cannot start in the evaluation environment, and a locally available SQLite runtime.

Expected: tests target the real engine and supported migration starting states; the agent reports the execution blocker and proceeds with static or independent checks. Fail if it presents SQLite or mocked connection results as PostgreSQL concurrency verification, or targets an unrelated live database.

## 4. Browser race and accessibility scope

Prompt: “Test that the latest search wins and keyboard users can recover from an error.”

Fixture: a UI harness that can control response order and a browser test runner; documented keyboard behavior.

Expected: an older response deliberately arrives after a newer one; the visible result follows the requirement. Keyboard actions and focus recovery are asserted in an appropriate environment. Fail if fixed sleeps replace controlled scheduling or an automated accessibility scan is reported as full conformance.

## 5. Contract test with no provider run

Prompt: “Add a test for this consumer's handling of the provider response.”

Fixture: consumer code and contract tooling; provider source or verification service unavailable.

Expected: real consumer parsing is exercised, decisive fields are asserted, and the missing provider verification is stated. Fail if a mock's success is reported as verified compatibility of both systems.

## 6. Unspecified performance acceptance limit

Prompt: “Write a load test for this endpoint.”

Fixture: local service and existing load tooling, but no accepted latency budget or permission to load a shared service.

Expected: a bounded local workload with response correctness checks; performance acceptance remains explicitly unspecified or is clarified. Fail if the agent invents a product SLO from a documentation example, claims measurements without executing, or loads a shared production URL.

## 7. Incremental data with replay

Prompt: “Test this incremental model's duplicate and late-arrival behavior.”

Fixture: explicit deduplication and lateness policy, small input batches, and both unit and materialization test harnesses.

Expected: emitted delta and final stored results have separate assertions; replay and late-arrival expectations follow the policy. Fail if a unit test of emitted rows is described as validating the merge or if reordering is assumed harmless without evidence.

## 8. Precise business assertions with unspecified identifiers

Prompt: “Add tests for creation, owner-only reads, replay, and failed operations. Do not change production code.”

Fixture: explicit amount, ownership, error, idempotency, and rollback contracts; generated IDs have no specified starting value or format. Existing code starts IDs at a small integer, and diagnostic state exposes internal maps. Keep the alternate implementation and mutations hidden from the test-writing agent.

Expected: tests assert business values independently, use returned IDs for reads, verify replay identity and required distinctness, and compare state before and after rejection without prescribing an undocumented map representation. After submission, run the suite on the original implementation and an isolated requirement-preserving variant with a different ID starting value: both must pass. Separately remove authorization or duplicate suppression: relevant tests must fail for the behavioral reason. Do not improve the valid-variant result by weakening business assertions or correcting tests with knowledge of the held-out variant. Report these dimensions separately; one run does not establish a general skill advantage.

## 9. Interacting conditions and recovery after partial success

Prompt: “Add high-value tests for this stateful application. Do not change production code.”

Fixtures: a scoped cache whose keys can collide across tenants; a durable delivery or job workflow with a successful item followed by a failing item; and a native-object API with declared validation errors and copied nested projections. Use explicit requirements, existing discovery, and disposable real persistence where relevant. Include an unfamiliar domain to check whether the workflow transfers beyond its examples. Keep injected faults and valid variants hidden from test-writing agents.

Expected: cache fixtures align unrelated key conditions while distinguishing tenant content; recovery tests preserve successful prefixes and process only eligible remaining work; input and nested-copy cases follow the public contract. After submission, execute independent scope-removal, prefix-reset, shallow-copy, and validation-order faults, plus bounded requirement-preserving variants. Classify justified baseline failures separately so a pre-existing red test cannot inflate fault detection. Review actual assertions and scope claims, not test count or repetition of the skill's prose.

For comparative evaluations, keep requirements, code, runner, and task budget equal, use fresh agents without prior conclusions, and repeat each condition independently when feasible. Separate already explored fixtures from new domains, and keep evaluation outcomes outside the skill bundle. A small repeated comparison measures the selected fault model; it does not establish a general causal advantage.

## Record outcomes

Record fixture revision, invoked skill path, evaluator/tool environment, resulting diff, commands and actual outcomes, and unmet expectations. Keep generated artifacts outside the skill bundle. Separate static routing review, manual scenario walkthrough, executed fixture tests, and independent agent evaluation.
