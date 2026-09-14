---
name: pubfig
description: Publication-style matplotlib figures in the lab's fixed convention (4-side framed axes, bold axis labels, ticks inside, no grid, black edges on filled elements, Arial, 300 dpi) plus the lab palette. Provides scripts/pubstyle.py — import it, call ps.use() once, draw, ps.save(fig, path). Project-agnostic; use for any result plot that goes into a paper, homework answer, or meeting slide when the user wants "the usual lab look". Korean triggers — "논문 스타일 그림", "논문 그림 규격", "박사님 스타일로", "pubfig", "publication figure", "그림 규격 맞춰", "lab style plot".
---

# pubfig

논문·과제·미팅용 결과 그림을 **항상 같은 규격**으로 그린다. 규격은 DRM 프로젝트 `drmstyle.py`
(2026-08-12 유저 확정)에서 프로젝트 색을 뺀 것. 스타일을 매번 새로 고르지 않는다.

## 규격 (변경 금지)
- 축 4면 테두리 1.6 pt, 거의 검정 `#1a1a1a` — "네모칸"
- 축 라벨·제목 **볼드**, 글꼴 Arial → DejaVu Sans 폴백
- **격자 없음.** `ax.grid()` 를 켰어도 `frame()`/`save()` 가 지운다
- 눈금 안쪽. 기본 `"none"`(눈금선 없이 숫자만). 필요 시 `use(ticks="lb")` / `"all"`
- 막대·영역 등 칠한 요소는 검은 외곽선 0.9 pt
- minor tick 없음, 범례 테두리 있음, 선 2.0 pt, 마커 5 pt
- 저장 300 dpi, `bbox_inches="tight"`, 흰 배경

## 팔레트
`C["navy" | "magenta" | "teal" | "amber" | "plum" | "sage" | "gray"]`, 순서 `ORDER`.
3계열까지는 navy / magenta / teal. 색과 함께 **마커도 다르게**(`MARKERS`) 두어 흑백 인쇄에서도 구분되게 한다.
연속값은 `cmap("navy")` 처럼 한 색의 그라데이션을 쓴다(기본 컬러맵과 팔레트가 따로 놀지 않게).

## 쓰는 법
```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/pubfig/scripts"))
import pubstyle as ps
ps.use()                                    # 1회

fig, ax = plt.subplots(figsize=(5, 4))
ax.plot(x, y, color=ps.C["navy"], marker="o", label="DFT")
ax.set_xlabel("Volume (Å$^3$/atom)"); ax.set_ylabel("Energy (eV/atom)")
ax.legend()
ps.save(fig, "fig.png")                     # frame() 자동 적용 + 300 dpi
```
- parity plot: `ps.parity_line(ax)` — y = x 점선 + 정사각 범위.
- 다중 패널: `ps.panel(ax, "a")` 로 볼드 패널 문자.
- 컬러바: `ps.cbar_frame(cb)`.
- 자가 점검: `python scripts/pubstyle.py` → `_pubstyle_selftest.png`.

## 하지 말 것
- 이 규격 위에 다른 스타일(`plt.style.use`, seaborn 등)을 덧씌우지 않는다.
- 그림에 격자·그림자·둥근 모서리·그라디언트 배경을 넣지 않는다.
- 색 하나로만 계열을 구분하지 않는다 (마커·선종류 병행).
