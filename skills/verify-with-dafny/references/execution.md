# Execution and evidence

Command shape for Dafny 4.11.0:

```sh
dafny --version
dafny verify --help
dafny verify model.dfy --verify-included-files --cores 1 --verification-time-limit 30 --log-format text
```

The timeout is **per assertion batch**, not a whole-process budget. Set a separate wall-clock budget for a large proof. Check exit status and final verifier summary; preserve stdout and stderr. A success that verifies zero intended obligations is not sufficient evidence. Confirm the file/symbol selection and included dependencies; library and external contracts may be trusted rather than checked.

For diagnosis, check version-supported options such as `--isolate-assertions`, `--log-format csv`, `--resource-limit`, `--analyze-proofs`, and `--extract-counterexample`. Proof analysis can warn about contradictory assumptions but may produce spurious warnings; it is not a complete consistency check. Experimental counterexample output needs interpretation and reproduction. Remove temporary symbol/position filters for the final full check.

Keep failed originals separate from repaired files. For a mutation check, copy the verified artifact, change a consequential implementation operation without changing the contract, and run it separately. A rejection caused solely by syntax/type errors does not demonstrate that the functional contract caught the mutation. Record the actual failed obligation.

Use project tooling if installed. Otherwise consult official installation instructions, select a compatible pinned release, and use a local tool directory where authorized. Do not silently change global tools. If unavailable, deliver source plus reproducible commands and clearly mark proof execution unverified. Compilation or runtime tests may need additional target-language tools; verification success does not establish those checks.

## Replay the bundled fixture

From this skill's directory, check [first-index.dfy](../assets/first-index.dfy) and [first-index-mutant.dfy](../assets/first-index-mutant.dfy) separately:

```sh
dafny verify assets/first-index.dfy --verify-included-files --cores 1 --verification-time-limit 30
dafny verify assets/first-index-mutant.dfy --verify-included-files --cores 1 --verification-time-limit 30
```

`FirstIndex` accepts any finite sequence of mathematical integers and returns the first matching index, or `-1` exactly when the target is absent. Its contract specifies bounds, membership, absence, and first occurrence. The loop invariant excludes matches in the processed prefix; `decreases` proves termination. No additional preconditions or assumed facts are needed. `Main` checks empty, singleton, duplicate, last-position, and absent cases. The explicit slice assertion helps the solver instantiate the duplicate case; it is itself proved.

The mutant changes only `while i < |values|` to `while i + 1 < |values|`, skipping the last element. Its contract, invariants, and caller checks are unchanged. For `[7]` and target `7`, the loop never runs and returns `-1`, violating the absence contract. Keep this expected failure separate from passing verification targets; do not verify both files together, because they declare the same methods.

Observed with Dafny 4.11.0 on macOS arm64, 2026-10-18:

| Check | Exit | Result |
| --- | --- | --- |
| Original verification | 0 | `3 verified, 0 errors` |
| Mutant verification | 4 | `2 verified, 1 error`; the absence postcondition fails at `return -1` |
| Original Python compilation and execution | 0 | `3 verified, 0 errors`, then `-1 0 1 1 -1` |

The mutant's caller can still verify against the declared contract, even though the method body fails to establish it. Only the full target's result supports a proof claim. The mutation check demonstrates sensitivity to this defect, not completeness of the specification.

To compile and run the original with the Python backend (requires Python 3), copy it to a temporary working directory so generated files stay outside the skill:

```sh
fixture_dir=$(mktemp -d)
cp assets/first-index.dfy "$fixture_dir/first-index.dfy"
dafny run --target py "$fixture_dir/first-index.dfy" --cores 1 --verification-time-limit 30
```

Expected output after successful verification is `-1 0 1 1 -1`. The proof covers all admitted inputs of this standalone Dafny method; the five executions are runtime examples. Neither establishes correspondence to a foreign-language or production implementation.

## Documentation

Use the [Dafny language guide](language-guide.md) for topic summaries and links to the versioned manual, tutorials, installation instructions, and releases. Consult the matching version when syntax or semantics are uncertain; installed CLI help determines available flags and defaults.

## Coverage and evidence integrity

Apply these checks when translating stateful implementations or investigating repeated/concurrent behavior; a small pure function does not need a concurrency campaign.

- Explain what each bound removes, not only its numeric value. Limiting each participant to one operation excludes repeated interaction even if exploration is exhaustive. When reuse or delayed observations matter, permit one participant to retain an observation while others complete repeated operations, recycle state, and then let it resume. Include recovery or retry cycles when relevant to the contract.
- Preserve arithmetic and identity semantics. A reduced finite domain can expose a failure mechanism; report it as a reduced-instance result and explain whether the trace transfers to production. Do not infer all-width correctness from a small passing instance, or production reachability from an arbitrary injected state.
- Separate safety, rejection behavior, and progress obligations. If the contract requires progress despite an unavailable participant, examine relevant interruption boundaries and the remaining participants' enabled behavior. Do not assume the unavailable participant eventually resumes. Distinguish a finite timeout from a demonstrated non-progress cycle or a proof.
- For each result, identify the required property, source/model version, premises, selected check, and supported conclusion. A successful known-failure scenario establishes that failure; it does not establish a repair. Verification counts aggregate unlike obligations and are not a measure of contract coverage.
- Retain a counterexample against its original version and replay it against the repair. At handoff, confirm that the delivered files are the versions used for the reported checks. Record hashes with commands and outcomes when local files can change independently of a commit; label stale evidence rather than silently attaching it to the latest files.
