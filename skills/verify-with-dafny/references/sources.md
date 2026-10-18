# Provenance and adaptation

This is an independently written community skill, not an official Dafny or Quint skill.

On 2026-10-05, inspected the full (non-truncated) tree of `dafny-lang/dafny` at `5f717bf447b19d38cad1b69b1bf9a9f102feccfb`: no `SKILL.md` or `skills/` paths. Also inspected the 22 public repositories returned for the Dafny organization and searched the web for official Dafny agent skills; no official distribution was identified. This search does not establish that no official skill could exist elsewhere or be published later.

Following the user's fallback instruction, the workflow draws on the official [Quint modeling skill](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-modeling/SKILL.md) and its [source-code intake guidance](https://github.com/quint-co/quint-llm-kit/blob/cc75369f741af7d490936f82002c2d28e3b3d78d/quint-llm-kit-plugin/skills/quint-modeling/guidelines/from-code.md). The local `verify-with-quint` skill provided repository layout conventions.

Retained ideas: inspect actual source, separate required properties from implementation, document abstractions and correspondence, develop executable artifacts incrementally, check that meaningful cases are possible, and report the scope of evidence.

Dafny-specific replacements: contracts and verification conditions replace Quint state exploration; inductive loop invariants and termination measures replace simulation depth; heap frames and old-state snapshots describe mutation; assumed/external contracts require a trust audit. The Quint modeling skill's simulation-only iteration policy is not carried over: a Dafny proof request requires running `dafny verify`. No Quint tools or companion skills are required.

The skill text is independently authored; upstream skill text/code is not vendored. The [Dafny language guide](language-guide.md) contains selective summaries and links to the official language documentation.
