---
description: 브랜치 간 API 응답 비교 테스트 (run1/run2 방식)
allowed-tools: Bash(curl:*), Bash(grep:*), Bash(mkdir:*), Bash(diff:*), Bash(python3:*), Bash(cat:*), Bash(sed:*), Bash(tr:*), Bash(ls:*), Bash(echo:*), Bash(jq:*), Read, Write, Glob, Grep
argument-hint: [티켓ID(WM-32517)]
---

# 브랜치 간 응답 비교 테스트

두 브랜치 조합의 API 응답을 비교하여 의도한 변경만 발생했는지 확인합니다.

## urltest.http 위치 탐색

다음 순서로 찾는다:
1. `testjob/urltest.http`
2. `../testjob/urltest.http`
3. `/Users/mskim/workspace/testjob/urltest.http`

## 실행 절차

### Step 1 — 준비

1. `$ARGUMENTS`에서 티켓 ID 추출. 없으면 브랜치명에서 감지
2. `testjob/{TICKET}/results/` 디렉토리 생성 (없으면)
3. `urltest.http`에서 host/token 읽기
4. 토큰 유효성 확인: GET 엔드포인트 하나 호출하여 200 확인. 401/403이면 갱신 요청

### Step 2 — 엔드포인트 목록 확인

1. `testjob/{TICKET}/TEST_ENDPOINTS.md` 읽기
2. GET 엔드포인트 목록 추출 (비교 대상)
3. 사용자에게 목록 표시 + run1/run2 브랜치 조합 확인:
   ```
   Run1: mail={branch}, member={branch}
   Run2: mail={branch}, member={branch}
   ```

### Step 3 — Run1 실행

1. `results/run1_{mail-branch}_member-{branch}/` 디렉토리 생성
2. 모든 GET 엔드포인트 호출
3. 응답을 `{endpoint-name}.json`으로 저장
4. 상태 코드 기록

### Step 4 — 브랜치 전환 대기

```
Run1 완료. 서버 브랜치를 전환해주세요.
전환 완료되면 알려주세요.
```

### Step 5 — Run2 실행

1. `results/run2_{mail-branch}_member-{branch}/` 디렉토리 생성
2. 동일 엔드포인트 호출
3. 응답 저장

### Step 6 — Diff 비교

1. run1/run2 동명 JSON 파일을 `python3 -m json.tool`로 정렬
2. `diff -u` 비교
3. 차이 항목 추출 및 분류:

| 유형 | 판정 |
|------|------|
| 의도된 변경 (새 필드, 필터 적용 등) | OK — 티켓 변경과 일치 |
| URL/경로 변경 | 리팩토링 의도 확인 필요 |
| 값 불일치 (동일 필드, 다른 값) | 버그 가능성 |
| 필드 누락 | breaking change 경고 |

### Step 7 — 결과 보고

`DIFF_REPORT.md` 생성:

```markdown
# {TICKET} Branch Diff Report

- **Date:** {date}
- **Run1:** mail={branch}, member={branch}
- **Run2:** mail={branch}, member={branch}

## Summary

| Endpoint | Status | Diff? | 분석 |
|----------|--------|-------|------|
| ...      | 200/200 | YES  | 의도된 변경 |
| ...      | 200/200 | NO   | 동일 |

## Diff Details

### {endpoint-name}
{변경 내용 + 분석}
```

`SMOKE_TEST_REPORT.md` 생성/갱신: 전체 상태 코드 표

## 규칙

- GET 엔드포인트만 비교 대상 (POST/PUT/DELETE는 상태 변경 위험)
- JWT/API 키를 채팅·PR에 절대 노출하지 않음
- 응답 JSON에 민감정보 있으면 마스킹
- 디렉토리 명명: `run1_mail-{branch}_member-{branch}/`
