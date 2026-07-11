# Visual System

## Baseline

Use `../scripts/example_builder.py` as the validated report builder. Replace its content while
preserving the component system, responsive behavior, data-URI embedding, and print rules.

The report must contain:

- a fixed top navigation with section anchors and a scroll progress indicator
- a hero with a small kick label, conclusion-led title, short lead, three to five result badges,
  and report metadata
- numbered sections with a one-line take, dominant figure, caption, and concise evidence
- restrained warning and failure notes that are visually distinct
- compact numeric tables with right-aligned values
- print CSS that hides navigation and creates clean section page breaks

## Figures

- Give every core section its own figure.
- Prefer real result plots, structure renderings, or calculation outputs.
- When no plot exists, create a clearly labeled concept flow, comparison matrix, or mechanism
  scheme without presenting it as data.
- Use English inside generated figures when Korean fonts are unavailable.
- Keep embedded images near 500 KB each when practical.
- Use enough canvas margin for text, shadows, and box padding.
- If content grows, increase the canvas together with the elements.
- Base subtitle offsets on the actual title line count.

For matplotlib diagrams, keep the coordinate limits at least five percent wider than the content
bounds. Do not fit the axes exactly to boxes or arrows.

## Layout

- Use a figure and text side by side only when both remain legible.
- Keep body text compact enough for a meeting screen.
- Put the section conclusion before supporting details.
- Use orange for cautions and red for failures or invalid predictions.
- Avoid decorative gradients, oversized empty areas, and dense walls of text.
- Keep the report self-contained with no remote scripts, fonts, or images.

## Visual QA

Render and open every generated figure before embedding it. Check:

- text stays inside boxes
- labels and arrows do not overlap
- no edge is clipped
- font size remains readable at normal browser zoom
- legends and units are present when needed
- table numbers and figure values agree

Then open the final HTML and verify both screen and print layouts.
