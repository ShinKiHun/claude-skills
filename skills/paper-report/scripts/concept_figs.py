#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper-report: 요약 개념도 헬퍼 (flow / matrix).

meeting-report/example_section_figs.py 의 box()/arrow()/heatmap 패턴을 이식.
원본은 하드코딩 1회성 스크립트였음 → 여기서는 JSON spec으로 파라미터화.
(맹목 복사 아님: 리눅스 절대경로 savefig·특정 프로젝트 데이터 제거하고 재사용 가능한 함수로 고침.)

kind:
  flow   : box-and-arrow 개념 흐름도 (예: 반응 메커니즘 단계, 파이프라인)
  matrix : 값 히트맵 + 셀 텍스트 (예: dopant×지표 비교, 세그리게이션 표)

figure 내부 텍스트는 영문 권장(한글 폰트 부재 대비).

spec 예 (flow):
{
  "kind": "flow", "title": "CO2 -> CH3OH (formate route)",
  "nodes": [
    {"id":"a","x":2,"y":40,"w":20,"h":22,"title":"CO2(g)","sub":"+ H*","color":"teal"},
    {"id":"b","x":30,"y":40,"w":20,"h":22,"title":"HCOO*","sub":"formate","color":"blue"}
  ],
  "arrows": [["a","b"]],
  "out":"figures/fig_flow.png"
}

spec 예 (matrix):
{
  "kind":"matrix","title":"Dopant screening",
  "rows":["Zn","Zr","Ce"], "cols":["Activity","Stability"],
  "values":[[0.8,0.5],[0.6,0.9],[0.7,0.7]],
  "vmin":0,"vmax":1,"cmap":"RdBu","fmt":"{:.2f}",
  "out":"figures/fig_matrix.png"
}
"""
import json
import sys
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _fonts  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

INK, INK2, MUTED, GRID, SURF = "#1B2733", "#33414F", "#6B7682", "#E5E9ED", "#FFFFFF"
TEAL, OCHRE, CLAY, BLUE = "#2E6F77", "#B5872E", "#B0564C", "#3F6E9A"
NAMED = {"teal": TEAL, "ochre": OCHRE, "clay": CLAY, "blue": BLUE, "ink": INK, "muted": MUTED}
FILL = {"teal": "#F2F7F7", "ochre": "#FBF7EE", "clay": "#FBF1EF", "blue": "#F1F5FA", "muted": "#FBFBFA"}

# 한글 = Malgun 우선(NanumSquare mpl space 버그 회피) + NanumSquare 등록
_FONT_STACK = _fonts.register_mpl()
plt.rcParams.update({"font.family": _FONT_STACK, "font.size": 10, "axes.unicode_minus": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK})


def _color(name):
    return NAMED.get(name, TEAL)


def make_flow(spec):
    nodes = spec["nodes"]
    arrows = spec.get("arrows", [])
    # 전역 여백: 요소 경계보다 넉넉히 (visual-system 규칙, 잘림/겹침 방지)
    xs = [n["x"] for n in nodes] + [n["x"] + n["w"] for n in nodes]
    ys = [n["y"] for n in nodes] + [n["y"] + n["h"] for n in nodes]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    mx = max(5, (xmax - xmin) * 0.07)
    my = max(8, (ymax - ymin) * 0.16)  # 제목(title)이 위에 얹히므로 상단 여백 크게
    fig, ax = plt.subplots(figsize=spec.get("figsize", [12.0, 5.4]), dpi=170)
    ax.set_xlim(xmin - mx, xmax + mx)
    ax.set_ylim(ymin - my, ymax + my)
    ax.set_aspect("equal")  # 박스 비율 유지 → 도형 왜곡·겹침 방지
    ax.axis("off")
    ax.set_title(spec.get("title", ""), fontsize=13, fontweight="bold", color=INK, pad=12)

    idx = {}
    for n in nodes:
        idx[n["id"]] = n
        col = n.get("color", "teal")
        ec, fc = _color(col), FILL.get(col, "#FBFBFA")
        ax.add_patch(mp.FancyBboxPatch((n["x"], n["y"]), n["w"], n["h"],
                                       boxstyle="round,pad=1.2", fc=fc, ec=ec, lw=1.6))
        cx, cy = n["x"] + n["w"] / 2, n["y"] + n["h"] / 2
        title = n.get("title", "")
        sub = n.get("sub", "")
        # 제목+부제를 박스 세로 중앙에 '한 덩어리'로 배치 (자간·행간 고른 그룹)
        if sub:
            ax.text(cx, cy + n["h"] * 0.12, title, ha="center", va="center",
                    fontsize=11.5, fontweight="bold", color=ec, linespacing=1.35)
            ax.text(cx, cy - n["h"] * 0.20, sub, ha="center", va="center",
                    fontsize=9, color=INK2, linespacing=1.5)
        else:
            ax.text(cx, cy, title, ha="center", va="center",
                    fontsize=11.5, fontweight="bold", color=ec, linespacing=1.35)

    for a in arrows:
        src, dst = (a[0], a[1]) if isinstance(a, (list, tuple)) else (a["from"], a["to"])
        s, d = idx[src], idx[dst]
        gap = 1.2  # 화살표가 박스에 닿지 않도록 양끝 여백
        if d["x"] >= s["x"] + s["w"]:      # dst가 오른쪽
            sx, dx = s["x"] + s["w"] + gap, d["x"] - gap
            sy, dy = s["y"] + s["h"] / 2, d["y"] + d["h"] / 2
        elif d["x"] + d["w"] <= s["x"]:    # dst가 왼쪽
            sx, dx = s["x"] - gap, d["x"] + d["w"] + gap
            sy, dy = s["y"] + s["h"] / 2, d["y"] + d["h"] / 2
        elif d["y"] > s["y"]:              # dst가 아래
            sy, dy = s["y"] - gap, d["y"] + d["h"] + gap
            sx, dx = s["x"] + s["w"] / 2, d["x"] + d["w"] / 2
        else:                              # dst가 위
            sy, dy = s["y"] + s["h"] + gap, d["y"] - gap
            sx, dx = s["x"] + s["w"] / 2, d["x"] + d["w"] / 2
        ax.annotate("", xy=(dx, dy), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.9,
                                    shrinkA=0, shrinkB=0))
    return fig


def make_matrix(spec):
    rows = spec["rows"]
    cols = spec["cols"]
    vals = np.array(spec["values"], dtype=float)
    fmt = spec.get("fmt", "{:.2f}")
    fig, ax = plt.subplots(figsize=spec.get("figsize", [max(5, 1.2 * len(cols) + 2), max(4, 0.8 * len(rows) + 2)]), dpi=170)
    im = ax.imshow(vals, cmap=spec.get("cmap", "RdBu"),
                   vmin=spec.get("vmin", np.nanmin(vals)), vmax=spec.get("vmax", np.nanmax(vals)))
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = vals[i, j]
            if np.isnan(v):
                continue
            rng = (spec.get("vmax", np.nanmax(vals)) - spec.get("vmin", np.nanmin(vals))) or 1.0
            far = abs(v - (spec.get("vmin", np.nanmin(vals)) + rng / 2)) > rng * 0.32
            ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=9,
                    color="white" if far else INK)
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), rows)
    ax.set_title(spec.get("title", ""), fontsize=11.5, fontweight="bold", color=INK, pad=10)
    if spec.get("xlabel"):
        ax.set_xlabel(spec["xlabel"], fontsize=9.5, color=INK2)
    if spec.get("ylabel"):
        ax.set_ylabel(spec["ylabel"], fontsize=9.5, color=INK2)
    cb = fig.colorbar(im, ax=ax, shrink=0.82)
    if spec.get("cbar_label"):
        cb.set_label(spec["cbar_label"], fontsize=9)
    return fig


KINDS = {"flow": make_flow, "matrix": make_matrix}


def render(spec):
    fig = KINDS[spec["kind"]](spec)
    if spec.get("note"):
        fig.text(0.99, 0.01, spec["note"], fontsize=9, color=CLAY, alpha=0.8,
                 ha="right", va="bottom", fontweight="bold")
    fig.tight_layout()
    out = Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor=SURF)
    plt.close(fig)
    print(f"[concept_figs] {spec['kind']} -> {out}")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: concept_figs.py <spec.json | ->")
    raw = sys.stdin.read() if sys.argv[1] == "-" else Path(sys.argv[1]).read_text(encoding="utf-8")
    data = json.loads(raw)
    specs = data if isinstance(data, list) else [data]
    for spec in specs:
        if spec.get("kind") not in KINDS:
            sys.exit(f"ERROR: kind must be one of {list(KINDS)} (got {spec.get('kind')})")
        render(spec)


if __name__ == "__main__":
    main()
