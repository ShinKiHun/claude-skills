#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper-report: PDF figure 추출 (PyMuPDF/fitz).

3개 모드:
  --dump-pages   : PDF 각 페이지를 PNG로 렌더 (모델 비전 입력용) + 페이지 텍스트 dump
  --crop         : figures.json(모델이 지정한 bbox) 대로 고DPI 렌더에서 크롭 → figure PNG
  --embedded     : 페이지에 박힌 raster 이미지 원본을 크기필터로 추출 (고해상 단일 이미지 figure용)

계산촉매 논문은 벡터 figure(반응경로·scheme·에너지도)가 많아 --crop 이 주력.
--embedded 는 SEM/TEM/사진 등 단일 raster 이미지일 때 원본 해상도로 뽑는 보조수단.

사용 예:
  python extract_figures.py --dump-pages paper.pdf out/ --dpi 200
  python extract_figures.py --crop out/figures.json out/ --dpi 300
  python extract_figures.py --embedded paper.pdf out/ --min-px 200
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("ERROR: PyMuPDF 필요. 설치: pip install pymupdf")


def dump_pages(pdf_path, outdir, dpi):
    """각 페이지를 PNG로 렌더하고, 페이지 텍스트를 pages_text.json으로 저장."""
    pdf_path = Path(pdf_path)
    outdir = Path(outdir)
    pages_dir = outdir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    texts = {}
    saved = []
    for i, page in enumerate(doc):
        n = i + 1
        pix = page.get_pixmap(dpi=dpi)
        png = pages_dir / f"p{n:02d}.png"
        pix.save(png)
        saved.append(str(png))
        texts[n] = page.get_text()
        # 페이지 크기(pt)도 기록 — crop 시 bbox_frac 환산에 사용
    meta = {
        "pdf": str(pdf_path),
        "n_pages": doc.page_count,
        "dpi": dpi,
        "page_size_pt": [list(doc[i].rect[2:]) for i in range(doc.page_count)],
    }
    (outdir / "pages_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "pages_text.json").write_text(json.dumps(texts, ensure_ascii=False, indent=2), encoding="utf-8")
    doc.close()
    print(f"[dump-pages] {len(saved)} pages -> {pages_dir}  (dpi={dpi})")
    print(f"[dump-pages] text -> {outdir/'pages_text.json'}  | meta -> {outdir/'pages_meta.json'}")
    for s in saved:
        print("  ", s)


def crop(spec_path, outdir, dpi):
    """figures.json 의 bbox_frac 대로 고DPI 렌더에서 크롭.

    figures.json 스키마 (list of):
      {"pdf": "paper.pdf", "page": 3, "fig_id": "fig2",
       "caption": "Figure 2. ...", "bbox_frac": [x0,y0,x1,y1]}
    bbox_frac = 페이지 대비 0~1 좌표, 원점 좌상단(fitz 규약).
    """
    spec_path = Path(spec_path)
    outdir = Path(outdir)
    figures_dir = outdir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    items = json.loads(spec_path.read_text(encoding="utf-8"))
    if isinstance(items, dict):  # {"figures":[...]} 도 허용
        items = items.get("figures", [])

    # PDF 캐시 (같은 파일 반복 open 방지)
    docs = {}
    def get_doc(p):
        p = str(Path(p))
        if p not in docs:
            docs[p] = fitz.open(p)
        return docs[p]

    made = []
    for it in items:
        pdf = it["pdf"]
        page_no = int(it["page"]) - 1
        fig_id = it["fig_id"]
        fr = it["bbox_frac"]
        doc = get_doc(pdf)
        page = doc[page_no]
        W, H = page.rect.width, page.rect.height
        x0, y0, x1, y1 = fr
        # 안전 클램프 + 정렬
        x0, x1 = sorted((max(0.0, min(1.0, x0)), max(0.0, min(1.0, x1))))
        y0, y1 = sorted((max(0.0, min(1.0, y0)), max(0.0, min(1.0, y1))))
        clip = fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
        if clip.is_empty or clip.width < 2 or clip.height < 2:
            print(f"  ! skip {fig_id}: bbox 너무 작음 {fr}")
            continue
        pix = page.get_pixmap(dpi=dpi, clip=clip)
        out = figures_dir / f"{fig_id}.png"
        pix.save(out)
        made.append((fig_id, str(out), pix.width, pix.height))

    for p in docs.values():
        p.close()

    print(f"[crop] {len(made)} figures -> {figures_dir}  (dpi={dpi})")
    for fid, path, w, h in made:
        print(f"   {fid}: {w}x{h}px  {path}")


def extract_embedded(pdf_path, outdir, min_px):
    """페이지에 박힌 raster 이미지 원본 추출 (크기필터로 로고/조각 제거)."""
    pdf_path = Path(pdf_path)
    outdir = Path(outdir)
    emb_dir = outdir / "embedded"
    emb_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    seen = set()
    made = []
    for i, page in enumerate(doc):
        n = i + 1
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                pix = fitz.Pixmap(doc, xref)
            except Exception as e:
                print(f"  ! p{n} xref{xref}: {e}")
                continue
            # CMYK / alpha → RGB 변환
            if pix.n - pix.alpha >= 4 or pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            if pix.width < min_px or pix.height < min_px:
                pix = None
                continue
            out = emb_dir / f"p{n:02d}_x{xref}.png"
            pix.save(out)
            made.append((str(out), pix.width, pix.height))
            pix = None
    doc.close()
    print(f"[embedded] {len(made)} images (>= {min_px}px) -> {emb_dir}")
    for path, w, h in made:
        print(f"   {w}x{h}px  {path}")


def main():
    ap = argparse.ArgumentParser(description="paper-report PDF figure 추출")
    sub = ap.add_subparsers(dest="mode", required=True)

    p1 = sub.add_parser("dump-pages", help="페이지 PNG 렌더 + 텍스트 dump")
    p1.add_argument("pdf")
    p1.add_argument("outdir")
    p1.add_argument("--dpi", type=int, default=200)

    p2 = sub.add_parser("crop", help="figures.json bbox 대로 크롭")
    p2.add_argument("spec")
    p2.add_argument("outdir")
    p2.add_argument("--dpi", type=int, default=300)

    p3 = sub.add_parser("embedded", help="박힌 raster 이미지 원본 추출")
    p3.add_argument("pdf")
    p3.add_argument("outdir")
    p3.add_argument("--min-px", type=int, default=200)

    # SKILL 문서상 '--dump-pages/--crop/--embedded' 형태도 받도록 첫 토큰의 '--' 제거
    argv = sys.argv[1:]
    if argv and argv[0] in ("--dump-pages", "--crop", "--embedded"):
        argv[0] = argv[0].lstrip("-")
    args = ap.parse_args(argv)

    if args.mode == "dump-pages":
        dump_pages(args.pdf, args.outdir, args.dpi)
    elif args.mode == "crop":
        crop(args.spec, args.outdir, args.dpi)
    elif args.mode == "embedded":
        extract_embedded(args.pdf, args.outdir, args.min_px)


if __name__ == "__main__":
    main()
