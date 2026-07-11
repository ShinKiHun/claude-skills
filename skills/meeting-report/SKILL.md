---
name: meeting-report
description: Create polished self-contained HTML reports for recurring research meetings. Use when the user says "자료 제작" for a daily report, "총자료 제작" for a weekly synthesis, or asks for a daily research report, weekly meeting report, lab update, or professor-facing progress summary from the current session and project evidence.
---

# Meeting Report

Generate a concise, evidence-first research report that can be opened offline and printed.
Use the current working directory as the project root.

## Select the mode

- For `자료 제작`, create one daily report from today's work.
- For `총자료 제작`, synthesize the active week's daily reports into `total.html`.
- For equivalent natural-language requests, infer daily versus weekly from the user's wording.

## Read the required guidance

1. Read [references/content-selection.md](references/content-selection.md) before gathering evidence.
2. Read [references/visual-system.md](references/visual-system.md) before building HTML or figures.
3. Reuse [scripts/example_builder.py](scripts/example_builder.py) as the HTML quality baseline.
4. Use [scripts/example_section_figs.py](scripts/example_section_figs.py) when a section needs a
   concept flow or comparison matrix and no result plot exists.

Do not replace the validated builder with a minimal template.

## Determine the report path

Store every report under `reports/<YYYYMMDD_YYYYMMDD>/`.

For a daily report:

1. Find the latest directory matching `YYYYMMDD_YYYYMMDD`.
2. Reuse it when today is inside its date range and it has no `total.html`.
3. Otherwise create `<today>_<today+6 days>`.
4. Write the daily report as `<today>.html`.

For a weekly report:

1. Use the active weekly directory.
2. Read its daily HTML files as the primary evidence.
3. Write `total.html`.
4. Ask before replacing an existing `total.html`.

## Build the report

1. Gather only task-relevant evidence from the current session, project journal, git history,
   and mentioned result files.
2. Separate observed results, interpretation, unresolved risk, and next action.
3. Select three to six meaningful sections for a daily report. Rebuild weekly reports as a
   coherent story rather than concatenating daily entries.
4. Put a dedicated figure, structure rendering, plot, scheme, or matrix in every core section.
5. Embed local images as data URIs and keep the report self-contained.
6. Preserve the user's language; default to Korean with established English technical terms.
7. Include professor decisions or discussion questions in the weekly report.

Never invent measurements, calculations, images, or conclusions. Label estimates and incomplete
evidence explicitly.

## Verify before finishing

1. Open the generated HTML.
2. Inspect every figure for clipping, overlap, broken text, and unreadable labels.
3. Check navigation anchors, scroll progress, local image embedding, and print layout.
4. Confirm that reported values can be traced to a source.
5. Return only the output path and a concise summary after verification.
