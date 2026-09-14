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
| [paper-report](skills/paper-report/) | active | 유저가 준 논문 PDF(+우리 데이터)를 figure-rich 한국어 미팅 보고 HTML로 만들 때 | “논문 미팅자료”, “논문 보고자료”, “사전조사 자료 제작” |
| [caveman](skills/caveman/) | active | 응답이 길어져 토큰이 아까울 때. 전역 규칙을 설치하면 상시 적용된다 | “간결하게”, “짧게”, “토큰 줄여”, “결론만” |
| [grilling](skills/grilling/) | active | 새 계산 셀·장시간 계산·해석을 바꾸는 방법론을 정하기 전 | “갈궈봐”, “계획 물어봐”, “하나씩 물어봐”, “합의부터 하자” |
| [handoff](skills/handoff/) | active | 세션을 이어받거나 마무리하며 컨텍스트를 넘길 때 | “이어서”, “어디까지 했지”, “핸드오프”, “오늘 정리” |
| [project-init](skills/project-init/) | active | 새 프로젝트/연구 폴더를 한 번에 세팅할 때 (CLAUDE.md·STATUS/LOG·폴더골격) | “프로젝트 세팅”, “여기 세팅해줘”, “리서치 폴더 초기화” |
| [apple-design](skills/apple-design/) | active | 제스처 UI·스프링/관성 모션·시트/드래그, 반투명 재질·타이포를 만들거나 검토할 때 | “애플처럼 만들어줘”, “스프링 애니메이션” |
| [emil-design-eng](skills/emil-design-eng/) | active | UI 폴리시·컴포넌트 설계·애니메이션 판단 등 디테일을 정할 때 | “디테일 살려줘”, “컴포넌트 다듬어줘” |
| [review-animations](skills/review-animations/) | active | 애니메이션·모션 코드를 엄격한 기준으로 리뷰할 때 (명시 호출 전용) | “애니메이션 리뷰해줘”, `/review-animations` |
| [improve-animations](skills/improve-animations/) | active | 코드베이스 전체 모션을 감사해 우선순위 개선 계획이 필요할 때 (소스는 수정 안 함) | “애니메이션 개선해줘”, “앱 느낌 좋게” |
| [animation-vocabulary](skills/animation-vocabulary/) | active | 모션 효과의 정확한 명칭을 찾아 프롬프트에 쓰고 싶을 때 | “이거 뭐라고 불러?”, “이 효과 이름이 뭐야” |
| [pubfig](skills/pubfig/) | active | 결과 그림을 정해진 룩으로 그릴 때 — plain(Catbench parity: 기본 rc+Arial 14/12/10, 300 dpi) / lab(drmstyle: 네모칸·볼드·격자 없음) | “논문 스타일 그림”, “박사님 스타일로”, “parity plot 스타일” |
| [humanizer](skills/humanizer/) | active | 글을 사람이 쓴 것처럼 다듬어 AI 티를 뺄 때 | “휴먼틱하게”, “AI 티 빼줘”, “자연스럽게 다듬어” |

기계가 읽을 수 있는 전체 목록과 경로는 [catalog.yaml](catalog.yaml)에 있다.

`caveman`과 `grilling`은 외부 MIT Skill을 이 저장소 기준으로 고쳐 쓰는 fork다.
`apple-design`·`emil-design-eng`·`review-animations`·`improve-animations`·`animation-vocabulary`는
[emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, © 2026 Emil Kowalski)를
**수정 없이 그대로 벤더링**한 것이다. 출처와
원문 라이선스는 각 Skill 폴더의 `LICENSE`와 `SKILL.md` 안에 남겨 두고, upstream 자체에 대한
평가 메모는 [resource-library/external/coding-agent-skills-yt.md](resource-library/external/coding-agent-skills-yt.md)에 둔다.

`humanizer`는 [blader/humanizer](https://github.com/blader/humanizer) (MIT, © 2025 Siqi Chen)를
**수정 없이 그대로 벤더링**한 것이다. 위키백과의 "Signs of AI writing" 패턴으로 글에서
AI가 쓴 티를 제거해 사람이 쓴 것처럼 다듬는다.

## 전역 규칙 (선택 설치)

[global/user-CLAUDE.md](global/user-CLAUDE.md)를 `~/.claude/CLAUDE.md`로 연결하면 **모든 폴더의
모든 세션**이 자동으로 읽는다. 매번 `/caveman`을 치지 않아도 된다. Skill이 아니라 규칙 파일
하나이므로 `--list`에는 나오지 않는다.

새 기기에서는 `setup.sh` 한 줄이면 전역 규칙과 Skill 전부가 함께 설치된다.

```bash
git clone https://github.com/ShinKiHun/claude-skills.git ~/claude-skills
~/claude-skills/setup.sh
```

```powershell
git clone https://github.com/ShinKiHun/claude-skills.git $HOME\claude-skills
& $HOME\claude-skills\setup.ps1
```

`setup.sh`는 `install.sh --global-rules`를 부르는 얇은 래퍼다(`install.sh`는 기본값으로 Skill
전부를 설치한다). 추가 인자는 그대로 전달되므로 `./setup.sh --target claude`처럼 좁힐 수 있다.
갱신은 `cd ~/claude-skills && git pull && ./setup.sh`.

설치기를 직접 부르려면 다음과 같다.

```bash
./install.sh --target claude --skill '*' --global-rules
```

```powershell
.\install.ps1 -Target Claude -Skill '*' -GlobalRules
```

`--global-rules`는 **명시할 때만** 동작한다. Skill 설치의 부수효과로 남의 전역 설정을 덮지
않기 위해서다. 기존 `~/.claude/CLAUDE.md`가 실제 파일이면 `.bak.<timestamp>`으로 백업한 뒤
링크한다. 다른 경로를 쓰려면 `CLAUDE_GLOBAL_RULES` 환경 변수로 덮어쓴다.

Windows에서 symlink와 junction은 **둘 다** 관리자 권한이나 개발자 모드를 요구한다. 권한이
없으면 설치기가 경고를 내고 **전역 규칙도 Skill 폴더도 복사로 대체**한다. 복사본은 `git pull`을
따라오지 않으므로, 규칙이나 Skill을 고쳤으면 **`.\setup.ps1`을 다시 실행**해야 로컬에 반영된다.
같은 내용이면 `.bak`을 다시 만들지 않는다.

현재 기기가 링크인지 복사인지는 이렇게 확인한다. `ReparsePoint=False`면 복사본이다.

```powershell
(Get-Item "$HOME\.claude\CLAUDE.md" -Force).Attributes
Get-ChildItem "$HOME\.claude\skills" -Directory | ForEach-Object { "$($_.Name): $($_.Attributes)" }
```

개발자 모드(설정 → 개인 정보 및 보안 → 개발자용)를 켠 뒤 `.\setup.ps1`을 한 번 더 실행하면
링크로 바뀌어 이후로는 `git pull`만으로 갱신된다. Linux/macOS는 기본이 링크라 해당 없다.

담긴 규칙은 여덟 가지다.

1. 답변은 항상 caveman 스타일 (`/caveman`을 치지 않아도 켜져 있음)
2. 새 셀·장시간 계산·방법론 결정 전에는 grilling으로 합의부터
3. 코드 3규칙: 결과는 print로 출력 / 완료 후 처음부터 재검토 / 타 폴더 코드는 참조하되 오류는 명시하고 고쳐 씀
4. 팩트만·날조 금지: 없는 지식 지어내지 말고, 문헌·데이터 없으면 없다고. DOI·수치는 검증된 것만
5. 가정 vs 확정 표기: `추정`/`문헌확인`/`계산확인`으로 근거 수준 명시
6. 하지 말 것: 코드 붙여넣기 금지(작업 중인 `.py` 끝에 셀로 추가), over-engineering 금지
7. **적대적 검토 — 무조건 OK 금지**: 프로젝트가 성공하면 불이익을 받는 입장으로 가정하고 사용자 가설을 먼저 의심·질문한다. 목표는 반대가 아니라 상호 납득 가설로의 수렴
8. **3중 검증 — 보고 전 필수**: 서로 다른 축 3개(①실행 검증 ②원문 대조 ③반증 시도)로 확인한 뒤 보고한다. 같은 검증 3회는 오류를 3회 재생산할 뿐이므로 금지

7·8번은 항상 켜져 있어야 의미가 있으므로 Skill로 빼지 않는다. 호출해야 켜지는 "항상 의심하라"는
필요한 시점에 이미 늦는다.

## 연속성 훅 (setup 이 자동 설치)

**문제**: `handoff` Skill 은 "이어서"라고 **쳐야만** 어제 상태를 읽는다. 그냥 일 얘기부터
시작하면 Claude 는 `STATUS.md` 존재조차 모르고, 사용자가 매번 어제를 다시 설명하게 된다.
규칙으로는 못 고친다 — Claude 가 아니라 harness 가 실행하는 **hook** 이어야 한다.

| 훅 | 스크립트 | 하는 일 |
|---|---|---|
| `SessionStart` | [hooks/inject-status.py](hooks/inject-status.py) | 새 창마다 `STATUS.md` · `dead-ends.md` · `decisions/` 인덱스 · `LOG.md` 최신 엔트리를 **컨텍스트에 자동 주입** |
| `Stop` | [hooks/status-stale.py](hooks/status-stale.py) | `STATUS.md` 가 실제 작업 파일보다 6시간 이상 낡으면 한 줄 경고 |

두 번째가 첫 번째를 지킨다. **낡은 STATUS 가 자동 주입되면 아무것도 없는 것보다 나쁘다** —
Claude 가 틀린 어제를 자신 있게 말하게 된다. 그래서 낡음을 감지한다.

`setup.sh` / `setup.ps1` 이 [hooks/install_hooks.py](hooks/install_hooks.py) 로 설치한다.
설치기는 `~/.claude/settings.json` 을 **병합**한다 — 다른 도구(orca 등)의 훅이 같은 파일에
있으므로 통째로 덮으면 전부 죽는다. 우리 항목만 식별해 교체하고, 백업을 남기고, 쓰기 전에
JSON 을 되읽어 검증한다. 깨진 settings.json 은 아예 건드리지 않고 종료한다.

```bash
python hooks/install_hooks.py <repo> --check       # 훅이 살아있는지 확인 (0=정상)
python hooks/install_hooks.py <repo> --dry-run     # 쓰지 않고 결과만
python hooks/install_hooks.py <repo> --uninstall   # 우리 훅만 제거
```

`--check` 가 필요한 이유: 훅 커맨드에는 `[ -f "$H" ]` 가드가 있어서 저장소를 옮기거나
지우면 **에러 없이 조용히** 아무것도 하지 않는다. 조용한 고장은 눈에 띄지 않는다.
"어제 상태가 안 불러와지는 것 같다" 싶으면 이걸 먼저 돌려라.

연속성 파일이 없는 폴더에서는 두 훅 모두 **조용히 통과**하므로 전역 설치해도 무해하다.
`python` 이 없으면 훅만 건너뛰고 Skill·전역 규칙 설치는 정상 진행된다. Windows 에서
`python3` 는 Microsoft Store 의 App Execution Alias 로 잡힐 수 있어(실행하면 `Python` 만
출력하고 실패) 설치기가 인터프리터를 **실제로 실행해 보고** 고른다.
훅은 새 세션부터 적용된다 — 기존 창에는 반영되지 않는다.

⚠️ `settings.json` 에는 **이 저장소 경로가 절대경로로** 박힌다. 저장소를 옮기거나 지우면
훅은 조용히 아무것도 하지 않는다(`[ -f "$H" ]` 가드). 옮겼으면 새 경로에서 `./setup.sh`
를 다시 실행하면 된다. 반대로 이 방식 덕분에 Linux 에서는 `git pull` 만으로 훅이 갱신된다.

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
│  ├─ meeting-report/
│  ├─ paper-report/
│  └─ project-init/
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
├─ hooks/
│  ├─ inject-status.py        # SessionStart: 연속성 파일을 세션에 자동 주입
│  ├─ status-stale.py         # Stop: STATUS.md 낡음 감지
│  └─ install_hooks.py        # settings.json 에 병합 설치 (--uninstall / --dry-run)
├─ evals/                    # 실제 요청으로 Skill 동작을 확인하는 사례
├─ install.ps1
├─ install.sh
├─ setup.ps1                 # install.ps1 -GlobalRules + 훅 (새 기기 진입점)
└─ setup.sh                  # install.sh --global-rules + 훅 (새 기기 진입점)
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
