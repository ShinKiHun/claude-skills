# -*- coding: utf-8 -*-
"""paper-report 공용 폰트 헬퍼.

- HTML: NanumSquare(R/B/EB)를 @font-face에 base64로 임베드 → 자체완결, 어느 브라우저서도 나눔스퀘어.
- matplotlib figure: NanumSquare _fix2를 등록하되, **Malgun Gothic을 1순위**로 둔다.
  이유: NanumSquare ttf는 mpl에서 space 글리프가 깨져(공백이 ▢로 렌더) → Malgun 우선.
  (유저 DRM 리포트에서 검증된 회피책. 그림 한글은 Malgun로 렌더되며 나눔스퀘어와 결이 비슷.)
  HTML(브라우저)에는 이 버그가 없어 진짜 NanumSquare가 나온다.

폰트 파일: ../assets/fonts/ (Naver NanumSquare, 무료·재배포 허용).
"""
import base64
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# matplotlib 등록용(공백버그 회피본) / HTML 임베드용(raw)
_MPL_FILES = ["NanumSquareR_fix2.ttf", "NanumSquareB_fix2.ttf", "NanumSquareEB_fix2.ttf"]
_HTML_WEIGHTS = [(400, "NanumSquareR.ttf"), (700, "NanumSquareB.ttf"), (800, "NanumSquareEB.ttf")]

MPL_FONT_STACK = ["Malgun Gothic", "NanumSquare", "DejaVu Sans"]


def register_mpl():
    """NanumSquare _fix2 를 matplotlib에 등록하고 폰트 스택을 돌려준다.

    반환: font.family 로 쓸 리스트(Malgun 우선). rcParams 설정은 호출자가.
    """
    try:
        from matplotlib import font_manager as fm
    except ImportError:
        return MPL_FONT_STACK
    for name in _MPL_FILES:
        p = FONTS_DIR / name
        if p.exists():
            try:
                fm.fontManager.addfont(str(p))
            except Exception:
                pass
    return list(MPL_FONT_STACK)


def font_faces_css():
    """NanumSquare R/B/EB를 base64 @font-face로 임베드하는 CSS 문자열.

    폰트 파일이 없으면 빈 문자열(→ 시스템 폰트 스택으로 폴백).
    """
    faces = []
    for weight, fname in _HTML_WEIGHTS:
        p = FONTS_DIR / fname
        if not p.exists():
            continue
        b64 = base64.b64encode(p.read_bytes()).decode()
        faces.append(
            "@font-face{font-family:'NanumSquare';font-style:normal;"
            f"font-weight:{weight};font-display:swap;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}"
        )
    return "\n".join(faces)
