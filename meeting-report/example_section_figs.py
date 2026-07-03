"""20260703 리포트 보강 figure 2장 (6/30 기준: 핵심 섹션마다 전용 그림).
① fig_qcd_flow — QCD 자산 회수 개념도 (DB → 4 추출물 → 엔진/검증)
② fig_ruban — Ruban 28쌍 대조 매트릭스 (부호 히트맵 + 일치 마킹)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

INK, INK2, MUTED, GRID, SURF = "#1B2733", "#33414F", "#6B7682", "#E5E9ED", "#FFFFFF"
TEAL, OCHRE, CLAY, BLUE = "#2E6F77", "#B5872E", "#B0564C", "#3F6E9A"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.unicode_minus": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK})

# ── ① QCD flow ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12.5, 5.6), dpi=170)
ax.set_xlim(0, 100); ax.set_ylim(0, 104); ax.axis("off")

def box(x, y, w, h, title, sub, fc, ec, title_c=INK, fs=11.5):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.4",
                                   fc=fc, ec=ec, lw=1.5))
    ax.text(x + w/2, y + h - 4, title, ha="center", va="top",
            fontsize=fs, fontweight="bold", color=title_c)
    ax.text(x + w/2, y + h - 12, sub, ha="center", va="top", fontsize=9, color=INK2,
            linespacing=1.5)

def arrow(x1, y1, x2, y2, c=MUTED):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.7))

box(2, 30, 23, 46, "QCD dataset", "DFT full-relax\n62,880\n(55 elem, size 3-55)\n+ UMA SP\n1,520,614", "#F2F7F7", TEAL, TEAL)
ax.text(13.5, 22, "new compute ~ 0\n(join / fit only)", ha="center", va="top",
        fontsize=9.5, color=CLAY, fontweight="bold")

ys = [79, 53, 27, 1]
labels = [("isomer anchor", "UMA-DFT tau 0.772\nsize55 argmin 6/8", BLUE),
          ("surface penalty order", "Au<Ag<Cu<Pd<Pt<Ni<Rh<Ir\n(3d < 4d < 5d)", BLUE),
          ("motif map (55 elem)", "14 ih-formers\nAu/Pt amorph = literature", OCHRE),
          ("skeleton library", "ih / anti-Mackay /\nlow-sym candidates", OCHRE)]
for y, (t, sb, c) in zip(ys, labels):
    box(35, y, 30, 24, t, sb, "#FBFBFA", c)
    arrow(25.5, 53, 35, y + 12)

box(76, 56, 22, 32, "validation\nstack", "UMA trust for\nskeleton pick\n+ Ruban / Kristoffersen", "#FBF7EE", OCHRE)
box(76, 10, 22, 32, "proposal engine\nMark 5", "multi-skeleton\n5/5 new records\n(+ supported pilot)", "#F2F7F7", TEAL, TEAL)
arrow(65, 91, 76, 78); arrow(65, 65, 76, 71)
arrow(65, 39, 76, 32); arrow(65, 13, 76, 24)
fig.savefig("/tmp/claude-1051/-DATA-user-scratch-khshin-NDU/c4ac04c8-57cb-4a1e-a937-280069f1f4c6/scratchpad/fig_qcd_flow.png",
            bbox_inches="tight", facecolor=SURF)
plt.close(fig)

# ── ② Ruban matrix ─────────────────────────────────────────
E = ["Ni", "Cu", "Rh", "Pd", "Ag", "Ir", "Pt", "Au"]
M = {  # host -> solute -> E_segr (Ruban Table II)
 "Ni": {"Cu":-.25,"Rh":-.10,"Pd":-.40,"Ag":-.80,"Ir":.16,"Pt":-.17,"Au":-.69},
 "Cu": {"Ni":.17,"Rh":.05,"Pd":-.20,"Ag":-.42,"Ir":.23,"Pt":-.04,"Au":-.29},
 "Rh": {"Ni":-.08,"Cu":-.38,"Pd":-.45,"Ag":-.92,"Ir":.23,"Pt":-.27,"Au":-.87},
 "Pd": {"Ni":.21,"Cu":.04,"Rh":.36,"Ag":-.26,"Ir":.70,"Pt":.19,"Au":-.22},
 "Ag": {"Ni":.49,"Cu":.22,"Rh":.42,"Pd":.28,"Ir":.55,"Pt":.34,"Au":.03},
 "Ir": {"Ni":.12,"Cu":-.12,"Rh":-.08,"Pd":-.55,"Ag":-1.00,"Pt":-.58,"Au":-1.20},
 "Pt": {"Ni":.43,"Cu":.32,"Rh":.26,"Pd":.00,"Ag":-.27,"Ir":.44,"Au":-.36},
 "Au": {"Ni":.56,"Cu":.34,"Rh":.44,"Pd":.28,"Ag":.00,"Ir":.50,"Pt":.34},
}
RANK = {"Au":7,"Ag":6,"Pd":5,"Pt":4,"Cu":3,"Rh":2,"Ni":1,"Ir":0}  # 클수록 표면

fig, ax = plt.subplots(figsize=(7.6, 6.4), dpi=170)
mat = np.full((8, 8), np.nan)
for i, h in enumerate(E):
    for j, s in enumerate(E):
        if h != s:
            mat[i, j] = M[h][s]
im = ax.imshow(mat, cmap="RdBu", vmin=-1.2, vmax=1.2)
for i, h in enumerate(E):
    for j, s in enumerate(E):
        if h == s:
            ax.add_patch(mp.Rectangle((j-.5, i-.5), 1, 1, fc="#EFF2F5", ec="none"))
            continue
        v = M[h][s]
        ax.text(j, i, f"{v:+.2f}".replace("+0.00", "0.00").replace("-0.00","0.00"),
                ha="center", va="center", fontsize=7.6,
                color="white" if abs(v) > 0.6 else INK)
        # 우리 예측과 부호 일치 여부 (near-zero |E|<0.05 는 중립)
        ours_surf = RANK[s] > RANK[h]          # solute가 표면 예측이면 음수여야
        ok = (v < 0) == ours_surf or abs(v) <= 0.05
        if not ok:
            ax.add_patch(mp.Rectangle((j-.5, i-.5), 1, 1, fill=False, ec=CLAY, lw=2.2))
ax.set_xticks(range(8), E); ax.set_yticks(range(8), E)
ax.set_xlabel("solute  (negative / red = segregates to surface)", fontsize=9.5, color=INK2)
ax.set_ylabel("host", fontsize=9.5, color=INK2)
ax.set_title("Ruban 1999 DFT E$_{segr}$ (eV) — red border = sign mismatch vs our ranking\n"
             "(2 cells only, both near-degenerate $|E| \\leq$ 0.12: Ni-Rh, Ir-Ni)",
             fontsize=10, pad=10)
cb = fig.colorbar(im, ax=ax, shrink=0.82)
cb.set_label("E$_{segr}$ (eV)", fontsize=9)
fig.tight_layout()
fig.savefig("/tmp/claude-1051/-DATA-user-scratch-khshin-NDU/c4ac04c8-57cb-4a1e-a937-280069f1f4c6/scratchpad/fig_ruban.png",
            bbox_inches="tight", facecolor=SURF)
print("saved 2 figs")
