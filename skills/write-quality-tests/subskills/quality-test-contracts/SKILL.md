---
name: quality-test-contracts
description: Write consumer and provider contract tests for HTTP APIs, events, and compatibility changes. Use within the write-quality-tests bundle to verify wire behavior across independently evolving components.
---

# Contract tests

Read the [common workflow](../../SKILL.md) once. Identify producer, consumer, authoritative schema, supported versions, and the behavior each side actually relies on.

## Choose the contract mechanism

| Need | Test approach | What it cannot establish alone |
| --- | --- | --- |
| An API conforms to its documented schema | Exercise real requests and validate responses against that schema | Correct business effects or consumer compatibility |
| A consumer depends on provider behavior | Run real consumer code against a controlled provider; verify resulting interactions on the provider | Whole-system wiring, availability, or transport security |
| A message format evolves | Exercise producer serialization and real consumer parsing for supported versions | Broker redelivery, ordering, or operational behavior |

Use the project's existing contract tooling. Pact is a candidate when interactions and provider states can be controlled; see [when Pact fits](https://docs.pact.io/getting_started/what_is_pact_good_for). Do not introduce a broker or publish artifacts merely to write a local test.

## Consumer and provider verification

Drive the real consumer adapter. Describe only the fields and semantics it needs, with exact values where meaning matters and flexible matching for incidental values. An overly permissive matcher can hide a broken amount, enum, or identifier; excessive exact matching can make harmless additions fail.

Verify the contract against real provider handlers, with independently established provider state per interaction. Cover meaningful success and error responses. A passing mock consumer test is incomplete without provider verification; [Pact's consumer testing documentation](https://docs.pact.io/implementation_guides/python/docs/consumer) makes this explicit.

Keep state setup deterministic and do not rely on interaction ordering. Record which consumer and provider revisions were verified. Check supported deployed-version combinations when the task concerns rollout compatibility, using the existing workflow and authorization.

## Schema and protocol cases

Test required versus optional versus nullable fields, enum evolution, error payloads, numeric precision, time representation, pagination tokens, and headers only as relevant to the API. For breaking-change analysis, exercise real consumer parsing: adding a field is not harmless if a supported consumer rejects unknown fields.

Schema-based tools such as [Schemathesis](https://schemathesis.readthedocs.io/en/stable/reference/checks/) can generate structural and negative cases. Independently verify business invariants; valid schema and status do not prove correct access control or state changes. Restrict generated requests to disposable authorized targets.

Where calls depend on earlier resources, use valid sequences and retained identifiers; see [stateful API testing](https://schemathesis.readthedocs.io/en/stable/explanations/stateful/). Ensure teardown and bounded generation.

## Evidence boundary

Report consumer-only, provider-only, or both-sided verification precisely, along with versions and substitutes. Use [backend](../quality-test-backend/SKILL.md) for semantic effects and [E2E](../quality-test-e2e/SKILL.md) for assembled-system checks. Contracts reduce uncertainty at interfaces; they do not replace all integration tests.
