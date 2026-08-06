---
name: xfer
description: 이 CLAUDE 세션이 도는 서버(LOCAL)와 원격 관문 서버(REMOTE, <USER>@<HOST>:<PORT>) 사이 폴더를 scp/rsync 로 전송. "LOCAL 의 A 를 REMOTE 의 B 하위로 보내", "REMOTE 의 B 를 LOCAL 의 A 하위로 가져와" 처럼 말하면 방향·포트·실행위치를 자동으로 맞춰 명령을 생성한다. 다른 사용자 계정으로 보내는 케이스 포함. 두 서버 간 push/pull/백업에 사용.
---

# xfer — 두 서버 간 파일 전송 (scp/rsync)

이 CLAUDE 세션이 도는 서버(**LOCAL**)와 원격 서버(**REMOTE**) 사이 폴더 전송을 한 줄 요청으로 처리한다.

## 설정값 (각 환경에서 채워 사용)

| 변수 | 뜻 |
|------|-----|
| `<HOST>` | 원격 서버(관문/gateway) 주소 (IP 또는 hostname) |
| `<PORT>` | 그 서버의 SSH 포트 |
| `<USER>` | 내 계정명 |
| LOCAL | 이 CLAUDE 세션이 도는 서버 (관문 뒤에 숨어있는 내부 머신) |

> 실제 값(HOST/PORT/USER)은 각자 로컬 환경 파일(프로젝트 CLAUDE.md 등)에만 두고, 이 스킬 파일엔 넣지 않는다.

## 서버 토폴로지 (방향 헷갈리지 말 것)

- **REMOTE(`<HOST>`) = 외부 관문. LOCAL = 실제 작업 머신, 관문 뒤에 숨어있음.**
- ⚠️ **scp/rsync 는 방향 무관 항상 LOCAL(이 세션)에서 실행.** REMOTE 는 LOCAL 주소를 모르므로 REMOTE 에서 칠 수 없음.
- ⚠️ **scp 포트 플래그는 `-P`(대문자). `-p`(소문자)는 timestamp/권한 보존 옵션** — `-p <PORT>` 로 쓰면 `<PORT>` 가 소스 파일명으로 먹혀 실패(포트는 기본 22 로 접속). ssh 는 반대로 `-p`(소문자)가 포트.
- LOCAL 의 `/home` 이 REMOTE 와 NFS 공유가 아니면 진짜 네트워크 복사.

## 절차

### 1. 요청에서 방향·경로 파악
- "LOCAL 의 A 를 REMOTE 의 B 하위로 보내/넘겨" → **push (LOCAL→REMOTE)**. local source=A, remote dest parent=B
- "REMOTE 의 B 를 LOCAL 의 A 하위로 가져와/받아" → **pull (REMOTE→LOCAL)**. remote source=B, local dest parent=A
- 폴더 이름만 주어지면 프로젝트 관례로 추정하되, **확신 없으면 절대경로를 되물어 확인**.

### 2. 명령 생성 (`<USER>@<HOST>:` 를 멀리 있는 쪽에만 붙임)
- **push (LOCAL→REMOTE)**:
  ```bash
  # (a) 원격 목적지 상위 폴더 먼저 생성
  ssh -p <PORT> <USER>@<HOST> 'mkdir -p <REMOTE_DEST_PARENT>'
  # (b) 전송
  scp -P <PORT> -r <LOCAL_SRC> <USER>@<HOST>:<REMOTE_DEST_PARENT>/
  ```
- **pull (REMOTE→LOCAL)**:
  ```bash
  mkdir -p <LOCAL_DEST_PARENT>
  scp -P <PORT> -r <USER>@<HOST>:<REMOTE_SRC> <LOCAL_DEST_PARENT>/
  ```
- 핵심 파일만(가벼움) 요청 시 scp 대신 rsync:
  ```bash
  rsync -avz -e "ssh -p <PORT>" --include='*/' \
    --include='CONTCAR' --include='OUTCAR' --include='OSZICAR' \
    --include='POSCAR' --include='INCAR' --include='KPOINTS' --include='run_slurm.sh' \
    --exclude='*' <SRC> <DEST>
  ```

### 3. 실행 방식 — 무인증(키 등록)일 때
LOCAL→REMOTE SSH 키가 등록돼 비번 없이 접속되면 **CLAUDE 가 Bash 로 직접 실행**한다 (사용자 `!` 복붙 불필요 — 모바일 줄바꿈 깨짐 방지). BatchMode 를 붙여라:
```
rsync -az -e "ssh -p <PORT> -o BatchMode=yes" <SRC> <DEST>
scp  -P <PORT> -o BatchMode=yes -r <SRC> <DEST>
```
- 먼저 `ssh -p <PORT> -o BatchMode=yes <USER>@<HOST> 'true'` 로 무인증 살아있는지 확인(exit 0).
- 깨졌으면(키 재등록 필요) `! ssh-copy-id -p <PORT> <USER>@<HOST>` 1회를 사용자에게 안내.
- 대용량(WAVECAR/CHGCAR/DOS) 전송은 `--stats`/진행량으로 실제 전송 여부 검증.

### 4. 사후 확인 (무인증이면 CLAUDE 가 양쪽 다 직접 확인)
- **pull** 직후: `ls <LOCAL_DEST_PARENT>/<폴더>`.
- **push** 직후: `ssh -p <PORT> -o BatchMode=yes <USER>@<HOST> 'ls <REMOTE_DEST_PARENT>/<폴더> && du -sh <...>'`.

## 다른 사용자 아이디로 전송 (남의 계정)

기본은 양쪽 다 내 계정(`<USER>`). **다른 사람 계정**으로 주고받을 땐 username 만 바꾼다:
```bash
# LOCAL → REMOTE 의 남의 계정 (예: 선배 id)
scp -P <PORT> -r <LOCAL_SRC> <OTHER_ID>@<HOST>:~/
```
- ⚠️ **포트는 반드시 `-P`(대문자).** `-p <PORT>` 는 `<PORT>` 가 소스 파일명으로 먹혀 실패.
- ⚠️ **무인증(BatchMode)은 내 키가 등록된 `<USER>@<HOST>` 계정에만 적용.** 남의 계정은 그쪽 `~/.ssh/authorized_keys` 에 내 공개키가 없으면 **비번을 물음** → `-o BatchMode=yes` 를 붙이면 그냥 실패. 이 경우 CLAUDE 가 직접 못 치고, 사용자가 `! scp -P <PORT> -r <SRC> <OTHER_ID>@<HOST>:~/` 로 실행해 비번 입력해야 함.
- 반대로 **남이 나(`<USER>`)에게 보낼 때**는 그쪽에서 `scp -P <PORT> -r <폴더> <USER>@<HOST>:~/`. 목적지가 내 홈이라, 도착 후 LOCAL 에서 pull 로 받으면 됨.

## 주의

- **실행 중인 SLURM 잡 폴더를 복사하면 중간 스냅샷**(OUTCAR/WAVECAR 불일치). 최종 결과 백업이면 잡 종료 후 전송.
- 목적지 상위 폴더가 없으면 scp 가 source 를 그 이름으로 rename 복사하는 사고 → push 는 항상 `mkdir -p` 먼저.
- `WAVECAR/CHGCAR/CHG/REPORT` 가 `100% 0` 으로 떠도 정상 (원본이 `LWAVE/LCHARG=.FALSE.` 면 0바이트).
