# Research Agent Workflows

Claude Code와 Codex에서 함께 사용하는 개인 연구 Skill, prompt library 및 외부 resource library다.
반복되는 긴 프롬프트를 매번 다시 쓰는 대신, 작업 절차와 품질 기준을 Skill에 저장하고
사용자는 이번 작업에서 달라지는 입력만 말하는 것을 목표로 한다.

## 가장 짧은 사용법

새 대화에서도 저장소를 확실히 찾게 하려면 다음 한 문장으로 시작한다.

> 내 GitHub의 `ShinKiHun/claude-skills`에서 이 작업에 필요한 Skill을 찾아 설치하고 바로 적용해.

특정 Skill을 알고 있다면 더 짧게 말해도 된다.

> `meeting-report` Skill 받아서 자료 제작해.

> `expand-task-brief`를 적용해서 이 논문 리뷰 발표자료를 만들어줘.

프롬프트 이름을 몰라도 목적만 말하면 된다.

> 내 GitHub 프롬프트 자료실에서 논문 리뷰 PPT 요청에 참고할 만한 사례를 찾아서, 좋은 구조만 반영해 새 프롬프트를 작성해줘.

> 내가 3D 연구 시각화를 부탁하려고 해. 저장된 프롬프트 중 참고할 만한 것을 골라 적용해줘.

외부 Skill이나 도구를 찾을 때는 다음처럼 요청한다.

> 내 GitHub의 외부 리소스 목록에서 디자인 작업에 도움이 될 Skill이나 MCP를 찾아서, 현재 환경에 맞는 것만 추천해줘.

에이전트는 사용자가 긴 프롬프트를 다시 작성하도록 요구하지 말고 다음을 알아서 수행해야 한다.

1. 이 저장소의 `AGENTS.md`와 `catalog.yaml`을 읽는다.
2. 현재 요청에 필요한 최소 Skill만 고른다.
3. 현재 실행 환경이 Claude Code인지 Codex인지, 운영체제가 무엇인지 확인한다.
4. 설치 스크립트로 Skill을 사용자 범위에 설치한다.
5. 설치 경로와 `SKILL.md` 접근 가능 여부를 검증한다.
6. 필요한 경우 새 세션에서 Skill을 다시 발견하도록 안내한다.
7. 원래 사용자가 요청한 작업을 이어서 수행한다.

과학적으로 결과가 달라지는 입력만 질문하고, 디자인이나 파일 구성처럼 되돌릴 수 있는
선택은 저장된 기준과 합리적인 기본값으로 진행한다.

## Skill 목록

| Skill | 상태 | 자동으로 사용해야 하는 상황 | 대표 요청 |
|---|---|---|---|
| [expand-task-brief](skills/expand-task-brief/) | active | 짧거나 모호한 요청을 실행 가능한 제작 명세로 확장해야 할 때 | “이 논문으로 수준급 발표자료 만들어줘” |
| [meeting-report](skills/meeting-report/) | active | 연구 진행 상황을 일일 또는 주간 미팅 자료로 만들 때 | “자료 제작”, “총자료 제작” |
| [caveman](skills/caveman/) | active | 응답이 길어져 토큰이 아까울 때. 전역 규칙을 설치하면 상시 적용된다 | “간결하게”, “짧게”, “토큰 줄여”, “결론만” |
| [grilling](skills/grilling/) | active | 새 계산 셀·장시간 계산·해석을 바꾸는 방법론을 정하기 전 | “갈궈봐”, “계획 물어봐”, “하나씩 물어봐”, “합의부터 하자” |

기계가 읽을 수 있는 전체 목록과 경로는 [catalog.yaml](catalog.yaml)에 있다.

`caveman`과 `grilling`은 외부 MIT Skill을 이 저장소 기준으로 고쳐 쓰는 fork다. 출처와
원문 라이선스는 각 Skill 폴더의 `LICENSE`와 `SKILL.md` 안에 남겨 두고, upstream 자체에 대한
평가 메모는 [resource-library/external/coding-agent-skills-yt.md](resource-library/external/coding-agent-skills-yt.md)에 둔다.

## 전역 규칙 (선택 설치)

[global/user-CLAUDE.md](global/user-CLAUDE.md)를 `~/.claude/CLAUDE.md`로 연결하면 **모든 폴더의
모든 세션**이 자동으로 읽는다. 매번 `/caveman`을 치지 않아도 된다.

```bash
./install.sh --target claude --skill '*' --global-rules
```

```powershell
.\install.ps1 -Target Claude -Skill '*' -GlobalRules
```

`--global-rules`는 **명시할 때만** 동작한다. Skill 설치의 부수효과로 남의 전역 설정을 덮지
않기 위해서다. 기존 `~/.claude/CLAUDE.md`가 실제 파일이면 `.bak.<timestamp>`으로 백업한 뒤
링크한다. 다른 경로를 쓰려면 `CLAUDE_GLOBAL_RULES` 환경 변수로 덮어쓴다.

담긴 규칙은 세 가지다.

- 답변은 항상 caveman 스타일 (`/caveman`을 치지 않아도 켜져 있음)
- 새 셀·장시간 계산·방법론 결정 전에는 grilling으로 합의부터
- 코드 3규칙: 결과는 print로 출력 / 완료 후 처음부터 재검토 / 타 폴더 코드는 참조하되 오류는 명시하고 고쳐 씀

## 설치

### 에이전트에게 맡기기

가장 권장하는 방식이다. 저장소 주소와 원하는 작업만 말하면 된다.

> `https://github.com/ShinKiHun/claude-skills`를 확인하고, 현재 작업에 필요한 Skill만 설치해서 적용해. 운영체제와 Claude/Codex 설치 경로는 네가 확인하고 설치 후 검증까지 해.

에이전트는 기존 일반 디렉토리를 임의로 삭제하거나 덮어쓰면 안 된다. 충돌이 있으면
현재 설치를 먼저 확인하고, 필요한 경우 백업 또는 사용자 확인 후 진행한다.

### 직접 설치

저장소를 한 번 복제한다.

```bash
git clone https://github.com/ShinKiHun/claude-skills.git ~/research-agent-workflows
```

Windows PowerShell:

```powershell
# 필요한 Skill 하나를 Codex에 설치
.\install.ps1 -Target Codex -Skill expand-task-brief

# 필요한 Skill 하나를 Claude Code에 설치
.\install.ps1 -Target Claude -Skill meeting-report

# 모든 Skill을 두 에이전트에 설치
.\install.ps1 -Target All -Skill '*'
```

Linux, macOS, 연구 서버:

```bash
# 필요한 Skill 하나를 Codex에 설치
./install.sh --target codex --skill expand-task-brief

# 필요한 Skill 하나를 Claude Code에 설치
./install.sh --target claude --skill meeting-report

# 모든 Skill을 두 에이전트에 설치
./install.sh --target all --skill '*'
```

기본 설치 위치:

| 대상 | 기본 경로 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `$CODEX_HOME/skills/` when configured, otherwise `~/.agents/skills/` |

환경에서 별도 경로를 사용한다면 `CLAUDE_SKILLS_DIR` 또는
`CODEX_SKILLS_DIR` 환경 변수로 덮어쓸 수 있다. 설치기는 기본적으로 원본 Skill
폴더를 연결하므로 `git pull` 뒤에 내용이 바로 갱신된다. 연결을 만들 수 없는
환경에서는 Windows 설치기가 복사 방식으로 대체할 수 있다.

## 저장소 구조

```text
claude-skills/
├─ AGENTS.md                 # 모든 에이전트가 따르는 설치·관리 계약
├─ CLAUDE.md                 # Claude Code가 AGENTS.md를 읽도록 연결
├─ catalog.yaml              # Skill, 전역 규칙, 외부 프로젝트의 기계 판독용 색인
├─ skills/
│  ├─ caveman/              # fork: JuliusBrussee/caveman (MIT)
│  ├─ expand-task-brief/
│  ├─ grilling/             # fork: mattpocock/skills (MIT)
│  ├─ handoff/
│  └─ meeting-report/
├─ global/
│  └─ user-CLAUDE.md        # ~/.claude/CLAUDE.md 로 연결 (--global-rules 로 선택 설치)
├─ prompt-library/
│  ├─ catalog.yaml           # 프롬프트 컬렉션과 파일의 기계 판독용 색인
│  ├─ inbox/                 # 아직 검증하지 않은 수집 자료
│  ├─ catalysis/             # 계산촉매 및 계산과학 분야 자료
│  ├─ cross-domain/          # 다른 분야지만 구조가 유용한 자료
│  ├─ external/              # 출처가 있는 외부 프롬프트
│  └─ archive/               # 중복·저품질·구버전
├─ resource-library/
│  ├─ catalog.yaml           # 외부 Skill, MCP, 도구와 가이드의 색인
│  ├─ design/                # 색상, 시각 시스템 등 재사용 가능한 디자인 레퍼런스
│  └─ external/              # 원문을 복제하지 않은 출처·용도·검증 메모
├─ evals/                    # 실제 요청으로 Skill 동작을 확인하는 사례
├─ install.ps1
└─ install.sh
```

## Prompt, Resource, Skill의 차이

- `prompt-library/`는 새 프롬프트를 작성할 때 구조와 품질 기준을 참고하는 사례집이다.
- `resource-library/`는 외부 Skill·MCP·도구와 재사용 가능한 디자인 레퍼런스를 관리하는 목록이다.
- `skills/`는 우리가 직접 관리하며 에이전트가 자동으로 발견하고 실행할 수 있는 워크플로다.
- 프롬프트가 한두 번 좋아 보였다는 이유만으로 바로 Skill로 만들지 않는다.
- 실제 작업에서 반복적으로 효과가 확인되면 공통 원칙을 추출해 Skill로 승격한다.

세 종류는 같은 저장소에 두되 폴더를 섞지 않는다. 프롬프트와 외부 리소스가 실제
Skill의 재료가 되는 경우가 많아서, 저장소를 분리하는 것보다 한 카탈로그에서 서로
연결하는 편이 검색과 유지보수에 유리하다.

에이전트는 프롬프트 참고 요청을 받으면 전체 원문을 합치지 않는다. 먼저
`prompt-library/catalog.yaml`에서 목적과 가까운 자료를 최대 세 개 고르고, 필요한
구조와 판단 기준만 현재 요청에 맞게 재구성한다. 사용한 자료의 ID도 짧게 알려준다.

운영 흐름은 다음과 같다.

```text
inbox에 수집
→ 출처와 용도 기록
→ 실제 작업에서 시험
→ 성공·실패 원인 기록
→ 재사용 원칙 추출
→ Skill 또는 reference로 승격
```

각 자료에는 분야, 작업 유형, 상태, 사용 빈도, 출처, 적합한 상황과 피해야 할 상황을
기록한다. 템플릿은 [prompt-library/_template.md](prompt-library/_template.md)를 사용한다.

## 새 Skill 추가 원칙

1. 폴더명은 소문자와 하이픈만 사용한다.
2. `skills/<skill-name>/SKILL.md`를 필수로 둔다.
3. 자동 선택에 필요한 조건을 YAML `description`에 구체적으로 쓴다.
4. 핵심 절차만 `SKILL.md`에 두고 긴 지식은 `references/`로 분리한다.
5. 반복 코드는 `scripts/`, 출력에 재사용할 템플릿은 `assets/`에 둔다.
6. `catalog.yaml`과 README의 Skill 표를 함께 갱신한다.
7. `quick_validate.py`와 `evals/`의 실제 요청으로 검증한다.

하나의 거대한 만능 Skill보다, 트리거가 분명한 작은 Skill 여러 개를 선호한다.

## 관련 독립 프로젝트

- [computational-paper-review-deck](https://github.com/ShinKiHun/computational-paper-review-deck):
  계산과학 논문 한 편을 HTML journal-club deck으로 만드는 완성형 템플릿 프로젝트
- [claude-codex-battery-windows](https://github.com/ShinKiHun/claude-codex-battery-windows):
  Claude/Codex 사용량을 표시하는 Windows 애플리케이션

이 저장소는 Skill과 prompt library만 관리한다. 연구 코드, 완성형 앱, 개별 발표자료
프로젝트는 여기에 합치지 않는다.
