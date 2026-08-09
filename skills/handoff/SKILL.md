---
name: handoff
description: Session continuity ("인수인계") for daily research work in any project folder. At session START ("이어서", "어디까지 했지", "resume", "오늘 시작") load STATUS.md + dead-ends.md + the decisions/ index + the latest LOG.md entry + running jobs so the new session continues as if it were the same conversation. At session END ("저장", "핸드오프", "오늘 정리", "마무리", "hand off") append today to LOG.md, promote confirmed decisions into decisions/ and failures into dead-ends.md, then rewrite STATUS.md with the explicit next action. MONTHLY ("월간 정리", "monthly rollup") archive old LOG entries — never discarding dead ends or decisions — and prune oversized session transcripts. Assumes the folder has CLAUDE.md / LOG.md / STATUS.md (create from references/templates.md if missing).
---

# Handoff — 세션 연속성 (인수인계)

하루를 마무리하며 **"내일의 claude에게" 인수인계 노트**를 쓰고, 다음 세션이 그 노트를 읽어 **어제와 이어서** 대화하게 만든다. Claude 내장 `/resume`은 거대 transcript를 로드해 렉을 유발할 수 있으므로, 이 스킬은 **가벼운 .md만** 읽는다.

## 어느 모드인지 먼저 판단
- 사용자 의도가 **시작/재개**("이어서", "어디까지", "resume") → **RESUME**
  - **날짜 지정**("이어서 07-11", "그저께꺼", "MM-DD에서") → RESUME 하되 최신 STATUS 대신 `project/STATUS_archive/YYYY-MM-DD.md` + 그날 LOG 엔트리를 읽는다.
- **마무리/저장**("저장", "핸드오프", "오늘 정리") → **HANDOFF**
- **월간**("월간 정리", "monthly") → **MONTHLY**
- 애매하면 물어본다.

작업 폴더 기준으로 `CLAUDE.md`, `STATUS.md`, `LOG.md`, `dead-ends.md`, `decisions/`, (있으면) `MARKS.md` 를 찾는다. 없으면 [references/templates.md](references/templates.md) 로 생성 제안.

**핵심 원칙 — 조회 키가 다르면 파일을 나눈다.** 나중에 아무도 *"7월 22일에 뭐 했지?"* 로
찾지 않는다. **"이거 왜 이렇게 정했지?"** 로 찾는다. 그래서 결정은 `decisions/`(사안별),
실패는 `dead-ends.md`(영구), 시간축은 `LOG.md`(최신 1개만 읽음)로 분리한다.
그래야 **다음 세션이 읽는 양이 시간에 따라 늘지 않는다.**

---

## MODE 1 — RESUME (세션 시작)

목적: 맥락 재설명 없이 "여기까지 왔고 다음은 X" 즉시 파악.

> **먼저 확인**: `SessionStart` 훅이 설치돼 있으면 `STATUS.md` · `dead-ends.md` ·
> `decisions/` 인덱스 · `LOG.md` 최신 엔트리가 **이미 컨텍스트에 주입돼 있다.**
> 그 경우 1~3단계를 **다시 읽지 말고** 4단계로 간다. 중복 읽기는 낭비다.
> (훅 설치: 저장소 루트에서 `./setup.sh` — `hooks/install_hooks.py` 가 병합 설치한다.)

1. **STATUS.md 전체** (현재 상태 + 즉시 다음 수 + 도는 잡). 핵심 인수인계 노트.
   - 날짜 지정 재개면 대신 `project/STATUS_archive/<그날>.md`를 읽는다 (없으면 가장 가까운 이전 날짜 + 그 이유 알림).
2. **`dead-ends.md` 전체.** 짧고 영구다. **이미 실패한 것을 다시 제안하지 않기 위해 매번 읽는다.**
3. **`decisions/` 는 파일명 인덱스만.** 본문은 관련된 것만 연다.
   이게 있어야 *그저께 왜 그렇게 정했는지*를 안다 — LOG 최신 1개만 읽으면 모른다.
4. **LOG.md 최신 엔트리 1개만** (전체 X — 길어서 렉·낭비). (날짜 지정이면 그날 엔트리.)
5. `MARKS.md` 있으면 훑어 현재 능력 단계 확인.
6. 도는 잡 확인: `squeue -u <user>` (또는 프로젝트의 job 시스템). STATUS의 "진행 중"과 대조.
7. **요약 보고**: `지금 어디 (한 줄) / 도는 잡·대기 결과 / 즉시 다음 수 1~3개`. 그 후 "이거 진행할까, 아니면 다른 거?" 묻거나 다음 수 착수.

주의: 무거운 스캔(`find`/`du` 트리 전체) 금지 — 캐시 렉. STATUS.md가 부실하면 그걸 지적하고 다음 HANDOFF서 개선.

**STATUS가 낡았으면 그대로 믿지 말 것.** 주입된 STATUS 날짜보다 새로운 산출물이
보이면 사용자에게 알리고, 그 공백을 이번 HANDOFF에서 메운다. 낡은 상태를 자신 있게
말하는 것이 아무 말 안 하는 것보다 나쁘다. (`Stop` 훅이 낡음을 감지해 경고한다.)

---

## MODE 2 — HANDOFF (세션 끝, "저장")

목적: 오늘을 기록하고 내일용 노트를 남긴다. **"다음 수"를 반드시 명시** (이게 있어야 resume이 매끄럽다).

**"오늘 한 것" 나열은 쓰지 마라.** 그건 폴더·파일 타임스탬프가 이미 말한다.
어제의 claude가 가졌던 것 중 **파일에서 복구되는 건 사실뿐**이고, **판단 · 합의 ·
무지의 경계**는 적지 않으면 사라진다. LOG는 그 셋만 적는다.

1. **LOG.md에 오늘 엔트리 append** (append-only, 덮어쓰지 말 것). 5칸 고정:
   - 헤더 `## YYYY-MM-DD (한 줄 요약)`
   - `### 판정` — 오늘 확정된 것 + **근거(파일:키/DOI)** + `[계산확인|문헌확인|추정]`
   - `### 결정` — 무엇을 골랐고 **무엇을 왜 버렸나** → `decisions/NNNN-*.md` 포인터
   - `### 막다른 길` — 시도 → 실패 이유 → `dead-ends.md` 에도 한 줄
   - `### 열린 질문` — 아직 모르는 것 + 답하려면 무엇이 필요한지
   - `### 다음 수` — 구체적으로
2. **승격** (이게 핵심 — LOG에 묻으면 나중에 못 찾는다):
   - 확정된 결정 → `decisions/NNNN-<slug>.md` 새 파일 (ADR 형식, 템플릿 §5).
     기존 결정이 뒤집혔으면 **그 파일을 지우지 말고** 상태를 `대체됨(→ NNNN)` 으로 바꾼다.
   - 실패 → `dead-ends.md` 에 한 줄 append. **영구 파일. 절대 지우지 말 것.**
3. **STATUS.md 덮어쓰기** (1페이지 유지, [references/templates.md](references/templates.md) 형식):
   - 지금 어디 (한 줄) / 진행 중 잡(표) / **즉시 다음 수(우선순위)** / 열린 질문·막다른 길 / 최근 산출물 경로
   - **덮어쓰기 전에 기존 STATUS.md를 `project/STATUS_archive/<기존날짜>.md`로 보존** (없으면 `mkdir -p STATUS_archive`), 그리고 **새 STATUS.md도 `STATUS_archive/YYYY-MM-DD.md`로 복사**. → 과거 특정일 상태로 분기 재개 가능. `cp`는 렉 안전.
4. **새 능력 milestone 도달**했으면 `MARKS.md` 갱신 (아니면 건드리지 말 것 — 실패·반복은 Mark 안 올림).
5. 마무리 한마디: "내일 새 창을 열면 여기서 재개됨. ('이어서 MM-DD'로 과거 특정일 분기 가능.)"

원칙: STATUS는 **덮어쓰기**(항상 현재만) + **STATUS_archive에 날짜별 스냅샷**(과거 분기용),
LOG는 **append**(시간축 색인), `decisions/`·`dead-ends.md`는 **영구 누적**(사안별),
MARKS는 **능력 도달 시만**.

---

## MODE 3 — MONTHLY (월간 정리, "월간 정리")

두 종류의 누적을 정리한다. 파괴적 작업은 **반드시 백업 먼저**.

**(A) LOG.md 텍스트 아카이브 — 칸마다 수명이 다르다**

| 칸 | 아카이브 시 |
|---|---|
| 막다른 길 | **영구.** 이미 `dead-ends.md` 에 있는지 확인하고 없으면 옮긴다 |
| 결정 | **영구.** `decisions/` 에 있는지 확인하고 없으면 승격시킨다 |
| 판정 | 영구. 뒤집혔으면 지우지 말고 취소선 + 정정 링크 |
| 열린 질문 | 닫혔으면 판정으로, 아직이면 STATUS 로 |
| 다음 수 · 진행 중 잡 | **하루살이. 버려도 된다** |

1. **버리기 전에 승격 여부부터 확인한다.** 막다른 길과 결정이 전용 파일에 없는 채로
   아카이브되면 사실상 소실이다.
2. 지난달 엔트리들을 `LOG_archive/YYYY-MM.md` 로 이동.
3. LOG.md에는 그 달 **1문단 요약**만 남긴다.
4. 그달에 능력 도달 있었으면 MARKS.md에 반영 확인.

⚠️ **"한 달 지나면 폐기"는 하지 마라.** 막다른 길을 버리는 순간 같은 실패를 반복한다.
아카이브는 *다음 세션이 읽는 양*을 줄이는 것이지 기록을 없애는 것이 아니다.

**(B) 세션 transcript 정리 (렉 예방 — 핵심)**
과거 세션 transcript(.jsonl)가 쌓이면 `/resume`·세션 로드 시 렉 유발 (100MB+ 사례 있음).
1. 프로젝트 transcript 디렉토리 찾기: `~/.claude/projects/<슬러그>/`.
2. **memory/ 폴더는 절대 건드리지 말 것** (프로젝트 기억).
3. 큰/오래된 `*.jsonl` (예: 30일 경과 또는 >20MB) → gzip 백업(`~/claude_session_backups/YYYYMM/`) 후 원본 삭제.
4. 정리 결과 보고 (몇 개, 몇 GB 확보). 복원법(`gunzip`) 안내.

주의: **현재 살아있는 세션 jsonl(최근 수정)은 제외.** mv/gzip은 메타데이터/압축이라 트리 스캔 아님(렉 안전).

---

## 다른 폴더에 적용 (포터블)
이 스킬은 전역 설치라 어느 폴더서든 작동. 새 폴더 세팅 (`project-init` 이 자동으로 해준다):
1. [references/templates.md](references/templates.md) 의 **CLAUDE.md 연속성 헤더 블록**을 그 폴더 CLAUDE.md 상단에 복붙.
2. 빈 `LOG.md`, `STATUS.md`, `dead-ends.md`, `decisions/` 디렉토리, (원하면) `MARKS.md` 생성.
그러면 그 폴더에서도 "이어서"/"저장"이 바로 작동.

## 자동화 — 사용자가 안 쳐도 돌게
"이어서"를 **쳐야만** 상태를 읽는 구조는 실패한다. 사용자가 그냥 일 얘기부터 시작하면
STATUS 존재조차 모른 채 대화가 시작되고, 사용자가 어제를 다시 설명하게 된다.

저장소 루트의 `./setup.sh` (Windows `.\setup.ps1`) 가 훅 2개를 **병합** 설치한다:

| 훅 | 하는 일 |
|---|---|
| `SessionStart` → `hooks/inject-status.py` | 새 창마다 STATUS · dead-ends · decisions 인덱스 · LOG 최신 1개를 **자동 주입** |
| `Stop` → `hooks/status-stale.py` | STATUS 가 실제 작업보다 6시간 이상 낡으면 한 줄 경고 |

연속성 파일이 없는 폴더에서는 두 훅 모두 **조용히 통과**한다. 설치기는 기존
`settings.json` 의 다른 훅을 보존하고 우리 항목만 교체한다(`--uninstall` 로 제거).
