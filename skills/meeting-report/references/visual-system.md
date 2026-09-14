# Visual System

## 디자인 시스템 — 먹과 주사 (2026-08-29 확정, 유저 승인)

**이 절이 룩앤필의 단일 진실원천이다.** 이전에는 구조만 규정하고 색·서체 규정이 없어
매번 기본값(청록+황토 그라디언트, 둥근 카드, 그림자)으로 흘러갔다. 그 조합은 쓰지 않는다.

### 팔레트 (hex 고정)

| 역할 | 값 | 쓰는 곳 |
|---|---|---|
| 바탕 | `#FAFAFA` | `--bg` 페이지 |
| 카드 | `#FFFFFF` | `--card` |
| 먹 면 | `#E7EAED` | `--fieldA` hero·take·중립 강조 **배경으로만** |
| 주사 면 | `#F2E8E7` | `--fieldB` 대비되는 두 번째 면 **배경으로만** |
| 먹 잉크 | `#1B2730` | `--ink` / `--inkA` (먹 면 위) |
| 주사 잉크 | `#5E2A26` | `--inkB` (주사 면 위) |
| 인라인 강조 | `#41525E` | `--acc` 링크·kick·강조 텍스트 |
| 주의 | `#8A6A1E` / 면 `#FAF4E6` | `--warn` / `--warnbg` |
| 실패·무효 | `#B02A20` / 면 `#F8E9E7` | `--fail` / `--failbg` |
| 헤어라인 | `#E4E3E1` | `--hair` **선은 이거 하나만** |

**★ 색 역할 분리 (중요)** — 주사(붉은 계열)를 인라인 강조로 쓰면 실패 신호와 겹친다.
- 주사 `#F2E8E7` 는 **배경 면으로만**. 텍스트·아이콘·막대에 쓰지 않는다.
- 인라인 강조는 먹 계열 `--acc`.
- 실패는 `--fail` 텍스트를 `--failbg` 채워진 면 위에서만.

### 구조 규칙 — 깔끔함은 색이 아니라 이 규칙에서 나온다

- **테두리 금지.** 구획은 선이 아니라 **색 면**으로 나눈다. 예외: `figure`, `table.s` 의 헤어라인 1 px.
- **그림자 금지.** `--shadow:none`. `box-shadow` 를 새로 넣지 말 것.
- **그라디언트 금지.** hero 배경도 단색 면(`--fieldA`).
- **좌측 accent bar 금지** (`.hero::before` 류). 흔한 AI 클리셰다.
- **`border-radius` 는 2~3 px.** 20 px 둥근 카드 쓰지 않는다.
- 헤어라인은 `--hair` 한 종류. 굵기·색을 여러 개 쓰지 않는다.
- 여백을 넉넉히. 밀도를 낮춘 만큼 투사 거리에서 읽힌다.

### 타이포그래피

- 서체는 기존 체계 유지 (meeting-report: `Noto Sans KR` 스택 / paper-report: NanumSquare base64 임베드).
  **자체완결이 우선이므로 Google Fonts 원격 링크로 바꾸지 말 것.**
- 위계는 **굵기로만** 만든다: 400 본문 / 600 강조 / 800 제목.
- 숫자는 `font-variant-numeric: tabular-nums`. 표에서 자릿수가 세로로 맞아야 한다.
- 투사 기준 최소 크기: 본문 15 px, 표 14 px, 핵심 수치 22 px 이상.

### 투사(미팅 화면) 전제

이 보고서는 **교수·박사 미팅에서 3~5 m 거리로 투사**된다.
- 회색 위 회색은 프로젝터에서 사라진다. 명도차로 구획한다.
- 한 화면에 한 주장. 대시보드식 밀집은 투사에서 무너진다.
- 결론(`take`)을 근거보다 먼저.


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
- a lightbox: every figure `<img>` carries `class="zoom"` and clicking it opens the image
  full-screen with its caption (`#lb` overlay, Esc or click-outside to close) — the builder has it

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
