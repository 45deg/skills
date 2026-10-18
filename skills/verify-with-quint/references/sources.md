# Official sources and adaptation

Reviewed 2026-10-05. Upstream skill snapshot: `quint-co/quint-llm-kit` commit `cc75369f741af7d490936f82002c2d28e3b3d78d`. This independently written workflow is informed by official materials; it does not vendor the upstream bundle or require its plugins, MCP servers, or Choreo framework. It is not an official Quint skill.

## Skill basis

- [quint-modeling](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-modeling/SKILL.md): state/pure-logic/property separation, incremental execution, constant instantiation, witnesses and invariants.
- [Code intake](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-modeling/guidelines/from-code.md): operation/state inventory, abstraction, atomic granularity, source correspondence.
- [Review](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-modeling/guidelines/review.md): initialization, transition completeness, meaningful properties and runtime checks.
- [quint-lang](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-lang/SKILL.md), [CLI](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-lang/guidelines/cli.md), [simulations](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-lang/guidelines/simulations.md): syntax, seeds, traces, sampled-check interpretation.
- [Upstream license](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/LICENSE): Apache-2.0; upstream authorship belongs to Informal Systems and contributors. Upstream text/code is not redistributed here.

## Technical authority

- [CLI manual](https://quint.sh/docs/quint): current command/flag semantics; installed help takes precedence for installed-version behavior.
- [Checking properties](https://quint.sh/docs/checking-properties): reachability, invariants, induction, and `TypeOK`.
- [Model checkers](https://quint.sh/docs/model-checkers): finite-state TLC, bounded symbolic Apalache, temporal support differences.
- [Simulator](https://quint.sh/docs/simulator): sampled execution without temporal verification.
- [Language manual](https://quint.sh/docs/lang) and [built-ins](https://quint.sh/docs/builtin): actions, types, collections, temporal operators.
- [Model-based testing](https://quint.sh/docs/model-based-testing): additional implementation-conformance evidence.
- [Apalache documentation](https://apalache-mc.org/docs/): backend configuration and limitations.

## Adaptation decisions

The official modeling workflow uses simulation while constructing a model and reserves model checking for explicit verification requests. This skill proceeds to a budgeted model check when the user requests formal verification; simulation is preparatory evidence.

Source behavior, requirements, and assumptions remain distinct. Model counterexamples need source-feasibility classification. Induction counterexamples may start in unreachable states. Witnesses show existential reachability: zero sampled hits do not prove unreachability, and positive hits do not prove liveness.

Message soup, thin actions, cohesive records, separate tests, and Choreo are useful choices rather than universal correctness conditions. Retain multiplicity/ordering when relevant. Routine modeling does not require repeated type-sketch approval; ask about material ambiguities.

Report backend-specific scope: depth for ordinary Apalache checks, completed finite exploration for TLC, and explicit obligations for induction. None automatically establishes implementation correctness.
