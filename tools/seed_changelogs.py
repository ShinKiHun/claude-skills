# -*- coding: utf-8 -*-
"""
모든 스킬에 CHANGELOG.md 를 넣는다. 과거 항목은 git log 에서 복원한다.

왜
  여러 Claude 세션이 각자 폴더에서 이 스킬들을 자유롭게 고친다.
  파일만 읽는 쪽에서는 "마지막에 누가 어디를 왜 고쳤는지" 가 안 보여서
  이전 결정을 모르고 되돌리거나 중복 수정이 난다. git log 는 파일을 읽는
  눈에 안 들어온다 — 그래서 스킬 폴더 안에 둔다.

규약 (각 CHANGELOG.md 머리말에 그대로 박는다)
  - 맨 위에 추가, 기존 항목은 수정하지 않는다
  - 담당 = <프로젝트 폴더명> / <모델명>.  전체 경로 금지 (저장소가 public)
  - 무엇 / 왜 / 검증 세 줄. '왜' 가 없으면 다음 사람이 되돌린다

사용: python tools/seed_changelogs.py          (덮어쓰지 않는다. 없는 것만 생성)
      python tools/seed_changelogs.py --force  (전부 다시 생성)
"""
import io
import os
import re
import sys
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

HEADER = """# {name} — 변경 기록

> **이 스킬을 고치는 Claude 에게**
> 코드를 바꿨으면 **맨 위에 항목 하나를 새로 추가**하고 커밋해라. 기존 항목은 고치지 않는다.
> 형식은 아래와 같다. `담당` 에는 **작업 중인 프로젝트 폴더명 + 모델명** 을 적는다.
> 폴더명을 쓰는 이유는 "어느 작업에서 고친 건지" 가 바로 보이기 때문이다.
> ⚠️ **전체 경로는 쓰지 말 것** — 이 저장소는 public 이고 경로에 계정명이 들어간다.
> 폴더 이름만 쓴다.  `AIzeroC` ○  /  `C:{bs}Users{bs}<이름>{bs}...{bs}AIzeroC` ✗
>
> ```markdown
> ## YYYY-MM-DD — <프로젝트 폴더명> / <모델명>
> **무엇** 한 줄 요약
> - `파일명` 바꾼 내용
> **왜** 이유. 안 적으면 다음 사람이 되돌린다
> **검증** 실제로 돌려본 것
> ```
>
> 규칙 세 가지
> 1. **기존 동작을 깨지 말 것.** 바꿔야 하면 하위호환을 남기고 여기 적는다.
> 2. **실제 연구 수치·사람 이름을 넣지 말 것.** 이 저장소는 public 이다. 예시는 더미값으로.
> 3. **고쳤으면 실제로 한 번 돌려보고** 그 결과를 `검증` 에 적는다.

---
"""

PAST = """## {date} — (기록 이전. git log 에서 복원)

{items}
> 이 시점에는 CHANGELOG 규약이 없었다. 커밋 메시지에서 옮긴 것이라
> `왜`·`검증` 이 비어 있다. 이후 항목부터는 채운다.
"""


def log_for(path):
    """해당 스킬 경로의 커밋을 (날짜, 제목) 목록으로. 최신 우선."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--date=short", "--format=%ad\t%s", "--", path],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode("utf-8", "replace")
    except Exception:
        return []
    rows = []
    for ln in out.strip().split("\n"):
        if not ln.strip():
            continue
        d, _, s = ln.partition("\t")
        rows.append((d, s))
    return rows


def build(name, path):
    rows = log_for(path)
    body = HEADER.format(name=name, bs=chr(92))
    if not rows:
        return body + "\n_아직 기록 없음. 다음에 고치는 사람이 첫 항목을 쓴다._\n"
    # 날짜별로 묶는다 (같은 날 여러 커밋이면 한 항목에)
    seen, order = {}, []
    for d, s in rows:
        if d not in seen:
            seen[d] = []
            order.append(d)
        seen[d].append(s)
    out = [body]
    for d in order:
        items = "\n".join("- " + re.sub(r"^\w+(\([^)]*\))?:\s*", "", s) for s in seen[d])
        out.append(PAST.format(date=d, items=items + "\n"))
        out.append("---\n")
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    force = "--force" in sys.argv
    made, kept = [], []
    for name in sorted(os.listdir(SKILLS)):
        d = os.path.join(SKILLS, name)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "SKILL.md")):
            continue
        p = os.path.join(d, "CHANGELOG.md")
        if os.path.exists(p) and not force:
            kept.append(name)
            continue
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            build(name, "skills/" + name))
        made.append((name, len(log_for("skills/" + name))))
    print("생성 %d개" % len(made))
    for n, c in made:
        print("   %-24s 과거 커밋 %d개 복원" % (n, c))
    if kept:
        print("\n이미 있어 건너뜀: %s" % ", ".join(kept))
