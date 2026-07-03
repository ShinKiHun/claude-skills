"""20260703 일일 리포트 — 6/30 '교수님급' 디자인 재사용 (build_html.py 패턴)."""
import base64
from pathlib import Path

SCRATCH = Path(__file__).parent
FIGDIR = Path("/DATA/user_scratch/khshin/NDU/reports/figures")
OUT = Path("/DATA/user_scratch/khshin/NDU/reports/20260703_20260709/20260703.html")

def b64(p):
    return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()

IMG = {
    "geom": b64(FIGDIR / "geom_ensemble.png"),
    "ih": b64(SCRATCH / "struct_gas_ih.png"),
    "al": b64(SCRATCH / "struct_al2o3.png"),
    "flow": b64(SCRATCH / "fig_qcd_flow.png"),
    "ruban": b64(SCRATCH / "fig_ruban.png"),
}

CSS = """
:root{--ink:#1B2733;--ink2:#33414F;--sub:#6B7682;--faint:#9AA4AE;
--hair:#E5E9ED;--line2:#EFF2F5;--bg:#FAFBFC;--card:#FFFFFF;
--teal:#2E6F77;--teald:#23565C;--ochre:#B5872E;--clay:#B0564C;--blue:#3F6E9A;
--shadow:0 1px 2px rgba(27,39,51,.04),0 8px 28px rgba(27,39,51,.07);}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',-apple-system,
BlinkMacSystemFont,system-ui,sans-serif;color:var(--ink);background:var(--bg);
line-height:1.62;-webkit-font-smoothing:antialiased;word-break:keep-all;overflow-wrap:break-word;}
.bar{position:fixed;top:0;left:0;right:0;height:56px;z-index:60;display:flex;align-items:center;
gap:24px;padding:0 32px;background:rgba(250,251,252,.86);backdrop-filter:saturate(160%) blur(10px);
border-bottom:1px solid var(--hair);}
.bar .b{font-weight:800;font-size:15px;letter-spacing:-.3px}
.bar .b i{font-style:normal;color:var(--teal)}
.bar nav{display:flex;gap:18px;font-size:13px;flex-wrap:wrap}
.bar nav a{color:var(--sub);text-decoration:none;padding:2px 0;border-bottom:2px solid transparent;transition:.15s}
.bar nav a:hover{color:var(--ink);border-color:var(--ochre)}
.bar .d{margin-left:auto;font-size:12px;color:var(--faint);letter-spacing:1px}
.prog{position:fixed;top:56px;left:0;height:3px;background:linear-gradient(90deg,var(--teal),var(--ochre));z-index:60;width:0}
main{max-width:1060px;margin:0 auto;padding:56px 32px 40px}
.hero{position:relative;padding:74px 44px 56px;margin:14px 0 8px;border-radius:20px;
background:linear-gradient(135deg,#F3F8F8 0%,#FAFBFC 52%,#FBF7EF 100%);
border:1px solid var(--hair);overflow:hidden}
.hero::before{content:"";position:absolute;top:0;left:0;width:6px;height:100%;
background:linear-gradient(180deg,var(--teal),var(--ochre))}
.hero .kick{font-size:12.5px;font-weight:800;letter-spacing:2.5px;color:var(--ochre);text-transform:uppercase}
.hero h1{margin-top:16px;font-size:34px;line-height:1.34;font-weight:800;letter-spacing:-.8px;max-width:940px}
.hero h1 em{font-style:normal;color:var(--teal)}
.hero .lead{margin-top:22px;font-size:17px;color:var(--ink2);max-width:800px;line-height:1.72}
.hero .pills{margin-top:30px;display:flex;gap:10px;flex-wrap:wrap}
.pill{font-size:12.5px;font-weight:700;padding:7px 15px;border-radius:22px;border:1px solid var(--hair);background:#fff}
.pill.k{color:var(--teal);border-color:#CFE0E2;background:#F2F7F7}
.pill.o{color:var(--ochre);border-color:#EAD9B0;background:#FBF7EE}
.pill.c{color:var(--clay);border-color:#E6C3BD;background:#FBF1EF}
.hero .meta{margin-top:24px;font-size:13px;color:var(--faint);border-top:1px solid var(--line2);padding-top:18px}
section{padding:50px 0}
section+section{border-top:1px solid var(--line2)}
.kick{font-size:12px;font-weight:800;letter-spacing:2px;color:var(--ochre);text-transform:uppercase}
h2{margin-top:10px;font-size:26px;font-weight:800;letter-spacing:-.5px;display:flex;align-items:center;gap:14px}
.num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;flex:0 0 auto;
border-radius:10px;background:var(--teal);color:#fff;font-size:15px;font-weight:800;box-shadow:var(--shadow)}
.take{margin:20px 0 6px;padding:16px 22px;background:#fff;border:1px solid var(--hair);
border-left:4px solid var(--teal);border-radius:10px;font-size:17px;font-weight:700;box-shadow:var(--shadow)}
figure{margin:24px 0 8px;background:#fff;border:1px solid var(--hair);border-radius:16px;
padding:14px;box-shadow:var(--shadow)}
figure img{width:100%;height:auto;display:block;border-radius:9px;background:#fff}
figcaption{margin-top:10px;font-size:13px;color:var(--sub);padding:0 6px}
.duo{display:grid;grid-template-columns:1fr 1.6fr;gap:16px;align-items:start}
@media(max-width:700px){.duo{grid-template-columns:1fr}}
ul.p{list-style:none;margin:16px 0}
ul.p li{position:relative;padding:6px 0 6px 24px;font-size:15.5px;color:var(--ink2)}
ul.p li::before{content:"";position:absolute;left:3px;top:14px;width:7px;height:7px;border-radius:50%;background:var(--teal)}
ul.p li b{color:var(--teald)}
.note{margin-top:18px;padding:14px 20px;border-radius:10px;font-size:14.5px;line-height:1.65}
.note.o{background:#FBF7EE;border:1px solid #EAD9B0;border-left:4px solid var(--ochre);color:#5C4A1E}
.note.o b{color:var(--ochre)}
.note.c{background:#FBF1EF;border:1px solid #E6C3BD;border-left:4px solid var(--clay);color:#6B2F28}
.note.c b{color:var(--clay)}
table.s{width:100%;border-collapse:separate;border-spacing:0;margin:20px 0;font-size:14.5px;
border:1px solid var(--hair);border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}
table.s th,table.s td{padding:12px 18px;text-align:left;border-bottom:1px solid var(--line2)}
table.s tr:last-child td{border-bottom:none}
table.s th{background:#F4F7F8;font-weight:800}
table.s td.n,table.s th.n{text-align:right;font-variant-numeric:tabular-nums}
.keep{color:var(--teal);font-weight:800}.drop{color:var(--clay);font-weight:800}.mn{color:var(--ochre);font-weight:800}
footer{max-width:1060px;margin:0 auto;padding:34px 32px 70px;color:var(--faint);font-size:12.5px;
text-align:center;border-top:1px solid var(--line2)}
footer code{background:#F1F4F6;padding:2px 7px;border-radius:5px;color:var(--sub)}
@media(max-width:660px){.hero h1{font-size:28px}.bar nav{display:none}main{padding-top:40px}}
@media print{.bar,.prog{display:none}main{padding-top:0}body{background:#fff}
.hero{background:#F5F9F9;margin:0}main>section{break-before:page;padding-top:6px}
figure,table.s{break-inside:avoid}h2,.take,.kick{break-after:avoid}}
"""

SCRIPT = ("const p=document.getElementById('prog');"
          "addEventListener('scroll',()=>{const h=document.documentElement;"
          "p.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';});")

HTML = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NDU Daily — 2026.07.03</title><style>{CSS}</style></head>
<body>
<div class="bar"><div class="b">NDU <i>Daily Report</i></div>
<nav><a href="#s1">① BH 판정</a><a href="#s2">② QCD 회수</a><a href="#s3">③ Mark 5</a>
<a href="#s4">④ Supported</a><a href="#s5">⑤ 문헌 검증</a><a href="#s6">⑥ 이슈·다음</a></nav>
<div class="d">2026.07.03 (금)</div></div>
<div class="prog" id="prog"></div>
<main>

<div class="hero">
<div class="kick">Daily Report · 2026년 7월 3일</div>
<h1>모양(기하) 축이 열렸다 — <em>Mark 5 달성</em>.<br>
기존 QCD 자산 재활용으로, 신규 계산 거의 없이.</h1>
<div class="lead">잠자던 QCD 데이터셋(DFT 62,880 full-relax + UMA 152만 SP 기계산분)을 회수해
제시 엔진에 skeleton 라이브러리를 연결. 5/5 시스템에서 icosahedron 신기록을 세우고,
Basin Hopping 직접탐색과의 1:1 판정(NiPdPt 5 replica)에서 동급 품질·1/100 비용을 확인.
밤에는 supported 확장 파일럿까지 4/4 성공 — Al₂O₃가 모양 선호를 뒤집는 것을 발견</div>
<div class="pills">
<span class="pill k">Mark 5 · geom_engine 달성</span>
<span class="pill k">multi-skeleton 5/5 신기록</span>
<span class="pill o">BH 5/5 판정 — 동급 품질 · 1/100 비용</span>
<span class="pill o">supported 4/4 (Mark 6 후보)</span>
<span class="pill c">신규 계산 ≈ 0 (QCD 재활용)</span>
</div>
<div class="meta">UMA-1p2-OMAT · NiPdPt/AuCuNi/IrNiPt/IrPdPtRh/AuCuNiPdPt 55 (+38) ·
A4500 직렬 무사고 · SLURM: BH blind 8시스템 진행 중</div>
</div>

<section id="s1">
<div class="kick">Head-to-head</div>
<h2><span class="num">1</span>BH 직접탐색 vs 제시 — NiPdPt 55 첫 완결 판정</h2>
<div class="take">제시(~15분)가 BH replica 평균(seed당 ~25시간)과 동급. BH가 찾은 정답 모티프(icosahedron)를 우리도 제시함</div>
<div class="duo">
<figure><img src="{IMG['ih']}" alt="NiPdPt ih proposal structure">
<figcaption>우리 제시 best 구조 (ih skeleton, −266.404 eV) — BH 상위 2개 seed가 찾은 것과 동일한 Mackay icosahedron 모티프</figcaption></figure>
<div>
<table class="s">
<tr><th>방법</th><th class="n">E (eV)</th><th class="n">비용</th></tr>
<tr><td>BH best (s4, ih)</td><td class="n">−266.972</td><td class="n">25 h × 5 seed</td></tr>
<tr><td>BH 평균 (5 replica)</td><td class="n">−266.39 ± 0.66</td><td class="n">〃</td></tr>
<tr><td><b>제시 (ih skeleton)</b></td><td class="n"><b>−266.404</b></td><td class="n keep">~15분</td></tr>
<tr><td>제시 (fcc, 기존)</td><td class="n">−266.31</td><td class="n">~10분</td></tr>
</table>
<ul class="p">
<li>제시가 BH 5개 중 <b>2개를 이기고 평균과 동률</b> — "싸게 BH 중앙값급" 스토리 그대로</li>
<li>GM 자체는 BH가 0.57 eV 우세 — 원인을 <b>pair-CE 해상도 한계</b>로 진단 완료 (탐색 부족 아님)</li>
</ul>
</div></div>
</section>

<section id="s2">
<div class="kick">Zero-cost harvest</div>
<h2><span class="num">2</span>QCD 데이터셋 회수 — 신규 계산 0으로 4건</h2>
<div class="take">과거 벤치마킹 자산에 UMA 계산이 전량 완료되어 있었음 — join만으로 검증·물성·라이브러리 확보</div>
<figure><img src="{IMG['flow']}" alt="QCD harvest flow">
<figcaption>QCD 자산 → 4개 추출물 → 검증 스택과 제시 엔진으로 흘러가는 구조. 전 과정 신규 계산 ≈ 0</figcaption></figure>
<table class="s">
<tr><th>추출물</th><th>핵심 수치</th><th>용도</th></tr>
<tr><td>isomer-ranking anchor (8원소 9,803개)</td><td>τ 0.772 · size 55 argmin 6/8 · miss 4.4 meV/atom (&lt;kT)</td><td>UMA가 skeleton 고를 자격</td></tr>
<tr><td>DFT 표면 페널티 서열</td><td>Au 1.49 &lt; Ag &lt; Cu &lt; Pd &lt; Pt &lt; Ni &lt; Rh &lt; Ir 5.75</td><td>세그리게이션 물리 근거</td></tr>
<tr><td>size-55 모티프 지도 (55원소)</td><td>ih 형성 14원소 (Ni·Cu·Ag·Co) · Au/Pt amorph — 문헌 재현</td><td>skeleton 후보 생성기</td></tr>
<tr><td>커리큘럼 정량 (decoration 7세트 교차검증)</td><td>zero-shot 광역 ρ 0.9 / 엘리트 판별은 refit 필수 (5–14 meV/atom)</td><td>543 SP refit의 근거</td></tr>
</table>
</section>

<section id="s3">
<div class="kick">Mark 5 · geometry axis</div>
<h2><span class="num">3</span>Multi-skeleton 제시 — 5/5 시스템 신기록</h2>
<div class="take">QCD skeleton + skeleton별 binary decoration 543 SP(2분) 재학습 = 임의 모양 위 ordering 제시. 전 시스템에서 fcc 제시를 경신</div>
<figure><img src="{IMG['geom']}" alt="geometry axis + ensemble + BH">
<figcaption>좌: skeleton별 제시 E − fcc 제시 (5/5 ih 승, 최대 IrPdPtRh −1.84 eV) ·
중: Boltzmann 모티프 점유 @800 K — ih 우세 83–100%, fcc/anti-Mackay 소수 공존 (ensemble 제시) ·
우: NiPdPt BH 대비 (1/100 비용)</figcaption></figure>
<ul class="p">
<li>size 38 이식 성공 (제시 vs 무작위 <b>−2.09 eV</b>) — 레시피가 size 무관</li>
<li>binary-only 학습 원칙 유지 — "새 모양 = binary 543 SP 한 번"으로 일반화</li>
<li>ensemble 지표 확립: 단일 GM이 아니라 <b>kT 창의 공존 모티프 비율</b>로 보고</li>
</ul>
</section>

<section id="s4">
<div class="kick">Toward Mark 6</div>
<h2><span class="num">4</span>Supported 확장 파일럿 — 4/4 성공 + 모양 선호 재편 발견</h2>
<div class="take">Al₂O₃ 위에서는 gas의 ih 선호가 fcc로 뒤집힘 (+0.55 eV) — 약결합 graphene은 ih 유지. support 대조쌍 시나리오 그대로</div>
<div class="duo">
<figure><img src="{IMG['al']}" alt="NiPdPt on Al2O3">
<figcaption>Al₂O₃ 위 제시 best (fcc skeleton, −2413.844 eV). 계면에 Pd/Pt 농축, Ni는 계면 회피 (예비 통계)</figcaption></figure>
<div>
<table class="s">
<tr><th>구성</th><th class="n">제시 min</th><th class="n">무작위 min</th><th class="n">Δ</th></tr>
<tr><td>graphene + ih</td><td class="n">−2481.247</td><td class="n">−2473.979</td><td class="n keep">−7.27</td></tr>
<tr><td>graphene + fcc</td><td class="n">−2481.211</td><td class="n">−2476.448</td><td class="n keep">−4.76</td></tr>
<tr><td>Al₂O₃ + ih</td><td class="n">−2413.296</td><td class="n">−2410.637</td><td class="n keep">−2.66</td></tr>
<tr><td><b>Al₂O₃ + fcc ★</b></td><td class="n"><b>−2413.844</b></td><td class="n">−2412.291</td><td class="n keep">−1.55</td></tr>
</table>
<div class="note o"><b>주의:</b> 계면 enrichment(Pd 1.8 / Pt 1.2 / Ni 0)는 contact 원자 5–7개 기준 —
통계 보강 후 Piccolo/Ismail (O-affinity 재편) 방향과 정성 비교 예정</div>
</div></div>
</section>

<section id="s5">
<div class="kick">Literature cross-check</div>
<h2><span class="num">5</span>Ruban 1999 전수 대조 — 표면 서열 4중 정합</h2>
<div class="take">8원소 28쌍 중 26쌍 일치, 정면 불일치 0 — 반직관 Cu–Pt 케이스까지 적중</div>
<figure><img src="{IMG['ruban']}" alt="Ruban comparison matrix">
<figcaption>Ruban 1999 DFT 세그리게이션 에너지 (빨강 = 표면행). 우리 서열과 부호가 어긋나는 셀은 적색 테두리 —
단 2셀, 둘 다 |E| ≤ 0.12 eV near-degenerate (Ruban 스스로 "세그리게이션 없음" 영역)</figcaption></figure>
<ul class="p">
<li>Ruban PRB 24×24 DFT 표에서 우리 쌍 전수 추출 (나머지 2쌍은 Ruban 자체가 near-zero "세그리게이션 없음")</li>
<li><b>Cu–Pt</b>: 표면에너지 순서를 거스르는 Pt-표면을 우리 모델도 예측 — <b>Calvo 2023 (EAM) 반론 방어 카드</b></li>
<li>표면 서열이 4중 정합: PairCE(UMA) ↔ QCD a_surf(DFT mono) ↔ Ruban(DFT 합금) ↔ Kristoffersen(DFT quinary)</li>
</ul>
</section>

<section id="s6">
<div class="kick">Honest report & next</div>
<h2><span class="num">6</span>이슈 · 다음 단계</h2>
<div class="note c"><b>틀린 예측 1건:</b> IrPdPtRh는 구성원소에 ih 형성자가 없어 anti-Mackay 승을 예측했으나
실제는 ih 승 (0.14 eV 차 공존). → mono 모티프 지도는 <b>후보 생성기이지 합금 오라클이 아님</b>
(합금은 size mismatch로 ih 안정화 — 문헌 정합). 그 외: supported CE validity ρ 0.11–0.37로 약함
(예상된 리스크, SP 재채점이 보정) · bond 회귀 분석 1건 방법 결함으로 폐기</div>
<ul class="p">
<li><b>BH blind test 8시스템</b> (54696/54701 실행 중, 며칠) — 제시값 전부 사전 등록 완료</li>
<li><b>Supported 후속</b>: 계면 통계 보강 + 문헌 정성 비교 → Mark 6 판단</li>
<li><b>DFT 검증 패키지</b> 38 구조 준비 완료 — INCAR 검토 후 자원 열리면 제출</li>
</ul>
</section>

</main>
<footer>NDU · MLIP 기반 nanocluster 구조 제시 · Generated 2026-07-04 00:20 (7/3 세션분) ·
<code>reports/20260703_20260709/20260703.html</code> · meeting-report skill</footer>
<script>{SCRIPT}</script>
</body></html>
"""

OUT.write_text(HTML)
print("saved:", OUT, f"({len(HTML)//1024} KB)")
