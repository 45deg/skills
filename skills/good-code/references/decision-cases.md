# Decision cases

Use the case that matches the difficulty in the current task. Examples illustrate stated contracts; they do not add requirements to the user's project.

## A harmless-looking cleanup changes behavior

Before renaming or substituting an operation, inspect consumers as well as local syntax. Public identifiers, serialized fields, command-line options, and dynamic registrations may remain in use even when a text search finds few references. Do not add a compatibility wrapper automatically, but do not silently break consumers either.

For measurements, establish the unit and representation. For a threshold, establish which side owns equality. For a range or time window, establish whether endpoints are included and whether the window follows calendar boundaries or a trailing duration. Express the distinction through the project's naming, types, or a concise contract. An identifier is a clue, not proof that the implementation follows it.

A name should distinguish the operation from plausible alternatives: requesting work is different from completing it; reading a stored value is different from computing or fetching it. If two independent settings have been combined under a vague label, clarify their responsibilities instead of searching for a broader label.

For data, identify what the value represents. Labels that say only "result" or "temporary" need enough local context to make the value's purpose apparent.

Include details such as encoding or validation state when confusing them would matter. A reassuring name does not make input safe. Avoid local jargon and redundant words. Ordinary abbreviations and short index names can be adequate in a small, obvious context; several interacting indices may require distinct roles. Follow existing capitalization and visibility conventions rather than inventing prefixes.

Make a boolean identifier state what a true value asserts, and check whether its false case produces a confusing double negative. Affirmative wording often helps, but a particular prefix is not mandatory. Names used across a wider scope need enough context to remain informative away from their definitions.

## A condition is difficult to verify

Name a meaningful decision or intermediate result when that lets readers reason about the domain instead of repeatedly decoding object access or arithmetic. A value does not have to be long or reused to deserve a name. Remove a temporary only when its absence makes the operation at least as clear.

When repeated expressions or literal values encode one policy, consider giving that policy one definition so that edits cannot accidentally diverge. Keep unrelated policies separate even when their current values happen to match.

Do not move a guarded call into an eager assignment without checking what can now execute, fail, or cost more. Similarly, consolidating repeated reads of a clock or mutable object can change when values are observed. Preserve an intentional snapshot rather than treating it as redundant state.

If enumerating accepted cases becomes complicated, try expressing the disqualifying cases, or divide the decision into independently understandable steps. Select branch order by what resolves the reader's uncertainty soonest: an exceptional case may be more useful up front than the normal path. Do not enforce positive conditions at the cost of a worse structure.

An easily dispatched case may belong first so that it no longer distracts from the rest. Where two arrangements are equally direct, prefer the one that avoids an extra mental negation. Read a comparison as a question about a value against a baseline, and order its operands naturally for that question. Equivalent boolean rewrites can help; verify both their truth conditions and their evaluation behavior.

Keep concise conditionals for simple alternatives. Expand nested choices or combined mutations when they require mental simulation. Boolean operators can legitimately express guards and defaults; establish whether zero, an empty string, or false is an allowed value before replacing a missing-value check with a truthiness check.

For example, assume delivery state and attempt counts have already been validated. A delivery is eligible only while ready and while its used attempts remain below the supplied budget:

```ts
type Delivery = {
  state: "ready" | "sent";
  attemptsUsed: number;
};

function maySendDelivery(delivery: Delivery, attemptBudget: number): boolean {
  return delivery.state === "ready" && delivery.attemptsUsed < attemptBudget;
}
```

With a budget of three, a ready delivery with two used attempts is eligible; one with three is not. A sent delivery is ineligible regardless of its remaining budget. These cases check separate parts of the contract. Changing the comparison, treating all states alike, or calling a sending API inside this predicate would require a different justification than a naming cleanup.

## Readers keep losing their place

Look at the complete operation, not just the recently inserted lines. Identify the small jobs it performs and group related work so that one calculation or policy can be followed without alternating between several others. Spacing and a brief section comment may suffice.

When a distinct piece of processing distracts from the caller's purpose, move it behind a boundary with an understandable contract. It can be useful even for a single caller or for project-specific behavior. Do not require an extracted operation to move into a shared utility module.

Compare the cost on both sides of an extraction. Does the caller have fewer details to remember? Does the new function receive reasonable inputs and avoid reaching back into caller state? A chain of names that merely forwards the same work adds navigation without buying isolation.

If the structure still feels arbitrary, explain the operation to a colleague in ordinary language. Use the concepts in that explanation to decide what belongs together, then examine those groups in the same way. Do not force every sentence into a new function.

Use repeated visual patterns where they help compare related cases. Local tables or aligned values may expose mistakes, but respect formatter behavior and avoid whitespace churn. Reordering for appearance must not change dependency or evaluation order.

When operations mention corresponding fields or arguments, retain a useful ordering across them unless dependencies require otherwise. For choices that are purely stylistic, follow the repository's established pattern instead of introducing a competing one.

## Local edits depend on distant state

Check whether a field or global exists only to carry a value from one operation to another. A parameter or local result may make that dependency explicit and reduce the code that can alter it. Splitting files or classes achieves little isolation if they still inspect and modify each other's internals.

Keep definitions within the narrowest useful scope, subject to the language's initialization and lifetime rules. Prefer a binding that is assigned once where practical, while remembering that its referenced object may remain mutable. Setting a default and updating it through an obvious preference sequence can be clearer than a complicated immutable expression.

Use an immediate return or loop exit when it removes a bookkeeping flag that only delays a decision already made. Keep flags that represent actual domain state. In independent per-item processing, an early skip may keep the remaining work clearer.

Make a loop's admission and stopping rules easy to find. Showing the condition before the body often avoids a second reading; keep ordinary traversal recognizable and handle exceptional stopping rules explicitly when that helps. Preserve resource release and required reporting on every exit. Use the language's resource-management facilities and retain clear established cleanup idioms where appropriate. Do not duplicate a loop body merely to move its condition, or change whether it runs at least once.

## Callers need information the interface does not reveal

Fix a misleading name or unnecessarily complicated operation before adding an explanation that compensates for it. Still, an explanation can be worthwhile even if a determined reader could eventually derive the same fact. The useful question is whether it saves effort or prevents a realistic misuse.

Document constraints that are easy to overlook: an expensive call, ownership, a surprising failure mode, a chosen approximation, or the reason a tuned value should not be casually changed. Add a brief overview when module responsibilities or data movement would otherwise require a tour from the author.

Choose an overview, an explanation of the mechanism, or a rationale according to the uncertainty readers face. Avoid narrating what is already obvious. A small example can distinguish cases that prose leaves ambiguous. Remove vague referents and unnecessary wording without dropping qualifications. When stuck, draft the intended meaning first and revise it for precision.

Where literal arguments remain confusing and the API offers no named alternative, a compact label before the value can help. Keep it unambiguous which parameter the label describes. Do not require this for every call.

When an explanation contradicts the implementation, determine the intended contract before changing either one. Keep acknowledged limitations and concrete follow-up conditions visible without adding a TODO for every possible improvement.

After an edit, recheck affected explanations and examples for accuracy. A formerly correct comment can become misleading when a boundary, default, or implementation choice changes.

## Test changes are harder to review than the implementation

Put the behavior-defining situation, action, and expectation in view. Move irrelevant construction into a small helper when that exposes what differs between cases. Use existing parameterized-test facilities, literals, or small builders before inventing a notation that needs its own parser.

Helper abstraction should reduce repetition without concealing the claim under test. Make it apparent whether a helper constructs data or performs assertions. Multiple assertions can belong to one behavioral claim; multiple independent claims may deserve separate cases.

Choose compact inputs that discriminate among plausible wrong results. Include empty input, zero, duplicates, and exact boundaries when relevant. Simplifying numbers or fixtures must not eliminate the distinction the test is meant to check. Generate large inputs reproducibly for a distinct load or stress objective rather than burying ordinary examples in huge fixtures.

Failures should reveal which case ran, the relevant input, and the expected and observed results. Use descriptive test names and informative assertions. Do not hide a failed condition behind an unhelpful boolean result when the underlying difference can be shown.

Derive expected results independently from the requirement. An implementation and its copied logic in a test can agree while both are wrong. Mocks that bypass authorization, persistence, or a network boundary cannot establish that boundary's behavior.

If a small unit needs extensive global initialization or external setup, revisit the dependency boundary. Make time, randomness, or external effects controllable where necessary without adding large frameworks, public test-only methods, or mutable switches. Keep coverage requirements and verification effort proportionate to existing project gates and failure impact.

## An adapter or replacement promises less code

An adapter is useful when it absorbs awkward preparation, conversion, or cleanup and presents callers with a stable operation. It should not conceal consequences callers must handle, including important failures. A wrapper that only changes the spelling of a call needs a stronger reason to exist.

Check standard libraries, existing dependencies, database operations, and available command-line tools before implementing another mechanism. Verify that a replacement preserves data types, ordering, multiplicity, encoding, and errors. A shorter expression is not an improvement if those contracts change unnoticed.

Do not build future extension points solely because a second use seems imaginable. Conversely, do not merge two rules only because today's implementations match. The useful boundary follows the responsibilities that can change independently.

Unused-looking code may still be reached through configuration, registration, or external consumers. Establish its status before removing it. Propose a smaller requirement when it would meet the user's actual need, but never silently remove supported behavior or safety constraints.

## An optimization moves cost or weakens guarantees

Compare a clear baseline against the actual workload and constraints. Consider computational work, memory growth, accuracy, and the cost of maintaining additional state. State whether a claimed gain comes from analysis or measurement.

For sustained workloads, assess growth with input rate and elapsed runtime, not just one small invocation. If aggregation or rounding reduces cost, define what information is lost and whether that loss is permitted. Sampling a clock once can keep one logical operation consistent and make it easier to reproduce, but do not collapse observations that intentionally refer to different instants.

More implementation code can be acceptable when it establishes clearer responsibilities and meets a real resource constraint. Also account for the complexity of interactions between the new pieces. Requirements about precision, retention, or supported inputs need confirmation before an optimization changes them.

## Work finishes through callbacks or concurrent paths

Identify where work is registered, when it can run, and which operation owns success, failure, and cleanup. Events, exceptions, and dynamic dispatch are useful mechanisms; clarify their paths instead of banning them.

Replacing sequential work with `Promise.all` changes scheduling even if returned results retain their order. Check shared updates, rate limits, ordering assumptions, and partial failure. A cancellation path must not abandon required cleanup, transaction handling, or audit events.

For a retry policy that already belongs to the task, make eligible failures, limits, deadlines, cancellation, and repeatable effects understandable. Do not create a retry subsystem or cache as a readability improvement.

## The patch grows beyond the problem

Remove unrelated formatting, renaming, and speculative improvements from the diff. Separate larger authorized cleanups into changes a reviewer can reason about, without imposing a fixed number of commits.

Explain a finding through an actual consequence. A changed admission rule can be a defect; an ambiguous unit can be a maintenance risk; choosing one familiar loop style over another may merely be a preference. Do not present all three with the same severity.

When the operation is already understandable and the requested behavior is satisfied, stop. A suggestion is useful only if its benefit exceeds the extra code, concepts, and review burden it introduces.
