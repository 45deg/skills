# Review and refactoring cases

Read the case that matches the proposed change. These checks apply to the actual contract; they do not introduce new requirements.

## One change requires coordinated edits in several places

Choose a change grounded in the request or actual maintenance history. Trace the implementation, callers, shared state, configuration or registrations, and tests that must change with it. Check whether a maintainer can discover those relationships from the code and contracts, rather than having to remember an unwritten checklist.

Distinguish a hidden shared policy from code that changes for independent reasons but is tied through shared internals or an overly broad interface. Make a required relationship explicit, or separate independent responsibilities, where that reduces real maintenance burden. Similar syntax, folder proximity, or the number of files touched does not decide which boundary is useful. External contracts and generated artifacts can legitimately require coordinated updates.

## Several symptoms may share a missing responsibility

Before patching each symptom separately, ask whether duplicated decisions, caller-specific flags, ordering conventions, or timing workarounds come from the same missing contract or unclear owner. Confirm that causal connection in the actual execution and requirements before proposing one fix for the group.

A special case can encode a real domain rule or external constraint. Preserve such distinctions; the number of branches or workarounds is not itself a quality measure. Choose the smallest authorized change that addresses the established cause. Do not force independent policies into one abstraction or turn a targeted fix into a codebase-wide redesign.

## A structural proposal needs evidence and a reviewable decision

Use relevant import or call relationships to locate dependencies, then inspect state access, registration, and execution paths that a static graph may omit. Where useful, inspect Git history for repeated coordinated edits and their reasons. Co-occurrence in one commit does not prove a shared responsibility, and absence of co-change does not prove independence.

Keep a compact decision record: affected files or symbols, the required relationship or suspected common cause, supporting evidence and uncertainty, the proposed boundary change, and behavior and checks to preserve. An inline explanation suffices for a small task; use existing project notes for a larger change rather than imposing a new document format. A review records a supported proposal; an authorized fix implements it.

After a fix, trace the same change scenario again. Check that the dependency became explicit or unnecessary coupling was removed, rather than merely moved behind another helper. Verify preserved behavior at the affected boundaries.

## A cleanup changes when work happens

Moving a guarded call into an eager assignment can make it execute, fail, or consume resources on paths that previously skipped it. Check both truth conditions and evaluation behavior when rewriting conditions or defaults.

Consolidating repeated reads of a clock or mutable object can change which state is observed. Preserve an intentional snapshot, and keep separate observations when the contract depends on different instants. Reordering corresponding fields or arguments must preserve dependency and evaluation order.

## An operation appears unused or replaceable

A text search alone may miss configuration, registration, reflection, or external consumers. Establish how a public identifier, serialized field, or command-line option is used before deleting or renaming it. Add a compatibility layer only when actual consumers require one.

Before replacing an implementation with a standard facility, database operation, or existing dependency, compare data types, ordering, multiplicity, encoding, and failures. Less code does not compensate for an unnoticed contract change.

## Extraction adds navigation without isolation

Compare the original caller with the proposed caller and helper. An extraction earns its boundary when it removes distracting detail or establishes a useful contract, including for one caller. A chain of forwarding functions, or a helper that reaches back into caller state, may leave readers with more definitions to visit and the same facts to remember.

Keep the helper with the concept it serves; reuse does not require a shared utility module. Splitting files or classes does not isolate responsibilities if they still inspect and modify each other's internals.

## Test helpers conceal the claim

Make it apparent whether a helper constructs data, invokes the operation, or performs assertions. Keep the behavior-defining setup and expectation visible; use existing parameterization or small builders before inventing a test notation.

Simplifying fixtures must preserve the input differences that distinguish plausible defects. Descriptive failures should expose the case, input, and expected and observed results. A mock that bypasses authorization, persistence, or a network boundary cannot establish that boundary's behavior.

Extensive global initialization for a small unit can indicate a dependency problem. Make time, randomness, and effects controllable where needed without adding public test-only methods or mutable switches. Multiple assertions can support one behavioral claim; split cases when they represent independent claims.

## An optimization moves cost or weakens guarantees

Compare a clear baseline with the actual workload and resource constraints. Distinguish measured improvements from analytical expectations. For sustained work, examine growth with input rate and elapsed runtime, not only one small invocation.

If aggregation, sampling, or rounding discards information, establish whether the contract permits that loss. More code may meet a real constraint, but account for retained state and interactions between the new pieces. Do not introduce a cache, retry subsystem, or future extension point as a readability cleanup.

## Parallel work changes completion and cleanup

Replacing sequential work with `Promise.all` changes scheduling even when results retain their input order. Check shared writes, rate limits, ordering assumptions, and what remains in flight after a failure. Establish which operation owns success, failure, cancellation, and cleanup.

For an existing retry policy, make eligible failures, limits, deadlines, cancellation, and repeatable effects understandable. A cancellation path must preserve required resource release, transaction handling, and reporting.
