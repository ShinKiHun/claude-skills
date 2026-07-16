# Writing Style & Content

교수·박사 대상 연구미팅 보고문체. content-selection에서 이식·조정.

## 내용 선정
- 결론을 바꾸는 것, 가설을 세우거나 기각하는 것, 미팅에서 질문 나올 수치, 실패와 그 진단, 다음 단계를 정하는 것 위주.
- 논문 서베이면: 각 논문의 핵심 결과·활성점·방법(실험/DFT)·수치를 뽑고, 논문 간 비교·우리 과제 함의로 종합.
- 루틴한 나열·저가치 서술 생략. figure로 말할 수 있으면 글 줄임.

## 과학 보고 원칙
- 모든 실질 주장에 근거·출처(DOI, figure, 수치) 부착.
- 부정적 결과·막힌 지점 정직히. 실패는 진단과 함께.
- **관측 / 해석 / 가정 / 예정 시험**을 구분.
- 불확실을 확실로 바꾸지 말 것.
- **날조 금지.** 공간 채우려 없는 plot·수치 만들지 말 것. 개념도는 "측정데이터 아님"이 분명할 때만.
- DOI·서지는 검증된 것만. 추정은 "추정" 표기.

## 문체
- **결론 먼저.**
- 한국어 보고체 `~했음`, `~로 판정`, `~규명`.
- 표준 영어 기술용어 보존(formate, coverage, reconstruction, RDS, inverse catalyst 등).
- **지수·아래첨자 표기**: 유니코드 위첨자(⁻¹ 등 U+207B)는 NanumSquare/Malgun에 글리프가 없어 깨질 수 있음.
  - HTML 본문: `h<sup>−1</sup>`, `CO<sub>2</sub>` 처럼 `<sup>`/`<sub>` 태그 사용. (일반 아래첨자 ₂나 CO₂는 대체로 OK, 위첨자 마이너스만 주의)
  - figure(matplotlib): LaTeX mathtext `$h^{-1}$`, `$CO_2$` 사용.
- 칭찬·홍보·장식 설명 지양.
- 독립 take·불릿·캡션·note 끝의 마침표 생략. 한 블록 안 여러 문장 사이 마침표는 유지.

## report.json 스키마 (build_report.py 입력)
```json
{
  "title": "결론형 제목 <em>강조</em> 허용",
  "subtitle": "한 문단 lead",
  "kicker": "Preliminary Survey · 2026-07-17",
  "brand": "cu-MOF", "date": "2026-07-17",
  "pills": [{"text":"핵심 배지", "cls":"k"}],   // cls: k=teal, o=ochre, c=clay
  "meta": "hero 하단 메타(시스템·방법 등)",
  "sections": [
    {"id":"s1","num":1,"nav":"① 라벨",
     "kicker":"Concept","title":"섹션 제목",
     "take":"한 줄 결론",
     "body_html":"<ul class='p'><li>근거…<b>강조</b></li></ul>",   // 자유 HTML(신뢰 입력)
     "figure":{"src":"figures/fig1.png","caption":"캡션","credit":"Fig.2 of DOI:10…"},
     "layout":"duo",                 // 있으면 figure|body 좌우
     "table_html":"<table class='s'>…</table>"
    }
  ],
  "refs": ["Zhu et al., Nat. Commun. 2020 — 10.1038/s41467-020-19438-w"],
  "footer": "cu-MOF · paper-report"
}
```
- `body_html`/`table_html`은 자유 HTML(스크립트가 이스케이프 안 함) — 우리가 쓰는 신뢰 입력만.
- 재사용 클래스: `ul.p`(불릿), `p.tx`(문단), `table.s`+`td.n`(숫자), `.keep/.drop/.mn`(색 수치), `.note.o`(주의)/`.note.c`(실패).
- 복수 figure는 `"figures":[…]`. 대표 1개면 `"figure":{…}`.
