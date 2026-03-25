---
description: 엔드포인트 스모크 테스트 실행 (curl 기반, Write→Verify 패턴 지원)
allowed-tools: Bash(curl:*), Bash(grep:*), Bash(mkdir:*), Bash(cp:*), Bash(diff:*), Bash(python3:*), Bash(git show:*), Bash(cat:*), Bash(sed:*), Bash(tr:*), Bash(ls:*), Bash(echo:*), Bash(jq:*), Read, Write, Glob, Grep
argument-hint: [GET /api/v2/mail/endpoint 또는 티켓ID(WM-XXXXX)]
---

# 스모크 테스트 실행

엔드포인트를 curl로 호출하여 응답 상태와 구조를 확인합니다.
Write 계열(POST/PUT/PATCH/DELETE)은 **Write→Verify 패턴**으로 GET 검증까지 수행합니다.

## urltest.http 위치 탐색

다음 순서로 `urltest.http` 파일을 찾는다:
1. `testjob/urltest.http` (현재 디렉토리 기준)
2. `../testjob/urltest.http`
3. `~/workspace/testjob/urltest.http`

```bash
HOST_MAIL=$(grep '^@host_mail' {path}/urltest.http | sed 's/^@host_mail = //' | tr -d '\r')
HOST_MEMBER=$(grep '^@host_member' {path}/urltest.http | sed 's/^@host_member = //' | tr -d '\r')
TOKEN=$(grep '^@token' {path}/urltest.http | sed 's/^@token = //' | tr -d '\r')
```

## 입력 모드

### 모드 A: 단일 엔드포인트 (`$ARGUMENTS`가 HTTP 메서드로 시작)

예:
- `GET /api/v2/mail/admin/mails/approvalfilters`
- `POST /api/v2/mail/admin/mails/representatives {"name":"test"}`
- `DELETE /api/v2/mail/admin/mails/representatives/1`

1. 메서드, 경로, (선택) JSON body 분리
2. 경로가 상대경로면 `/api/v2/mail/` 접두사 추가
3. mail 계열(`/api/v2/mail/`) → `HOST_MAIL`, member 계열(`/api/v2/member/`) → `HOST_MEMBER`
4. **GET**: curl 실행 → 상태코드 + 응답 구조 출력
5. **POST/PUT/PATCH/DELETE**: Write→Verify 패턴 실행 (아래 참고)

### 모드 B: 티켓 기반 일괄 테스트 (`$ARGUMENTS`가 티켓 ID)

예: `WM-XXXXX`

1. `testjob/{TICKET}/TEST_ENDPOINTS.md` 파일 읽기
2. 테이블에서 모든 엔드포인트 추출 (METHOD, Path, verify, 비고)
3. **실행 전 사용자에게 목록 표시** 후 확인 요청
   - GET: 기본 자동 실행
   - POST/PUT/PATCH/DELETE: 체크리스트로 표시, 사용자 선택 후 실행
4. 각 엔드포인트 실행 (Write 계열은 Write→Verify)
5. 결과를 `testjob/{TICKET}/results/`에 저장
6. `SMOKE_TEST_REPORT.md` 생성/갱신

### 모드 C: 인수 없음

사용자에게 안내:
- `/test-affected` — 영향 엔드포인트 자동 추적 + 스모크
- `/smoke-test WM-XXXXX` — 티켓 기반 일괄 테스트

## curl 표준 템플릿

### GET / DELETE (body 없음)
```bash
curl -sS -o {output_file} -w "%{http_code}" \
  -X {METHOD} \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  "${URL}"
```

### POST / PUT / PATCH (body 있음)
```bash
curl -sS -o {output_file} -w "%{http_code}" \
  -X {METHOD} \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d '${BODY_JSON}' \
  "${URL}"
```

## Write→Verify 패턴

Write 계열(POST/PUT/PATCH/DELETE) 실행 시 자동으로 GET 검증을 수행한다.

### 실행 흐름

```
1. GET {verify_path} → before.json 저장
2. {METHOD} {path} {body} 실행 → 상태코드 확인 (200/201/204)
3. GET {verify_path} → after.json 저장
4. python3 -m json.tool로 정렬 후 diff -u before.json after.json
5. 변경 분석 결과 출력
```

### verify 경로 결정

**우선순위:**
1. TEST_ENDPOINTS.md의 `verify` 컬럼에 명시된 경로
2. `verify` 컬럼이 없거나 비어있으면 **자동 추론**:
   - `POST /xxx` → `GET /xxx` (같은 경로)
   - `PUT /xxx` → `GET /xxx` (같은 경로)
   - `PATCH /xxx/1` → `GET /xxx/1` (같은 경로)
   - `DELETE /xxx/1` → `GET /xxx` (부모 경로, ID 제거)
3. `verify` 컬럼이 `-` 이면 verify 스킵 (Write만 실행)

### 결과 출력 예시

```
🔍 Before: GET /api/v2/mail/admin/mails/representatives
✏️  Write:  POST /api/v2/mail/admin/mails/representatives → 201
🔍 After:  GET /api/v2/mail/admin/mails/representatives

📊 Verify 결과:
  + id:5 "test" 항목이 새로 추가됨
  총 항목: 3 → 4 (1개 증가)
  ✓ Write→Verify 성공
```

### DELETE 추가 경고

```
⚠️  DELETE /api/v2/mail/admin/mails/representatives/1
   이 작업은 되돌릴 수 없습니다. 실행하시겠습니까? (y/n)
```

## SMOKE_TEST_REPORT.md 템플릿

```markdown
# {TICKET} Smoke Test Report

- **Date:** {date}
- **Host:** {host}

## GET 결과

| Endpoint | Status | Size | 비고 |
|----------|--------|------|------|
| ...      | 200    | 1.2K | OK   |

## Write→Verify 결과

| Endpoint | Method | Status | Verify | Diff | 비고 |
|----------|--------|--------|--------|------|------|
| representatives | POST | 201 | GET representatives | +1 항목 | ✓ |
| representatives/1 | DELETE | 200 | GET representatives | -1 항목 | ✓ |
```

## 규칙

- JWT/API 키를 채팅·PR에 절대 노출하지 않음
- 응답에 민감정보 있으면 마스킹 후 요약
- 토큰 만료(401/403) 시 사용자에게 갱신 요청
- POST/PUT/PATCH/DELETE는 사용자 확인 후에만 실행
- body가 필요한데 없으면 사용자에게 요청
- 응답 JSON 저장: `{method}_{endpoint-name}.json` (경로의 `/`를 `-`로 치환)
- verify 저장: `verify_before_{endpoint-name}.json`, `verify_after_{endpoint-name}.json`
