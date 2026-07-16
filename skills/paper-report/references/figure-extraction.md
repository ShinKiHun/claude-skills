# Figure Extraction (PDF → PNG)

`scripts/extract_figures.py` (PyMuPDF/fitz) 사용. 3개 모드.

## 왜 렌더+크롭인가
계산촉매 논문의 figure 상당수가 **벡터 그래픽**(반응경로 다이어그램·scheme·에너지도·구조모식도).
벡터는 PDF에 raster 이미지로 안 박혀 있어 `get_images()` 임베디드 추출로는 **놓친다**.
→ 페이지를 렌더한 뒤, 모델이 figure 영역을 지정해 **크롭**하는 방식이 주력.
임베디드 추출은 SEM/TEM/사진 같은 단일 raster 이미지를 원본 해상도로 뽑을 때만 보조로.

## 모드 1: dump-pages
```
python extract_figures.py --dump-pages <paper.pdf> <WORK> --dpi 200
```
- `<WORK>/pages/pNN.png` : 각 페이지 렌더(모델이 Read로 보고 figure 선별).
- `<WORK>/pages_text.json` : 페이지별 본문 텍스트(figure 텍스트 검색·캡션 확인·수치 인용).
- `<WORK>/pages_meta.json` : 페이지 크기(pt) 등.
- DPI 150~200 이면 비전 판독 충분. 크롭용 고해상은 4단계에서 따로.

## 모드 2: crop (주력)
```
python extract_figures.py --crop <WORK>/figures_spec.json <WORK> --dpi 300
```
`figures_spec.json` = list of:
```json
{"pdf":"paper.pdf","page":3,"fig_id":"zhu_fig2",
 "caption":"Fig. 2. …","bbox_frac":[x0,y0,x1,y1]}
```
- **bbox_frac** = 페이지 대비 0~1 좌표, **원점 좌상단**(fitz 규약). `[좌, 상, 우, 하]`.
- 좌표는 렌더된 페이지 PNG를 보고 눈대중 → 크롭 결과 Read로 확인 → 잘리면 조정.
- 캡션 텍스트를 figure 안에 포함할지는 판단(보통 포함하면 자체설명적).
- 스크립트가 bbox를 0~1로 클램프하고 정렬하므로 좌우/상하 순서 뒤바뀌어도 안전.
- 고DPI(300) 재렌더에서 크롭 → 인쇄·확대에도 선명.

## 모드 3: embedded (보조)
```
python extract_figures.py --embedded <paper.pdf> <WORK> --min-px 200
```
- `page.get_images(full=True)` → xref별 원본 pixmap 저장(`<WORK>/embedded/pNN_x###.png`).
- `--min-px` 로 로고·아이콘·조각 이미지 필터(가로·세로 둘 다 이상).
- CMYK/alpha 는 자동 RGB 변환.
- 주의: 한 figure가 여러 raster 조각으로 쪼개져 있을 수 있음(패널 분리). 그럴 땐 crop이 낫다.

## 함정
- **벡터 figure**: embedded로 안 나옴 → crop 사용.
- **캡션-그림 연결**: 텍스트 레이어만으론 어려움 → 모델 비전으로 페이지 보고 판단.
- **좌표계**: fitz는 좌상단 원점(y 아래로 증가). bbox_frac도 동일.
- **CMYK**: 인쇄용 PDF는 CMYK 이미지 → embedded 모드가 RGB 변환 처리.
- **스캔 PDF**: 텍스트 레이어 없으면 pages_text가 빈다 → 비전으로만 진행.
- 의존성: `pip install pymupdf` 만 필요(그 외 stdlib).
