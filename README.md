# claude-skills

개인용 Claude Code 스킬 모음 (ShinKiHun). 어떤 프로젝트 폴더에서든 동작하도록
사용자 레벨(`~/.claude/skills/`)에 설치해서 쓴다.

## 설치 (서버마다 1회)

```bash
git clone git@github.com:ShinKiHun/claude-skills.git ~/claude-skills
bash ~/claude-skills/install.sh        # 각 스킬을 ~/.claude/skills/ 에 symlink
```

업데이트: `cd ~/claude-skills && git pull` (symlink라 자동 반영).

## 스킬 목록

| 스킬 | 트리거 | 하는 일 |
|---|---|---|
| [meeting-report](meeting-report/) | **"자료 제작"** / **"총자료 제작"** | 당일/주간 미팅 보고자료를 self-contained HTML로 `reports/<주간폴더>/`에 생성 |

## meeting-report 사용법

- 매일 (또는 보고할 게 있는 날): Claude Code 세션에서 `자료 제작`
  → `reports/20260701_20260707/20260703.html`
- 미팅 전날: `총자료 제작` → 같은 폴더에 `total.html` (그 주 일일 리포트 종합)
- 주간 폴더는 자동 관리: total 생성 후 첫 일일 리포트가 새 주(7일 창)를 연다
