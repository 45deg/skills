---
name: quality-test-database
description: Write database tests for queries, constraints, transactions, concurrency, migrations, and row-level access. Use within the write-quality-tests bundle when real persistence behavior matters.
---

# Database tests

Read the [common workflow](../../SKILL.md) once. Inspect the engine and version, migrations, ORM mapping, connection configuration, isolation level, application role, and current test fixture lifecycle.

## Establish fidelity and isolation

Use a disposable database with the relevant production engine, extensions, and settings when engine behavior matters. Reuse existing container or test-service infrastructure. An in-memory substitute can test application decisions but cannot establish SQL, locking, collation, or migration compatibility. [Testcontainers](https://java.testcontainers.org/modules/databases/) documents this distinction; a container still does not reproduce managed-service topology or production load.

Before setup or cleanup, verify the resolved target and restrict operations to test-owned databases or schemas. Give parallel workers separate namespaces. Use synthetic fixtures and teardown that runs on failure. Do not run a global truncate or migration against an unverified connection.

Transaction rollback fixtures work only for changes made within their transaction. Separate connections, background jobs, committed transactions, and some DDL need other cleanup. Test after-commit behavior with real commits in disposable state.

## Queries and constraints

Check actual returned data, cardinality, and ordering when ordered results are part of the contract. Include relevant duplicates, absent relationships, nulls, boundary timestamps, precision, and collation cases. Exercise constraints through direct writes as well as the repository API when correctness depends on database enforcement.

For pagination, test ties and the promised ordering semantics; test concurrent changes only if the API promises stability under them. Avoid asserting exact query text or plans unless SQL generation or a specific plan property is the requirement.

Null and uniqueness semantics vary by engine. PostgreSQL's [constraint documentation](https://www.postgresql.org/docs/current/ddl-constraints.html) is an example to consult for the installed version, not a portable rule.

## Transactions and contention

Create separate connections with known isolation settings. Coordinate their execution so the intended conflict occurs. Assert final invariants such as no lost update, preserved total, or bounded inventory according to the product contract. Do not assume a race was exercised because two futures started together.

Check partial-failure rollback, serialization failures, and the application's retry path. For PostgreSQL, [serialization retry](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html) includes the whole transaction's decision logic. Verify the behavior of the actual [isolation level](https://www.postgresql.org/docs/current/transaction-iso.html). Avoid repeating external effects on transaction retry.

## Schema and data migrations

Test both a clean migration chain and upgrade from each relevant supported prior schema with representative old data. Assert data preservation, defaults, constraints, new read/write behavior, and application compatibility during staged rollout where required.

Checksum or history validation is a separate check from successful migration and preserved behavior; see [Flyway validate](https://documentation.red-gate.com/flyway/reference/commands/validate). Versioned migrations are not necessarily designed to execute twice. Test reruns, resumable backfills, or repeatable migrations according to their actual contract.

For failure recovery, verify rollback where supported or the documented forward-repair path. Do not invent a reversible down migration for an irreversible data transformation. Measure locks or duration with representative data when they affect rollout feasibility; a tiny fixture cannot establish production migration safety.

## Access policies

Use the actual application role, multiple users or tenants, and both allowed and denied operations. An administrative connection may bypass policies. PostgreSQL documents owner and privileged-role behavior in [row security policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html). Cover reads and writes, and verify rejected operations leave data unchanged.

## Evidence boundary

Report engine/version, real connections and roles used, migration starting states, and which contention schedule was exercised. If the engine is unavailable, retain useful tests but mark integration verification blocked; do not silently substitute SQLite and claim production-engine validation.
