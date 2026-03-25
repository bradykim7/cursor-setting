---
description: 브랜치 간 API 응답 비교 테스트 (master URL 패턴으로 즉시 비교)
allowed-tools: Bash(curl:*), Bash(grep:*), Bash(mkdir:*), Bash(diff:*), Bash(python3:*), Bash(cat:*), Bash(sed:*), Bash(tr:*), Bash(ls:*), Bash(echo:*), Bash(jq:*), Read, Write, Glob, Grep
argument-hint: [티켓ID(WM-XXXXX)]
---

# 브랜치 간 응답 비교 테스트

현재 브랜치(feature)와 master의 API 응답을 비교하여 의도한 변경만 발생했는지 확인합니다.
**서버 브랜치 전환 없이** `{host}/master/{path}` 패턴으로 즉시 비교합니다.

## urltest.http 위치 탐색

다음 순서로 찾는다:
1. `~/.claude-dotfiles/urltest.http`
2. `testjob/urltest.http`
3. `../testjob/urltest.http`
4. `~/workspace/testjob/urltest.http`

## URL 패턴

| 대상 | URL 패턴 |
|------|----------|
| Feature (현재 브랜치) | `{HOST}/api/v2/mail/{path}` |
| Master | `{HOST}/master/api/v2/mail/{path}` |

- mail 계열: `HOST_MAIL` 사용
- member 계열: `HOST_MEMBER` 사용
- 둘 다 `/master/` 접두사 지원

## 실행 절차

### Step 1 — 준비

1. `$ARGUMENTS`에서 티켓 ID 추출. 없으면 브랜치명에서 감지
2. `testjob/{TICKET}/results/` 디렉토리 생성 (없으면)
3. `urltest.http`에서 host/token 읽기
4. 토큰 유효성 확인: GET 하나 호출 → 200 확인. 401/403이면 갱신 요청

### Step 2 — 엔드포인트 목록 확인

1. `testjob/{TICKET}/TEST_ENDPOINTS.md` 읽기
2. GET 엔드포인트 목록 추출 (비교 대상)
3. 사용자에게 목록 표시

### Step 3 — Feature + Master 동시 호출

각 GET 엔드포인트에 대해:

```bash
# Feature (현재 브랜치)
curl -sS -o results/feature/{name}.json -w "%{http_code}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  "${HOST}/api/v2/mail/{path}"

# Master
curl -sS -o results/master/{name}.json -w "%{http_code}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  "${HOST}/master/api/v2/mail/{path}"
```

**서버 전환 대기 없이 연속 실행.**

결과 저장 디렉토리:
```
testjob/{TICKET}/results/
├── feature/          ← 현재 브랜치 응답
│   ├── auto-complete.json
│   └── representatives.json
├── master/           ← master 응답
│   ├── auto-complete.json
│   └── representatives.json
├── DIFF_REPORT.md
└── SMOKE_TEST_REPORT.md
```

### Step 4 — Diff 비교

1. feature/master 동명 JSON을 `python3 -m json.tool`로 정렬
2. `diff -u` 비교
3. 차이 항목 분류:

| 유형 | 판정 |
|------|------|
| 의도된 변경 (새 필드, 필터 적용 등) | OK — 티켓 변경과 일치 |
| URL/경로 변경 | 리팩토링 의도 확인 필요 |
| 값 불일치 (동일 필드, 다른 값) | 버그 가능성 |
| 필드 누락 | breaking change 경고 |

### Step 5 — 결과 보고

`DIFF_REPORT.md` 생성:

```markdown
# {TICKET} Branch Diff Report

- **Date:** {date}
- **Feature:** {branch name}
- **Master:** {host}/master/...
- **비교 방식:** master URL 패턴 (서버 전환 없음)

## Summary

| Endpoint | Feature | Master | Diff? | 분석 |
|----------|---------|--------|-------|------|
| auto-complete | 200 | 200 | YES | Google 계정 제외됨 (의도) |
| representatives | 200 | 200 | NO | 동일 |

## Diff Details

### {endpoint-name}
{변경 내용 + 분석}
```

`SMOKE_TEST_REPORT.md` 생성/갱신.

## Fallback: 기존 방식 (서버 전환)

사용자가 `--legacy` 옵션을 주거나, master URL이 동작하지 않는 경우:

1. Run1 실행 (현재 브랜치)
2. **사용자에게 브랜치 전환 요청 + 대기**
3. Run2 실행 (전환된 브랜치)
4. Diff 비교

## 규칙

- GET 엔드포인트만 비교 대상 (POST/PUT/DELETE는 상태 변경 위험)
- JWT/API 키를 채팅·PR에 절대 노출하지 않음
- 응답 JSON에 민감정보 있으면 마스킹
- master URL 호출 실패 시 자동으로 fallback(기존 방식) 안내
