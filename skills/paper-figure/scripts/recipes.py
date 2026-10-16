# -*- coding: utf-8 -*-
"""
pubfig 레시피 — "값으로 색칠 + 컬러바 + 제목에 지표 병기" 3종.

연구실 참고 코드에서 추출한 3종.
  value_scatter  <- 상태방정식(EOS) 포물선, k점 수렴곡선
  value_barh     <- 모델 벤치마크 MAE 순위 막대
  metric_title   <- 공통 (제목 2줄, 2번째 줄 괄호 안에 지표)

핵심 규칙 (이 룩을 만드는 것)
  - 마커/막대 색 = y 값 자체. cmap="inferno". 옆에 컬러바를 붙여 값↔색을 읽게 한다
  - 제목 2줄: 1줄 무엇을, 2줄 괄호 안에 피팅값·최고값 같은 지표
  - 그림 안에 설명 주석을 쓰지 않는다. 지표는 제목으로 올린다
  - 300 dpi, tight_layout

쓰는 법
    import sys, os
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/paper-figure/scripts"))
    import pubstyle as ps, recipes as rp
    ps.use()
    fig, ax = plt.subplots(figsize=(5, 4))
    rp.value_scatter(ax, V, E, cbar_label="Total energy (eV)", fig=fig)
    rp.metric_title(ax, "Equation of State",
                    "$a_0$ = %.4f $\\AA$, $B_0$ = %.1f GPa" % (a0, B0))
    ps.save(fig, "fig_eos.png")
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

try:
    import pubstyle as ps
except ImportError:                                  # 단독 실행 대비
    ps = None

CMAP = "inferno"


def metric_title(ax, what, metric, **kw):
    """제목 2줄. 2번째 줄 괄호 안에 지표. 그림 안 주석 대신 이걸 쓴다."""
    return ax.set_title("%s\n(%s)" % (what, metric), **kw)


def value_scatter(ax, x, y, c=None, fig=None, cbar_label=None, s=110,
                  cmap=CMAP, line=None, line_kw=None, zero_line=False, **kw):
    """값으로 색칠한 산점도 + 컬러바.  c 를 안 주면 y 로 색칠한다 (원본 동작).

    line      : (xg, yg) 를 주면 먼저 검은 점선 가이드를 깐다 (EOS 피팅곡선 등)
    zero_line : y=0 에 k-- 기준선 (수렴 그림용)
    """
    if line is not None:
        kwl = dict(color="k", linestyle="--", linewidth=1.5, zorder=1)
        kwl.update(line_kw or {})
        ax.plot(line[0], line[1], **kwl)
    if zero_line:
        ax.axhline(0, color="k", linestyle="--", linewidth=1, zorder=0)
    sc = ax.scatter(x, y, c=(y if c is None else c), cmap=cmap, s=s,
                    edgecolors="k", linewidths=0.8, zorder=3, **kw)
    cb = None
    if cbar_label is not None:
        cb = (fig or ax.figure).colorbar(sc, ax=ax, label=cbar_label)
        if ps is not None:
            ps.cbar_frame(cb)
    return sc, cb


def value_barh(ax, names, values, fig=None, label="", unit="", title=None, cmap=CMAP,
               fmt="%.4f", highlight=None, height=0.72, fontsize=8,
               ascending=True, cbar=True):
    """값으로 색칠한 가로막대 + 막대 끝 숫자 + 컬러바. 모델 순위표용.

    names/values : 정렬은 이 함수가 한다 (ascending=True 면 작은 값이 위)
    highlight    : 굵게+검은 테두리로 강조할 이름들 (set/list). 우리 모델 표시용
    반환         : 정렬된 (names, values)
    """
    names = np.asarray(names, dtype=object)
    values = np.asarray(values, dtype=float)
    o = np.argsort(values if ascending else -values)
    names, values = names[o], values[o]
    hi = np.array([n in (highlight or ()) for n in names])

    y = np.arange(len(values))
    cm = matplotlib.colormaps[cmap]
    norm = plt.Normalize(values.min(), values.max())
    ax.barh(y, values, color=cm(norm(values)), height=height,
            edgecolor=["k" if p else "none" for p in hi],
            linewidth=[1.6 if p else 0 for p in hi], zorder=3)
    lo, hi_v = min(0.0, values.min()), max(0.0, values.max())   # 음수 막대 지원 (양수만이면 기존과 동일)
    span = (hi_v - lo) or 1.0
    for yi, vi in zip(y, values):
        ax.text(vi + (span if vi >= 0 else -span) * 0.012, yi, fmt % vi, va="center",
                ha="left" if vi >= 0 else "right", fontsize=fontsize - 0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=fontsize)
    # fontweight 는 리스트를 못 받는다 -> 라벨별로 따로
    for t, p in zip(ax.get_yticklabels(), hi):
        if p:
            t.set_fontweight("bold")
    ax.invert_yaxis()
    ax.set_xlim(lo - (0.14 * span if lo < 0 else 0), hi_v + (0.14 * span if hi_v > 0 else 0))
    if lo < 0:
        ax.axvline(0, color="k", linewidth=0.8, zorder=4)
    ax.set_xlabel(label)
    if cbar:
        sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
        sm.set_array([])
        cb = (fig or ax.figure).colorbar(sm, ax=ax, label=label, pad=0.02)
        if ps is not None:
            ps.cbar_frame(cb)
    if title is not None:                    # 제목은 여기서 달아야 "(best = ...)" 가 붙는다
        metric_title(ax, title, "best = %s, %s %s" % (names[0], fmt % values[0], unit))
    return names, values


def parity(ax, ref, pred, c=None, fig=None, cbar_label="Number of atoms",
           s=50, alpha=0.8, cmap=CMAP, margin=0.1, unit="eV/atom",
           what=None, band=False):
    """parity plot — 참고 노트북(choung_style_code) 을 그대로 옮긴 것.

    원본:  plt.figure(figsize=(5,4))
           plt.scatter(ref, pred, c=atom_counts, cmap='inferno', s=50, alpha=0.8)
           plt.plot([lo-m, hi+m], [lo-m, hi+m], 'k--')      m = 범위의 10%
           plt.title(f'{element} Formation Energy 
(MAE = {mae:.3f} {unit})')
           plt.colorbar(scatter, label='Number of atoms')

    what  : 주면 제목을 "<what>
(MAE = x.xxx unit)" 로 단다
    band  : True 면 +-MAE 띠를 옅게 깐다 (오차 크기를 숫자 안 읽고 보이게)
    반환  : (scatter, cbar, mae, rmse)
    """
    ref = np.asarray(ref, float)
    pred = np.asarray(pred, float)
    mae = float(np.mean(np.abs(pred - ref)))
    rmse = float(np.sqrt(np.mean((pred - ref) ** 2)))

    lo = min(ref.min(), pred.min())
    hi = max(ref.max(), pred.max())
    m = (hi - lo) * margin
    if band:
        ax.fill_between([lo - m, hi + m], [lo - m - mae, hi + m - mae],
                        [lo - m + mae, hi + m + mae],
                        color="0.5", alpha=0.12, lw=0, zorder=0)
    ax.plot([lo - m, hi + m], [lo - m, hi + m], "k--", zorder=1)
    sc = ax.scatter(ref, pred, c=(ref if c is None else c), cmap=cmap,
                    s=s, alpha=alpha, zorder=3)
    ax.set_xlim(lo - m, hi + m)
    ax.set_ylim(lo - m, hi + m)
    cb = None
    if cbar_label is not None:
        cb = (fig or ax.figure).colorbar(sc, ax=ax, label=cbar_label)
        if ps is not None:
            ps.cbar_frame(cb)
    if what is not None:
        metric_title(ax, what, "MAE = %.3f %s" % (mae, unit))
    return sc, cb, mae, rmse


def label_points(ax, x, y, labels, bold=(), s=70, fontsize=8, pad=1.5, priority=None):
    """점 라벨을 서로/마커와 겹치지 않게 배치 (외부 패키지 없음, 탐욕 배치).

    후보 위치 = 8 방향 x 6 거리. 이미 놓인 라벨 상자 + 모든 마커 상자 + 축 밖과의 겹침이
    최소인 곳을 고르고, 바로 옆(1단계)이 아니면 회색 연결선을 긋는다.
    s        : 마커 크기 (scatter 의 s, pt^2) — 마커 상자 크기 계산용
    bold     : 굵게 쓸 라벨 집합 (후보군 강조)
    priority : 먼저 자리를 잡을 라벨 집합 (기본 = bold)
    반환     : Text 객체 리스트
    """
    fig = ax.figure
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    x = np.asarray(x, float); y = np.asarray(y, float)
    pix = ax.transData.transform(np.c_[x, y])
    r = np.sqrt(s) / 2 * fig.dpi / 72.0                       # marker radius in pixels
    marks = [(px - r, py - r, px + r, py + r) for px, py in pix]
    axb = ax.get_window_extent(rend)
    placed, texts = [], []

    def overlap(a, b):
        w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
        return w * h if (w > 0 and h > 0) else 0.0

    pri = set(bold if priority is None else priority)
    order = sorted(range(len(labels)), key=lambda i: (labels[i] not in pri, -pix[i][1]))
    dirs = [(1, 0, "left", "center"), (1, 1, "left", "bottom"), (0, 1, "center", "bottom"),
            (-1, 1, "right", "bottom"), (-1, 0, "right", "center"), (-1, -1, "right", "top"),
            (0, -1, "center", "top"), (1, -1, "left", "top")]
    for i in order:
        best = None
        for k, dist in enumerate((0.9, 1.6, 2.6, 3.8, 5.2, 7.0)):
            for dx, dy, ha, va in dirs:
                off = (dx * (r + pad) * dist, dy * (r + pad) * dist)
                t = ax.text(pix[i][0] + off[0], pix[i][1] + off[1], labels[i], transform=None,
                            fontsize=fontsize, ha=ha, va=va,
                            fontweight="bold" if labels[i] in bold else "normal")
                bb = t.get_window_extent(rend)
                box = (bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad)
                t.remove()
                cost = sum(overlap(box, b) for b in placed) * 10
                cost += sum(overlap(box, m) for j, m in enumerate(marks) if j != i)
                out = max(0, axb.x0 - box[0]) + max(0, box[2] - axb.x1) + max(0, axb.y0 - box[1]) + max(0, box[3] - axb.y1)
                cost += out * 50 + k * 4 + (0.5 if dy != 0 and dx == 0 else 0)
                if best is None or cost < best[0]:
                    best = (cost, off, ha, va, box, k)
        cost, off, ha, va, box, k = best
        xy_text = ax.transData.inverted().transform((pix[i][0] + off[0], pix[i][1] + off[1]))
        t = ax.annotate(labels[i], (x[i], y[i]), xytext=xy_text, textcoords="data", fontsize=fontsize,
                        ha=ha, va=va, fontweight="bold" if labels[i] in bold else "normal", zorder=6,
                        arrowprops=(dict(arrowstyle="-", color="0.25", lw=0.8, shrinkA=0, shrinkB=np.sqrt(s) / 2)
                                    if k >= 1 else None))
        placed.append(box)
        texts.append(t)
    return texts


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pubstyle as ps                                       # noqa: F811
    ps.use()
    rng = np.random.default_rng(0)

    fig, axs = plt.subplots(1, 3, figsize=(16, 4.6))
    # (a) EOS 꼴
    V = np.linspace(100, 140, 9)                       # 더미 데이터 (실제 결과 아님)
    E = 0.0020 * (V - 120) ** 2 - 50.0
    Vg = np.linspace(V.min() - 3, V.max() + 3, 400)
    value_scatter(axs[0], V, E, fig=fig, cbar_label="Total energy (eV)",
                  line=(Vg, 0.0020 * (Vg - 120) ** 2 - 50.0))
    metric_title(axs[0], "Equation of State", "$a_0$ = 4.0000 $\\AA$, $B_0$ = 150.0 GPa")
    axs[0].set_xlabel("Volume ($\\AA^3$)"); axs[0].set_ylabel("Total energy (eV)")
    ps.panel(axs[0], "a", dx=-0.16, dy=1.10)
    label_points(axs[0], V, E, ["V%d" % i for i in range(len(V))], s=110, bold={"V4"})

    # (b) 수렴 꼴
    x = np.arange(6)
    dE = np.array([9.0, 0.40, 0.05, 0.02, 0.01, 0.0])
    value_scatter(axs[1], x, dE, fig=fig, cbar_label="$\\Delta$E per atom (meV)",
                  line=(x, dE), line_kw=dict(color="#3D6EA8", linestyle="-", linewidth=1.8),
                  zero_line=True)
    metric_title(axs[1], "k-point Convergence", "max deviation above 7$\\times$7$\\times$7 = 0.05 meV/atom")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(["%dx%dx%d" % ((2 * i + 1,) * 3) for i in x], rotation=30, ha="right")
    axs[1].set_ylabel("$\\Delta$E per atom (meV)")
    ps.panel(axs[1], "b", dx=-0.16, dy=1.10)

    # (c) 순위 막대 꼴
    nm = ["model-%02d" % i for i in range(12)]
    vv = rng.uniform(0.05, 0.09, 12)
    value_barh(axs[2], nm, vv, fig=fig, label="Energy MAE (eV/atom)", unit="eV/atom",
               title="MLIP Benchmark — Energy", highlight={"model-03"})
    ps.panel(axs[2], "c", dx=-0.30, dy=1.10)

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_recipes_selftest.png")
    ps.save(fig, out)
    print("-> %s" % out)
