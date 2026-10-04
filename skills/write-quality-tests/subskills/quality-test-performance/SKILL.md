---
name: quality-test-performance
description: Design and write bounded performance and reliability tests for latency, throughput, capacity, saturation, and recovery. Use within the write-quality-tests bundle when measurable service behavior or failure recovery is in scope.
---

# Performance and reliability tests

Read the [common workflow](../../SKILL.md) once. Identify the product promise, workload, environment, and resource budget before generating a benchmark or load script. Do not invent an SLO from a documentation example.

## Define a measurable question

Record operation mix, input sizes, data volume, arrival pattern, concurrent users, warmup, measurement duration, and the environment being compared. Select relevant latency percentiles, throughput, error rate, saturation, queue age, or recovery time. Distinguish an agreed acceptance limit from an exploratory measurement.

For local benchmarks, isolate the changed operation and use the language's existing benchmark harness. Account for warmup, caching, garbage collection, compiler optimization, and measurement noise as appropriate. Compare equivalent environments and report variability; avoid brittle nanosecond assertions in ordinary unit tests.

## Model load honestly

A fixed-concurrency workload slows its arrival rate when the system slows. Use an arrival-rate model when arrivals should remain independent of completion, and track dropped work or generator saturation. This distinction and coordinated omission are explained in [k6's open and closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).

Validate response correctness during load. A fast stream of unauthorized or empty responses is not evidence that the intended operation is fast. Use representative payloads and data distribution; separate cache-warm and cache-cold questions when relevant.

Encode accepted limits as actual runner gates. For example, [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) can fail a run when metrics violate conditions. Verify exit behavior and metric tags; successful request checks alone need not make the process fail on a performance regression.

## Reliability and recovery

Choose a specific failure hypothesis: dependency timeout, partial response, exhausted pool, worker crash, queue backlog, or storage interruption. Inject it at a controlled seam and verify bounded retries, useful degraded behavior, preserved state, and recovery after removal.

Use representative integration environments when validating operational recovery. A mocked timeout tests the application's branch but cannot establish actual network or process behavior. Keep controlled tests distinct from live-service observations; see [Google SRE's reliability testing discussion](https://sre.google/sre-book/testing-reliability/).

## Bound impact

Before execution, verify target ownership, authorization, traffic ceilings, duration, resource budget, and stop conditions. Default to local or disposable test environments. Do not launch load or faults against production or shared systems based solely on a request to write tests. Stop when limits are reached or the target is unstable; preserve diagnostic artifacts.

## Evidence boundary

Report the exact workload, generator and target environment, run duration, observed metrics, errors, gate results, and limitations. Separate implemented scripts from executed measurements. Local results do not establish production capacity or long-term availability.
