---
name: quality-test-backend
description: Write tests for backend domain rules, service handlers, workers, retries, idempotency, and concurrent effects. Use within the write-quality-tests bundle; route real persistence semantics to the database subskill.
---

# Backend tests

Read the [common workflow](../../SKILL.md) once. Map the request or job through policy, orchestration, persistence, and external effects. Locate transaction ownership and dependency seams before choosing a test level.

## Domain decisions

Derive examples and boundaries from the actual policy: amounts and rounding, effective dates, eligibility, quotas, ownership, and legal state transitions. Use explicit units and time zones. Make competing conditions visible with a small decision table. Test rejected operations for unchanged state as well as the declared error.

Use properties for a broad input domain only after justifying the invariant. Isolate wall-clock access when the decision is about time; retain real timing where scheduling is the mechanism under test. See [test design](../../references/test-design.md).

## Handlers and service integration

Exercise the framework's real request pipeline when validating routing, deserialization, validation, authentication, authorization, exception mapping, or response serialization. Calling a handler method directly cannot prove middleware behavior.

Check the decisive response fields, durable state, and relevant effects. A successful status alone cannot prove correct ownership or amount. For rejected input, verify no write or downstream action occurred. Keep error assertions tied to the supported contract rather than incidental stack traces.

Use a controlled external dependency for timeout, malformed response, cancellation, and unavailable-service cases. Keep the business decision real. Route wire compatibility to [contracts](../quality-test-contracts/SKILL.md).

## Jobs, retries, and duplicate delivery

Establish delivery guarantees and the idempotency contract first. Select cases such as duplicate delivery, a lost response after commit, retry exhaustion, out-of-order messages, or restart during work. Verify durable effects and acknowledgement behavior at the boundary that owns them.

For idempotency, distinguish the same key and same intent from the same key with changed intent. Check key scope, concurrent repeats, and expiry if specified. Count durable business effects, not merely function calls. [AWS's idempotent API guidance](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) motivates these distinctions; it does not impose EC2 semantics on other products.

For transactional outboxes or similar designs, inject failure at meaningful boundaries: before commit, after commit before publish, or after publish before acknowledgement. Check the application's recovery contract rather than claiming generic “exactly once” delivery. Verify broker behavior separately when a fake cannot reproduce it.

## Concurrency and resource ownership

Use barriers, latches, or controllable schedulers to establish the relevant overlap; collect all results and check the final invariant. Apply timeouts and always join or cancel spawned work. Avoid inferring thread or process safety from sequential retries.

Transaction conflicts and cross-process uniqueness require [database tests](../quality-test-database/SKILL.md). Controlled failure injection checks recovery logic; capacity and sustained degradation belong in [performance and reliability](../quality-test-performance/SKILL.md).

## Evidence boundary

State whether tests exercised pure rules, the actual framework pipeline, real adapters, or a broker. Document substituted dependencies and any compatibility assumptions left unverified.
