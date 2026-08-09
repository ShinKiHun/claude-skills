#!/usr/bin/env python3
"""Stop hook — STATUS.md 가 실제 작업보다 낡았을 때만 한 줄 알린다.

SessionStart 훅이 STATUS.md 를 자동 주입하기 때문에, STATUS 가 낡으면
"조용히 틀린 어제"가 주입된다. 아무 말 없는 것보다 나쁘다. 그래서 낡음을 감지한다.

시끄러우면 안 되므로 조건을 좁게 잡는다:
  - STATUS.md 가 있고 (연구 폴더)
  - 프로젝트 안에 STATUS 보다 최소 STALE_HOURS 이상 새로운 파일이 있을 때만
알림은 systemMessage 한 줄. 턴을 막지 않는다(continue 를 건드리지 않음).
"""
import json
import os
import sys
import time

STALE_HOURS = 6
SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__", ".ipynb_checkpoints", ".venv"}
SKIP_FILES = {"STATUS.md", "LOG.md"}
MAX_SCAN = 4000  # 큰 데이터 폴더에서 훅이 오래 걸리면 안 된다


def newest_work_file(root, status_mtime):
    """STATUS 보다 새로운 파일 중 가장 최근 것. (mtime, 상대경로) 또는 None."""
    best = None
    seen = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            seen += 1
            if seen > MAX_SCAN:
                return best
            if name in SKIP_FILES or name.startswith("."):
                continue
            path = os.path.join(dirpath, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > status_mtime and (best is None or mtime > best[0]):
                best = (mtime, os.path.relpath(path, root))
    return best


def main():
    if not os.path.isfile("STATUS.md"):
        return 0  # 연구 폴더가 아님

    try:
        status_mtime = os.path.getmtime("STATUS.md")
    except OSError:
        return 0

    newest = newest_work_file(".", status_mtime)
    if newest is None:
        return 0  # STATUS 가 최신

    gap_h = (newest[0] - status_mtime) / 3600.0
    if gap_h < STALE_HOURS:
        return 0  # 아직 낡지 않음

    days = (time.time() - status_mtime) / 86400.0
    msg = (
        f"STATUS.md 가 {days:.0f}일 전에 멈춰 있음 "
        f"(더 새로운 작업 파일: {newest[1]}). "
        f"다음 세션에 낡은 상태가 주입된다 — \"오늘 정리\" 로 갱신할 것."
    )
    payload = json.dumps({"systemMessage": msg}, ensure_ascii=False)
    sys.stdout.buffer.write(payload.encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # 훅이 턴을 막으면 안 된다
