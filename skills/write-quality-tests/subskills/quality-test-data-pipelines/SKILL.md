---
name: quality-test-data-pipelines
description: Write tests for SQL transformations, ETL or ELT, incremental processing, replay, and output data quality. Use within the write-quality-tests bundle when correctness depends on transforming or moving datasets.
---

# Data pipeline tests

Read the [common workflow](../../SKILL.md) once. Identify the input contract, output grain, business definitions, ordering assumptions, checkpoints, and replay semantics. Inspect the actual transformation engine and adapter versions.

## Transformation logic

Use small explicit input tables with independently expected output rows. Select cases for joins with missing or duplicate keys, grouping, window ties, nulls, type conversion, time boundaries, and rounding as they affect the transformation. Verify row multiplicity and keys, not only aggregate totals that may cancel errors.

For SQL models, distinguish transformation tests with fixed inputs from assertions on built datasets. [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests) and [data tests](https://docs.getdbt.com/docs/build/data-tests) document these separate roles. Validate business transformations rather than retesting the warehouse's built-in aggregate functions without a specific reason.

## Data quality contracts

Check uniqueness, required values, allowed domains, relationships, completeness, and freshness only where they express a real contract. Define whether violations should fail, quarantine, warn, or be tolerated within an agreed bound. Keep malformed fixture tests distinct from production data monitoring.

Use synthetic data and preserve the expected schema. Avoid silently normalizing invalid source records before the code under test sees them. Testing with clean fixtures alone cannot validate the error-handling path.

## Incremental processing and replay

Exercise initial load, subsequent batch, duplicate input, late arrival, update or deletion, and restart around a checkpoint when supported. Compare incremental results with a justified full-recompute oracle on the same bounded dataset, accounting for intentional differences in retention or historical semantics.

Assert both the produced delta and the final persisted state at their respective boundaries. In dbt incremental unit tests, expected rows describe what is emitted for insertion or merge; they do not prove the framework's final merge result. Add an integration check where that behavior matters. See [dbt incremental unit testing](https://docs.getdbt.com/docs/build/unit-tests#unit-testing-incremental-models).

For streams, distinguish event time from processing time, establish watermark and allowed-lateness rules, and control progress without arbitrary sleeps. Check duplicate handling and checkpoint recovery against the actual delivery contract. Partitioning and reordering properties are valid only when the computation is designed to preserve them.

## Orchestration and destinations

Test dependency ordering, failure propagation, retry boundaries, and ownership of committed outputs. A transformation test cannot prove the scheduler or destination adapter works. Use disposable schemas or paths and avoid overwriting real datasets. Route persistence semantics to [database tests](../quality-test-database/SKILL.md) and operational recovery to [performance and reliability](../quality-test-performance/SKILL.md).

## Evidence boundary

Report fixture transformations, built-dataset checks, incremental integration, and orchestration execution separately. Specify engine, adapter, relevant batch state, and what replay or failure boundary was exercised. A warehouse substitute does not establish dialect or production-engine equivalence.
