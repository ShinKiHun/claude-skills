---
name: paper-report
description: Turn user-supplied research paper PDFs (and our own result data) into a figure-rich, professor-facing Korean research-meeting report as a self-contained HTML plus PNG figures. Extracts the papers' own figures from the PDF, plots our calculation data, and renders concept diagrams in one unified visual system. Use when the user supplies paper PDFs and wants a 사전조사/미팅자료/보고자료, or asks to build a figure-rich survey report. Korean triggers: "논문 미팅자료", "논문 보고자료", "사전조사 자료 제작", "논문 figure 뽑아서 자료", "논문 정리해서 보고자료".
---

# paper-report

교수·박사 보고용 **연구미팅 자료(figure-rich HTML)** 를 만든다. 입력은 유저가 주는 논문 PDF(1편 이상)와, 선택적으로 우리 계산결과 데이터. 그림이 많고 글은 결론 위주로 압축된 자료를 지향한다("그림 적고 글 많음"의 반대).

## 언제
- 유저가 논문 PDF를 두고 "사전조사/미팅자료/보고자료 만들어줘" 할 때.
- 논문 여러 편을 종합한 figure-rich 서베이가 필요할 때.
- 우리 계산결과(흡착E·PES·성능비교 등)를 논문과 함께 한 리포트로 묶고 싶을 때.

## figure 3소스 (핵심)
1. **논문 원본 figure** — PDF에서 추출(PNG). 주력.
2. **우리 데이터 플롯** — 계산결과를 리포트와 같은 팔레트로 시각화(`plot_data.py`).
3. **개념도** — 메커니즘 flow / 비교 매트릭스(`concept_figs.py`). 데이터인 척 금지, 개념도로만.

## 시작 전 필독
- `references/figure-extraction.md` — PDF→PNG 추출 방법·bbox 스펙·함정(먼저 읽기).
- `references/visual-system.md` — 시각 규칙(빌더/그림 만들기 전 읽기).
- `references/writing-style.md` — 한국어 보고문체·관측 vs 해석·날조 금지.
- 빌더 품질 기준 = `scripts/build_report.py`(meeting-report CSS 이식). 최소 템플릿으로 대체하지 말 것.

## 워크플로우
작업 폴더(`WORK`): `<cwd>/paper-reports/<YYYYMMDD>/<NN>_<topic-slug>/`
- 날짜 폴더(`20260717`) 안에 리포트별 폴더. 하루 여러 개면 `01_`, `02_` 순번.
- 각 리포트 폴더 = 자체완결: `report.html`, `figures/`, `report.json`, 원논문은 `src/`.
- 날짜·순번은 코드로 못 구하니(스크립트 환경 제약 아님) 유저에게 오늘 날짜 확인하거나 폴더를 보고 다음 순번 결정.

1. **입력 수집.** 유저가 준 PDF 경로 확인(`WORK/src/`에 복사). N편이면 종합 서베이로 구성.

2. **페이지 렌더 + 텍스트.**
   ```
   python scripts/extract_figures.py --dump-pages <paper.pdf> WORK --dpi 200
   ```
   → `WORK/pages/pNN.png`, `WORK/pages_text.json`, `WORK/pages_meta.json`.

3. **핵심 figure 선별 (모델 비전).** `WORK/pages/*.png` 를 **Read 로 직접 보고** 리포트에 넣을 figure를 고른다. 각 figure의 캡션("Figure N ...") 원문과 페이지 대비 bbox(0~1, 좌상단 원점)를 `WORK/figures_spec.json` 에 적는다:
   ```json
   [{"pdf":"<paper.pdf>","page":3,"fig_id":"zhu_fig2",
     "caption":"Fig. 2 …원문 캡션…","bbox_frac":[0.08,0.30,0.92,0.66]}]
   ```
   - bbox는 캡션까지 포함할지 말지 판단해서 넉넉히. 잘리면 다시 조정.
   - 단일 raster 이미지(SEM/TEM/사진)면 `--embedded` 로 원본 고해상 추출도 고려.

4. **크롭.**
   ```
   python scripts/extract_figures.py --crop WORK/figures_spec.json WORK --dpi 300
   ```
   → `WORK/figures/<fig_id>.png`. Read로 열어 잘림 없나 확인, 필요시 bbox 고쳐 재실행.

5. **우리 데이터·개념도(선택).**
   - `python scripts/plot_data.py spec.json` (kind: line/bar/scatter/pes)
   - `python scripts/concept_figs.py spec.json` (kind: flow/matrix)
   - 실데이터가 아니면 spec의 `"note"` 에 표기(예 `"개략도"`/`"예시"`).
   - **figure 라벨·note 한글 OK** — 스크립트가 Malgun Gothic으로 렌더(NanumSquare는 mpl space 버그로 Malgun 우선, `references/visual-system.md` 참조). LaTeX 수식(`$...$`)은 영문/기호만.

6. **DOI 검증.** 인용 논문 DOI는 Crossref/출판사로 대조. 미검증·추정은 "추정" 표기. 날조 금지.

7. **본문 작성 → `WORK/report.json`.** 한국어, 결론 우선. 섹션마다 대표 figure 1개. 스키마는 `references/writing-style.md` 와 `scripts/build_report.py` 상단 docstring 참조. 핵심 필드: `title`(em 허용)·`subtitle`·`kicker`·`brand`·`date`·`pills`·`meta`·`sections[{id,num,nav,kicker,title,take,body_html,figure|figures,layout,table_html}]`·`refs`·`footer`.

8. **HTML 조립.**
   ```
   python scripts/build_report.py WORK/report.json WORK WORK/report.html
   ```
   → 자체완결 HTML(figure는 data-URI 인라인). 원본 PNG는 `WORK/figures/` 에 그대로 남음("png + html").

9. **검증.** `WORK/report.html` 을 열어(또는 figure PNG를 Read로) 그림 잘림/겹침·캡션·nav·인쇄레이아웃·값 출처(DOI resolve) 확인. 유저에게 경로 + 요약만 보고.

## 원칙
- 그림 우선, 글은 결론 위주. 섹션마다 figure 1개.
- 자체완결(원격 스크립트·폰트·이미지 금지).
- 논문 figure는 출처 표기(`credit`: "Fig. N of DOI:…").
- 관측 / 해석 / 가정 / 예정 구분. 부정적 결과도 정직히.
