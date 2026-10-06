# -*- coding: utf-8 -*-
"""make_vesta.py — 구조파일 → **space-filling .vesta**. 프로젝트 무관, 어느 폴더에서나.

출처: DRM_finish/make_vesta.py → cu-MOF/calc/_env/make_vesta.py → 이 스킬로 일반화 (2026-10-06).
템플릿 `vesta_template.vesta` 의 **구조 의존 섹션만** 갈아끼운다
(TITLE / CELLP / STRUC / THERI / SBOND / SITET / ATOMT).
STYLE(MODEL 1 = space-filling)·조명·카메라는 템플릿 그대로 → 열면 바로 그 룩이 나온다.

원소 지정 — **주기율표 전체(103종)가 파일 안에 미리 박혀 있다**
  ELEM 딕셔너리에 H~Lr 전부 (반지름, RGB) 로 들어 있다. 런타임 생성 없음.
  -> 어떤 구조를 던져도 색이 이미 정해져 있고, 파일만 열면 뭐가 나올지 보인다.
  -> 35종은 연구실 확정값, 나머지는 Jmol 표준색. 바꾸려면 ELEM 한 줄만 고친다.

결합(SBOND) — 역시 자동
  ① 연구실 확정 규칙(BONDS)이 있으면 우선.
  ② 없는 쌍은 `d_max = BOND_SCALE x (r_i + r_j)` 로 생성.
     **금속-금속 쌍과 동일원소 쌍은 만들지 않는다** (space-filling 에서 거미줄이 되므로).

사용
  python make_vesta.py <파일 또는 폴더> [출력폴더] [--norep] [--rep 3x3x1] [--all-bonds]
    · 폴더를 주면 그 안의 구조파일 전부 (vasp/POSCAR/cif/xyz/extxyz/cfg/traj 마지막 프레임)
    · 기본 출력 = 입력 옆 `VESTA/`
    · 기본 2x2x1 슈퍼셀 (PBC 로 잘린 분자가 겹쳐 보이는 것 방지). 원셀은 --norep
    · --all-bonds : 금속-금속·동일원소 쌍도 결합으로 그린다
"""
import sys
from pathlib import Path
from ase.io import read
from ase.data import atomic_numbers, covalent_radii

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
TMPL = (HERE / "vesta_template.vesta").read_text().splitlines()

# ── 원소표 — **주기율표 전체(H~Lr 103종) 가 여기 다 박혀 있다** ────────────────
#    (space-filling 반지름 A, (r,g,b))
#    · 35종은 **연구실 확정값** (O/C/H/N/Ni/Pt/Ce/La = DRM 확정 · Cu/Zn/Zr/In 등은 서로 안 겹치게 고른 값).
#      예전 그림과 색이 같아야 하므로 **이 값들을 바꾸지 말 것.**
#    · 나머지 68종은 Jmol 표준색 + 공유결합반지름으로 미리 채워 넣었다.
#      런타임에 만들지 않는다 — 파일만 보면 어떤 원소가 무슨 색으로 나올지 다 보인다.
#    · 바꾸고 싶으면 여기 줄만 고치면 된다.
ELEM = {
    "H": (0.46, (255, 204, 204)), "He": (0.60, (255,   0, 255)), "Li": (1.28, (204, 128, 255)),
    "Be": (0.96, (194, 255,   0)), "B": (0.84, (255, 181, 181)), "C": (0.77, (128,  73,  41)),
    "N": (0.74, ( 48,  80, 248)), "O": (0.74, (254,   3,   0)), "F": (0.57, (144, 224,  80)),
    "Ne": (0.58, (179, 227, 245)), "Na": (1.66, (171,  92, 242)), "Mg": (1.41, (138, 255,   0)),
    "Al": (1.43, (191, 166, 166)), "Si": (1.17, (240, 200, 160)), "P": (1.07, (255, 128,   0)),
    "S": (1.04, (255, 255,  48)), "Cl": (1.02, ( 31, 240,  31)), "Ar": (1.06, (128, 209, 227)),
    "K": (2.03, (143,  64, 212)), "Ca": (1.76, ( 61, 255,   0)), "Sc": (1.70, (230, 230, 230)),
    "Ti": (1.47, (191, 194, 199)), "V": (1.34, (166, 166, 171)), "Cr": (1.28, (138, 153, 199)),
    "Mn": (1.27, (156, 122, 199)), "Fe": (1.26, (224, 102,  51)), "Co": (1.25, (240, 144, 160)),
    "Ni": (1.25, (183, 187, 189)), "Cu": (1.28, ( 34,  71, 220)), "Zn": (1.39, (143, 143, 129)),
    "Ga": (1.41, (194, 143, 143)), "Ge": (1.22, (102, 143, 143)), "As": (1.19, (189, 128, 227)),
    "Se": (1.20, (255, 161,   0)), "Br": (1.20, (166,  41,  41)), "Kr": (1.16, ( 92, 184, 209)),
    "Rb": (2.20, (112,  46, 176)), "Sr": (1.95, (  0, 255,   0)), "Y": (1.90, (148, 255, 255)),
    "Zr": (1.60, (148, 224, 224)), "Nb": (1.46, (115, 194, 201)), "Mo": (1.39, ( 84, 181, 181)),
    "Tc": (1.47, ( 59, 158, 158)), "Ru": (1.34, ( 36, 143, 143)), "Rh": (1.34, ( 10, 125, 140)),
    "Pd": (1.37, (  0, 105, 133)), "Ag": (1.44, (192, 192, 192)), "Cd": (1.44, (255, 217, 143)),
    "In": (1.67, (166, 117, 115)), "Sn": (1.40, (102, 128, 128)), "Sb": (1.39, (158,  99, 181)),
    "Te": (1.38, (212, 122,   0)), "I": (1.39, (148,   0, 148)), "Xe": (1.40, ( 66, 158, 176)),
    "Cs": (2.44, ( 87,  23, 143)), "Ba": (2.15, (  0, 201,   0)), "La": (1.88, ( 90, 196,  73)),
    "Ce": (1.82, (209, 252,   6)), "Pr": (2.03, (217, 255, 199)), "Nd": (2.01, (199, 255, 199)),
    "Pm": (1.99, (163, 255, 199)), "Sm": (1.98, (143, 255, 199)), "Eu": (1.98, ( 97, 255, 199)),
    "Gd": (1.96, ( 69, 255, 199)), "Tb": (1.94, ( 48, 255, 199)), "Dy": (1.92, ( 31, 255, 199)),
    "Ho": (1.92, (  0, 255, 156)), "Er": (1.89, (  0, 230, 117)), "Tm": (1.90, (  0, 212,  82)),
    "Yb": (1.87, (  0, 191,  56)), "Lu": (1.87, (  0, 171,  36)), "Hf": (1.75, ( 77, 194, 255)),
    "Ta": (1.70, ( 77, 166, 255)), "W": (1.39, ( 33, 148, 214)), "Re": (1.51, ( 38, 125, 171)),
    "Os": (1.44, ( 38, 102, 150)), "Ir": (1.36, ( 22,  84, 135)), "Pt": (1.39, (203, 197, 191)),
    "Au": (1.44, (255, 209,  35)), "Hg": (1.32, (184, 184, 208)), "Tl": (1.45, (166,  84,  77)),
    "Pb": (1.75, ( 87,  89,  97)), "Bi": (1.48, (158,  79, 181)), "Po": (1.40, (171,  92,   0)),
    "At": (1.50, (117,  79,  69)), "Rn": (1.50, ( 66, 130, 150)), "Fr": (2.60, ( 66,   0, 102)),
    "Ra": (2.21, (  0, 125,   0)), "Ac": (2.15, (112, 171, 250)), "Th": (2.06, (  0, 186, 255)),
    "Pa": (2.00, (  0, 161, 255)), "U": (1.96, (  0, 143, 255)), "Np": (1.90, (  0, 128, 255)),
    "Pu": (1.87, (  0, 107, 255)), "Am": (1.80, ( 84,  92, 242)), "Cm": (1.69, (120,  92, 227)),
    "Bk": (2.00, (138,  79, 227)), "Cf": (2.00, (161,  54, 212)), "Es": (2.00, (179,  31, 212)),
    "Fm": (2.00, (179,  31, 186)), "Md": (2.00, (179,  13, 166)), "No": (2.00, (189,  13, 135)),
    "Lr": (2.00, (199,   0, 102)),
    "Og": (1.20, (255,   0, 255)),   # 미지정 원소용 폴백 색 (자홍) — 실제로 쓸 일은 없다
}
FALLBACK = (1.20, (255, 0, 255))     # 표에 없으면 자홍으로 그리고 경고만 — 죽지 않는다

# ── ① 연구실 확정 결합 규칙 (x, y, d_min, d_max) ────────────────────────────
BONDS = [
    ("C", "O", 0.0, 1.97), ("C", "H", 0.0, 1.20), ("H", "O", 0.0, 1.20), ("H", "O", 1.20, 2.10),
    ("C", "N", 0.0, 1.80), ("N", "H", 0.0, 1.20), ("N", "O", 0.0, 1.60),
    ("Ni", "O", 0.0, 2.28), ("Ni", "C", 0.0, 2.10),
    ("Pt", "O", 0.0, 2.35), ("Pt", "C", 0.0, 2.20), ("Pt", "Ni", 0.0, 2.90),
    ("Cu", "O", 0.0, 2.40), ("Cu", "C", 0.0, 2.30), ("Cu", "H", 0.0, 2.00),
    ("Zn", "O", 0.0, 2.40), ("Zn", "C", 0.0, 2.40), ("Zn", "H", 0.0, 2.10),
    ("Zr", "O", 0.0, 2.55), ("Zr", "C", 0.0, 2.45), ("Zr", "H", 0.0, 2.20),
    ("Ce", "O", 0.0, 2.75), ("In", "O", 0.0, 2.55), ("Ti", "O", 0.0, 2.45),
    ("Al", "O", 0.0, 2.20), ("Si", "O", 0.0, 2.00),
]

NONMETAL = {"H", "B", "C", "N", "O", "F", "Si", "P", "S", "Cl", "Se", "Br", "I"}
BOND_SCALE = 1.35          # 자동 결합 길이 = 이 값 x (공유결합반지름 합)
REP = (2, 2, 1)            # 보기용 슈퍼셀. 계산과 무관 — .vesta 파일만
ALL_BONDS = False          # True 면 금속-금속·동일원소 쌍도 그린다
EXT = (".vasp", ".cif", ".xyz", ".extxyz", ".traj", ".cfg", ".poscar", ".contcar", ".json")


def elem(sym):
    """(반지름, (r,g,b)). 표가 주기율표 전체를 덮으므로 사실상 항상 적중한다."""
    if sym not in ELEM:
        print(f"  [경고] ELEM 에 {sym} 없음 — 폴백색(자홍)으로 그린다. ELEM 에 추가할 것")
    return ELEM.get(sym, FALLBACK)


def bond_rules(els):
    """확정 규칙 먼저, 없는 쌍은 공유결합반지름으로 자동 생성."""
    out = [b for b in BONDS if b[0] in els and b[1] in els]
    have = {frozenset((x, y)) for x, y, _, _ in out}
    for i, x in enumerate(els):
        for y in els[i:]:
            k = frozenset((x, y))
            if k in have:
                continue
            if not ALL_BONDS and (x == y or (x not in NONMETAL and y not in NONMETAL)):
                continue          # 금속-금속·동일원소는 space-filling 에서 거미줄이 된다
            rx = covalent_radii[atomic_numbers[x]]; ry = covalent_radii[atomic_numbers[y]]
            out.append((x, y, 0.0, round(BOND_SCALE * (rx + ry), 2)))
            have.add(k)
    return out


def hdr(name):
    for i, l in enumerate(TMPL):
        if l.strip().split()[0:1] == [name] or l.strip() == name:
            return i
    raise KeyError(name)


def make_vesta(src, out, rep=None):
    a = read(str(src), index=-1)
    rep = REP if rep is None else rep
    if rep != (1, 1, 1):
        a = a.repeat(rep)
    S = a.get_chemical_symbols(); n = len(a)
    P = a.get_scaled_positions(wrap=True); cp = a.cell.cellpar()
    els = list(dict.fromkeys(S))
    lab, cnt = [], {}
    for s in S:
        cnt[s] = cnt.get(s, 0) + 1; lab.append(f"{s}{cnt[s]}")
    TITLE = ["TITLE", " ".join(f"{e:<2s}" for e in els) + " "]
    CELLP = ["CELLP", f" {cp[0]:.6f}  {cp[1]:.6f}  {cp[2]:.6f}  {cp[3]:.6f}  {cp[4]:.6f}  {cp[5]:.6f}",
             "  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000"]
    STRUC = ["STRUC"]
    for i in range(n):
        STRUC.append(f"{i+1:>3d}  {S[i]:<2s}  {lab[i]:>8s}  1.0000  "
                     f"{P[i,0]:9.6f}  {P[i,1]:9.6f}  {P[i,2]:9.6f}    1a       1")
        STRUC.append("                            0.000000   0.000000   0.000000  0.00")
    STRUC.append("  0 0 0 0 0 0 0")
    THERI = ["THERI 1"] + [f"{i+1:>3d}  {lab[i]:>8s}  0.000000" for i in range(n)] + ["  0 0 0"]
    SBOND = ["SBOND"]
    for bn, (x, y, dmn, dmx) in enumerate(bond_rules(els), 1):
        SBOND.append(f"{bn:>3d}  {x:>4s}  {y:>4s}  {dmn:.5f}  {dmx:.5f}  0  1  1  0  1  "
                     f"0.250  2.000 127 127 127")
    SBOND.append("  0 0 0 0")
    SITET = ["SITET"]
    for i in range(n):
        r, (cr, cg, cb) = elem(S[i])
        SITET.append(f"{i+1:>3d}  {lab[i]:>8s}  {r:.4f} {cr:>3d} {cg:>3d} {cb:>3d} "
                     f"{cr:>3d} {cg:>3d} {cb:>3d} 204  0")
    SITET.append("  0 0 0 0 0 0")
    ATOMT = ["ATOMT"]
    for j, e in enumerate(els, 1):
        r, (cr, cg, cb) = elem(e)
        ATOMT.append(f"{j:>3d}  {e:>9s}  {r:.4f} {cr:>3d} {cg:>3d} {cb:>3d} "
                     f"{cr:>3d} {cg:>3d} {cb:>3d} 204")
    ATOMT.append("  0 0 0 0 0 0")
    iG, iCE, iSH, iSB, iVE, iAT, iSC = (hdr("GROUP"), hdr("CELLP"), hdr("SHAPE"), hdr("SBOND"),
                                        hdr("VECTR"), hdr("ATOMT"), hdr("SCENE"))
    lines = (TMPL[0:hdr("TITLE")] + TITLE + TMPL[iG:iCE] + CELLP + STRUC + THERI
             + TMPL[iSH:iSB] + SBOND + SITET + TMPL[iVE:iAT] + ATOMT + TMPL[iSC:])
    Path(out).write_text("\n".join(lines) + "\n")
    auto = [e for e in els if e not in ELEM]
    print(f"  {Path(out).name}  ({n} atoms, {els}"
          + (f", 자동색 {auto}" if auto else "") + ")")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__); sys.exit(0)
    if "--norep" in argv:
        REP = (1, 1, 1); argv.remove("--norep")
    if "--all-bonds" in argv:
        ALL_BONDS = True; argv.remove("--all-bonds")
    if "--rep" in argv:
        i = argv.index("--rep")
        REP = tuple(int(x) for x in argv[i + 1].lower().split("x")); del argv[i:i + 2]
    src = Path(argv[0])
    files = sorted(f for f in src.rglob("*") if f.suffix.lower() in EXT or f.name.upper()
                   in ("POSCAR", "CONTCAR")) if src.is_dir() else [src]
    outd = Path(argv[1]) if len(argv) > 1 else (src if src.is_dir() else src.parent) / "VESTA"
    outd.mkdir(parents=True, exist_ok=True)
    ok = 0
    for f in files:
        try:
            make_vesta(f, outd / (f.stem + ".vesta")); ok += 1
        except Exception as e:
            print(f"  [건너뜀] {f.name}: {type(e).__name__} {e}")
    print(f"완료: {ok}/{len(files)} .vesta -> {outd}  "
          f"(space-filling, 보기용 {REP[0]}x{REP[1]}x{REP[2]} 슈퍼셀)")
