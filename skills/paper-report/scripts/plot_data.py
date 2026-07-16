#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper-report: 우리 계산결과 데이터 플롯 헬퍼.

리포트의 시각 시스템과 같은 팔레트로 result plot(line/bar/scatter)을 그린다.
논문 figure 추출과 별개로, 우리가 계산한 데이터(흡착에너지·반응경로 PES·성능비교 등)를
같은 톤으로 시각화해 한 리포트에 통합하기 위한 것.

입력: JSON spec (파일 또는 stdin). CSV 경로도 허용.
figure 내부 텍스트는 한글 폰트 부재 대비 영문 권장(visual-system 규칙).

spec 예:
{
  "kind": "bar",                     # line | bar | scatter | pes
  "title": "CO2 adsorption energy",
  "xlabel": "site", "ylabel": "E_ads (eV)",
  "series": [{"name":"Cu/ZnO", "x":["top","bridge","hollow"], "y":[-0.42,-0.55,-0.38]}],
  "note": "예시 데이터",            # 실데이터 아니면 반드시 명시 → figure에 워터마크
  "out": "figures/fig_ads.png"
}

'pes' kind: 반응경로 에너지 다이어그램(계단식 수평선 + 연결선).
  series[].x = 상태 라벨(IS, TS1, INT, ...), series[].y = 상대에너지(eV).

사용:
  python plot_data.py spec.json
  echo '{...}' | python plot_data.py -
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

# ── 리포트 CSS와 동일 팔레트 (example_builder.py :root 토큰과 일치) ──
INK, INK2, MUTED, GRID, SURF = "#1B2733", "#33414F", "#6B7682", "#E5E9ED", "#FFFFFF"
TEAL, OCHRE, CLAY, BLUE = "#2E6F77", "#B5872E", "#B0564C", "#3F6E9A"
CYCLE = [TEAL, CLAY, BLUE, OCHRE, "#6A8D3F", "#7A5C9E"]

# 한글 = Malgun 우선(NanumSquare mpl space 버그 회피) + NanumSquare 등록. 그림에도 한글 OK.
_FONT_STACK = _fonts.register_mpl()
plt.rcParams.update({
    "font.family": _FONT_STACK, "font.size": 10, "axes.unicode_minus": False,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2,
})


def _style(ax, spec):
    ax.set_title(spec.get("title", ""), fontsize=12, fontweight="bold", color=INK, pad=10)
    if spec.get("xlabel"):
        ax.set_xlabel(spec["xlabel"], fontsize=10.5)
    if spec.get("ylabel"):
        ax.set_ylabel(spec["ylabel"], fontsize=10.5)
    ax.grid(True, color=GRID, lw=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _watermark(fig, note):
    """실데이터 아님 등 주의 라벨을 눈에 띄게(중앙 옅은 대각) — 오해 방지."""
    if not note:
        return
    fig.text(0.5, 0.5, note, fontsize=30, color=CLAY, alpha=0.13,
             ha="center", va="center", rotation=24, fontweight="bold", zorder=0)
    fig.text(0.99, 0.01, note, fontsize=9, color=CLAY, alpha=0.8,
             ha="right", va="bottom", fontweight="bold")


def plot_line(spec):
    fig, ax = plt.subplots(figsize=(7.6, 4.8), dpi=170)
    for i, s in enumerate(spec["series"]):
        c = CYCLE[i % len(CYCLE)]
        ax.plot(s["x"], s["y"], marker="o", ms=5, lw=2, color=c, label=s.get("name"))
    if any(s.get("name") for s in spec["series"]):
        ax.legend(frameon=False, fontsize=9.5)
    _style(ax, spec)
    return fig


def plot_bar(spec):
    fig, ax = plt.subplots(figsize=(7.6, 4.8), dpi=170)
    series = spec["series"]
    cats = series[0]["x"]
    n = len(series)
    import numpy as np
    idx = np.arange(len(cats))
    w = 0.8 / max(n, 1)
    for i, s in enumerate(series):
        c = CYCLE[i % len(CYCLE)]
        ax.bar(idx + i * w - 0.4 + w / 2, s["y"], width=w, color=c, label=s.get("name"), edgecolor="white", lw=0.6)
    ax.set_xticks(idx)
    ax.set_xticklabels(cats)
    if any(s.get("name") for s in series):
        ax.legend(frameon=False, fontsize=9.5)
    _style(ax, spec)
    return fig


def plot_scatter(spec):
    fig, ax = plt.subplots(figsize=(7.0, 5.4), dpi=170)
    for i, s in enumerate(spec["series"]):
        c = CYCLE[i % len(CYCLE)]
        ax.scatter(s["x"], s["y"], s=48, color=c, label=s.get("name"), edgecolor="white", lw=0.6, alpha=0.9)
    if any(s.get("name") for s in spec["series"]):
        ax.legend(frameon=False, fontsize=9.5)
    _style(ax, spec)
    return fig


def plot_pes(spec):
    """반응경로 에너지 다이어그램: 각 상태를 짧은 수평선, 상태 사이를 점선으로 연결."""
    fig, ax = plt.subplots(figsize=(8.4, 4.8), dpi=170)
    seg = 0.6  # 수평선 반폭
    for si, s in enumerate(spec["series"]):
        c = CYCLE[si % len(CYCLE)]
        xs, ys = s["x"], s["y"]
        for j, (lab, e) in enumerate(zip(xs, ys)):
            ax.hlines(e, j - seg, j + seg, color=c, lw=3)
            if j > 0:
                ax.plot([j - 1 + seg, j - seg], [ys[j - 1], e], ls="--", lw=1.2, color=c, alpha=0.7)
            ax.annotate(f"{e:+.2f}", (j, e), textcoords="offset points", xytext=(0, 7),
                        ha="center", fontsize=8.5, color=INK)
        ax.plot([], [], color=c, lw=3, label=s.get("name"))
    ax.set_xticks(range(len(spec["series"][0]["x"])))
    ax.set_xticklabels(spec["series"][0]["x"])
    if any(s.get("name") for s in spec["series"]):
        ax.legend(frameon=False, fontsize=9.5)
    _style(ax, spec)
    ax.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.7)
    ax.grid(False, axis="x")
    return fig


KINDS = {"line": plot_line, "bar": plot_bar, "scatter": plot_scatter, "pes": plot_pes}


def render(spec):
    fig = KINDS[spec["kind"]](spec)
    _watermark(fig, spec.get("note"))
    fig.tight_layout()
    out = Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor=SURF, dpi=170)
    plt.close(fig)
    print(f"[plot_data] {spec['kind']} -> {out}"
          + (f"  (note: {spec['note']})" if spec.get("note") else ""))


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: plot_data.py <spec.json | ->")
    raw = sys.stdin.read() if sys.argv[1] == "-" else Path(sys.argv[1]).read_text(encoding="utf-8")
    data = json.loads(raw)
    specs = data if isinstance(data, list) else [data]
    for spec in specs:
        if spec.get("kind") not in KINDS:
            sys.exit(f"ERROR: kind must be one of {list(KINDS)} (got {spec.get('kind')})")
        render(spec)


if __name__ == "__main__":
    main()
