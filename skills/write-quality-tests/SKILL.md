---
name: write-quality-tests
description: Design, write, and verify risk-based software tests, including regressions, missing coverage, and test-suite improvement. Route to focused guidance for UI, services, databases, contracts, security, performance, and data pipelines. Do not activate for prose proofreading or merely running an unchanged test suite.
---

# Write Quality Tests

Protect observable behavior with grounded expectations and evidence that plausible defects are detected.

## Inspect and scope

Inspect project instructions, the requested behavior, existing tests, fixtures, runner configuration, and CI commands. Reuse the repository's tools and conventions. Run a relevant baseline when feasible and distinguish existing failures from new ones.

For a narrow bug, write a focused regression. For a broad request, identify the highest-impact failures and choose boundaries that preserve their failure mechanisms. A mock cannot establish behavior that depends on the real database, browser, or service.

## Select relevant guidance

Read only the subskills that match the task. These file-based routes share this workflow and its references; keep the bundle together. If entering through a subskill, read the common workflow once.

| Boundary or risk | Subskill |
| --- | --- |
| Components, forms, client state, accessibility, visual changes | [Frontend](subskills/quality-test-frontend/SKILL.md) |
| Business rules, handlers, jobs, retries, concurrency | [Backend](subskills/quality-test-backend/SKILL.md) |
| Queries, constraints, transactions, migrations, row security | [Database](subskills/quality-test-database/SKILL.md) |
| HTTP, events, consumers, providers, schema evolution | [Contracts](subskills/quality-test-contracts/SKILL.md) |
| Complete journeys, system wiring, deployment smoke tests | [End to end](subskills/quality-test-e2e/SKILL.md) |
| Authorization, sessions, hostile inputs, privacy | [Security](subskills/quality-test-security/SKILL.md) |
| Capacity, saturation, benchmarks, fault recovery | [Performance and reliability](subskills/quality-test-performance/SKILL.md) |
| Transformations, incremental processing, replay, data quality | [Data pipelines](subskills/quality-test-data-pipelines/SKILL.md) |

For cross-layer changes, give each assertion an owner; repeat an edge case at another layer only when it tests a distinct failure mechanism.

## Ground the test design

For each important behavior, identify its impact, evidence for the expected result, plausible defect, test boundary, and observable assertion, including forbidden effects. Keep this inline for small tasks; use existing project planning formats when needed.

Use requirements, agreed contracts, incidents, or justified invariants as the oracle. Do not derive business expectations from the production algorithm or current output. Resolve ambiguity only when it changes the expected behavior; continue independent cases meanwhile. Label characterization tests as observations, especially around suspected defects.

Keep promised values precise while leaving unspecified representation choices free. Capture generated identifiers and assert required identity relationships instead of assuming a starting value or format. Read [contract precision](references/test-design.md#contract-precision-without-implementation-coupling) when implementation coupling is a risk.

For interacting state, hold unrelated conditions equal so they cannot mask the boundary under test. For recovery, include a successful prefix before a later failure. Exercise invalid inputs and nested returned data at the depth promised by the public API. Read [interaction and failure sequences](references/test-design.md#interaction-and-failure-sequences) when these risks apply; do not impose these cases on every task.

Read [test design](references/test-design.md) when choosing boundary cases, decision tables, state transitions, properties, fuzzing, fixtures, or doubles. Before accepting generated tests, use [AI test review](references/ai-test-review.md) to check for false confidence.

## Implement and verify

- Write a small batch through public boundaries. Assert precise outputs, state changes, and relevant absent effects; avoid copying the production algorithm into expectations.
- Confirm discovery, fixture resolution, awaited asynchronous work, and failure propagation. Zero selected tests do not validate a change.
- For a regression, observe failure before the fix and confirm it exposes the defect, not a harness error. If already fixed, use an isolated copy of the previous implementation when available. For important new behavior, consider a bounded, targeted mutation; see [failure-detection evidence](references/test-design.md#targeted-mutation-and-redgreen-evidence). Do not alter the user's working implementation merely to manufacture a red run.
- Classify unexpected failures as product defects, incorrect expectations, fixture/environment problems, or flakiness. In tests-only work, retain a justified failing regression and report the defect; production fixes require task scope.
- Run the focused suite and required related checks. Broaden based on affected boundaries and project policy. Repeat, reorder, or parallelize runs when isolation or nondeterminism is a risk; one green run does not establish absence of flakiness.
- Remove redundant cases and inspect relevant coverage gaps. Preserve project gates without inventing universal coverage, mutation-score, or test-count targets.

Do not weaken justified assertions, swallow failures, disable tests, relax security behavior, or accept uninspected snapshots to make tests pass. Stop retries when they produce no new evidence and report the reproducible blocker.

Use disposable or explicitly authorized environments, synthetic data, and bounded runs. Verify the resolved target before migrations, cleanup, load, or fault injection. Test work alone does not authorize real payments or messages, production changes, third-party scans, or publication. Add dependencies only to address a concrete gap under project installation policy.

## Report evidence

Report protected behaviors, changed files, actual commands and results, and remaining blockers. Distinguish static checks, unit tests, real-service integration, browser/visual checks, load execution, and manual accessibility evaluation. Claim red/green, mutation detection, CI, or deployment verification only when observed; local automation does not establish security certification or accessibility conformance.

## Supporting material

For research rationale and limitations, read the [research synthesis](references/research-synthesis.md) and [dated source register](references/sources.md). Consult upstream documentation when framework APIs or version-specific behavior matter.

For skill maintenance, use [behavioral evaluation scenarios](evals/scenarios.md). These specify checks, not completed evaluation results.
