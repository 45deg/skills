# Review AI-generated tests

Apply this review to the changed tests. Its purpose is to catch false confidence, not to require a separate audit project.

| Failure pattern | Diagnostic question | Correction |
| --- | --- | --- |
| Implementation copied into the oracle | Would the same bug appear in both expected and actual values? | Derive a literal example or property from an independent requirement |
| Current bugs frozen as requirements | What justifies the asserted behavior? | Separate characterization from correctness and expose ambiguity |
| Incidental values frozen as requirements | Could another implementation satisfying the contract fail because of an ID, timestamp, order, or storage-layout assumption? | Assert specified values exactly and unspecified values through their required relationships; retain independent business-field expectations |
| Assertion-free exercise | Which incorrect result would fail this test? | Assert the product result and relevant state changes |
| Subject mocked away | Does real production logic execute? | Move the double to the external boundary |
| Overbroad matchers | Could a wrong amount, owner, or state still pass? | Assert decisive fields exactly; allow flexibility only where the contract does |
| False-positive negative test | Could an unrelated error satisfy the assertion? | Verify the intended rejection and unchanged state; assert an error class or code only when the contract specifies it |
| Missing asynchronous failure | Can the test finish before the operation or assertion? | Await completion and ensure rejection reaches the runner |
| Snapshot laundering | Was the changed output independently reviewed? | Inspect the difference before accepting a baseline |
| Hidden permissive fixture | Does setup bypass the behavior under test? | Use explicit identity, state, and policy inputs |
| Accidental protection by another condition | Would distinct users, versions, or epochs hide a missing tenant or other scope check? | Hold unrelated relevant conditions equal, vary the protected boundary, and keep independently different observable data |
| Recovery checked only before any success | Does a later failure preserve an already committed or acknowledged prefix? | Establish prior success, fail subsequent work, reopen and retry when supported, and assert durable effects and remaining work |
| Adversarial fixtures shallower than the contract | Would validation after serialization or a shallow returned copy still pass? | Exercise supported invalid representations and nested data at the public boundary; assert the declared error and independent state |
| Hallucinated tooling | Are the API, import, flag, and version present? | Inspect installed versions and repository examples before adapting code |
| Non-discovered test | Did the runner actually execute it? | Check discovery, selection, counts, and runner output |
| Retry-based green result | What caused the first failure? | Diagnose and retain flakiness evidence rather than suppress it |
| Coverage gaming | Does the assertion evaluate the executed behavior? | Add discriminating cases; do not merely execute lines |
| Unbounded generation | Does each new case protect a distinct risk? | Stop when prioritized risks are addressed or explicitly deferred |

Reject tests that pass vacuously, rely on incidental timing, or assert only their own stubs. Do not infer confidence from test names, assertion counts, or generated explanations.

## Acceptance questions

- Can a reviewer trace the decisive expected value to a requirement or justified invariant?
- Could a requirement-preserving implementation change fail these assertions? If there is a concrete coupling risk, check a bounded valid variant separately from fault mutations.
- Does the chosen environment preserve the failure mechanism?
- Would a plausible wrong implementation fail, and what evidence supports that answer?
- Are setup, effects, isolation, and cleanup visible enough to explain a failure?
- Does the report accurately distinguish implemented, executed, failed, and blocked checks?

For a trivial test, these questions can be answered briefly. A payment transition or data migration deserves stronger evidence. A second pass can challenge the first pass's assumptions, but is not independent validation when it reuses the same inferred oracle.

The empirical research supports filtering and evaluating generated candidates, while leaving oracle validity and generalization as important limitations. See [S04–S06](sources.md#strategy-and-ai-generated-tests).
