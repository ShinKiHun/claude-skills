# paper-figure — 변경 기록

> **이 스킬을 고치는 Claude 에게**
> 코드를 바꿨으면 **맨 위에 항목 하나를 새로 추가**하고 커밋해라. 기존 항목은 고치지 않는다.
> 형식은 아래와 같다. `담당` 에는 **작업 중인 프로젝트 폴더명 + 모델명** 을 적는다.
> 폴더명을 쓰는 이유는 "어느 작업에서 고친 건지" 가 바로 보이기 때문이다.
> ⚠️ **전체 경로는 쓰지 말 것** — 이 저장소는 public 이고 경로에 계정명이 들어간다.
> 폴더 이름만 쓴다.  `AIzeroC` ○  /  `C:\Users\<이름>\...\AIzeroC` ✗
>
> ```markdown
> ## YYYY-MM-DD — <프로젝트 폴더명> / <모델명>
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

## 2026-10-16 (2) — 현대자동차 / Claude Opus 5.5 (1M context)

**무엇** 점 라벨 겹침 방지 `label_points` 추가, SKILL.md 에 사용 규칙 명시.

- `scripts/recipes.py` — `label_points(ax, x, y, labels, bold=(), s=70, fontsize=8, pad=1.5, priority=None)`: 8 방향 x 6 거리 후보 중 (기존 라벨 겹침 x10 + 마커 겹침 + 축 밖 x50 + 거리) 비용 최소 위치. 굵은(우선) 라벨 먼저, 바로 옆이 아니면 회색 연결선. 외부 패키지 없음. 자가검사 (a) 패널에 적용.
- `SKILL.md` — 레시피 3) 추가, 규칙: 점 라벨 산점도는 `label_points` 필수.
- 연결선 shrinkB 를 포인트 단위 마커 반지름(√s/2)으로 (처음 픽셀 값을 넣어 선이 사라졌음). 굵은 테두리 마커는 호출 측에서 s 를 키워 넘길 것.

**왜** 고정 오프셋 annotate 로 근접한 점들의 라벨이 서로·마커와 겹쳐 읽을 수 없다는 지적.

**검증**
- 밀집 더미(8점 σ=0.05 + 10점) seed 1–3: 글자 영역 기준 라벨-라벨 겹침 0, 라벨-마커 겹침 0. (Annotation.get_window_extent 는 연결선까지 포함하므로 검사는 Text.get_window_extent 로)
- `python scripts/recipes.py` 자가검사 통과

---

## 2026-10-16 — 현대자동차 / Claude Opus 5.5 (1M context)

**무엇** `value_barh` 가 음수 값을 그릴 수 있게 했다. SKILL.md·recipes.py 의 import 경로를 실제 폴더명으로 고쳤다.

- `scripts/recipes.py` — `value_barh`: x 범위를 `[min(0,v), max(0,v)]` + 14 % 여유로, 숫자 라벨은 음수면 막대 왼쪽(ha=right), 음수가 있으면 x=0 기준선. 양수만이면 기존과 동일(`xlim = (0, max*1.14)`, 오프셋 `max*0.012`).
- `SKILL.md`, `scripts/recipes.py` docstring — `skills/pubfig/scripts` → `skills/paper-figure/scripts` (개명 후 남은 구 경로).

**왜** 기준 대비 차이(ΔE vs 기준 표면)처럼 음·양이 섞인 순위 막대를 그리면 `set_xlim(0, max*1.14)` 때문에 음수 막대가 잘렸다.

**검증**
- `python scripts/recipes.py` 자가검사 통과 (양수 순위 막대 기존과 같은 범위)
- 음수 더미 [-0.6 … 0.7] → xlim (-0.782, 0.882), 정렬·강조 정상

---

## 2026-10-06 — AIzeroC / Claude Opus 5 (1M context)

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

## 2026-09-14 — (기록 이전. git log 에서 복원 — 담당 미상)

**무엇** 스킬 최초 작성 + `plain` 프리셋 추가.

- `scripts/pubstyle.py` 신설 — DRM `drmstyle.py` 규약을 프로젝트 무관하게 옮긴 것
- `preset="lab"` — 4면 테두리 1.6 pt, 볼드 라벨, 눈금 안쪽, lab 팔레트
- `preset="plain"` (기본) 추가 — matplotlib 기본 rc + Arial 14/12/10 + 300 dpi, parity plot 룩
- plain 계열색을 `inferno` 추출(진보라·적주황·노랑)로 통일

**왜** 그림 스타일을 매번 새로 고르지 않으려고. 두 룩만 쓴다.
