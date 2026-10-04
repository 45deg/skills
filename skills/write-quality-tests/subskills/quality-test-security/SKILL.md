---
name: quality-test-security
description: Write defensive regression tests for authorization, sessions, input handling, business abuse, and sensitive-data exposure. Use within the write-quality-tests bundle for scoped application security behavior, not an unsolicited penetration test.
---

# Security regression tests

Read the [common workflow](../../SKILL.md) once. Map the changed feature's trust boundaries, actors, resources, and permitted actions. Translate relevant threats into precise expected behavior using the project's policy and the [OWASP Web Security Testing Guide](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/).

## Authorization and tenant isolation

Create an actor-resource-action table with allowed and denied cases. Exercise the actual enforcement boundary, not just UI visibility. Distinguish unauthenticated access, wrong role, wrong owner, and wrong tenant where the policy distinguishes them.

Use at least two independent identities when testing ownership. Attempt access using another identity's object reference through relevant read, mutation, list, or export paths. Assert no unauthorized data or effects, not just an error status. OWASP's [object-reference testing guidance](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/) explains this test shape.

Check fields as well as objects when field-level permissions exist. Include valid allowed cases so “deny everything” cannot satisfy the suite. For database policies, use the actual application role; see [database tests](../quality-test-database/SKILL.md).

## Sessions and credentials

Select relevant expiry, revocation, logout, reset, and reuse cases from the authentication contract. Control time when testing expiry rules. Verify tokens or sessions stop authorizing requests at the promised boundary. Error responses and logs should avoid exposing secrets or account details beyond the established policy.

Test CSRF or cross-origin behavior where the application's credential mechanism and browser threat model require it. A mocked HTTP client does not prove browser enforcement; use browser integration for browser-owned behavior.

## Untrusted input and business abuse

Choose payloads that represent the application's actual parsing and rendering contexts. Verify parameterized query behavior, context-appropriate output handling, path boundaries, accepted upload types and sizes, or redirect destinations where changed code owns those decisions. Do not paste an indiscriminate exploit corpus into every test suite.

Exercise attempts to skip workflow steps, replay a one-time operation, modify protected fields, or exceed limits only when those risks apply. Verify the denied action leaves state unchanged. Use [backend](../quality-test-backend/SKILL.md) and [contracts](../quality-test-contracts/SKILL.md) to place these assertions at the owning boundary.

For privacy requirements, seed identifiable synthetic markers and check relevant responses, exports, and captured logs for disallowed disclosure. Avoid real user data in fixtures or failure artifacts.

## Execution boundary

Write and run tests against local disposable or explicitly authorized targets. Bound input sizes, request volume, and time. Active scanning, destructive payloads, and testing third-party systems require scope beyond ordinary regression authoring. Honor existing authorization and do not add a redundant approval step.

## Evidence boundary

Report covered policies, exercised identities and enforcement layers, and untested trust boundaries. Passing regression tests do not establish that the product is secure or replace a requested specialist assessment.
