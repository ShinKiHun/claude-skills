# -*- coding: utf-8 -*-
"""pubstyle - 논문(publication)용 matplotlib 그림 규격. 프로젝트 무관. 프리셋 2개.

    preset="plain"  (기본)  Catbench/석현 선배 parity plot 룩.
                            matplotlib 기본 rc + Arial + 제목 14 / 축라벨 12 / 눈금 10 + 300 dpi.
                            얇은 4면 테두리(0.8), 눈금 바깥, 격자 없음, 계열색 = inferno 에서 추출(진보라/적주황/노랑).
                            원본: /home/jovyan/1_Seokhyun/0_utility/ 의 Arial 등록 블록 + plot_parity_from_csv.
    preset="lab"            DRM drmstyle.py(2026-08-12 확정) 룩. 4면 테두리 1.6·볼드 라벨·눈금 없음·
                            검은 외곽선·lab 팔레트(navy/magenta/teal/amber…). 발표·인쇄용으로 더 무겁다.

쓰는 법
    import sys, os
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/pubfig/scripts"))
    import pubstyle as ps
    ps.use()                            # plain.  lab 룩은 ps.use(preset="lab")
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, marker="o", label="DFT")
    ps.parity_line(ax)                  # parity plot 이면 y = x 점선
    ps.save(fig, "fig.png")             # 300 dpi, bbox tight

    Arial 이 시스템에 없는 리눅스 서버: ps.use(font_path="/path/to/arial.ttf")

plain 규약
    ★ rc 는 matplotlib 기본값에서 글꼴·크기·dpi 만 바꾼다 (테두리·눈금·격자 건드리지 않음)
    ★ Arial → DejaVu Sans 폴백.  제목 14 / 축라벨 12 / 눈금·범례 10
    ★ 저장 300 dpi, bbox tight, 흰 배경
lab 규약
    ★ 네모칸 4면 테두리 1.6, 볼드 축라벨·제목, 격자 없음(frame()이 지움), 눈금 안쪽 "none"/"lb"/"all",
      칠한 요소 검은 외곽선 0.9, minor tick 없음, 범례 테두리, Arial, 300 dpi

팔레트
    C / ORDER : lab 4색 + 보조 3색 (drmstyle 값).  cycle() 은 plain 이면 inferno_cycle(4), lab 이면 ORDER.
    inferno_cycle(n) : 범주 n개를 inferno 에서 등간격 추출.  MARKER_KW : ms=7, alpha=0.85 (scatter s=50 느낌).
    MARKERS   : 색과 함께 마커도 다르게 — 흑백 인쇄 대비.
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
TAB10 = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
PRESET = "plain"


def _register_font(font_path):
    """서버에 Arial 이 없을 때 ttf 를 직접 등록 (석현 선배 블록과 동일)."""
    if not font_path:
        return
    from matplotlib import font_manager as fm
    try:
        fm.fontManager.addfont(font_path)
    except Exception as e:
        print("pubstyle: font register failed (%s): %s" % (font_path, e))


def _tickcfg(ticks=None):
    t = (ticks or TICKS)
    if t == "all": return 5.2, True, True
    if t == "lb":  return 5.2, False, False
    return 0.0, False, False


def use(preset="plain", base=10.0, ticks=None, font_path=None):
    """rcParams 적용. 스크립트 맨 위에서 1회.

    preset : "plain"(기본, Catbench parity 룩) | "lab"(drmstyle 룩)
    base   : lab 프리셋의 기준 글자 크기 (plain 은 14/12/10 고정)
    ticks  : lab 프리셋 눈금 "none"/"lb"/"all"
    font_path : Arial ttf 경로 (리눅스 서버 등 시스템에 없을 때)
    """
    global PRESET
    PRESET = preset
    _register_font(font_path)
    if preset == "plain":
        matplotlib.rcdefaults()
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 10, "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "figure.facecolor": "white", "axes.facecolor": "white",
        })
        return
    if preset != "lab":
        raise ValueError("preset must be 'plain' or 'lab'")
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
    if PRESET == "plain":        # 기본 rc 그대로 (얇은 4면 테두리·눈금 바깥). 손대지 않는다
        return ax
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
    """컬러바에도 같은 테두리·눈금 규약 (lab 프리셋만)."""
    if PRESET == "plain":
        return cb
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
    kw.setdefault("color", "k" if PRESET == "plain" else EDGE); kw.setdefault("ls", "--")
    kw.setdefault("lw", 1.5 if PRESET == "plain" else 1.2); kw.setdefault("zorder", 0)
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
    """색 순환 리스트. plain 프리셋이면 inferno 에서 뽑은 색(parity plot 색감), lab 이면 ORDER."""
    if keys is None and PRESET == "plain":
        return inferno_cycle(4)
    return [C[k] for k in (keys or ORDER)]


def inferno_cycle(n=3, lo=0.12, hi=0.82, cmap_name="inferno"):
    """범주형 계열 n개를 inferno(기본) 컬러맵에서 등간격으로 뽑는다 — parity plot 컬러바와 같은 색감.
    lo/hi 로 양끝(검정·연노랑) 을 잘라 흰 배경에서 읽히게 한다.  n=3: 진보라 / 적주황 / 노랑."""
    import matplotlib.colors as mc
    import numpy as np
    cm = plt.get_cmap(cmap_name)
    return [mc.to_hex(cm(v)) for v in np.linspace(lo, hi, n)]


MARKER_KW = dict(ms=7, alpha=0.85, mec="none")   # parity plot 의 s=50, alpha=0.8 에 해당하는 line-plot 마커 설정


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
    # self-test: python pubstyle.py  ->  _pubstyle_selftest_plain.png / _lab.png
    import os, numpy as np
    here = os.path.dirname(os.path.abspath(__file__))
    for preset in ("plain", "lab"):
        use(preset=preset)
        fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
        x = np.linspace(0, 10, 60); cols = cycle()
        for i in range(3):
            axs[0].plot(x, np.sin(x + i), color=cols[i], marker=MARKERS[i], markevery=12, label="series %d" % i, **(MARKER_KW if preset == "plain" else {}))
        axs[0].set_xlabel("x label"); axs[0].set_ylabel("y label"); axs[0].set_title("line"); axs[0].legend()
        rng = np.random.default_rng(0); a = rng.normal(2, 0.6, 80); b = a + rng.normal(0, 0.08, 80)
        sc = axs[1].scatter(a, b, c=rng.integers(2, 55, 80), cmap="inferno", s=50, alpha=0.8)
        parity_line(axs[1]); cbar_frame(fig.colorbar(sc, ax=axs[1], label="Number of atoms"))
        axs[1].set_xlabel("DFT (eV/atom)"); axs[1].set_ylabel("Model (eV/atom)"); axs[1].set_title("parity (MAE = 0.038 eV/atom)")
        fig.tight_layout()
        save(fig, os.path.join(here, "_pubstyle_selftest_%s.png" % preset))
