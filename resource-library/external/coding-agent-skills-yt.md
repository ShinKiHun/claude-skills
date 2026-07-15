---
title: "코딩 에이전트 스킬 세트 (YouTube 소개 6+1)"
resource_type: "external-guide"
status: "partially-adopted"
source_url: "https://www.youtube.com/watch?v=5rbzj5IUA78"
collected_at: "2026-07-12"
updated_at: "2026-07-15"
verbatim_copy: false
license_checked: true
---

# Summary

한 YouTube 영상에서 소개된 Claude Code(터미널·에이전트)용 커뮤니티 스킬 묶음이다.
모두 `~/.claude/skills/`에 설치하거나 플러그인 마켓플레이스로 붙이는 방식이며, claude.ai
웹·앱 스킬과는 별개다. 대부분 소프트웨어 엔지니어링 워크플로에 최적화되어 있어, 계산촉매
연구(DFT/MLIP, Python 분석, 논문·발표자료) 관점에서 곧바로 쓸모 있는 것과 과한 것을
`frequency`로 구분해 둔다. 개별 출처와 검색 메타데이터는 [../catalog.yaml](../catalog.yaml)에 있다.

## Classification

| 스킬 | 제작자/저장소 | 종류 | 주된 역할 | frequency | 채택 |
|---|---|---|---|---|---|
| `ponytail` | DietrichGebert | 외부 Skill | 과설계 억제, 최소 코드(YAGNI·표준/네이티브 우선) | occasional | 보류 |
| `caveman` | JuliusBrussee | 외부 Skill | 출력 토큰 절약용 terse 응답(코드·에러는 원문 유지) | core | **채택 → `skills/caveman`** |
| `taste-skill` | Leonxlnx | 외부 Skill | 프론트엔드 디자인 취향(과감함·모션·밀도) 조절 | occasional | 보류 |
| `mattpocock/skills` | Matt Pocock | 스킬 모음 | 계획 인터뷰(grill), TDD, triage, code-review 등 | occasional | **부분 채택 → `skills/grilling`** |
| `ECC` | affaan-m | 프레임워크 | 60+ 에이전트·200+ 스킬·보안 스캐너 하네스 | rare | 보류 |
| `last30days` | mvanhorn | 외부 Skill | 지난 30일 커뮤니티·웹 조사 후 근거 있는 요약 | occasional | 보류 |
| `superpowers` | obra(Jesse Vincent) | 프레임워크 | brainstorming→계획→TDD→서브에이전트 방법론 | rare | 보류 |

`taste-skill`(3번)은 이미 `fieldby-claude-design-top-5` 컬렉션에 `design-taste-frontend`로
등록되어 있어 catalog.yaml에 중복 추가하지 않는다. 이 표에서는 세트 구성상 함께 표기만 한다.

## Frequency 기준

- `core` 는 실제 연구 작업에서 반복 검증된 스킬에만 부여한다. 2026-07-15 기준 `caveman` 만
  해당한다(DRM 세션에서 계속 켜 두고 사용).
- `occasional` 은 지금 워크플로에 바로 얹어 볼 만한 것, `rare` 는 본격 소프트웨어 개발이나
  팀 규모 작업에 가까워 연구용으로는 과한 것을 뜻한다.
- 실제로 자주 쓰게 되면 catalog.yaml의 해당 `frequency` 를 `core` 로 올린다.

## 채택 현황 (2026-07-15)

두 개를 커스텀 fork 로 가져와 `skills/` 에서 직접 관리한다. 원문을 그대로 쓰는 게 아니라
연구 워크플로에 맞게 고쳐 쓰기 때문에, 외부 참조 메모로만 두지 않고 이 저장소의 Skill 로
승격했다. upstream 라이선스(MIT)는 각 Skill 폴더의 `LICENSE` 로 동봉했다.

| 채택 | upstream | 커스텀 내용 |
|---|---|---|
| [`skills/caveman`](../../skills/caveman/) | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 한국어 유지. 압축 금지 목록(에너지 수치+단위, 경로·JSON 키·셀 번호·시스템 태그, 화학 표기 `CH3*`/`Ov`/`MvK`/`μ_O`, 코드블록, 계산 파라미터). 장식용 표 금지. 보고 형식 = 결론 1줄 + 수치 + 다음 스텝. 압축 해제 조건에 "계산 제출 전 확인", "데이터가 결론을 지지하지 않을 때" 추가 |
| [`skills/grilling`](../../skills/grilling/) | [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/productivity/grilling`) | Matlantis 셀 설계 시 필수 발동. 사실(잠긴 결정·기존 `.py`·기존 JSON)은 직접 읽고 **결정만** 질문. 질문 6단 의존 순서 = 과학적 질문 → 판정 기준 → 참조 상태 → 탐색 범위 → 수렴·검증 → 출력 스키마. 과거 실패 사례(흡착물 표면 침투, 볼츠만 평균 붕괴, best-only 저장) 명시 |

한글 트리거를 각 `SKILL.md` 의 `description` 에 추가해 두어서 한국어로 말해도 자동 발동한다.
`caveman` 은 [`global/user-CLAUDE.md`](../../global/user-CLAUDE.md) 를 설치하면 매 세션 상시 적용된다.

`ponytail` 은 같은 자리에서 검토했지만 이번엔 채택하지 않았다. 최소 코드 원칙 자체는
전역 규칙의 "over-engineering 금지" 항목으로 이미 흡수했다.

## Use when

- 연구용 Python 분석 스크립트를 짧고 단순하게 유지하고 싶을 때 → `ponytail`
- 긴 코딩·분석 세션에서 응답 토큰을 아끼고 싶을 때 → `caveman`
- MLIP·계산 방법론처럼 빠르게 바뀌는 분야의 최신 동향을 훑고 싶을 때 → `last30days`
- 발표자료·연구 시각화의 프론트엔드 품질을 높이고 싶을 때 → `taste-skill`
- 복잡한 작업을 시작하기 전에 범위를 집요하게 확정하고 싶을 때 → `mattpocock`의 grill

## Avoid when

- 원자 좌표·물리 모델·도메인 정확성이 핵심인 계산화학 작업(디자인/코드 최소화 스킬은 무관)
- 탐색적 분석 스크립트 수준에 ECC·superpowers 같은 무거운 프레임워크를 얹으려 할 때
- 원본 저장소·패키지 소유자·최신 명령어·라이선스를 확인하지 않고 곧바로 설치할 때
- `last30days`의 API 키(OpenAI·xAI 등) 같은 비밀값을 저장소나 공유 명령어에 남기려 할 때

## Verification notes

- 각 스킬의 설명은 공개 저장소·문서를 요약한 것이며 원문 전체를 복제하지 않았다.
  단 `caveman` 과 `grilling` 은 fork 로 채택했으므로 `skills/` 안에 원문 기반 파일과
  upstream `LICENSE`(둘 다 MIT)를 함께 둔다.
- 채택한 두 개는 2026-07-15 에 설치·발동까지 확인했다(`tested_locally: true`).
  나머지 다섯 개는 여전히 미검증이다.
- 이전 메모에 `caveman` 을 "Matt Pocock 의 원본에서 파생" 이라고 적었던 것은 **오류**였다.
  `LICENSE` 기준 저작자는 Julius Brussee 이고, Matt Pocock 은 `grilling` 쪽 upstream 이다.
  2026-07-15 에 `catalog.yaml` 과 함께 수정했다.
- `ECC`는 규모가 크고 공식 채널(github.com/affaan-m/ECC, npm의 ecc-universal·ecc-agentshield)
  외 미러에 악성코드 위험이 보고되므로 설치 시 출처를 반드시 확인한다.
- 실제 설치 시 원본 저장소, 패키지 소유자, 최신 명령어와 라이선스를 다시 확인한다.
