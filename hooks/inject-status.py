#!/usr/bin/env python3
"""SessionStart hook — 연구 폴더의 연속성 파일을 세션 컨텍스트에 자동 주입한다.

사용자가 "이어서"라고 치지 않아도, 새 창을 열자마자 어제 상태가 들어간다.
연속성 파일이 하나도 없는 폴더(연구 폴더가 아닌 곳)에서는 조용히 아무것도 하지 않는다.

주입 대상 (있는 것만):
  STATUS.md      현재 상태 스냅샷
  dead-ends.md   반복 금지 목록
  decisions/     결정 기록 인덱스 (파일명만)
  LOG.md         가장 최근 엔트리 1개 (append-only이므로 맨 아래)
"""
import json
import os
import re
import sys

MAX_TOTAL = 12000  # 주입 총량 상한(문자). 넘으면 LOG부터 잘라낸다.


def read(path):
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def latest_log_entry(text):
    """append-only LOG에서 마지막 '## ' 섹션만 돌려준다."""
    heads = list(re.finditer(r"^## .+$", text, re.M))
    if not heads:
        return None
    return text[heads[-1].start():].strip()


def decisions_index():
    if not os.path.isdir("decisions"):
        return None
    names = sorted(
        n for n in os.listdir("decisions")
        if n.endswith(".md") and not n.startswith(".")
    )
    if not names:
        return None
    return "\n".join(f"- decisions/{n}" for n in names)


def main():
    blocks = []

    status = read("STATUS.md")
    if status and status.strip():
        blocks.append(("STATUS.md — 현재 상태", status.strip()))

    dead = read("dead-ends.md")
    if dead and dead.strip():
        blocks.append(("dead-ends.md — 이미 실패한 것. 다시 시도 금지", dead.strip()))

    idx = decisions_index()
    if idx:
        blocks.append(("decisions/ — 확정된 결정. 재논의 전에 먼저 읽을 것", idx))

    log = read("LOG.md")
    if log:
        entry = latest_log_entry(log)
        if entry:
            blocks.append(("LOG.md — 최신 엔트리", entry))

    if not blocks:
        return 0  # 연구 폴더가 아님. 조용히 통과.

    # 상한 초과 시 뒤쪽(LOG)부터 잘라낸다. STATUS는 끝까지 보존.
    while len(" ".join(b[1] for b in blocks)) > MAX_TOTAL and len(blocks) > 1:
        blocks.pop()

    body = "\n\n".join(f"### {title}\n\n{content}" for title, content in blocks)
    context = (
        "이 폴더의 연구 연속성 파일이 자동으로 주입됐다. "
        "사용자에게 어제 뭘 했는지 다시 설명하게 요구하지 말 것. "
        "아래를 이미 읽은 상태로 대화를 시작한다.\n\n" + body
    )

    payload = json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        },
        ensure_ascii=False,
    )
    # 콘솔 기본 인코딩(Windows=cp949)으로 쓰면 한글에서 UnicodeEncodeError 가 나고
    # 이미 흘러나간 앞부분 때문에 반쪽 JSON 이 남는다. 반드시 바이트로 한 번에 쓴다.
    sys.stdout.buffer.write(payload.encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # 훅이 세션 시작을 막으면 안 된다. 실패하면 조용히 통과.
        sys.exit(0)
