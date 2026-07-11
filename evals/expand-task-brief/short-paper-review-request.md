# Case: short paper review request

## User request

```text
이 논문 PDF로 다음 연구실 미팅에서 발표할 수준급 리뷰 자료 만들어줘.
```

## Expected behavior

- 논문, 청중, 발표 맥락과 사용 가능한 발표 도구를 먼저 확인한다.
- 연구 질문, novelty, method, evidence, limitations, discussion questions로 서사를 만든다.
- figure를 페이지 순서가 아니라 주장에 기여하는 역할로 선택한다.
- 계산 주장, 검증, 한계와 해석을 구분한다.
- 긴 프롬프트를 사용자에게 다시 작성하라고 요구하지 않는다.
- 발표 길이가 결과를 크게 바꾸고 추론할 수 없을 때만 짧게 질문한다.
- 결과물을 생성하고 전체 슬라이드를 렌더링해 잘림과 깨진 이미지를 확인한다.

## Failure conditions

- PDF를 요약한 텍스트만 반환한다.
- 논문에 없는 주장이나 수치를 만든다.
- 내용보다 장식과 웹 UI 패턴을 우선한다.
- 계획이나 프롬프트만 제시하고 실행을 멈춘다.
