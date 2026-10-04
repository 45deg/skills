---
name: quality-test-e2e
description: Write focused end-to-end tests for complete product journeys and assembled-system behavior. Use within the write-quality-tests bundle when the failure requires multiple real application layers.
---

# End-to-end tests

Read the [common workflow](../../SKILL.md) once. Select journeys by product impact and integration risk. A complete sign-up, reservation, or recovery flow may justify a system test; every validation edge case usually does not.

## Define the system boundary

List which components are real: browser or client, frontend, API, authentication, database, queue, and external services. If first-party APIs are stubbed, describe the result as a frontend journey with mocked services, not a complete system check.

Use a disposable assembled application or an explicitly authorized environment. Provide synthetic accounts and unique data per test or worker. Configure external effects to authorized sandboxes or controlled fakes. Keep any unverified third-party integration visible in the report.

## Build a meaningful journey

Start from a realistic entry point, perform the user's actions, and assert the final product outcome. Observe persistence through a reload, a second session, or a trusted read boundary when that is part of the promise. A transient success notification alone may hide an uncommitted operation.

Use APIs or fixtures for unrelated preconditions to shorten tests; do not bypass the behavior being tested. Reused authentication state is appropriate for unrelated flows, but login tests must exercise the login path. Select a few meaningful recovery journeys, such as interrupted submission or expired authorization, based on risk.

Keep cases independent with explicit setup and cleanup. Use stable semantic locators and bounded condition-based waits. Inspect traces, application errors, and relevant service logs when assertions fail. [Playwright's guidance](https://playwright.dev/docs/best-practices/) provides concrete browser practices.

## Control suite cost

Move combinatorial rule cases into [backend](../quality-test-backend/SKILL.md), [frontend](../quality-test-frontend/SKILL.md), or [contract](../quality-test-contracts/SKILL.md) tests when they can detect the same defect. Keep system cases that prove wiring and product outcomes. Google's [E2E testing discussion](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) motivates balancing confidence against slow, ambiguous feedback; its example proportions are not a target.

Choose browsers, viewports, locale, and supported deployment configurations from the product matrix. A single-browser pass is not cross-browser evidence. Preserve failure artifacts without exposing credentials or personal data. Treat whole-test retries as diagnostic evidence, not proof that the first failure was harmless.

## Deployment smoke tests

Only exercise a deployed environment when authorized. Check actual readiness and a bounded representative operation under the deployment's version and configuration. Offline tests cannot prove the deployed wiring; conversely, a smoke test is not broad regression coverage. [Google SRE](https://sre.google/sre-book/testing-reliability/) distinguishes these environments.

## Evidence boundary

Report journeys, environment, component versions if known, real and substituted integrations, executed browser matrix, and failure artifacts. Keep deployment results distinct from local system tests.
