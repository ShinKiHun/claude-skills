# Execution-Ready Brief Schema

Use this schema selectively. Omit sections that add no value.

## 1. Outcome

Define the artifact or decision to produce in observable terms. Name the file type, working
experience, or final state when relevant.

## 2. Audience and context

Identify who will use or review the result, what they already know, and how the artifact will be
used. A journal-club deck, lab update, public website, and internal analysis need different
narratives even when they start from the same source.

## 3. Inputs and evidence

List the files, data, URLs, repository context, and prior outputs that are authoritative. State
what to do when an input is missing. Prefer a labeled gap over invented content.

## 4. Domain truth

Record facts and constraints that must remain correct. Separate:

- supplied facts
- verified facts from source material
- reversible design defaults
- assumptions requiring disclosure
- unknowns that require a user decision

## 5. Required behaviors

Describe the scenes, sections, controls, analyses, or steps the result must contain. Tie each
requirement to the audience or purpose rather than accumulating decorative features.

## 6. Forbidden shortcuts

Name likely failure modes, for example:

- replacing a requested artifact with a static mockup
- inventing scientific results or citations
- summarizing a paper without building an argument
- generating code without running or rendering it
- using decorative visuals that hide missing evidence
- ignoring an existing template, component system, or project convention

## 7. Workflow

Define the smallest reliable sequence:

1. inspect inputs
2. infer and state the narrative or technical approach
3. build with the appropriate specialist tools
4. validate intermediate outputs
5. render or run the final artifact
6. repair failures and report remaining limitations

## 8. Deliverables

List exact files or outputs and distinguish required from optional artifacts.

## 9. Acceptance criteria

Use checks that can fail clearly:

- scientific claims trace to source evidence
- required sections or interactions are present
- files open and render without errors
- text and figures do not overlap or clip
- links, controls, navigation, or scripts work
- unsupported conclusions are labeled

## Compact example

A short request such as “이 논문으로 연구실 발표자료 만들어줘” can expand internally to:

- build a figure-first review deck for a computational-science lab audience
- extract the paper's research question, novelty, method, main evidence, limitations, and
  discussion questions
- preserve the paper's uncertainty and distinguish calculation from validation
- select figures by argumentative role rather than page order
- use claim-style slide titles and one dominant visual per slide
- render every slide and inspect overflow, readability, and broken images
- deliver the deck plus a short list of unresolved source gaps

The user should only be asked about choices such as presentation length or audience when the
available context cannot support a safe default.
