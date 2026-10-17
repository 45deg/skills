---
name: good-code
description: Improve code clarity and maintainability during implementation, refactoring, and review. Use when names, branching, state, interfaces, comments, or tests make a change difficult to understand, or when AI-generated code adds unnecessary complexity. Not intended for formatting-only tasks, prose editing, or architecture-wide redesign.
---

# Good Code

Make behavior easier to learn, check, and modify, including its interactions with surrounding code. Reduce the understanding effort for maintainers, including newcomers and people returning after a long gap. Extra lines can be worthwhile when they clarify intent or expose a mistake. Make changes reviewable while preserving requested functionality and project conventions; a preferred style is not a reason to compromise either.

## Start with the requested outcome

Read the applicable project instructions, affected implementation, callers, and relevant tests. Separate existing user changes from your own work. A request for review authorizes findings, not unsolicited edits. Implementation and cleanup requests authorize changes within their stated scope.

Establish the behavior that matters before editing: accepted inputs, returned values, failures, observable effects, and any relevant ordering, resource, or compatibility constraints. If something is unclear, investigate the actual implementation and dependency version. Ask only when a consequential requirement cannot be established from available evidence.

Use the following questions to choose what to change. They are diagnostic prompts, not a checklist that every function must satisfy.

## Questions for a useful change

- **Can the next reader predict the operation?** Names, signatures, and call sites should reveal the relevant action, data representation, and consequences. Resolve ambiguity where it could lead to a wrong edit or misuse.
- **Can the decision be checked locally?** Make it possible to see which conditions admit a case, reject it, or end processing without retaining a large amount of context. Group calculations around the decisions they support.
- **Can the effects be accounted for?** Make important writes, external calls, ownership, and cleanup visible. Restrict access to mutable data and make the lifetime of temporary state easy to follow.
- **Does each boundary earn its cost?** Introduce a helper, adapter, or type when it removes a real burden from its callers or establishes a useful contract. Keep independent policies separate, even if their implementations happen to resemble each other.
- **Is necessary context available where it is used?** Keep non-obvious constraints and decisions in code, tests, or concise documentation. A conversation with the author should not be required to understand a maintained interface. Keep one authoritative explanation where practical instead of copying the same rule into multiple documents that can drift apart.
- **What evidence would reject an incorrect change?** Identify checks that exercise the relevant contract and report a useful failure. Treat AI-written implementation and tests as proposals to inspect, not as evidence for each other.

When names or layout solve the problem, leave the structure alone. When a simpler algorithm or existing facility meets the requirement, avoid adding machinery. Do not invent numerical limits for function length, parameters, nesting, or abstraction counts. Leave satisfactory code unchanged and stop when further cleanup adds more concepts or review effort than it removes.

Read [decision-cases.md](references/decision-cases.md) only for situations where the tradeoff needs closer examination.

## Guard against plausible but unsupported code

Confirm unfamiliar APIs, options, and packages against the version actually used. Type assertions do not validate external data. Do not disguise an operational failure as a normal empty result unless that is the agreed contract. A fallback needs a defined trigger and an intended outcome.

Do not introduce speculative compatibility layers, dependencies, retry policies, or caches. For asynchronous changes, account for scheduling, cancellation, rate limits, duplicate execution, and shared updates. Keep sensitive values out of diagnostic output.

Do not weaken assertions, suppress type errors, or accept new snapshots merely to obtain a passing check. Use project tooling and focused verification appropriate to the impact; a small rename does not justify a new test framework.

## Finish with a reviewable result

Read the edited operation in context as well as the diff. A small-looking patch can leave a confusing whole. Keep unrelated formatting and cleanup out of the change, and preserve public names or formats that consumers depend on unless changing them is part of the task.

For a review, identify the affected location, the condition or maintenance problem, and the practical consequence. Offer a specific correction when it clarifies the finding. Separate defects and material comprehension problems from optional preferences. Mark uncertainty rather than turning an unverified suspicion into a defect, and report no findings when none are supported.

For an implementation, summarize the resulting behavior or maintenance benefit, the checks actually performed, and any consequential gaps. Distinguish static inspection from executed verification. Commit, publish, or otherwise affect external systems only within the user's authorization.
