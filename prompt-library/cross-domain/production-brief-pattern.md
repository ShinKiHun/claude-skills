---
title: "Prompt as a production brief"
domain: "cross-domain"
workflow: "complex artifact creation"
status: "curated"
frequency: "core"
source_type: "synthesized"
source_url: ""
author: "ShinKiHun"
collected_at: "2026-07-11"
last_tested: "2026-07-11"
tested_with:
  - "Codex"
---

# Summary

고품질 장문 프롬프트를 주문 문장이 아니라 제작 발주서, 평가 기준, 실패 방지
체크리스트의 결합으로 다루는 패턴이다.

## Use when

- 웹사이트, 앱, 게임, 발표자료, 연구 시각화처럼 결과물이 복합적일 때
- “멋있게”, “수준급으로”처럼 평가가 주관적인 요청을 검증 가능한 기준으로 바꿀 때
- 코드를 생성하는 것보다 실행·렌더·검증이 중요한 작업

## Avoid when

- 한 줄 수정이나 단순 변환처럼 결과가 이미 명확한 작업
- 실제 데이터가 필요한데 입력이 없는 상태에서 세부 수치를 채우려는 경우
- 요구사항을 늘리는 것이 목적과 무관한 복잡성만 만드는 경우

## Reusable pattern

1. 최종 결과물을 파일 또는 작동 상태로 정의한다.
2. 사용자와 사용 맥락을 정한다.
3. 입력 자료와 신뢰할 출처를 나눈다.
4. 반드시 포함할 장면, 섹션, 기능 또는 분석을 적는다.
5. 자주 발생하는 편법과 실패를 금지한다.
6. 분석, 설계, 구현, 검증 순서를 지정한다.
7. 완료 여부를 판정할 수 있는 acceptance criteria를 둔다.
8. 과학적·사실적 미지수와 디자인 기본값을 구분한다.

## Compact skeleton

```text
Outcome
- 무엇을 실제로 완성할 것인가

Audience and context
- 누가, 어디에서, 왜 사용하는가

Authoritative inputs
- 파일, 데이터, 링크, 기존 프로젝트

Required behaviors
- 반드시 들어가야 하는 기능, 내용, 장면

Forbidden shortcuts
- 정적 모형으로 대체, 근거 없는 생성, 검증 생략 등

Workflow
- inspect → design → build → render/run → verify → repair

Deliverables
- 필수 파일과 선택 파일

Acceptance criteria
- 열림, 작동, 정확성, 가독성, 출처 추적성
```

## Test notes

길이 자체가 품질을 만들지는 않았다. 도구 선택, 실패 금지, 실제 검증 항목이 포함될
때 결과가 안정적으로 좋아졌다. 도메인 사실이 부족한 경우에는 프롬프트가 길어도
정확성이 생기지 않으므로, 입력 파일을 요청하거나 불확실성을 명시해야 한다.
