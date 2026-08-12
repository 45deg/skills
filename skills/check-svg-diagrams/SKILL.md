---
name: check-svg-diagrams
description: Inspect, render, visually review, validate, and help repair standalone SVG diagrams using available SVG-to-image or browser tools plus a dependency-free Python CLI that inventories labels, checks safe markup and references, estimates bounds, lists likely overlaps and clipping, and audits connectors and arrow markers. Use when reviewing, diagnosing, fixing, or performing pre-delivery QA on SVG flowcharts, architecture or network diagrams, ER or organization charts, state or sequence diagrams, timelines, maps, UML, dashboards, icons, charts, or dense composite diagrams. Do not use for raster-only inputs or for purely aesthetic redesign with no SVG inspection task.
---

# Check SVG Diagrams

Combine structural evidence with an actual rendered view. Keep renderer choice flexible: discover what the current environment provides, probe a suitable option with the target SVG, and fall back when rendering or font behavior is unreliable. The bundled Python CLI itself remains headless and never opens a browser, GUI, or network connection.

## Workflow

1. Identify the SVG path and any explicit requirements: expected labels, stable IDs, or directed relationships.
2. Run the complete static inspection before opening the SVG in a browser or another active renderer:

   ```bash
   python3 <skill-directory>/scripts/svg_check.py report diagram.svg --format table
   ```

3. Stop before visual rendering when the report contains unsafe markup or external references. Resolve or isolate those errors first.
4. As the Coding Agent, inspect the current session's tools and the local environment for a viable SVG renderer, image viewer, browser workflow, or computer-use capability. Keep this discovery and orchestration outside `svg_check.py`.
5. Render with any viable SVG-to-image tool or isolated browser workflow. Verify that an image was produced, inspect it at the intended delivery size, and try another renderer when fonts, filters, clipping, or external resources fail.
6. Compare overlap, overflow, connector, and alignment warnings with the rendered view. Compare semantic relationships with the source specification or user intent.
7. Make the smallest SVG edit that fixes the confirmed defect. Preserve unrelated layout, content, styling, and identifiers.
8. Rerun the relevant static command, render again, and inspect the corrected region. Summarize what was confirmed, changed, and rechecked.

Read [visual-rendering.md](references/visual-rendering.md) before choosing or invoking a renderer. Read [checks.md](references/checks.md) when interpreting severities, requirement files, approximate bounds, or structured connector metadata. Read [review-heuristics.md](references/review-heuristics.md) when planning inspection passes for an unfamiliar or dense SVG.

## Commands

Run one focused command or the aggregate `report` command:

```bash
python3 <skill-directory>/scripts/svg_check.py validate diagram.svg
python3 <skill-directory>/scripts/svg_check.py labels diagram.svg --format table
python3 <skill-directory>/scripts/svg_check.py overlaps diagram.svg --format json
python3 <skill-directory>/scripts/svg_check.py connectors diagram.svg --format table
python3 <skill-directory>/scripts/svg_check.py report diagram.svg --format json
```

Supply explicit requirements when available:

```bash
python3 <skill-directory>/scripts/svg_check.py report diagram.svg \
  --require-label "Payment approved" \
  --require-id approval-arrow \
  --spec requirements.json
```

Use JSON for automation and tables for interactive review. Exit code `1` means one or more deterministic errors; exit code `2` means the file could not be inspected. Warnings do not change the exit code.

## Judgment Rules

- Do not prescribe one universal renderer. Choose among available native tools, CLI rasterizers, browser automation, or session-provided image tools according to the SVG features and environment constraints.
- Treat command discovery as a candidate list, not proof of capability. Probe the actual SVG and verify the output file; an installed renderer can still fail on fonts or unsupported SVG features.
- Run structural safety checks before browser rendering. Use an isolated browser session without personal profiles or credentials, disable or restrict network access when possible, and close the session afterward.
- Do not install software, download browser binaries, open a headed GUI, or exceed the current environment's permissions without the required user approval.
- Do not report an approximate overlap as a confirmed visual defect without rendered evidence. Text width is estimated because the CLI does not load or shape fonts.
- Ignore intentional containment, such as text inside a labeled box, unless text crosses the box boundary or another label.
- Audit color-only encoding separately from contrast. First inventory every non-color cue already present—explicit text, value, shape, pattern, icon, position, or line style. Report color-only encoding only when the intended distinction would be lost without color; do not require an extra non-text cue when a clear label already distinguishes the states. A label can still fail contrast even when it prevents color-only encoding.
- Prefer stable `id`, `data-role`, `data-source`, and `data-target` attributes when relating findings to diagram semantics.
- Match required labels exactly after whitespace normalization. Do not silently translate, paraphrase, or infer missing content.
- Prioritize blocking markup and reference errors, then label collisions and clipping, then connector direction and marker defects, then cosmetic spacing.

## Report Findings

For each actionable finding, include:

- affected element IDs or generated element keys;
- category and severity;
- the structural or geometric evidence;
- the renderer and output size used for visual confirmation;
- the smallest proposed correction;
- the command or visual check used after the edit.

Separate deterministic machine failures, likely visual defects, and semantic uncertainty. If the CLI reports no defect, state only that the static checks passed; do not claim pixel-perfect or semantic correctness.
