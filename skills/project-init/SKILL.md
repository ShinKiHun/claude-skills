---
name: project-init
description: One-shot scaffolding for a new project/research folder. Run once in a directory to create a lean CLAUDE.md, STATUS.md, LOG.md (handoff-compatible), and the ref/ code/ analysis/ reports/ skeleton so the folder is ready for continuous work. Field-agnostic. Relies on the global ~/.claude/CLAUDE.md for the always-on universal rules (caveman, grilling, facts-only, assumption-vs-confirmed). Use when starting a new project or setting up a folder. Korean triggers: "프로젝트 세팅", "폴더 세팅", "project init", "새 프로젝트 시작", "여기 세팅해줘", "리서치 폴더 초기화".
---

# project-init

새 프로젝트/연구 폴더를 **한 번에 세팅**한다. 실행한 **현재 디렉토리(cwd)를 프로젝트 루트로** 잡고 로컬 파일·폴더를 만든다. 분야 무관.

## 역할 분담 (이 스킬의 위치)
- **project-init** = 세팅(1회). 여기.
- **전역 `~/.claude/CLAUDE.md`** = 범용 규칙(항상): caveman(간결)·grilling·팩트만·가정vs확정. **폴더마다 안 만든다.** 한 번 설치로 모든 폴더 자동 적용.
- **handoff** = 기록·연속성(STATUS/LOG 유지). project-init이 만든 파일을 이어서 씀.
- **meeting-report / paper-report** = 보고(HTML).

## 만드는 것 (표준)
현재 폴더에:
```
<cwd>/
 ├ CLAUDE.md    # 얇은 프로젝트 규칙(개요·폴더맵·연속성·전역규칙 적용 명시)
 ├ STATUS.md    # 현재 상태 1p (handoff 포맷)
 ├ LOG.md       # 누적 기록 (handoff 포맷)
 ├ ref/         # 참고문헌/자료 (원문 PDF 등)
 ├ code/        # 코드/입력
 ├ analysis/    # 분석 스크립트·플롯·가공데이터
 └ reports/     # 보고 산출물 (HTML 등)
```
각 폴더에 `.gitkeep` 또는 짧은 `README.md` 한 줄.

## 워크플로우
1. **cwd 확인.** 실행된 디렉토리가 프로젝트 루트. 이미 CLAUDE.md/STATUS.md/LOG.md가 있으면 **덮지 않는다**(idempotent) — 없는 것만 만든다. 있으면 "이미 있음"이라고 알림.
2. **프로젝트 정보 파악.** 폴더명·기존 파일을 보고 프로젝트 성격을 추정. 목표가 불명확하면 유저에게 **한 줄**만 물음("이 프로젝트 한 줄 목표?"). 나머지는 placeholder로 두고 진행.
3. **템플릿으로 생성.** `references/templates.md`의 CLAUDE.md / STATUS.md / LOG.md 템플릿을 이 폴더에 맞게 채워 씀. 폴더 골격 mkdir.
   - CLAUDE.md는 **얇게**(전역규칙이 이미 항상 적용되므로 중복 나열 금지, "전역규칙 적용됨"만 명시 + 프로젝트 고유 내용).
4. **결과 print/요약.** 만든 파일·폴더 목록 출력. "handoff로 이어서 기록, meeting-report/paper-report로 보고" 안내 한 줄.

## 원칙
- **idempotent**: 기존 파일·폴더 절대 덮어쓰지 않음. 없는 것만 채움.
- **얇게**: CLAUDE.md에 전역규칙 복붙 금지(항상 로드되는 전역과 중복 = 컨텍스트 낭비). 프로젝트 고유만.
- 폴더 골격은 표준(ref/code/analysis/reports). 프로젝트가 코드 없으면 code/ 생략 등 상황에 맞게 조정 가능(유저가 원하면).
- 전역규칙(`~/.claude/CLAUDE.md`)이 설치돼 있어야 범용 규칙이 적용됨. 없으면 유저에게 "전역규칙 설치할까요?"(claude-skills `--global-rules`) 안내.
