---
name: drm-blender
description: Render DRM (dry reforming) atomic structures — CH4/CO2 activation on Ni / Pt-Ni / Pt(111) metal slabs and CeO2 / LaDC oxide supports, plus metal nanoclusters — as publication-ready space-filling figures via headless Blender 5.1 (EEVEE). Encodes the approved DRM palette (steel Ni, light-silver Pt, gray Ce, teal La, red O, charcoal C, white H, orange highlight for reacting species) and the render pipeline (tilt40, edge-fill, localized-feature centering, IS/TS/FS fixed-camera reaction panels). Use whenever rendering DRM structure sets (vasp / ASE .traj / reactions JSON) for paper figures or benchmarks. Korean triggers — "DRM 렌더", "DRM 방식으로 렌더", "블렌더 구조 렌더", "IS/TS/FS 렌더".
---

# DRM_blender — 원자구조 렌더 스킬

계산촉매 DRM 프로젝트의 **승인된 블렌더 렌더 방식**. 블렌더 프로젝트 루트의 `scripts/` 에 구현돼 있다. 루트 기준으로 실행한다.
(루트 경로는 각자 환경에 맞게. 이 저장소는 public 이라 절대경로를 적지 않는다.)

## 환경
- Blender: `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`
- Python: ASE 필요. import 애드온 = `bl_ext.blender_org.atomic_blender_pdb_xyz` (space-filling)
- 엔진 EEVEE(GPU), 프레임당 별도 프로세스(재질 오염 방지), Windows 콘솔은 `PYTHONIOENCODING=utf-8`

## 팔레트 (단일 소스 = `scripts/palette.py`)
색 바꾸려면 **palette.py 만** 고친다. 렌더러가 거기서 읽음. (io_mesh_atomic 재질명=원소 풀네임, 부분일치)

| 원소 | RGB | 용도 |
|------|-----|------|
| Oxygen | 0.78, 0.12, 0.10 | 빨강 (격자 O + 흡착 O 공통) |
| Carbon | 0.20, 0.20, 0.22 | charcoal |
| Hydrogen | 0.92, 0.92, 0.95 | 흰 |
| Cerium | 0.50, 0.50, 0.53 | 어두운 회색 |
| Lanthanum | 0.42, 0.66, 0.62 | teal (도판트) |
| Nickel | 0.40, 0.50, 0.62 | steel (Ce와 분리) |
| Platinum | 0.80, 0.77, 0.72 | 밝은 은 (Ni와 분리) |
| Fluorine | 1.00, 0.55, 0.10 | **강조 마커**(주황). 반응 중 CO2/흡착종 원자를 'F'로 라벨링하면 이 색 |
| Gold/Silver/Copper/Cobalt/Palladium/Iron | (클러스터 금속, palette.py 참조) | 나노입자용 |

- 재질: Metallic 0, Roughness 0.55, Specular 0.15 (무광). 클러스터는 살짝 광택 가능.
- 팔레트 실험: 환경변수 `OVR_<원소>="r,g,b"` 로 임시 오버라이드 가능.

## 렌더 규칙 (핵심)
- **시점 tilt40** = 방향벡터 `(0, -0.77, 0.64)` (옆면+40° 내려봄). 정면/옆모습은 `(0, -0.99, 0.12)`.
- **space-filling 공만** (결합 막대 절대 금지), smooth shading, 다크 회색 배경.
- **edge-fill**: 주기 슬랩만 3×3 복제해 가장자리 이빨빠짐 제거. **국소 구조(Pt 섬, 금속 클러스터, 흡착종)는 복제 안 하고** 정수 격자 이동으로 슬랩 중앙에 배치. hex 셀 대응 = `n = round(solve([a_xy,b_xy], target-feat))`.
  - 슬랩 원소 판정: 금속표면 Ni(111)/Pt-Ni → 슬랩=Ni (Pt는 국소 섬); Pt(111) → 슬랩=Pt; 산화물 → 슬랩=Ce/La/O(격자).
  - 흡착 O vs 격자 O: 금속표면은 O 전부 흡착(격자O 없음); 산화물은 C에서 1.6Å 이내 O만 흡착으로 취급.
- **프레이밍(중요)**: 흡착물이 주인공 → **xy 중심 = 흡착종(C/H/O) 무게중심**(Pt섬 무게중심 아님), **cz = 국소구조(Pt섬+흡착) z-중심**(전체 원자 평균 아님 — 그러면 흡착물이 위로 뜨고 아래 여백 생김). ortho 목표: Ni(111) 16 / Pt-Ni 18 / Pt(111) 16 / 산화물 22.
- **IS/TS/FS 반응경로**: 같은 반응이면 **카메라 고정**. 단 IS 하나가 아니라 **IS/TS/FS 흡착물 위치 union**으로 xy중심·cz 잡고, ortho는 세 상태 흡착물이 다 들어오게 자동확장(`max(목표, 2*최대변위+여백)`). 반응 중 원자가 떨어져나가도 안 잘림. 3패널로 조립.
- **강조(옵션)**: 반응 중 CO2 등 특정 분자를 추적해 그 원자를 'F'로 라벨 → 주황. index 소스(json의 iC/iO)나 C-최근접 O로 특정. CH4 dehydrogenation 등 일반 흡착종은 강조 없이 자연색.
- 해상도 800(기본). 논문 최종은 1600~2000으로 상향 가능.

## 스크립트 (scripts/)
- `render_frame_gray_eevee.py` — **1프레임 렌더 코어** (palette.py 읽음). 인자: `<xyz> <png> <cx> <cy> <cz> <ortho> [vx vy vz]`. 좌표 복원(importer 원점이동) 내장.
- `render_ch4_final.py` — 정리된 `blender_structures/`(Ni/PtNi/Pt111 각 반응 IS/TS/FS + 단독흡착 + clean) 일괄. 반응 카메라 고정 + 개요/시트.
- `render_ch4_path.py` — 옛 레이아웃(IS__*/FS__*/path/*_TS) 반응경로.
- `render_co2_final.py` — **CO2 트랙 확정 런처** (BLENDER_MANIFEST.csv 기반). P1=NEB IS/TS/FS 반응패널, P2=bent/linear 개별+컨택트시트. CO2는 CSV `idx_C/O1/O2`로 특정(거리 X), MIC로 분자 연속화(PBC 조각남 방지), 상태별 격자중앙정렬, Pt섬까지 ortho fit. bare ortho16/Pt28.
- `render_drm_isfsts.py` — (구) CO2 activation IS/TS/FS. 거리기반 O탐지라 FS 먼 O 틀림 → 신규는 render_co2_final.py 사용.
- `render_drm_batch.py` / `render_drm_json.py` — vasp 무더기 / 반응 DB(JSON, ASE db InputFile) 벤치마크 + 컨택트시트.
- `render_co_events.py` — MD traj CO 형성 이벤트 시계열(추적분자 강조).
- `render_wet_bench.py` — MLIP 벤치마크(동일계 여러 방법, 같은 카메라 top/front).
- `render_cluster_frame_eevee.py` / `render_cluster_md_gif.py` — 금속 나노클러스터 정적/MD GIF.
- `extract_xyz.py` / `render_traj_gray_eevee.py` — 슬랩 MD traj → GIF.

## DRM 함정 (반드시)
1. **C\* 노드 = 단독 C** (`isolated_C.vasp` / `single_C_*.vasp`, 조성 C1). `dehydro__CH_to_C/FS.vasp`는 C+H 공흡착이라 6c 끝점이지 노드 아님. **CO\* 노드 = `oxid__C_O_to_CO/FS.vasp`** (단독 CO).
2. **Pt(111)은 검증된 3반응만** (dehydro__CH4_to_CH3, dehydro__CH_to_C, oxid__CH_O_to_CHO). 다른 Pt(111) 숫자/구조 쓰지 말 것.
3. 원자수 sanity: Ni계 397~401, Pt-Ni계 437~441, Pt(111)계 65~69. 벗어나면 잘못 집은 것.

## 작업 순서 (권장)
1. 새 구조셋 받으면 **먼저 전수 검증**: 경로 존재·조성(ads)·원자수 대조, MISSING 0 확인.
2. 표면 종류·Pt 배치(섬 vs 오버레이어)·격자셀(직교 vs hex) 확인 → 슬랩/국소 판정.
3. 대표 1~2개 테스트 렌더로 프레이밍·색 확인 후 전체 배치(백그라운드).
4. 완료 후 3축 검증(실행·원문대조·반증)으로 보고. 컨택트시트/개요로 한눈보기 제공.
5. 결과는 `PtNiLaDC/<세트명>/` 아래 정리. 새로 갈 땐 기존은 `_backup_old/`로.

---

## 고칠 때 — `CHANGELOG.md` 에 날짜별로 남긴다

이 스킬은 여러 Claude 세션이 각자 프로젝트에서 돌아가며 고친다.
**바꾸기 전에 `CHANGELOG.md` 를 먼저 읽어라** — 왜 지금 모양인지, 이미 시도했다 되돌린 게
뭔지 거기 있다. **고쳤으면 맨 위에 항목을 추가하고 커밋해라**
(날짜 / 프로젝트 폴더명·모델명 / 무엇·왜·검증). 형식은 그 파일 머리말에 있다.
