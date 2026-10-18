# Execution and evidence

Examples use Quint 0.33.0 syntax; replace paths, names, and budgets for the task. `quint` means the project's local executable/wrapper. Check installed help and current official documentation when flags differ.

## Prepare execution

Inspect `quint --version`, `quint run --help`, and `quint verify --help`. Check compatible Java/backend availability. Checkers may be downloaded; keep caches/output in permitted locations and record resolved versions. Avoid modifying global runtime configuration.

In 0.33.0, `QUINT_HOME` can direct checker/evaluator downloads to a dedicated writable directory. The default Rust evaluator may require a separate download; use the supported TypeScript evaluator explicitly for simulation/tests when that dependency is unavailable, recording the backend. TLC uses the Apalache distribution's JAR, so an available Java executable alone is not sufficient.

Bind constants in a concrete analysis module, e.g. `import protocol(NODES = Set(1, 2)).*`. Select the intended module explicitly in multi-module files. Record custom init/step, source revision or hashes, model/instance, commands, seed, versions, output, and exit status.

Use available timeout/process controls for a wall-clock budget and backend configuration for memory. Apalache depth limits do not limit TLC runtime. Inspect state growth before expanding. Retain partial logs and label interrupted runs incomplete.

## Static, scenario, and sampled checks

```sh
quint typecheck specs/quint/protocol.qnt
quint test specs/quint/protocolTest.qnt --main protocolTest --match regressionTest --backend typescript
quint run specs/quint/protocol.qnt --main protocolAnalysis \
  --backend typescript --invariant safety --witnesses completed rejected \
  --max-samples 10000 --max-steps 50 --seed 12345
```

Typechecking does not establish executability or properties. `run` definitions can contain nondeterminism; not all Quint tests are deterministic.

In Quint 0.33.0, `quint test` without `--match` selects names ending in `Test`. Selecting a module with `--main` does not select every `run` definition in it. For a differently named scenario, pass its name via `--match`; for example, `--match regressionScenario`. Check the result for the intended name and a nonzero passing/failing count. A zero exit code or a module heading alone can mean no tests ran. Treat missing or zero counts as unconfirmed execution, fix selection, and rerun before reporting success. Preserve whether each test expects the property to hold or expects a known violation; a passing counterexample scenario is evidence of the defect.

Start with a debugging sample, then choose task-appropriate sample/depth budgets. No fixed sample size proves correctness. Positive witness hits establish observed paths; zero is inconclusive. Save simulation traces with `--out-itf trace.itf.json`; replay the same seed, module, init/step, limits, and evaluator backend. Use `--verbosity 3`, optionally `--mbt`, to inspect picks and action names; instrumentation is not necessarily complete.

## Apalache bounded checking

```sh
quint verify specs/quint/protocol.qnt --main protocolAnalysis \
  --backend apalache --invariant safety --max-steps 10
```

A completed ordinary invariant check covers executions through the specified depth in this instance. State both depth and domain/assumption bounds; longer executions and other sizes remain outside the claim. Confirm intended properties were selected.

`--random-transitions` uses symbolic sampling. SMT unknown, timeout, translation error, exhaustion, or interruption is inconclusive. In 0.33.0, verification `--out-itf` is Apalache-only and suppresses console output; inspect the artifact and exit status rather than treating silence as success.

## TLC finite-state exploration

```sh
quint verify specs/quint/protocol.qnt --main protocolAnalysis \
  --backend tlc --invariant safety
```

All reachable state must be finite, including counters, queues, and history. TLC does not use Apalache's `--max-steps` bound. Only completed exploration supports an exhaustive claim, for the selected finite instance/configuration rather than arbitrary sizes.

Inspect deadlock diagnostics. Valid termination and unintended lack of enabled work differ. Idle actions intentionally allow stuttering but change deadlock detection and can admit infinite non-progress executions; document that choice.

## Temporal properties and fairness

Witnesses/scenarios do not prove liveness. Define eventual outcome plus premises excluding starvation, permanent loss, or endless crashes. State weak/strong fairness and its action/actor scope; fairness of combined `step` need not imply fairness of each participant.

Check current documentation and the installed backend's support for the exact formula/specification. TLC supports temporal checking; Apalache temporal support is partial. A bounded safety pass does not establish unbounded temporal properties.

Where supported, use `--temporal propertyName` with the chosen backend. Inspect effective generated/configured specification and fairness premises, not just a `temporal` declaration. If required premises cannot be represented/checked, report the gap; a bounded progress monitor or reachability check is weaker evidence and must be labeled accordingly.

Do not assume fairness of failures/retries without an actual environment guarantee. Check consistency of premises and reachability of meaningful work to avoid vacuous implications.

## Inductive invariants

Use Apalache's `--inductive-invariant` only for a justified stronger safety argument. Read current [induction guidance](https://quint.sh/docs/checking-properties#inductive-invariants), including `TypeOK` constraints on arbitrary candidate states.

Check initiation (`Init` implies `Inv`), preservation (`Inv` and `Next` imply `Inv'`), and implication of required safety. All relevant obligations must complete for the actual encoding. Preservation counterexamples can begin in unreachable states: they refute inductiveness, not necessarily reachable safety. Strengthen a justified candidate or diagnose encoding before claiming a source defect.

Successful induction still applies to modeled domains/premises; it is not automatically parameterized verification or implementation refinement.

## Report language

| Evidence | Supported statement |
| --- | --- |
| Static checks pass | Model passed static checks |
| Positive witness hit | Target state reached in sampled execution(s) |
| No sampled violation | No counterexample in N samples, depth D, seed S |
| Completed ordinary Apalache check | No violation for selected instance through depth D |
| Completed TLC exploration | Property holds for fully explored finite instance/configuration |
| Completed induction obligations | Modeled safety established by initiation, preservation, implication |
| Invariant counterexample | Model property violated; source feasibility classified separately |
| Error/timeout/partial exploration | Verification incomplete; name the blocker |

Separate properties and methods. A successful command proves nothing about properties not selected. Source-level claims additionally need fidelity, refinement, regression reproduction, or implementation conformance evidence.

## Replay the bundled fixture

From this skill's directory, use `assets/check-then-act.qnt` as the input. It has multiple modules, so always select one:

```sh
quint typecheck assets/check-then-act.qnt
quint test assets/check-then-act.qnt --main checkThenActTest --backend typescript
quint test assets/check-then-act.qnt --main recheckedTest --backend typescript
quint run assets/check-then-act.qnt --main Current --backend typescript \
  --invariant safety --max-samples 100 --max-steps 10 --seed 12345
quint verify assets/check-then-act.qnt --main Current \
  --backend apalache --invariant safety --max-steps 4
quint verify assets/check-then-act.qnt --main Rechecked \
  --backend tlc --invariant safety
```

The current variant intentionally violates `safety` after both actors observe and commit; a counterexample exit is expected for that query. The `staleCheckTest` passes by asserting the existence of this known bad sequence. The rechecked variant allows only one commit. Both variants have a finite state space and intentionally admit idle/stuttering; do not infer liveness from their safety checks.

## Coverage and evidence integrity

Apply these checks when translating stateful implementations or investigating repeated/concurrent behavior; a small pure function does not need a concurrency campaign.

- Explain what each bound removes, not only its numeric value. Limiting each participant to one operation excludes repeated interaction even if exploration is exhaustive. When reuse or delayed observations matter, permit one participant to retain an observation while others complete repeated operations, recycle state, and then let it resume. Include recovery or retry cycles when relevant to the contract.
- Preserve arithmetic and identity semantics. A reduced finite domain can expose a failure mechanism; report it as a reduced-instance result and explain whether the trace transfers to production. Do not infer all-width correctness from a small passing instance, or production reachability from an arbitrary injected state.
- Separate safety, rejection behavior, and progress obligations. If the contract requires progress despite an unavailable participant, examine relevant interruption boundaries and the remaining participants' enabled behavior. Do not assume the unavailable participant eventually resumes. Distinguish a finite timeout from a demonstrated non-progress cycle or a proof.
- For each result, identify the required property, source/model version, premises, selected check, and supported conclusion. A successful known-failure scenario establishes that failure; it does not establish a repair. Verification counts aggregate unlike obligations and are not a measure of contract coverage.
- Retain a counterexample against its original version and replay it against the repair. At handoff, confirm that the delivered files are the versions used for the reported checks. Record hashes with commands and outcomes when local files can change independently of a commit; label stale evidence rather than silently attaching it to the latest files.
