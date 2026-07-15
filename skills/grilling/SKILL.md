---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. Korean triggers: "그릴링", "갈궈봐", "나 좀 갈궈", "계획 물어봐", "하나씩 물어봐", "코딩 전에 물어봐", "합의부터 하자", "질문 공세", "따져봐", "설계부터 짚자".
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

---

## 출처

Fork of [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/productivity/grilling`) —
MIT, © 2026 Matt Pocock. 원문 라이선스는 이 폴더의 `LICENSE`. 위 본문이 원문이고,
아래 "유저 커스텀" 절이 이 저장소에서 추가한 부분이다.

## 유저 커스텀 (계산촉매 — Matlantis 셀 설계)

유저 = 계산촉매 연구자. 계산 한번 = 수 시간~수십 시간. **잘못 설계한 셀 = 하루 날림.** 그래서 합의가 코드보다 싸다.

### 필수 발동 (유저가 안 불러도)
- 새 셀/스크립트 설계
- 장시간 계산(NEB, MD, 전수 스크리닝) 제출 유발
- 방법론 결정이 결과 해석을 바꿈 (descriptor 선택, 판정 기준, 참조 상태)

### 먼저 직접 확인할 것 (묻지 말고 읽어라)
사실은 파일에 있음. 물어보기 전에:
- 프로젝트 `CLAUDE.md`, `results.md` — 이미 잠긴 결정 확인. **재론 금지 항목 건드리지 말 것.**
- 기존 `.py` 셀 — 재사용 가능한 헬퍼/패턴
- 기존 `*.json` 결과 — 이미 계산된 값
- 파일 실제 존재 여부 (경로 추측 금지)

### 유저에게 물을 것 (결정만)
셀 설계 시 대개 이 순서로 의존성 풀림:
1. **이 셀이 답하는 과학적 질문이 뭐냐** — 못 답하면 셀이 필요 없음
2. **판정 기준** (예: CHxO vs C 분기를 뭘로 가르나)
3. **참조 상태 / 기준 에너지** (E_ads의 ref, μ_O regime)
4. **탐색 범위** (몇 자리, 몇 각도, region 분류)
5. **수렴·검증** (fmax, max_steps, 침투/겹침 배제 기준, TS면 imag=1)
6. **출력** (JSON 스키마, 구조 저장 범위 — best만? 전수?)

질문 하나씩. 각 질문에 **추천안 + 이유(화학적 근거) 1줄**. 답 기다림.

### 합의 후 코드 규칙
- `.py` **끝에 셀로 추가**. 터미널/채팅 붙여넣기 금지. "마지막에 세팅할까요?" 먼저.
- 결과 print 필수. 짜고 나서 처음부터 재검토.
- **전수 저장 후 best 선별** — best만 저장하면 두번 일함.
- 재개 가능하게(RESET 플래그, 종별 JSON 저장) — 서버 렉으로 날리지 말 것.

### 이전 실패 (이거 막으려고 이 스킬 씀)
- Cell 18: 합의 없이 자동배치 짬 → 흡착물이 표면 뚫고 들어감 → 폐기, 재작업.
- 볼츠만 평균 descriptor: 검증 없이 씀 → kT(0.075 eV) ≪ 에너지 퍼짐(eV)이라 최소값 하나로 붕괴 → 폐기.
- Cell 8: best만 저장 → region별 분석 필요해짐 → 전체 재실행 3h.
