#!/usr/bin/env python3
"""연속성 훅을 ~/.claude/settings.json 에 **병합** 설치한다.

왜 별도 스크립트인가: settings.json 에는 이미 다른 도구의 훅이 여러 개 걸려 있을 수
있다(orca 등). 통째로 덮어쓰면 그것들이 전부 죽는다. 이 스크립트는 우리 항목만
식별해서 교체하고 나머지는 손대지 않는다.

설치되는 것:
  SessionStart -> hooks/inject-status.py   STATUS/dead-ends/decisions/LOG 를 세션에 자동 주입
  Stop         -> hooks/status-stale.py    STATUS 가 낡았을 때만 한 줄 경고

사용:
  python install_hooks.py <repo_dir> [--settings PATH] [--uninstall] [--dry-run]

경로가 없는 폴더에서는 훅이 스스로 조용히 통과하므로, 전역 설치해도 비연구 폴더에
영향이 없다.
"""
import argparse
import json
import os
import shutil
import sys
import time

# (이벤트, 스크립트 파일명, 타임아웃, 스피너 문구)
HOOK_SPECS = [
    ("SessionStart", "inject-status.py", 15, "연구 연속성 파일 불러오는 중"),
    ("Stop", "status-stale.py", 15, None),
]
OURS = {name for _, name, _, _ in HOOK_SPECS}


def build_command(script_path):
    """python3 우선, 없으면 python. 스크립트가 없으면 조용히 통과."""
    return (
        f"H='{script_path}'; [ -f \"$H\" ] && "
        f'{{ python3 "$H" 2>/dev/null || python "$H" 2>/dev/null; }} || true'
    )


def is_ours(entry):
    """이 그룹이 우리가 심은 것인지. 스크립트 파일명으로 식별한다."""
    for hook in entry.get("hooks", []):
        cmd = hook.get("command", "")
        if any(name in cmd for name in OURS):
            return True
    return False


def load_settings(path):
    if not os.path.isfile(path):
        return {}, False
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        return {}, True
    return json.loads(text), True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_dir", help="claude-skills 저장소 경로")
    ap.add_argument("--settings", default=None, help="기본: ~/.claude/settings.json")
    ap.add_argument("--uninstall", action="store_true", help="우리 훅만 제거")
    ap.add_argument("--dry-run", action="store_true", help="쓰지 않고 결과만 출력")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo_dir).replace("\\", "/")
    hooks_dir = f"{repo}/hooks"
    settings_path = args.settings or os.path.join(
        os.path.expanduser("~"), ".claude", "settings.json"
    )

    if not args.uninstall:
        missing = [n for _, n, _, _ in HOOK_SPECS if not os.path.isfile(os.path.join(hooks_dir, n))]
        if missing:
            print(f"ERROR: 훅 스크립트를 찾을 수 없음: {missing} (in {hooks_dir})", file=sys.stderr)
            return 1

    try:
        settings, existed = load_settings(settings_path)
    except json.JSONDecodeError as exc:
        print(f"ERROR: settings.json 이 이미 깨져 있음 — 건드리지 않음: {exc}", file=sys.stderr)
        return 1

    if not isinstance(settings, dict):
        print("ERROR: settings.json 최상위가 객체가 아님 — 건드리지 않음", file=sys.stderr)
        return 1

    before = json.dumps(settings, ensure_ascii=False, sort_keys=True)
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        print("ERROR: settings.hooks 가 객체가 아님 — 건드리지 않음", file=sys.stderr)
        return 1

    removed = added = 0
    for event, script, timeout, status_msg in HOOK_SPECS:
        groups = hooks.get(event, [])
        if not isinstance(groups, list):
            print(f"ERROR: hooks.{event} 가 배열이 아님 — 건드리지 않음", file=sys.stderr)
            return 1
        kept = [g for g in groups if not is_ours(g)]
        removed += len(groups) - len(kept)

        if not args.uninstall:
            hook = {
                "type": "command",
                "command": build_command(f"{hooks_dir}/{script}"),
                "timeout": timeout,
            }
            if status_msg:
                hook["statusMessage"] = status_msg
            kept.append({"hooks": [hook]})
            added += 1

        if kept:
            hooks[event] = kept
        else:
            hooks.pop(event, None)

    if not hooks:
        settings.pop("hooks", None)

    after = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"

    # 쓰기 전에 반드시 되읽기 검증 (깨진 JSON 을 남기면 그 파일의 설정이 전부 죽는다)
    json.loads(after)

    if args.dry_run:
        print(f"[dry-run] {settings_path}: 기존 우리항목 {removed}개 제거, {added}개 추가")
        print(after)
        return 0

    if before == json.dumps(settings, ensure_ascii=False, sort_keys=True):
        print(f"변경 없음 (이미 최신): {settings_path}")
        return 0

    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    if existed:
        backup = f"{settings_path}.bak.{time.strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(settings_path, backup)
        print(f"백업: {backup}")

    tmp = settings_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(after)
    os.replace(tmp, settings_path)

    other = sum(
        1
        for groups in settings.get("hooks", {}).values()
        for g in groups
        if not is_ours(g)
    )
    verb = "제거" if args.uninstall else "설치"
    print(f"{verb} 완료: {settings_path}")
    print(f"  우리 훅 {added}개 · 교체된 기존 우리항목 {removed}개 · 보존된 남의 훅 그룹 {other}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
