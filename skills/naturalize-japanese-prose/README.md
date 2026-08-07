# Naturalize Japanese Prose

Agent Skill for revising AI-generated or AI-assisted Japanese without changing its meaning, facts, logical relations, information, stance, or claim strength.

The skill focuses on practical editing:

- diagnose repetitive structures, excessive signposting, and forced contrasts
- replace vague abstractions and noun-heavy phrasing with clearer syntax
- reduce mechanical connective patterns and uniform sentence rhythms
- remove unnecessary dramatic commas from titles and headings
- preserve terminology, qualifications, quotations, and genre-specific conventions
- audit the rewrite in both directions for semantic additions or omissions

## Contents

- `SKILL.md`: Agent-facing workflow, preservation rules, and output modes
- `references/analysis.md`: Detailed taxonomy of recurring prose patterns and editing guidance
- `references/checklist.md`: Semantic-preservation and naturalness checks

## Install

```bash
npx skills add 45deg/skills --skill naturalize-japanese-prose
```

## Language

The skill instructions and references are written in Japanese because the editing criteria depend on Japanese syntax, punctuation, register, and genre conventions.
