#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper-report: report.json + figures -> 자체완결 HTML.

meeting-report/example_builder.py 의 CSS 디자인 시스템을 그대로 이식하되,
1회성 하드코딩 아티팩트가 아니라 report.json 을 받는 파라미터화 제너레이터로 재작성.
figure는 data-URI로 인라인(자체완결) + 원본 PNG는 figures/ 에 그대로 남김("png + html").

report.json 스키마:
{
  "title": "…(결론형)…",            # hero h1 (HTML em 태그 허용)
  "subtitle": "…",                    # hero lead
  "kicker": "Preliminary Survey · 2026-07-17",
  "brand": "cu-MOF",
  "date": "2026-07-17",
  "pills": [{"text":"…","cls":"k"}],   # cls: k(teal)|o(ochre)|c(clay)
  "meta": "…hero 하단 메타…",
  "sections": [
    {
      "id": "s1", "num": 1, "nav": "① 개념",
      "kicker": "Concept", "title": "…",
      "take": "…한 줄 결론…",
      "body_html": "<ul class='p'><li>…</li></ul>",   # 자유 HTML (신뢰 입력)
      "figure": {"src":"figures/fig1.png","caption":"…","credit":"Fig.2 of DOI:10…"},
      "figures": [ … ],                # 복수 figure (figure 대신/추가)
      "layout": "duo",                 # duo면 figure|body 좌우 배치
      "table_html": "<table class='s'>…</table>"
    }
  ],
  "refs": ["Zhu et al., Nat. Commun. 2020 — 10.1038/s41467-020-19438-w", …],
  "footer": "…"
}

사용:
  python build_report.py report.json <figures_base_dir> out.html
  (figure src는 figures_base_dir 기준 상대경로 또는 절대경로)
"""
import base64
import html as _html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _fonts  # noqa: E402

# ── meeting-report example_builder.py 에서 이식한 CSS (팔레트/컴포넌트 동일) ──
# 폰트: NanumSquare 임베드(자체완결) + 자간(letter-spacing) 조정. 폴백은 Malgun/Noto.
CSS = """
:root{--ink:#1B2733;--ink2:#33414F;--sub:#6B7682;--faint:#9AA4AE;
--hair:#E5E9ED;--line2:#EFF2F5;--bg:#FAFBFC;--card:#FFFFFF;
--teal:#2E6F77;--teald:#23565C;--ochre:#B5872E;--clay:#B0564C;--blue:#3F6E9A;
--shadow:0 1px 2px rgba(27,39,51,.04),0 8px 28px rgba(27,39,51,.07);}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'NanumSquare','Malgun Gothic','Noto Sans KR','Apple SD Gothic Neo',
-apple-system,BlinkMacSystemFont,system-ui,sans-serif;color:var(--ink);background:var(--bg);
line-height:1.66;letter-spacing:-.01em;-webkit-font-smoothing:antialiased;
word-break:keep-all;overflow-wrap:break-word;}
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
.hero .lead{margin-top:22px;font-size:17px;color:var(--ink2);max-width:820px;line-height:1.72}
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
figcaption .credit{color:var(--faint);font-size:12px}
.duo{display:grid;grid-template-columns:1fr 1.6fr;gap:16px;align-items:start}
@media(max-width:700px){.duo{grid-template-columns:1fr}}
ul.p{list-style:none;margin:16px 0}
ul.p li{position:relative;padding:6px 0 6px 24px;font-size:15.5px;color:var(--ink2)}
ul.p li::before{content:"";position:absolute;left:3px;top:14px;width:7px;height:7px;border-radius:50%;background:var(--teal)}
ul.p li b{color:var(--teald)}
p.tx{margin:14px 0;font-size:15.5px;color:var(--ink2)}
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
.refs{max-width:1060px;margin:0 auto;padding:10px 32px 0;font-size:12.5px;color:var(--sub)}
.refs ol{margin:8px 0 0 20px}.refs li{margin:5px 0}
img.zoom{cursor:zoom-in;transition:filter .15s}
figure:hover img.zoom{filter:brightness(.97)}
/* 라이트박스: figure 클릭 시 확대 */
#lb{position:fixed;inset:0;z-index:200;display:none;align-items:center;justify-content:center;
background:rgba(15,20,28,.86);backdrop-filter:blur(3px);cursor:zoom-out;padding:24px}
#lb.on{display:flex}
#lb img{max-width:96vw;max-height:92vh;width:auto;height:auto;border-radius:8px;
box-shadow:0 12px 48px rgba(0,0,0,.5);background:#fff;cursor:default}
#lb .x{position:fixed;top:16px;right:24px;color:#fff;font-size:30px;font-weight:700;
cursor:pointer;line-height:1;opacity:.85;font-family:system-ui,sans-serif}
#lb .x:hover{opacity:1}
#lb .cap{position:fixed;bottom:16px;left:0;right:0;text-align:center;color:#E5E9ED;
font-size:13px;padding:0 24px}
@media(max-width:660px){.hero h1{font-size:28px}.bar nav{display:none}main{padding-top:40px}}
@media print{.bar,.prog,#lb{display:none}main{padding-top:0}body{background:#fff}
.hero{background:#F5F9F9;margin:0}main>section{break-before:page;padding-top:6px}
figure,table.s{break-inside:avoid}h2,.take,.kick{break-after:avoid}}
"""

SCRIPT = ("const p=document.getElementById('prog');"
          "addEventListener('scroll',()=>{const h=document.documentElement;"
          "p.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';});"
          # 라이트박스: figure 이미지 클릭 → 확대, 배경/×/ESC 로 닫기
          "const lb=document.getElementById('lb'),li=document.getElementById('lbimg'),"
          "lc=document.getElementById('lbcap');"
          "function closeLb(){lb.classList.remove('on');}"
          "document.querySelectorAll('img.zoom').forEach(im=>{im.addEventListener('click',()=>{"
          "li.src=im.src;const f=im.closest('figure'),c=f&&f.querySelector('figcaption');"
          "lc.textContent=c?c.textContent:'';lb.classList.add('on');});});"
          "lb.addEventListener('click',e=>{if(e.target!==li)closeLb();});"
          "addEventListener('keydown',e=>{if(e.key==='Escape')closeLb();});")


def b64_img(path):
    data = Path(path).read_bytes()
    suffix = Path(path).suffix.lower().lstrip(".")
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix or "png"
    return f"data:image/{mime};base64," + base64.b64encode(data).decode()


def resolve(src, base):
    p = Path(src)
    if not p.is_absolute():
        p = Path(base) / src
    return p


def esc(s):
    return _html.escape(s or "", quote=True)


def render_figure(fig, base):
    src = resolve(fig["src"], base)
    if not src.exists():
        raise FileNotFoundError(f"figure 없음: {src}")
    uri = b64_img(src)
    cap = fig.get("caption", "")
    credit = fig.get("credit", "")
    cred_html = f" <span class='credit'>({esc(credit)})</span>" if credit else ""
    cap_html = f"<figcaption>{esc(cap)}{cred_html}</figcaption>" if (cap or credit) else ""
    alt = esc(fig.get("alt", cap[:80]))
    return f'<figure><img class="zoom" src="{uri}" alt="{alt}">{cap_html}</figure>'


def render_section(s, base):
    figs = s.get("figures")
    if not figs and s.get("figure"):
        figs = [s["figure"]]
    figs = figs or []
    fig_html = "".join(render_figure(f, base) for f in figs)
    body = s.get("body_html", "")
    table = s.get("table_html", "")
    num = s.get("num", "")
    kicker = f'<div class="kick">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
    take = f'<div class="take">{esc(s["take"])}</div>' if s.get("take") else ""

    if s.get("layout") == "duo" and figs:
        # figure(들) | (body+table) 좌우
        right = body + table
        inner = f'<div class="duo"><div>{fig_html}</div><div>{right}</div></div>'
    else:
        inner = fig_html + body + table

    return (f'<section id="{esc(s.get("id",""))}">{kicker}'
            f'<h2><span class="num">{esc(str(num))}</span>{s.get("title","")}</h2>'
            f'{take}{inner}</section>')


def render_pills(pills):
    out = []
    for p in pills or []:
        cls = p.get("cls", "k")
        out.append(f'<span class="pill {esc(cls)}">{esc(p.get("text",""))}</span>')
    return "".join(out)


def render_nav(sections):
    out = []
    for s in sections:
        label = s.get("nav") or s.get("title", "")[:14]
        out.append(f'<a href="#{esc(s.get("id",""))}">{esc(label)}</a>')
    return "".join(out)


def render_refs(refs):
    if not refs:
        return ""
    items = "".join(f"<li>{esc(r)}</li>" for r in refs)
    return f'<div class="refs"><b>참고문헌 (DOI)</b><ol>{items}</ol></div>'


def build(report, base):
    sections = report.get("sections", [])
    title = report.get("title", "")           # h1: em 태그 허용 → 이스케이프 안 함
    subtitle = report.get("subtitle", "")
    kicker = report.get("kicker", "")
    brand = report.get("brand", "Report")
    date = report.get("date", "")
    meta = report.get("meta", "")
    doc_title = report.get("doc_title") or _html.unescape(
        title.replace("<em>", "").replace("</em>", "").replace("<br>", " "))

    nav = render_nav(sections)
    pills = render_pills(report.get("pills"))
    body_sections = "".join(render_section(s, base) for s in sections)
    footer = report.get("footer", f"{esc(brand)} · paper-report skill")

    font_css = _fonts.font_faces_css()
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(doc_title)}</title><style>{font_css}
{CSS}</style></head>
<body>
<div class="bar"><div class="b">{esc(brand)} <i>Report</i></div>
<nav>{nav}</nav>
<div class="d">{esc(date)}</div></div>
<div class="prog" id="prog"></div>
<main>
<div class="hero">
<div class="kick">{esc(kicker)}</div>
<h1>{title}</h1>
<div class="lead">{esc(subtitle)}</div>
<div class="pills">{pills}</div>
<div class="meta">{esc(meta)}</div>
</div>
{body_sections}
</main>
{render_refs(report.get("refs"))}
<footer>{esc(footer)}</footer>
<div id="lb"><span class="x">&times;</span><img id="lbimg" alt=""><div class="cap" id="lbcap"></div></div>
<script>{SCRIPT}</script>
</body></html>
"""


def main():
    if len(sys.argv) < 4:
        sys.exit("usage: build_report.py <report.json> <figures_base_dir> <out.html>")
    report_path, base, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    html = build(report, base)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"[build_report] saved: {out_path}  ({len(html)//1024} KB, {len(report.get('sections',[]))} sections)")


if __name__ == "__main__":
    main()
