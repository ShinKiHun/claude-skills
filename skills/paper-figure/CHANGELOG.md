# paper-figure — 변경 기록

> **이 스킬을 고치는 Claude 에게**
> 코드를 바꿨으면 **맨 위에 항목 하나를 새로 추가**하고 커밋해라. 기존 항목은 고치지 않는다.
> 형식은 아래와 같다. `담당` 에는 자기 모델명을 적는다 (예: `Claude Opus 5`, `Claude Sonnet 5`).
>
> ```markdown
> ## YYYY-MM-DD — <담당 모델>
> **무엇** 한 줄 요약
> - `파일명` 바꾼 내용
> **왜** 이유. 안 적으면 다음 사람이 되돌린다
> **검증** 실제로 돌려본 것
> ```
>
> 규칙 세 가지
> 1. **기존 API 를 깨지 말 것.** 함수 시그니처를 바꿔야 하면 기본값으로 하위호환을 남기고 여기 적는다.
> 2. **실제 연구 수치·사람 이름을 넣지 말 것.** 이 저장소는 public 이다. 예시는 더미값으로.
> 3. **고쳤으면 자가검사를 돌려라.** `python scripts/pubstyle.py`, `python scripts/recipes.py`

---

## 2026-10-06 — Claude Opus 5 (1M context)

**무엇** `pubfig` → `paper-figure` 로 개명하고, 그림 레시피 3종을 `recipes.py` 로 분리했다.

- `SKILL.md` — `name: pubfig` → `paper-figure`. 트리거에 구명 `pubfig` 는 남겨 기존 호출 유지.
  레시피 절 추가. 개인 호칭 제거.
- `scripts/recipes.py` — **신설**
  - `value_scatter(ax, x, y, ...)` 마커 색 = 값 + 컬러바. `line=` 가이드선, `zero_line=` 기준선
  - `value_barh(ax, names, values, ...)` 막대 색 = 값. 정렬·끝단 숫자라벨·컬러바·`highlight=` 강조
  - `metric_title(ax, what, metric)` 제목 2줄, 2번째 줄 괄호에 지표
- `scripts/pubstyle.py` — 주석에서 개인 호칭만 제거. **코드 변경 없음**
- `.gitignore` — 자가검사 png / `__pycache__` / `.bak` 제외

**왜**
`pubfig` 는 목록에서 뭔지 안 보였다. `paper-report`(논문→HTML)와 짝이 되게 `paper-figure` 로.
레시피는 여러 프로젝트에서 같은 코드를 매번 다시 쓰고 있었다 — EOS 포물선, k점 수렴곡선,
모델 벤치 MAE 막대. 공통점이 **"색 = 값 + 옆에 컬러바 + 지표는 제목 2번째 줄"** 이라
그 셋만 함수로 뽑았다. 스타일 프리셋(`pubstyle`)과 그림 레시피(`recipes`)는 층이 달라 파일을 나눴다.

**검증**
- `python scripts/recipes.py` → 3패널 자가검사 통과
- `python scripts/pubstyle.py` → plain / lab 둘 다 통과
- 스킬 폴더 밖에서 `sys.path` 로 import 해 동작 확인 (전역 스킬에 의존 안 함)

---

## 2026-09-14 — (기록 이전. git log 에서 복원)

**무엇** 스킬 최초 작성 + `plain` 프리셋 추가.

- `scripts/pubstyle.py` 신설 — DRM `drmstyle.py` 규약을 프로젝트 무관하게 옮긴 것
- `preset="lab"` — 4면 테두리 1.6 pt, 볼드 라벨, 눈금 안쪽, lab 팔레트
- `preset="plain"` (기본) 추가 — matplotlib 기본 rc + Arial 14/12/10 + 300 dpi, parity plot 룩
- plain 계열색을 `inferno` 추출(진보라·적주황·노랑)로 통일

**왜** 그림 스타일을 매번 새로 고르지 않으려고. 두 룩만 쓴다.
