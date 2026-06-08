# Apply UD Color Design

Agent Skill for applying Color Universal Design (CUD) palette data and UD color-design checks to web, DTP, charts, maps, slides, signs, and other visual artifacts.

The skill focuses on practical use:

- choose screen RGB or print CMYK values by medium
- select starter color sets for charts, maps, and signage
- flag hard-to-distinguish color pairs
- add redundant cues such as labels, icons, patterns, borders, line styles, and marker shapes
- keep generated diagrams, swatches, and design outputs project-specific

## Contents

- `SKILL.md`: Agent-facing workflow and application rules
- `references/cud-palette-data.md`: Screen RGB and print CMYK palette data
- `references/cud-combination-guidance.md`: Candidate color sets and risk pairs
- `references/ud-color-design-rules.md`: Practical rules for redundant cues,
  labeling, contrast, and output checks

## Install

```bash
npx skills add 45deg/skills --skill ud-color-design
```

## Reference

> 出典: 『カラーユニバーサルデザイン推奨配色セット ガイドブック』第２版  
> 発行年: 2018年  
> 発行者: カラーユニバーサルデザイン推奨配色セット制作委員会