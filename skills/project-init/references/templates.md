# project-init 템플릿

새 폴더에 아래 3개 파일을 만든다. `<...>`는 폴더명/유저 답변으로 채우고, 모르면 placeholder 유지.
STATUS/LOG 포맷은 **handoff 스킬과 호환**(세팅=project-init, 유지=handoff).

---

## 1. CLAUDE.md (얇게 — 전역규칙과 중복 금지)

```markdown
# <프로젝트명> (Claude 필독 — 매 세션 자동 로드)

> **세션 연속성 (handoff 스킬)**:
> - **시작 시** ("이어서"/"어디까지 했지"): `STATUS.md` + `LOG.md` 최신 엔트리 읽고 "여기까지, 다음 X" 요약부터.
> - **끝낼 때** ("저장"/"오늘 정리"): `LOG.md`에 오늘 append + `STATUS.md` 덮어쓰기(다음 수 명시).

## 프로젝트 개요
- **목표:** <한 줄 목표 — 모르면 유저에게 물어 채움>
- **성격:** <연구/개발/분석 등>
- <핵심 제약·배경 필요시>

## 폴더 구조
- `ref/` — 참고문헌·자료 원문
- `code/` — 코드·입력
- `analysis/` — 분석 스크립트·플롯·가공데이터
- `reports/` — 보고 산출물(HTML 등)
- `STATUS.md`/`LOG.md` — 연속성(handoff)

## 규칙
- **전역 규칙 적용됨** (`~/.claude/CLAUDE.md`): 간결(caveman)·grilling·팩트만·날조금지·가정vs확정 표기. 여기 중복 안 씀.
- <이 프로젝트 고유 규칙만 추가 — 코드 컨벤션·네이밍·방법론 등, 확정 시>
```

---

## 2. STATUS.md (현재 상태 1p, 매 세션 덮어쓰기)

```markdown
# STATUS — <YYYY-MM-DD>

## 지금 어디 (한 줄)
<프로젝트가 지금 어느 지점인지 한 문장 — 초기면 "세팅 완료, 착수 전">

## 진행 중 (도는 잡 + 대기 결과)
| Job | 뭐 | 상태 | 완료 시 판정 |
|---|---|---|---|
| - | 없음 | - | - |

## 즉시 다음 수 (우선순위)
1. <가장 먼저 할 것>
2. <그다음>

## 열린 질문 / 막다른 길 (반복 방지)
- <아직 못 정한 것 / 시도했다 실패한 것 + 이유>

## 최근 산출물 (파일 경로)
- <path> — <뭐>
```

---

## 3. LOG.md (누적, append-only)

```markdown
# <프로젝트명> 로그 (append-only)

## <YYYY-MM-DD> (프로젝트 세팅)
- **★ 핵심 결과**: project-init으로 폴더 세팅 완료 (CLAUDE.md/STATUS.md/LOG.md + ref/code/analysis/reports).
- 전역규칙 적용 확인.
- **다음**: <첫 작업>
```

---

## 4. 폴더 골격
```
mkdir: ref/ code/ analysis/ reports/
각 폴더에 README.md 한 줄 (예: "ref/ — 참고문헌·자료 원문") 또는 .gitkeep
```
프로젝트 성격상 불필요한 폴더(예: 코드 없는 순수 문헌조사면 code/)는 유저 동의 하에 생략 가능.
