# Agent Contract

이 저장소는 Claude Code와 Codex가 함께 사용하는 Skill 및 prompt library다.
사용자가 짧게 요청하더라도 긴 프롬프트를 다시 쓰게 하지 말고, 저장된 워크플로를
찾아 설치하고 적용하는 데 목적이 있다.

## Skill 설치 또는 적용 요청

사용자가 “내 GitHub에서 필요한 스킬 받아서 적용해”, “이 저장소의 스킬 설치해”처럼
말하면 다음 순서로 처리한다.

1. `catalog.yaml`을 읽고 요청과 가장 가까운 Skill을 찾는다.
2. 후보 Skill의 YAML `name`과 `description`을 확인한다.
3. 현재 작업에 필요한 최소 Skill만 선택한다. 무조건 전부 설치하지 않는다.
4. 현재 에이전트와 운영체제를 감지한다.
5. Windows에서는 `install.ps1`, Unix 계열에서는 `install.sh`를 사용한다.
6. 환경이 제공하는 사용자 Skill 경로가 있으면 그것을 우선하고, 없으면 README의
   기본 경로를 사용한다.
7. 설치 후 대상 경로에서 `SKILL.md`, 필요한 `references/`, `scripts/`,
   `assets/`가 접근 가능한지 확인한다.
8. 자동 발견에 새 세션이 필요하면 그 사실만 짧게 알린다.
9. 설치가 끝나면 원래 요청으로 돌아가 Skill을 실제로 사용한다.

사용자가 이미 저장소와 작업을 지정했다면 설치 방법을 다시 묻지 않는다. 파일 충돌,
권한 부족, 과학적 입력의 부재처럼 결과를 바꾸는 문제가 있을 때만 질문한다.

## 작업 해석

- 짧고 복잡한 제작 요청은 `expand-task-brief`를 사용해 내부 실행 명세로 확장한다.
- 사용자가 저장된 프롬프트를 찾거나 참고하라고 하면 `prompt-library/catalog.yaml`과
  해당 컬렉션의 README를 먼저 읽고, 관련 원문만 선택해서 읽는다.
- 사용자가 “프롬프트만” 요청하지 않았다면 명세를 보여주고 멈추지 말고 실제 작업까지
  수행한다.
- 디자인·파일명·레이아웃처럼 되돌릴 수 있는 선택은 합리적인 기본값으로 진행한다.
- 연구 결론, 수치, 계산 조건, 실제 데이터처럼 과학적으로 중요한 정보는 추측하거나
  조작하지 않는다.
- 기존 전문 Skill이 있으면 범용 Skill보다 전문 Skill을 우선한다.
- 결과물은 해당 형식에 맞는 렌더링 또는 실행 검증을 마친 뒤 전달한다.

## 저장소 관리

- Skill은 `skills/<name>/`에 둔다.
- Skill 폴더 안에는 필수 `SKILL.md`와 필요한 `agents/`, `references/`,
  `scripts/`, `assets/`만 둔다.
- 긴 예시와 분야별 지식은 `SKILL.md`에 쌓지 말고 한 단계 깊이의
  `references/`로 분리한다.
- 외부 프롬프트는 `prompt-library/external/`에 출처, 작성자, 수집일과 함께 둔다.
- 검증 전 자료는 `inbox/`, 반복 검증을 통과한 워크플로만 `skills/`에 둔다.
- Skill 추가·이동·이름 변경 시 `catalog.yaml`, README와 설치기 동작을 함께 확인한다.
- 다른 GitHub 저장소나 연구 프로젝트는 사용자의 명시적 요청 없이 수정하지 않는다.

## 검증

- 변경된 모든 Skill에 `quick_validate.py`를 실행한다.
- Python 스크립트에는 최소한 구문 검사를 실행한다.
- `install.ps1 -List`와 `install.sh --list`가 동일한 Skill 목록을 보여야 한다.
- 대표 요청은 `evals/`의 기대 동작과 비교한다.
