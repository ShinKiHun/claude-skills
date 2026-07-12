---
title: "코딩 에이전트 스킬 세트 (YouTube 소개 6+1)"
resource_type: "external-guide"
status: "reference"
source_url: "https://www.youtube.com/watch?v=5rbzj5IUA78"
collected_at: "2026-07-12"
verbatim_copy: false
license_checked: false
---

# Summary

한 YouTube 영상에서 소개된 Claude Code(터미널·에이전트)용 커뮤니티 스킬 묶음이다.
모두 `~/.claude/skills/`에 설치하거나 플러그인 마켓플레이스로 붙이는 방식이며, claude.ai
웹·앱 스킬과는 별개다. 대부분 소프트웨어 엔지니어링 워크플로에 최적화되어 있어, 계산촉매
연구(DFT/MLIP, Python 분석, 논문·발표자료) 관점에서 곧바로 쓸모 있는 것과 과한 것을
`frequency`로 구분해 둔다. 개별 출처와 검색 메타데이터는 [../catalog.yaml](../catalog.yaml)에 있다.

## Classification

| 스킬 | 제작자/저장소 | 종류 | 주된 역할 | frequency |
|---|---|---|---|---|
| `ponytail` | DietrichGebert | 외부 Skill | 과설계 억제, 최소 코드(YAGNI·표준/네이티브 우선) | occasional |
| `caveman` | JuliusBrussee | 외부 Skill | 출력 토큰 절약용 terse 응답(코드·에러는 원문 유지) | occasional |
| `taste-skill` | Leonxlnx | 외부 Skill | 프론트엔드 디자인 취향(과감함·모션·밀도) 조절 | occasional |
| `mattpocock/skills` | Matt Pocock | 스킬 모음 | 계획 인터뷰(grill), TDD, triage, code-review 등 | rare |
| `ECC` | affaan-m | 프레임워크 | 60+ 에이전트·200+ 스킬·보안 스캐너 하네스 | rare |
| `last30days` | mvanhorn | 외부 Skill | 지난 30일 커뮤니티·웹 조사 후 근거 있는 요약 | occasional |
| `superpowers` | obra(Jesse Vincent) | 프레임워크 | brainstorming→계획→TDD→서브에이전트 방법론 | rare |

`taste-skill`(3번)은 이미 `fieldby-claude-design-top-5` 컬렉션에 `design-taste-frontend`로
등록되어 있어 catalog.yaml에 중복 추가하지 않는다. 이 표에서는 세트 구성상 함께 표기만 한다.

## Frequency 기준

- `core` 는 실제 연구 작업에서 반복 검증된 스킬에만 부여한다. 이 세트는 아직 미검증이므로
  `core` 로 시작하는 항목이 없다.
- `occasional` 은 지금 워크플로에 바로 얹어 볼 만한 것, `rare` 는 본격 소프트웨어 개발이나
  팀 규모 작업에 가까워 연구용으로는 과한 것을 뜻한다.
- 실제로 자주 쓰게 되면 catalog.yaml의 해당 `frequency` 를 `core` 로 올린다.

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
- 이 세트는 아직 이 저장소 환경에서 설치·실행 검증하지 않았다(`tested_locally: false`).
- `ECC`는 규모가 크고 공식 채널(github.com/affaan-m/ECC, npm의 ecc-universal·ecc-agentshield)
  외 미러에 악성코드 위험이 보고되므로 설치 시 출처를 반드시 확인한다.
- 실제 설치 시 원본 저장소, 패키지 소유자, 최신 명령어와 라이선스를 다시 확인한다.
