# Windows 복사 설치 시 손본 것 (2026-08-24)

`install.sh --claude-only --copy` 로 설치하면 **스킬 폴더만** 오고
`scripts/` · `.claude-plugin/` 이 따라오지 않는다.  그대로 두면 두 가지가 조용히 깨진다.

## 1. SKILL_ROOT 유도 실패

`SKILL.md` 는 `.claude-plugin/` 을 만날 때까지 상위로 거슬러 올라가 `SKILL_ROOT` 를 잡는다.
복사 설치본에는 그게 없어서 shim(`prepare_monolith_input.py`)을 못 찾는다.

**고침** — 저장소에서 두 폴더를 스킬 안으로 복사

```
cp -R <repo>/scripts        ~/.claude/skills/humanize-korean/scripts
cp -R <repo>/.claude-plugin ~/.claude/skills/humanize-korean/.claude-plugin
```

## 2. metrics 모듈 import 실패 (`degraded=True`)

`scripts/prepare_monolith_input.py` 는 **저장소 레이아웃**을 가정한다.

```python
HERE         = <...>/scripts
PROJECT_ROOT = HERE.parent
METRICS_DIR  = PROJECT_ROOT / "skills" / "humanize-korean" / "references"
```

즉 `{root}/scripts` 와 `{root}/skills/humanize-korean/references` 가 나란히 있어야 한다.
복사 설치본은 `references/` 가 스킬 폴더 **바로 밑**에 있어서 경로가 어긋나고,
`00_metrics.error: metrics module import failed` 가 나며 `route_hint` 없이 degrade 된다.
(degrade 해도 윤문 자체는 돌지만 정량 점수·경로 판정·철칙 #4 게이트가 사라진다.)

**고침** — 스크립트를 고치지 않고 기대하는 계층을 만들어 준다

```
mkdir -p ~/.claude/skills/humanize-korean/skills/humanize-korean
cp -R    ~/.claude/skills/humanize-korean/references \
         ~/.claude/skills/humanize-korean/skills/humanize-korean/references
```

원본 스크립트를 수정하지 않으므로 `update.sh` 로 갱신해도 충돌하지 않는다.
다만 **갱신 후 이 복사를 다시 해야 한다** (references 가 바뀌었을 수 있으므로).

## 3. python3

`python3` 는 Windows Store 껍데기다.  shim 을 직접 부를 때는 실물 경로를 쓴다.

```
C:\Users\<사용자>\AppData\Local\Programs\Python\Python312\python.exe
```

스킬 안에서 Bash 로 `python3` 를 부르면 Git Bash 가 껍데기를 잡을 수 있으니,
`degraded=True` 가 뜨면 이걸 먼저 의심할 것.

## 확인 방법

```
SKILL_ROOT="$(d="$(cd -P ~/.claude/skills/humanize-korean && pwd)"; \
  while [ "$d" != / ] && [ ! -d "$d/.claude-plugin" ]; do d="$(dirname "$d")"; done; echo "$d")"
ls "$SKILL_ROOT/scripts/prepare_monolith_input.py"     # 있어야 함
```

그리고 아무 텍스트로 shim 을 한 번 돌려 `degraded=False` 인지 본다.
`degraded=True` 면 위 2번이 안 된 것이다.
