---
name: quality-test-frontend
description: Write frontend component and interaction tests for rendered behavior, forms, client state, accessibility, and visual regressions. Use within the write-quality-tests bundle; use the E2E subskill for complete deployed journeys.
---

# Frontend tests

Read the [common workflow](../../SKILL.md) once. Inspect the actual framework, rendering mode, existing DOM or browser harness, and supported browser matrix. Select only the modes affected by the task.

## Components and forms

Test through rendered semantics and realistic interaction sequences. Prefer accessible roles and names or associated labels; use a stable test identifier when there is no suitable user-facing locator. Avoid coupling assertions to private component state or incidental DOM nesting. Testing Library's [principles](https://testing-library.com/docs/guiding-principles/) and [user-event guidance](https://testing-library.com/docs/user-event/intro/) support this boundary.

For a form, choose relevant states: initial values, input, validation timing, invalid submission, pending submission, success, and failure recovery. Verify the submitted values as well as the visible outcome. Assert that invalid or repeated submission causes no forbidden request or durable effect when the product contract requires that behavior. A disabled button alone does not establish server-side duplicate prevention.

## Async state and navigation

Use controlled responses to cover empty, loading, success, permission-denied, and recoverable-error states where meaningful. For search or route changes, deliberately resolve earlier requests after later requests and check the final visible state. Test optimistic updates against rejection and reconciliation, not only immediate display.

Keep state stores and routing real when they own the behavior. Place network substitutions at the transport boundary rather than mocking the hook or component being tested. Define cache and state reset between cases. Browser navigation, persistence across reloads, hydration, and browser APIs need an environment that actually supports them.

Use condition-based async assertions and inspect runtime failures. The [Playwright best-practices guide](https://playwright.dev/docs/best-practices/) explains resilient locators and web-first assertions. Do not fix races with arbitrary delays.

## Accessibility

Target the product's accessibility requirements, normally WCAG 2.2 AA for web UI. Combine automated checks in relevant interactive states with keyboard checks for reachability, activation, focus entry and return, and error recovery. Check labels, status announcements, reflow, zoom, text and UI contrast, and information conveyed without color alone as applicable. Use [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for exact criteria and exceptions rather than inventing blanket thresholds.

An automated scan cannot establish conformance. Record what was inspected, including browser and assistive technology where used, and which manual checks remain. See [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/) and [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing).

## Visual regressions

Use screenshots only when visual output is itself the contract. Fix the rendering environment, viewport, fonts, data, and animation state. Compare meaningful states and supported layouts. Inspect differences before updating expected images; mask only irrelevant volatility, not the changed feature. Follow the existing baseline policy. [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) describes environment sensitivity.

## Evidence boundary

A simulated DOM is suitable for many interaction tests but does not prove layout, rendering, or native browser behavior. Report simulated-DOM execution, real-browser execution, screenshot inspection, and manual accessibility checks separately. Route integrated journeys to [E2E](../quality-test-e2e/SKILL.md) and server access enforcement to [security](../quality-test-security/SKILL.md).
