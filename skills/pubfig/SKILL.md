---
name: pubfig
description: Publication-style matplotlib figures with the lab's two fixed looks, via scripts/pubstyle.py. preset "plain" (default) = the Catbench/parity-plot look — matplotlib defaults + Arial, title 14 / labels 12 / ticks 10, 300 dpi, inferno for continuous color; preset "lab" = DRM drmstyle look — 4-side framed axes 1.6 pt, bold labels, ticks inside, no grid, black edges, lab palette. Import, ps.use(), draw, ps.save(fig, path). Project-agnostic; use for any result plot going into a paper, homework answer, or slide. Korean triggers — "논문 스타일 그림", "그림 규격 맞춰", "박사님 스타일로", "석현 선배 스타일", "parity plot 스타일", "pubfig", "publication figure", "lab style plot".
---

# pubfig

논문·과제·미팅용 결과 그림을 **정해진 두 룩 중 하나**로 그린다. 스타일을 매번 새로 고르지 않는다.

## 프리셋
| preset | 출처 | 모양 |
|---|---|---|
| `plain` (기본) | Catbench parity plot (석현 선배 `0_utility` Arial 블록 + `plot_parity_from_csv`) | matplotlib 기본 rc + **Arial**, 제목 14 / 축라벨 12 / 눈금·범례 10, 얇은 4면 테두리, 눈금 바깥, 격자 없음, **계열색 = inferno 추출**(`ps.cycle()` / `ps.inferno_cycle(n)`: 진보라·적주황·노랑), 마커 `ps.MARKER_KW`(ms 7, alpha 0.85), 연속값 `inferno` 컬러바, 기준선 `k--`, 300 dpi |
| `lab` | DRM `drmstyle.py` (2026-08-12 확정) | 4면 테두리 1.6 pt, **볼드** 라벨·제목, 눈금 안쪽(`"none"`/`"lb"`/`"all"`), 격자 없음, 칠한 요소 검은 외곽선, lab 팔레트 navy/magenta/teal/amber, 300 dpi |

## 쓰는 법
```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/pubfig/scripts"))
import pubstyle as ps
ps.use()                                    # plain.  lab 룩: ps.use(preset="lab")

fig, ax = plt.subplots(figsize=(5, 4))
cols = ps.cycle()                           # plain: inferno 추출색 / lab: 팔레트
ax.plot(x, y, color=cols[0], marker=ps.MARKERS[0], label="DFT", **ps.MARKER_KW)
ax.set_xlabel("Volume (Å$^3$/atom)"); ax.set_ylabel("Energy (eV/atom)"); ax.legend()
ps.save(fig, "fig.png")                     # 300 dpi, bbox tight (lab 이면 frame() 자동)
```
- parity plot: `sc = ax.scatter(x, y, c=n, cmap="inferno", s=50, alpha=0.8)`; `ps.parity_line(ax)`; `ps.cbar_frame(fig.colorbar(sc, label="Number of atoms"))`
- 다중 패널: `ps.panel(ax, "a")`
- 리눅스 서버에 Arial 없으면: `ps.use(font_path="/path/arial.ttf")`
- 자가 점검: `python scripts/pubstyle.py` → `_pubstyle_selftest_plain.png`, `_lab.png`

## 규칙
- 색 하나로만 계열을 구분하지 않는다 — `ps.MARKERS` 로 마커 병행 (흑백 인쇄 대비).
- 이 위에 `plt.style.use`/seaborn 을 덧씌우지 않는다. 격자·그림자·그라디언트 배경 금지.
- 유니코드 첨자(₂)는 Arial 에 없다 → mathtext `$_2$` 로 쓴다.
