---
title: "클로드 디자인 스킬 TOP 5 설치 가이드"
resource_type: "external-guide"
status: "reference"
source_url: "https://fieldby.notion.site/TOP-5-392d730b3953818184e8c0700d2d7548"
collected_at: "2026-07-11"
verbatim_copy: false
license_checked: false
---

# Summary

Claude Code에 디자인 방향 설정, 취향 조절, 브라우저 검수, 모션 교정과 Figma 연동을
추가하는 외부 Skill·MCP 다섯 가지를 소개하는 설치 가이드다. 프롬프트 모음이라기보다
프론트엔드 제작 품질을 높이는 도구 체인에 대한 참고 자료다.

## Classification

| 항목 | 종류 | 주된 역할 |
|---|---|---|
| `frontend-design` | 외부 Skill | 구현 전 시각적 방향과 기본 디자인 원칙 설정 |
| `design-taste-frontend` | 외부 Skill | 과감함, 모션과 밀도 조절 |
| `playwright-mcp` | MCP 서버 | 실제 브라우저에서 결과를 확인하고 수정 |
| `animate` | 외부 Skill | UI 모션의 속도와 타이밍 교정 |
| `figma-developer-mcp` | MCP 서버 | Figma 시안 정보를 코드 구현에 전달 |

개별 출처와 검색 메타데이터는 [../catalog.yaml](../catalog.yaml)에 기록한다.

## Reusable workflow

이 자료에서 재사용할 핵심은 특정 호출 문구보다 다음 제작 순서다.

```text
시각적 방향 설정
→ 구현
→ 필요한 모션 조정
→ 실제 브라우저에서 렌더링·상호작용 확인
→ 발견한 문제 수정
→ Figma 시안이 있으면 수치와 스타일 대조
```

즉, 좋은 결과는 한 번의 긴 프롬프트만으로 만들어지는 것이 아니라 디자인 기준,
외부 도구와 반복 검수 과정이 결합되어 만들어진다.

## Use when

- 프론트엔드나 인터랙티브 웹 결과물의 시각적 품질을 높일 도구를 찾을 때
- Skill과 MCP의 역할 차이를 설명하거나 설치 후보를 비교할 때
- 제작 후 브라우저 기반 검수 루프를 설계할 때

## Avoid when

- 계산화학 구조 생성처럼 원자 좌표, 물리 모델과 도메인 정확성이 핵심인 작업
- 외부 저장소와 패키지의 최신 상태를 확인하지 않고 곧바로 설치할 때
- Figma 토큰 등 비밀값을 저장소나 공유 명령어에 직접 기록해야 하는 방식

## Verification notes

- 이 파일은 공개 Notion 페이지를 구조적으로 요약한 것이며 원문 전체를 복제하지 않았다.
- 페이지에 소개된 리소스는 아직 이 저장소 환경에서 설치·실행 검증하지 않았다.
- 실제 설치 시 원본 저장소, 패키지 소유자, 최신 명령어와 라이선스를 다시 확인한다.
