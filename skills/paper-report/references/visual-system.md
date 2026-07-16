# Visual System

meeting-report에서 검증된 시각 시스템을 이식. 빌더 = `scripts/build_report.py`(CSS 내장).
컴포넌트·반응형·data-URI 임베딩·인쇄 규칙을 보존하고 내용만 바꾼다. 최소 템플릿으로 대체 금지.

## 리포트 필수 구성
- 상단 고정 nav(섹션 앵커) + 스크롤 진행바
- hero: 작은 kick 라벨 + **결론형 제목** + 짧은 lead + 결과 배지(pill) 3~5개 + 메타
- 번호 섹션: 한 줄 take(결론) + 대표 figure + 캡션 + 간결한 근거
- 절제된 주의(orange)/실패(red) note — 시각적으로 구분
- 우측정렬 수치 표(`table.s`, 숫자셀 `td.n`)
- 인쇄 CSS: nav 숨김 + 섹션 page-break

## 폰트
- **HTML 텍스트 = NanumSquare**(`assets/fonts/`의 R/B/EB를 @font-face base64로 임베드 → 자체완결, 어느 브라우저서도 나눔스퀘어). `_fonts.font_faces_css()`가 처리.
- **figure(matplotlib) = Malgun Gothic 1순위 + NanumSquare 폴백.** NanumSquare ttf는 mpl에서 **space 글리프가 깨져 공백이 ▢로 렌더**되는 버그가 있어 Malgun을 먼저 쓴다(유저 DRM 리포트서 검증된 회피책). `_fonts.register_mpl()`가 처리.
  - 결과: figure 한글 라벨·note 모두 정상 렌더(Malgun). 영문 강제 불필요.
  - 단 LaTeX 수식(`$...$`)은 mathtext라 영문/기호만.

## Figure 규칙
- **핵심 섹션마다 전용 figure 1개.**
- 우선순위: 논문 원본 figure > 우리 실데이터 플롯 > 개념도. 개념도를 데이터인 척 쓰지 말 것.
- 실데이터가 아니면 `"note"`에 `"개략도"`/`"예시"` 표기 → figure에 워터마크로 박힘.
- 임베디드 이미지는 실용상 500 KB 내외 목표(과대해상 지양). 크롭 DPI 300은 선명하나 큼 → 페이지폭 그림은 200도 충분.
- 캔버스 여백은 텍스트·그림자·박스패딩 고려해 넉넉히. 내용 늘면 캔버스도 같이 키움.
- **겹침 금지**: 도형·화살표·텍스트가 서로 겹치거나 잘리지 않게. 좌표한계는 내용보다 넉넉히, `concept_figs` flow는 박스 세로중앙 텍스트 + 화살표 양끝 gap + `set_aspect('equal')`로 처리됨.

## Layout
- figure+텍스트 좌우 배치(`layout:"duo"`)는 둘 다 읽힐 때만.
- 본문은 미팅 화면에서 읽힐 만큼 압축. 섹션 결론(take)을 먼저.
- orange=주의, red=실패/무효 예측.
- 장식 그라디언트·거대 여백·빽빽한 텍스트 벽 지양.
- 자체완결 유지(원격 스크립트·폰트·이미지 없음).

## 시각 QA (임베딩 전 필수)
생성한 figure를 Read로 열어 확인:
- 텍스트가 박스 안에 있나
- 라벨·화살표 겹침 없나
- 가장자리 잘림 없나
- 일반 확대에서 폰트 읽히나
- 범례·단위 있나
- 표 수치와 figure 값 일치하나

그다음 최종 HTML을 열어 화면·인쇄 레이아웃 둘 다 확인.
