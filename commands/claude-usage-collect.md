---
description: Claude Code 사용량 수집 — ccusage로 본인 데이터 추출 후 공유 패키지 생성
allowed-tools: Bash(npx:*), Bash(ccusage:*), Bash(mkdir:*), Bash(zip:*), Bash(ls:*), Bash(whoami:*), Bash(date:*), Bash(du:*), Bash(mv:*), Bash(rm:*), Bash(echo:*), Bash(test:*), Bash(uname:*), Read
argument-hint: [output 경로 생략 가능, 기본 ~/Desktop]
---

# Claude Usage Collect (사용량 수집)

본인 머신에서 Claude Code 사용 통계를 추출하여 팀장/분석가에게 공유할 수 있는 패키지를 생성합니다.
개인정보/대화 내용은 포함되지 않습니다 — 토큰/세션/모델 집계만.

**This command packages your own Claude Code usage statistics to share with your team lead. No conversation content is included — only aggregated token/session/model metrics.**

---

## 사전 조건 / Prerequisites

- `npx` 실행 가능 (Node.js 설치됨)
- 인터넷 연결 (첫 실행 시 `ccusage` 패키지 다운로드, ~30초)
- macOS / Linux / WSL

---

## 실행 흐름 / Flow

### Step 1: 환경 점검

다음을 확인:

```bash
command -v npx >/dev/null && echo "npx OK" || echo "npx MISSING"
test -d ~/.claude/projects && echo "claude data OK" || echo "claude data MISSING"
uname -s  # OS 확인
```

`claude data MISSING` 이면 중단하고 안내:

```
[✗] ~/.claude/projects/ 가 없습니다.
    Claude Code를 한 번이라도 실행한 적이 있는지 확인하세요.
```

### Step 2: 출력 경로 결정

- 인자가 있으면 해당 경로
- 없으면 `~/Desktop/` (macOS) 또는 `~/` (기타)
- 파일명: `claude-usage-{whoami}-{YYYYMMDD}.zip`

### Step 3: 임시 디렉토리 생성

```bash
TMPDIR="$(mktemp -d -t claude-usage-XXXXXX)"
cd "$TMPDIR"
```

### Step 4: ccusage 실행 (3종류)

병렬 실행 가능. 실패 시 경고만 하고 계속 진행 (부분 산출도 가치 있음):

```bash
npx ccusage@latest daily   --json > daily.json
npx ccusage@latest session --json > session.json
npx ccusage@latest monthly --json > monthly.json
```

각 파일 크기 확인 — 0바이트면 해당 서브커맨드 경고.

### Step 5: 메타 파일 추가

`meta.json` 작성:

```json
{
  "collected_at": "<ISO8601>",
  "collector": "<whoami>@<hostname>",
  "os": "<uname>",
  "node_version": "<node -v>",
  "ccusage_version": "<npx ccusage@latest --version>",
  "schema_version": "1.0"
}
```

`README.txt` 첨부 (수신자용 짧은 안내):

```
Claude Code 사용 통계 패키지
포함: daily.json, session.json, monthly.json, meta.json
개인정보/대화 내용 없음. 토큰/세션/모델 집계만.
분석: /claude-usage-report 로 통합 리포트 생성 가능.
```

### Step 6: 패키징

```bash
zip -j "$OUTPUT" daily.json session.json monthly.json meta.json README.txt
```

### Step 7: 결과 출력

```
[✓] 수집 완료
    파일: ~/Desktop/claude-usage-mskim-20260424.zip
    크기: 142 KB

수신자에게 전달하세요.
받는 사람은 /claude-usage-report 로 통합 리포트를 생성할 수 있습니다.

포함된 데이터:
  daily.json    — 일별 토큰/모델/비용
  session.json  — 세션별 시작/종료/토큰
  monthly.json  — 월별 집계
  meta.json     — 수집 메타데이터
```

---

## 프라이버시 / Privacy

- ✅ **포함**: 토큰 수, 모델명, 타임스탬프, 세션 ID, 프로젝트 경로 해시
- ❌ **미포함**: 대화 내용, 프롬프트 텍스트, 파일 내용, 환경변수, 자격증명

`ccusage` 원본 출력이 포함하는 것만 전달합니다. 직접 확인하려면:

```bash
unzip -p ~/Desktop/claude-usage-*.zip daily.json | jq . | less
```

---

## 실패 처리 / Error Handling

| 상황 | 대응 |
|------|------|
| `npx` 없음 | Node.js 설치 안내 후 중단 |
| `ccusage` 실행 실패 (네트워크) | 에러 출력 + 수동 실행 가이드 |
| JSON이 비어있음 | 경고 + 계속 진행 (부분 제출 가능) |
| zip 명령 없음 | tar.gz fallback |
| Desktop 경로 없음 | `~/` 로 fallback |

---

## 팀원에게 보낼 안내문 (복붙용)

커맨드 실행 전 팀원에게 공유할 메시지:

```
Claude Code 사용량 집계에 협조 부탁드립니다.

1. 이 저장소를 설치 (또는 업데이트) 후:
   /claude-usage-collect

2. 생성된 zip 파일을 [수신자]에게 전달

소요시간: ~30초 (첫 실행 시 ~1분)
개인정보/대화 내용 없음
```
