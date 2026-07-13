---
name: handoff
description: Session continuity ("인수인계") for daily research work in any project folder. At session START ("이어서", "어디까지 했지", "resume", "오늘 시작") load STATUS.md + the latest LOG.md entry + running jobs so the new session continues as if it were the same conversation. At session END ("저장", "핸드오프", "오늘 정리", "마무리", "hand off") append today to LOG.md and rewrite STATUS.md with the explicit next action. MONTHLY ("월간 정리", "monthly rollup") archive old LOG entries and prune oversized session transcripts. Assumes the folder has CLAUDE.md / LOG.md / STATUS.md (create from references/templates.md if missing).
---

# Handoff — 세션 연속성 (인수인계)

하루를 마무리하며 **"내일의 claude에게" 인수인계 노트**를 쓰고, 다음 세션이 그 노트를 읽어 **어제와 이어서** 대화하게 만든다. Claude 내장 `/resume`은 거대 transcript를 로드해 렉을 유발할 수 있으므로, 이 스킬은 **가벼운 .md만** 읽는다.

## 어느 모드인지 먼저 판단
- 사용자 의도가 **시작/재개**("이어서", "어디까지", "resume") → **RESUME**
  - **날짜 지정**("이어서 07-11", "그저께꺼", "MM-DD에서") → RESUME 하되 최신 STATUS 대신 `project/STATUS_archive/YYYY-MM-DD.md` + 그날 LOG 엔트리를 읽는다.
- **마무리/저장**("저장", "핸드오프", "오늘 정리") → **HANDOFF**
- **월간**("월간 정리", "monthly") → **MONTHLY**
- 애매하면 물어본다.

작업 폴더 기준으로 `CLAUDE.md`, `LOG.md`, `STATUS.md`, (있으면) `MARKS.md` 를 찾는다. 없으면 [references/templates.md](references/templates.md) 로 생성 제안.

---

## MODE 1 — RESUME (세션 시작)

목적: 맥락 재설명 없이 "여기까지 왔고 다음은 X" 즉시 파악.

1. **STATUS.md 전체**를 읽는다 (현재 상태 + 즉시 다음 수 + 도는 잡). 이게 핵심 인수인계 노트.
   - 날짜 지정 재개면 대신 `project/STATUS_archive/<그날>.md`를 읽는다 (없으면 가장 가까운 이전 날짜 + 그 이유 알림).
2. **LOG.md의 가장 최근 엔트리 1개만** 읽는다 (전체 X — 길어서 렉·낭비). 최근 결정/결과 맥락. (날짜 지정이면 그날 엔트리.)
3. `MARKS.md` 있으면 훑어 현재 능력 단계 확인.
4. 도는 잡 확인: `squeue -u <user>` (또는 프로젝트의 job 시스템). STATUS의 "진행 중"과 대조.
5. **요약 보고**: `지금 어디 (한 줄) / 도는 잡·대기 결과 / 즉시 다음 수 1~3개`. 그 후 "이거 진행할까, 아니면 다른 거?" 묻거나 다음 수 착수.

주의: 무거운 스캔(`find`/`du` 트리 전체) 금지 — 캐시 렉. STATUS.md가 부실하면 그걸 지적하고 다음 HANDOFF서 개선.

---

## MODE 2 — HANDOFF (세션 끝, "저장")

목적: 오늘을 기록하고 내일용 노트를 남긴다. **"다음 수"를 반드시 명시** (이게 있어야 resume이 매끄럽다).

1. **LOG.md에 오늘 엔트리 append** (append-only, 덮어쓰지 말 것):
   - 헤더 `## YYYY-MM-DD (한 줄 요약)`
   - 오늘 한 것: 결정 / 결과(수치·Job ID) / **막다른 길·실패도 기록**(반복 방지)
2. **STATUS.md 덮어쓰기** (1페이지 유지, [references/templates.md](references/templates.md) 형식):
   - 지금 어디 (한 줄) / 진행 중 잡(표) / **즉시 다음 수(우선순위)** / 열린 질문·막다른 길 / 최근 산출물 경로
   - **덮어쓰기 전에 기존 STATUS.md를 `project/STATUS_archive/<기존날짜>.md`로 보존** (없으면 `mkdir -p STATUS_archive`), 그리고 **새 STATUS.md도 `STATUS_archive/YYYY-MM-DD.md`로 복사**. → 과거 특정일 상태로 분기 재개 가능. `cp`는 렉 안전.
3. **새 능력 milestone 도달**했으면 `MARKS.md` 갱신 (아니면 건드리지 말 것 — 실패·반복은 Mark 안 올림).
4. 마무리 한마디: "내일 '이어서'라고 하면 여기서 재개됨. ('이어서 MM-DD'로 과거 특정일 분기 가능.)"

원칙: STATUS는 **덮어쓰기**(항상 현재만) + **STATUS_archive에 날짜별 스냅샷**(과거 분기용), LOG는 **append**(역사 보존), MARKS는 **능력 도달 시만**.

---

## MODE 3 — MONTHLY (월간 정리, "월간 정리")

두 종류의 누적을 정리한다. 파괴적 작업은 **반드시 백업 먼저**.

**(A) LOG.md 텍스트 아카이브**
1. 지난달 엔트리들을 `LOG_archive/YYYY-MM.md` 로 이동.
2. LOG.md에는 그 달 **1문단 요약**만 남긴다.
3. 그달에 능력 도달 있었으면 MARKS.md에 반영 확인.

**(B) 세션 transcript 정리 (렉 예방 — 핵심)**
과거 세션 transcript(.jsonl)가 쌓이면 `/resume`·세션 로드 시 렉 유발 (100MB+ 사례 있음).
1. 프로젝트 transcript 디렉토리 찾기: `~/.claude/projects/<슬러그>/`.
2. **memory/ 폴더는 절대 건드리지 말 것** (프로젝트 기억).
3. 큰/오래된 `*.jsonl` (예: 30일 경과 또는 >20MB) → gzip 백업(`~/claude_session_backups/YYYYMM/`) 후 원본 삭제.
4. 정리 결과 보고 (몇 개, 몇 GB 확보). 복원법(`gunzip`) 안내.

주의: **현재 살아있는 세션 jsonl(최근 수정)은 제외.** mv/gzip은 메타데이터/압축이라 트리 스캔 아님(렉 안전).

---

## 다른 폴더에 적용 (포터블)
이 스킬은 전역 설치라 어느 폴더서든 작동. 새 폴더 세팅:
1. [references/templates.md](references/templates.md) 의 **CLAUDE.md resume 헤더 블록**을 그 폴더 CLAUDE.md 상단에 복붙.
2. 빈 `LOG.md`, `STATUS.md`, (원하면) `MARKS.md` 생성.
그러면 그 폴더에서도 "이어서"/"저장"이 바로 작동.
