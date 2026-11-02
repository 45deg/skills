# Construction examples

Use the relevant case only. Examples are original design sketches, not executable code or project requirements.

## Start with a call

Define what a caller needs before inventing a manager or framework:

```text
copy_file(source, destination, if_exists = FAIL)
Returns: information about the copied file
Failures: unreadable source, existing destination, write failure
Specify: whether failure can leave a partial destination
```

Without named arguments, consider an enum, meaningful options record, or distinct operation name. Prefer an existing standard API when it fits. Do not mirror its entire interface in a wrapper without a useful contract.

## Represent valid states

Independent `done`, `failed`, `result`, and `error` fields make callers remember valid combinations. Consider:

```text
JobState = Pending | Succeeded(value) | Failed(error)
```

Use a sum type where available, or tagged values with validated construction. Preserve the invariant through serialization. An existing result convention may suffice for simple success/failure.

For quantities, expose consequential semantics: currency and rounding, instant versus duration, units, time zone, or coordinate system. Choose the lightest effective combination of standard types, domain types, names, and documentation.

## Name processing stages

Suppose the specified pricing rule applies a discount before tax:

```text
subtotal = sum(line_total(item) for item in items)
discount = calculate_discount(subtotal, policy)
taxable_amount = subtotal - discount
tax = calculate_tax(taxable_amount, tax_rule)
total = taxable_amount + tax
```

These names expose stages; `temp1` would not. Currency and rounding belong in the actual contract. This example does not prescribe a tax rule. Keep a simple expression intact when staging adds no meaning; keep saving or sending outside expressions that appear to be calculation alone.

## Choose branches, tables, or matching

A fixed code-to-label mapping fits a table with a defined missing-key policy. Ordered decisions should expose precedence:

```text
if not authenticated: return UNAUTHENTICATED
if not valid:         return INVALID
return ACCEPTED
```

An unauthenticated, invalid request returns `UNAUTHENTICATED`; order is part of this contract. Use matching or symmetric branches for exclusive states with different data. Use guards to dispose of independent exceptional cases. Neither form is universally preferable.

## Choose iteration by intent

Use familiar map/filter/existence operations when they directly express the task. A loop may be clearer for coordinated accumulators, early exit, or resource handling. Avoid `map` solely for effects or a large fold that conceals changing state.

Check empty inputs, order, eager versus lazy evaluation, early termination, and memory use. Equivalent-looking forms need not have equivalent execution behavior.

## Choose processing phases by observable guarantees

For a pure batch planner, validating and processing one item at a time can avoid retaining a second normalized batch. If all updates remain private and failure returns no result, an error on a later item does not expose earlier updates.

A separate validation phase is useful when it creates a reusable representation, simplifies a substantial algorithm, or must precede external effects. Validation alone does not make later writes atomic: failures during execution still need the specified transaction or recovery behavior.

Within either structure, check all prerequisites for an all-or-none operation before committing its changes. Prefer the structure that makes the actual guarantee easiest to verify.

## Let context carry its share of naming

A nearby `total` may be clear; a cross-module result may need `invoiceTotal` or a meaningful result type. Do not repeat what the namespace already says.

Use corresponding vocabulary: `source`/`destination`, `minimum`/`maximum`. Distinguish counts from indices and identifiers from entities where confusion matters. Declare values at the stage that uses them, while respecting language and repository declaration-order conventions.

## Preserve useful failure distinctions

```text
Found(user)       -> use the user
NotFound          -> follow the specified absence policy
Unavailable(err) -> report or handle operational failure
```

Implement these distinctions using the language's conventions, not necessarily three custom variants. An empty user must not disguise a failed lookup.

Validate at trust boundaries and rely on established invariants internally. Reassess assumptions at persistence, service, or concurrency boundaries rather than copying identical defensive checks into every function.

## Adapt the principle to the language

| Goal | Possible idioms | Avoid imposing |
| --- | --- | --- |
| Group related data | Records, structs, classes, maps, row types | Classes everywhere |
| Express alternatives | Sum types, enums, tags, matching, branches | Polymorphism everywhere |
| Express transformation | Loops, higher-order operations, pipelines, SQL | Always loops or always chains |
| Bound resource lifetime | RAII, with/using, defer, finally, explicit release | Assuming GC releases every resource |
| Report failure | Exceptions, results, error values, exit status | One universal error abstraction |

In SQL, name intermediate relations where useful and account for join multiplicity, NULL, and ordering guarantees; do not impose procedural execution order. In shell, preserve argument boundaries, quoting, and exit status. Verify concrete semantics against the target implementation.

## Explain purpose before mechanics

Suppose a verified provider contract deduplicates retries only when they reuse the original key:

```text
# Reuse the original key so the provider treats this retry as the same request.
send(request, idempotency_key = original_key)
```

“Send the request” adds nothing. The useful comment records the constraint that a future edit could violate. Add the real specification link when available; do not invent one or assume this behavior for other providers.

For a caller-facing operation, give a brief purpose and any consequential contract details the signature does not convey. For example, if established by the implementation and requirements:

```text
Returns records in [start, end), ordered by timestamp.
An empty result means no matches; storage failures propagate.
```

If invalid inputs and arithmetic overflow use different public error categories, document and test that distinction. If callers need no distinction and project conventions allow it, a single documented category can suffice. Do not let different branches accidentally define the error policy.

For a difficult loop, explain the invariant that supports the next step, rather than narrating each assignment. For a workaround, state the affected condition and when it can be removed. Keep explanations local and specific; a bare issue URL or “temporary fix” leaves the reader guessing.

## Give the reader a map with ASCII

For a reservation planner, a short overview can connect readable statements into a coherent operation. This diagram describes per-request planning on private state, not a transaction spanning external services:

```text
// Decide whether the whole request can be fulfilled before consuming stock.
//
// items -> combine repeated SKUs -> collect shortages
//                                      |
//                         +------------+------------+
//                         |                         |
//                    any shortage              no shortages
//                         |                         |
//                    reject request             deduct totals
//                    stock unchanged            accept request
```

A decision table can clarify failure categories without asking the reader to reconstruct all branches:

```text
// Preserve the distinction between invalid input and an unfulfillable request.
//
// Condition             | Outcome        | Stock effect
// ----------------------+----------------+-------------------
// malformed input       | throw          | no external effect
// valid, any shortage   | reject request | unchanged
// valid, no shortages   | accept request | deduct all totals
//
// The planner works on private stock; throwing returns no partial plan.
```

Use a diagram for flow, a table for case comparison, or a range sketch for boundaries. Do not duplicate the same explanation in all three forms. These examples illustrate options, not mandatory comments for every planner.

Purpose comments should connect a step to its downstream need:

```text
// Combine repeated SKUs so the availability check uses each SKU's total demand.
// Keep first-appearance order so shortage reports follow the caller's item order.
```

These explain what the representation accomplishes. "Create a map" only names the mechanism; "ensure correctness" leaves the intended property unspecified. Add local invariant comments where the next step relies on a fact the reader might otherwise have to reconstruct.

## Explain the handoff between stages

For the aggregation stage above, a useful postcondition is:

```text
// Each SKU now appears once with its total requested quantity.
// The availability check can compare that total against stock without missing
// a shortage spread across repeated items.
```

This identifies both the established fact and the next stage's reason to rely on it. State a precondition where an operation would otherwise look unsafe; avoid repeating invariants at every statement.

Before finishing, read as a maintainer encountering the operation for the first time. If the purpose requires reading the whole body, add a short overview. If a transition seems arbitrary, explain its prerequisite or outcome. If related cases are scattered, consider a table or diagram. Remove explanations that add no orientation or merely restate the adjacent syntax. Check every visual against the actual branches and guarantees.

## Make tests discriminating examples

For “allow only ready deliveries with attempts used below the budget,” consider:

| State | Used | Budget | Expected |
| --- | ---: | ---: | --- |
| ready | 2 | 3 | allow |
| ready | 3 | 3 | deny |
| sent | 2 | 3 | deny |

These distinguish unconditional denial, an inclusive comparison, and ignoring state. Derive expectations from the contract rather than reproducing the implementation. Explain non-obvious constraints with verified rationale; do not invent reasons to make code seem deliberate.
