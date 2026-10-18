# Modeling existing systems

## Extract behavior

Inventory operations relevant to the property: inputs, state read/written, preconditions, outcomes, and intervention points. Inspect callers, error branches, tests, and concurrency/persistence boundaries instead of translating the whole repository.

| Input | Extract | Avoid |
| --- | --- | --- |
| Code | State holders, calls, awaits, locks, transactions, callbacks, recovery | Treating a function as atomic |
| Protocol | Roles, messages, phases, thresholds, failure and delivery guarantees | Filling unspecified behavior with optimistic defaults |
| State chart | Initial/terminal states, guards, effects, rejected events | Assuming omitted events cannot arrive |
| Existing `.qnt` | Instances, actions, properties, assumptions, domains, source correspondence | Trusting historical passes after source changes |

An API rejection may update persistent deduplication or response state. Model it as an observable outcome when relevant. A disabled action means no transition occurs; it is not automatically equivalent to an error response.

## Preserve interference

For read-check-write, identify whether the implementation prevents intervening changes. Otherwise preserve observation in actor-local state, permit interference, and model actual commit logic. A single guarded atomic update cannot expose stale-check races.

Establish lock scope: a process-local mutex does not serialize independent processes/database sessions. Inspect transaction isolation, uniqueness constraints, compare-and-swap, and rollback. A transaction alone does not imply serializability.

For crash recovery, distinguish volatile/durable state and write/ack boundaries; include intervening crashes when needed. Cancellation, timeout, retry, and completion can be independent events. Wall-clock calls across actors do not establish a total order.

## Preserve relevant data behavior

| Concern | Representation choice | Required justification |
| --- | --- | --- |
| Actor-local phase/metadata | Record or actor-to-record map | Identities/roles preserved, all actors initialized |
| Unordered unique pending events | `Set[Message]` | Duplicate identical events irrelevant or identity distinguished |
| FIFO events | Lists or per-channel lists | Actual FIFO boundary, empty-queue guards |
| Redelivery | Counts or event IDs | Consumption, loss, and repeated delivery semantics |
| Idempotency | Request-ID-to-result map | ID repetition, retention, crash behavior |
| Fixed-width arithmetic | Explicit bounded arithmetic | Overflow is source behavior, not a shortcut |
| Deadlines | Logical time or abstract timeout | Preconditions/reset/races; lost quantitative timing claims |

Use small instances admitting the failure mechanism: competing actors for exclusion, repeated IDs for deduplication, and relevant quorum intersections for agreement. Explain each size; passing several sizes does not prove a cutoff theorem. Keep IDs opaque unless their arithmetic/order is contractual.

Overapproximations can produce spurious traces; underapproximations can hide bugs. Explain preservation of the target property where possible. A correspondence table is not a formal refinement proof.

## Review the oracle and reachability

Use requirements independent of update logic. Type/bounds checks may pass while assigning results to the wrong owner; conservation, ownership, and prerequisite relations can be the actual promise.

Inspect all relevant initial states, distinguishing clean start from recovery over durable state. Omitted environment actions are absent from every checked execution. Ensure transition witnesses are false at initialization and cannot fire through unrelated actions. Model-only monitors must not restrict system behavior; unbounded histories prevent finite-state exploration.

When a witness is not sampled, inspect selection, bounds, initialization, and enabled transitions before changing guards or properties. Use a focused scenario or reaching-trace query. Negating a target as an invariant is a reachability query: its violation is success for that query.

Preserve current/proposed systems in separate instances or modules with the same property. State which variant matches source. Model-based replay needs explicit state projection, action/input mapping, and treatment of implementation stuttering. It provides conformance evidence for exercised paths; a refinement proof needs separate initial-state and transition obligations.
