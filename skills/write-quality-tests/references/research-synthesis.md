# Research synthesis

Research reviewed: **2026-10-05**. Scope: AI-assisted test generation and practical testing across application layers. The [source register](sources.md) contains 38 primary documentation and research sources.

## Method and evidence strength

Searches covered test strategy, generated-test oracles, mutation analysis, browser behavior, contract verification, database semantics, accessibility, security regression testing, load models, and incremental data processing. Follow-up reading checked the mechanisms and limitations behind candidate recommendations. Search results and community commentary were used for discovery; recommendations below rely on primary papers, standards, and maintainers' documentation.

This is a targeted engineering review, not a systematic literature review or a comparative benchmark of testing tools. The named tools illustrate capabilities; the skill keeps the repository's existing stack. Research findings are not assumed to transfer unchanged between languages, products, models, or execution environments.

## Decisions derived from the evidence

| Question | Evidence and tension | Decision in this skill |
| --- | --- | --- |
| Should AI generate as many tests as possible? | TestGen-LLM filters candidates for buildability, passing execution, and added coverage. Those checks evaluate candidate usefulness within a specific regression workflow. [S04](sources.md#strategy-and-ai-generated-tests) | Generate focused batches, verify execution and incremental value, and reject redundant cases. |
| Should a generated test that fails be discarded? | TestGen-LLM discards failures because it cannot automatically separate a product bug from a wrong assertion. [S04](sources.md#strategy-and-ai-generated-tests) | In an interactive task, investigate the oracle. Keep a justified failing regression; do not inherit the paper's automated discard rule. |
| Is high coverage enough? | Coverage identifies executed code and omissions; Google's guidance explicitly treats it as an imperfect measure. [S03](sources.md#strategy-and-ai-generated-tests) | Use coverage to locate gaps, then assess assertions and likely fault detection. Retain project gates without inventing universal percentages. |
| Can mutation establish quality? | ACH targets relevant uncaught faults; mutation tools classify outcomes differently, including timeouts. [S06–S07](sources.md#strategy-and-ai-generated-tests) | Use targeted fault sensitivity where valuable, inspect survivors and invalid mutants, and report the chosen fault model. A score is not a proof of correctness. |
| Should tests be mostly unit tests or E2E tests? | Google's strategy guidance emphasizes feedback cost; browser and integration documentation expose behavior that an isolated test cannot establish. [S01–S02](sources.md#strategy-and-ai-generated-tests), [S15](sources.md#frontend-and-browser-testing), [S23](sources.md#databases) | Select the smallest boundary that preserves the failure mechanism. Keep complete journeys for assembly risks and avoid fixed test ratios. |
| Should dependencies always be mocked? | Controlled boundaries improve repeatability, while contracts and real engines expose semantic differences. [S17–S19](sources.md#backend-and-contracts), [S23](sources.md#databases) | Mock irrelevant or uncontrolled effects; retain real components when their semantics determine correctness. State what remains assumed. |
| Can automation establish accessibility or reliability? | W3C requires human evaluation for accessibility judgments; operational testing depends on deployed configuration. [S30](sources.md#accessibility-and-security), [S36](sources.md#performance-and-data) | Separate automated checks from manual evaluation and local results from operational evidence. |
| Is testing a transformation enough to trust stored results? | dbt distinguishes unit inputs/outputs from built-data checks and incremental materialization behavior. [S37–S38](sources.md#performance-and-data) | Test transformations, materialized state, and orchestration at distinct boundaries when their risks matter. |

These decisions are this skill's synthesis. They are not quotations, mandatory rules issued by the source organizations, or evidence that all tools agree.

## What the AI studies establish

**TestGen-LLM (2024)** reports a production-oriented workflow for improving existing tests. Its practical contribution here is a sequence of executable filters. Its passing-test requirement serves regression preservation and does not settle whether existing behavior is correct. See [the paper](https://arxiv.org/html/2402.09171v1).

**Do LLMs Generate Useful Test Oracles? (ASE 2025)** evaluates 13,866 oracles from 135 Java projects. The study reports average mutation scores of 43% for generated oracles and 45% for human-written ones. This is evidence for the evaluated oracle-generation setting, not equivalence of complete suites or demonstrated real-world bug detection. Its dataset construction addresses training-data leakage but does not make the finding universal. See [the author-hosted paper](https://homes.cs.washington.edu/~mernst/pubs/neurosymbolic-oracles-ase2025.pdf).

**Mutation-Guided LLM-based Test Generation at Meta (2025)** describes generating tests against currently uncaught faults associated with a concern. It motivates checking concrete fault sensitivity rather than accepting coverage alone. Its industrial context and generated fault set limit generalization; an LLM's opinion that a mutant is equivalent is not a correctness proof. See [the paper](https://arxiv.org/html/2501.12862v1).

## Deliberate limits

- No universal coverage threshold, mandatory mutation score, fixed pyramid percentage, or promise of bug-free software.
- No requirement to replace the project's runner, introduce a SaaS service, or provision containers for a pure function.
- No assumption that a schema-valid API implements the right policy, a simulated DOM proves rendering, or a clean migration proves an upgrade.
- No claim that tests determine product desirability or replace appropriate exploratory evaluation.

Refresh version-specific documentation when applying the skill. Preserve stable principles, but revise a recommendation when a changed tool or observed failure invalidates its mechanism.
