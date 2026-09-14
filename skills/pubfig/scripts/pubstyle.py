# -*- coding: utf-8 -*-
"""pubstyle - 논문(publication)용 matplotlib 그림 규격. 프로젝트 무관.

DRM 프로젝트의 drmstyle.py(2026-08-12 유저 확정 규약)에서 프로젝트 색만 떼어내고
규격만 남긴 것. 어느 폴더에서든 같은 모양의 그림이 나오게 하는 것이 목적이다.

쓰는 법
    import sys, os
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/pubfig/scripts"))
    import pubstyle as ps
    ps.use()                         # rcParams 적용 (스크립트 맨 위에서 1회)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, color=ps.C["navy"], marker="o")
    ps.frame(ax)                     # 저장 직전 모든 축에 (4면 테두리·격자 제거·눈금 정리)
    ps.save(fig, "fig.png")          # 300 dpi, bbox tight, 흰 배경

규약 (drmstyle 그대로)
    ★ 네모칸: 축 4면 테두리 (linewidth 1.6, 거의 검정)
    ★ 축 라벨 볼드, 제목 볼드
    ★ 격자 없음 — 배경이 데이터보다 먼저 보이면 안 된다
    ★ 눈금: 안쪽. 기본 "none"(눈금선 없이 숫자만) / "lb" / "all"
    ★ 칠한 요소(막대·영역)는 검은 외곽선 0.9
    ★ minor tick 없음, 범례 테두리 있음, 글꼴 Arial → DejaVu Sans 폴백
    ★ 저장 300 dpi

팔레트 (실험 그림과 맞춘 lab 기본 4색 + 보조 3색; drmstyle 값 그대로)
    navy #1B2A41 / magenta #A81C4E / teal #1FBDB2 / amber #EFA53C
    plum #622348 / sage #AEB37A / gray #6E6E6E,  ACCENT #c0143c
    ORDER 는 인접 색이 서로 잘 구분되도록 navy → magenta → teal → amber → … 순.
"""
import matplotlib
import matplotlib.pyplot as plt

# ---------------- 색 ----------------
C = {
    "navy":    "#1B2A41",
    "magenta": "#A81C4E",
    "teal":    "#1FBDB2",
    "amber":   "#EFA53C",
    "plum":    "#622348",
    "sage":    "#AEB37A",
    "gray":    "#6E6E6E",
}
ORDER = ["navy", "magenta", "teal", "amber", "plum", "sage", "gray"]
ACCENT = "#c0143c"      # 강조(운전점·기준선 등)
NEUTRAL = "#4a4a4a"
GRID = "#c8c8c8"
EDGE = "#1a1a1a"        # 테두리·외곽선 색
LW_AXIS = 1.6           # 축 테두리
LW_EDGE = 0.9           # 칠한 요소의 검은 외곽선
TICKS = "none"          # "none" | "lb" | "all"
MARKERS = ["o", "s", "^", "D", "v", "P", "X"]


def _tickcfg(ticks=None):
    t = (ticks or TICKS)
    if t == "all": return 5.2, True, True
    if t == "lb":  return 5.2, False, False
    return 0.0, False, False


def use(base=10.0, ticks=None):
    """논문 그림용 rcParams. 스크립트 맨 위에서 1회 호출."""
    _len, _top, _right = _tickcfg(ticks)
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": base,
        "axes.unicode_minus": False,
        "axes.titlesize": base + 1.5,
        "axes.titleweight": "bold",
        "axes.labelsize": base + 1.0,
        "axes.labelweight": "bold",
        "xtick.labelsize": base - 0.5,
        "ytick.labelsize": base - 0.5,
        "legend.fontsize": base - 1.0,
        "figure.titlesize": base + 3.0,
        "axes.spines.top": True, "axes.spines.right": True,
        "axes.spines.left": True, "axes.spines.bottom": True,
        "axes.linewidth": LW_AXIS,
        "axes.edgecolor": EDGE,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": _top, "ytick.right": _right,
        "xtick.color": EDGE, "ytick.color": EDGE,
        "xtick.major.size": _len, "ytick.major.size": _len,
        "xtick.major.width": 1.4 if _len else 0.0,
        "ytick.major.width": 1.4 if _len else 0.0,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "xtick.minor.size": 0.0, "ytick.minor.size": 0.0,
        "patch.linewidth": LW_EDGE,
        "patch.edgecolor": EDGE,
        "patch.force_edgecolor": True,
        "hatch.linewidth": LW_EDGE,
        "legend.frameon": True,
        "legend.framealpha": 0.95,
        "legend.edgecolor": "#888888",
        "legend.fancybox": False,
        "lines.linewidth": 2.0,
        "lines.markersize": 5.0,
        "axes.grid": False,
        "grid.color": GRID, "grid.linewidth": 0.6, "grid.alpha": 0.5,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "figure.dpi": 200,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def frame(ax, lw=LW_AXIS, minor=False, ticks=None):
    """축 하나에 4면 테두리 강제 + 격자 제거 + 눈금 규약. 저장 직전 모든 축에 부른다."""
    _len, _top, _right = _tickcfg(ticks)
    for s in ax.spines.values():
        s.set_visible(True); s.set_linewidth(lw); s.set_color(EDGE)
    ax.grid(False, which="both")
    ax.tick_params(which="both", direction="in", top=_top, right=_right, color=EDGE)
    ax.tick_params(which="major", length=_len, width=1.4 if _len else 0.0)
    from matplotlib.ticker import AutoMinorLocator, NullLocator
    if minor and _len:
        ax.tick_params(which="minor", length=3.0, width=1.0, top=_top, right=_right)
        if ax.get_xscale() == "linear": ax.xaxis.set_minor_locator(AutoMinorLocator())
        if ax.get_yscale() == "linear": ax.yaxis.set_minor_locator(AutoMinorLocator())
    else:
        ax.xaxis.set_minor_locator(NullLocator()); ax.yaxis.set_minor_locator(NullLocator())
        ax.tick_params(which="minor", length=0.0, width=0.0)
    return ax


def cbar_frame(cb, lw=LW_AXIS, ticks=None):
    """컬러바에도 같은 테두리·눈금 규약."""
    _len, _, _ = _tickcfg(ticks)
    cb.outline.set_linewidth(lw); cb.outline.set_edgecolor(EDGE)
    cb.ax.tick_params(direction="in", width=1.2 if _len else 0.0, length=_len * 0.8, color=EDGE)
    cb.ax.tick_params(which="minor", length=0.0, width=0.0)
    return cb


def panel(ax, letter, dx=-0.13, dy=1.02, pt=None):
    """패널 문자 (a, b, c …) 볼드, 축 좌상단 바깥."""
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=pt or plt.rcParams["font.size"] + 2,
            fontweight="bold", va="bottom", ha="left")
    return ax


def parity_line(ax, lo=None, hi=None, margin=0.1, **kw):
    """y = x 기준선 (parity plot). lo/hi 없으면 현재 데이터 범위에서 잡는다."""
    if lo is None or hi is None:
        xs = ax.get_xlim(); ys = ax.get_ylim()
        lo = min(xs[0], ys[0]); hi = max(xs[1], ys[1])
    m = (hi - lo) * margin
    kw.setdefault("color", EDGE); kw.setdefault("ls", "--"); kw.setdefault("lw", 1.2); kw.setdefault("zorder", 0)
    ax.plot([lo - m, hi + m], [lo - m, hi + m], **kw)
    ax.set_xlim(lo - m, hi + m); ax.set_ylim(lo - m, hi + m)
    return ax


def save(fig, path, dpi=300):
    """모든 축에 frame() 적용 후 저장. 300 dpi, bbox tight, 흰 배경."""
    for ax in fig.get_axes():
        if getattr(ax, "_colorbar", None) is None and ax.get_label() != "<colorbar>":
            frame(ax)
    fig.savefig(str(path), dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  -> %s" % path)


def cycle(keys=None):
    return [C[k] for k in (keys or ORDER)]


def cmap(color, light="#fdfdfb", dark=0.55, n=256):
    """계 색 하나로 만든 연속 컬러맵 (거의 흰색 → 그 색 → 어둡게). 어두운 색은 중간톤을 밝게."""
    import matplotlib.colors as mc
    hexv = C.get(color, color)
    c = mc.to_rgb(hexv)
    lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    if lum < 0.38:
        mid = tuple(x + (1.0 - x) * 0.55 for x in c)
        stops = [light, mid, c]
    else:
        dk = tuple(min(1.0, x * dark) for x in c)
        stops = [light, c, dk]
    return mc.LinearSegmentedColormap.from_list("pub_%s" % str(color), stops, N=n)


if __name__ == "__main__":
    # self-test: python pubstyle.py  ->  _pubstyle_selftest.png
    import os, numpy as np
    use()
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.6))
    x = np.linspace(0, 10, 60)
    for i, k in enumerate(ORDER[:4]):
        axs[0].plot(x, np.sin(x + i), color=C[k], marker=MARKERS[i], markevery=12, label=k)
    axs[0].set_xlabel("x label"); axs[0].set_ylabel("y label"); axs[0].legend(ncol=2); panel(axs[0], "a")
    axs[1].bar(range(4), [1.08, 0.62, 0.48, 0.3], color=cycle(ORDER[:4]))
    axs[1].set_xticks(range(4)); axs[1].set_xticklabels(ORDER[:4]); axs[1].set_ylabel("value (eV)"); panel(axs[1], "b")
    save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pubstyle_selftest.png"))
