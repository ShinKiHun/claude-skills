# -*- coding: utf-8 -*-
"""CHANGELOG.md 맨 위에 항목 하나를 끼워 넣는다 (머리말 뒤, 기존 항목 앞).

사용:
    python tools/add_entry.py <skill> <date> <담당> <<'TXT'
    **무엇** ...
    **왜** ...
    **검증** ...
    TXT
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "\n---\n"          # 머리말 끝 구분선


def add(skill, date, who, body):
    p = os.path.join(ROOT, "skills", skill, "CHANGELOG.md")
    s = io.open(p, encoding="utf-8").read()
    i = s.index(MARK) + len(MARK)
    entry = "\n## %s — %s\n\n%s\n\n---\n" % (date, who, body.strip())
    io.open(p, "w", encoding="utf-8", newline="\n").write(s[:i] + entry + s[i:])
    return p


if __name__ == "__main__":
    skill, date, who = sys.argv[1], sys.argv[2], sys.argv[3]
    print("추가:", add(skill, date, who, sys.stdin.read()))
