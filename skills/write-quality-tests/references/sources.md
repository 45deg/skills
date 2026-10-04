# Source register

Reviewed **2026-10-05**. Entries identify primary sources, the narrow lesson used, and a limit on its application. Publication years are provided for dated research and essays; documentation is a living source unless a version is named. Consult the target project's installed version before copying an API or configuration.

## Strategy and AI-generated tests

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S01 | Google Testing Blog, [Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html), 2010 | Describe execution dependencies and isolation. Historical runtime budgets and Java mechanisms are not current universal requirements. |
| S02 | Google Testing Blog, [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html), 2015 | Balance system confidence against feedback and diagnosis costs. Do not mandate its illustrative test proportions. |
| S03 | Google Testing Blog, [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html), 2020 | Inspect uncovered risks and assertion quality. Coverage is an indirect measure, not proof of correctness. |
| S04 | Alshahwan et al., [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/html/2402.09171v1), 2024 | Evaluate generated candidates with executable filters. Regression-preservation filters do not decide whether a failing test exposes an existing bug. |
| S05 | Molinelli et al., [Do LLMs Generate Useful Test Oracles? An Empirical Study with an Unbiased Dataset](https://homes.cs.washington.edu/~mernst/pubs/neurosymbolic-oracles-ase2025.pdf), ASE 2025 | Distinguish oracle evaluation from test execution and study dataset limits. Results concern selected Java projects and tested models. |
| S06 | Foster et al., [Mutation-Guided LLM-based Test Generation at Meta](https://arxiv.org/html/2501.12862v1), 2025 | Target tests at relevant, currently uncaught faults. Generated mutants and one organization's deployment do not cover every failure class. |
| S07 | Stryker, [Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) | Interpret killed, survived, uncovered, timeout, and invalid outcomes. Other tools may calculate scores differently. |
| S08 | pytest, [Flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html) | Investigate uncontrolled state, order, timing, and thread cleanup. Repetition alone does not prove determinism. |

## Generative techniques

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S09 | fast-check, [What is property-based testing?](https://fast-check.dev/docs/introduction/what-is-property-based-testing/) | Use properties, generated inputs, shrinking, and reproducibility. Sampling does not exhaust the domain or validate the property itself. |
| S10 | fast-check, [Model based testing](https://fast-check.dev/docs/advanced/model-based-testing/) | Exercise operation sequences against a simpler model. A model that repeats the implementation can repeat its bugs. |
| S11 | Hypothesis, [Stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html) | Generate actions and state transitions, not only individual values. Follow installed-version APIs and establish valid model invariants. |
| S12 | Go, [Go Fuzzing](https://go.dev/doc/security/fuzz/) | Use coverage-guided inputs and preserve reproducing failures. Runtime robustness is narrower than semantic correctness. |

## Frontend and browser testing

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S13 | Testing Library, [Guiding Principles](https://testing-library.com/docs/guiding-principles/) | Test through user-relevant interfaces. DOM tests do not establish all native browser behavior. |
| S14 | Testing Library, [user-event introduction](https://testing-library.com/docs/user-event/intro/) | Model interactions as sequences instead of isolated low-level events. Simulation is not a substitute for browser-specific validation. |
| S15 | Playwright, [Best Practices](https://playwright.dev/docs/best-practices) | Isolate browser cases and use resilient locators and condition-based assertions. Follow the installed API version. |
| S16 | Playwright, [Visual comparisons](https://playwright.dev/docs/test-snapshots) | Stabilize the rendering environment and inspect baseline changes. Screenshots do not prove semantics or accessibility. |

## Backend and contracts

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S17 | Pact, [When to use Pact](https://docs.pact.io/getting_started/what_is_pact_good_for) | Choose contract tests where interactions and states can be controlled. They do not replace all integration testing. |
| S18 | Pact, [Consumer Testing](https://docs.pact.io/implementation_guides/python/docs/consumer) | Pair consumer expectations with provider verification. The Python examples do not prescribe a language. |
| S19 | Pact, [FAQ](https://docs.pact.io/faq) | Isolate provider states and understand consumer-driven boundaries. A contract proves only the interactions verified. |
| S20 | AWS Builders' Library, [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | Distinguish duplicate intent, changed intent, and late retries. Exact key lifetime and response semantics are product-specific. |
| S21 | Schemathesis, [Checks](https://schemathesis.readthedocs.io/en/stable/reference/checks/) | Add schema, response, and negative-input validation. Built-in checks do not express every business invariant. |
| S22 | Schemathesis, [Understanding Stateful Testing](https://schemathesis.readthedocs.io/en/stable/explanations/stateful/) | Exercise valid API sequences using prior results. Generated calls still require scoped targets and cleanup. |

## Databases

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S23 | Testcontainers for Java, [Database containers](https://java.testcontainers.org/modules/databases/) | Use real engines where substitutes differ. Container tests do not reproduce all production topology and operational conditions. |
| S24 | PostgreSQL, [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) | Check actual constraints, including null semantics. Rules and syntax differ across engines and versions. |
| S25 | PostgreSQL, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | Model anomalies and guarantees at the configured isolation level. Do not generalize PostgreSQL behavior to every database. |
| S26 | PostgreSQL, [Serialization Failure Handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html) | Test whole-transaction retry behavior. Application side effects need separate handling. |
| S27 | PostgreSQL, [Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | Exercise application roles and policy bypass differences. Administrative test connections can provide misleading results. |
| S28 | Redgate Flyway, [Validate](https://documentation.red-gate.com/flyway/reference/commands/validate) | Separate migration-history validation from behavioral migration tests. A matching checksum does not prove preserved data. |

## Accessibility and security

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S29 | W3C, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/), Recommendation | Map checks to relevant success criteria and their exceptions. Automated checks alone cannot establish conformance. |
| S30 | W3C WAI, [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Combine tooling with knowledgeable human evaluation. Report actual evaluation scope. |
| S31 | Playwright, [Accessibility testing](https://playwright.dev/docs/accessibility-testing) | Integrate automated accessibility checks in relevant states. Tool findings are a subset of accessibility evaluation. |
| S32 | OWASP, [Web Security Testing Guide v4.2](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/) | Select threat-relevant security test categories. This skill implements scoped regressions, not the entire guide. |
| S33 | OWASP WSTG v4.2, [Testing for Insecure Direct Object References](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/) | Use distinct identities and resource references to test authorization. A single endpoint does not prove tenant isolation everywhere. |

## Performance and data

| ID | Primary source | Use and limitation |
| --- | --- | --- |
| S34 | Grafana k6, [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | Encode measurable acceptance gates. Documentation example numbers are not product SLOs. |
| S35 | Grafana k6, [Open and closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/) | Match arrivals to the intended workload and recognize coordinated omission. Check generator capacity and dropped work too. |
| S36 | Google SRE Book, [Testing for Reliability](https://sre.google/sre-book/testing-reliability/), 2016 | Separate offline tests from operational configuration and live-service evidence. Live tests require explicit scope. |
| S37 | dbt, [Unit tests](https://docs.getdbt.com/docs/build/unit-tests) | Test SQL transformations and incremental output with controlled inputs. Emitted rows do not prove the final materialized merge result. |
| S38 | dbt, [Data tests](https://docs.getdbt.com/docs/build/data-tests) | Assert properties of built datasets. Such checks do not replace transformation examples or orchestration tests. |

## Maintenance

Keep lessons and limitations together when updating this register. Replace unavailable sources with equivalent primary documentation rather than silently treating a search snippet as full evidence. Review exact framework behavior when applying the skill; do not perform a new broad search for every routine test edit.
