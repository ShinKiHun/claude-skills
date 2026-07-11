---
name: expand-task-brief
description: Turn short or underspecified requests for complex research, presentation, visualization, document, app, or coding work into execution-ready briefs and then carry out the work. Use when the user cannot provide a detailed prompt, asks for a stronger or reusable prompt, gives only a rough goal for a substantial artifact, or expects the agent to infer workflow, quality criteria, validation, and deliverables without repeated prompting.
---

# Expand Task Brief

Convert a rough request into a complete internal production brief, then continue to execution.
Do not make the user write the detailed prompt that this Skill exists to supply.

## Decide whether expansion is needed

Use this workflow for complex artifacts, multi-step research work, or requests whose quality
depends on hidden criteria. Skip it for simple, already well-defined actions.

When the user explicitly asks for a prompt only, return the completed brief as a reusable prompt.
Otherwise keep the brief internal or summarize it briefly and perform the requested work.

## Build the brief

Read [references/brief-schema.md](references/brief-schema.md) and fill only the sections that
matter for the current task.

1. Inspect the conversation, attached files, repository instructions, and available Skills.
2. Identify the real outcome, audience, input evidence, final deliverables, and quality bar.
3. Separate facts supplied by the user from reversible defaults and material unknowns.
4. Choose reversible defaults without asking.
5. Ask only when a missing choice changes scientific meaning, external impact, cost, or the
   fundamental shape of the result.
6. Add required behaviors, forbidden shortcuts, an execution sequence, and concrete checks.
7. Route the work to the narrowest relevant specialist Skill when one is available.

## Execute

1. Gather or inspect source material before producing the artifact.
2. Use deterministic tools for fragile or factual operations.
3. Preserve scientific integrity: do not invent data, methods, citations, figures, or certainty.
4. Produce the actual deliverable unless the user requested planning or prompt text only.
5. Render, run, or inspect the result using checks appropriate to its format.
6. Iterate on visible or testable failures before reporting completion.

## Interaction policy

- Do not dump a long questionnaire on the user.
- Prefer one concise blocking question over many optional questions.
- State assumptions that could affect interpretation.
- Preserve the user's language and technical vocabulary.
- Do not mistake a visually impressive result for a scientifically valid result.
- Do not stop after proposing a plan when execution is authorized and feasible.

## Prompt-only output

When asked to provide a reusable prompt, write it as an executable production brief with:

- outcome and audience
- supplied inputs and missing-input policy
- required content and behavior
- domain constraints and integrity rules
- forbidden shortcuts
- workflow and tool choices
- deliverables
- validation and acceptance criteria

Avoid model-flattering language, magic phrases, and requirements that cannot be verified.
