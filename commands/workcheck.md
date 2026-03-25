---
description: 작업 중간 점검 — 영향 분석 + 스모크 테스트 한번에 실행
allowed-tools: Bash(curl:*), Bash(grep:*), Bash(mkdir:*), Bash(cp:*), Bash(diff:*), Bash(python3:*), Bash(cat:*), Bash(sed:*), Bash(tr:*), Bash(ls:*), Bash(echo:*), Bash(jq:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git status:*), Read, Write, Glob, Grep
argument-hint: [티켓ID 또는 생략(자동감지)]
---

# 작업 중간 점검 (workcheck)

코드 변경 사항의 영향 분석 + 스모크 테스트 + master 비교를 한번에 실행합니다.
`/affected-endpoints` + `/test-affected` + `/branch-diff`를 순차 실행하는 메타 커맨드입니다.

## 실행 흐름

각 Step 완료 후 결과를 표시하고, 사용자가 중단하지 않으면 다음 Step으로 진행합니다.

### Step 1 — 티켓 ID 감지 & 변경 파일 수집

1. `git branch --show-current` → 티켓 ID 추출 (`WM-\d+`, `LA-\d+`, `LS-\d+`)
2. `$ARGUMENTS`가 있으면 티켓 ID로 사용
3. 변경 파일 수집:
   - 스테이징: `git diff --staged --name-only`
   - 브랜치: `git diff master...HEAD --name-only`
   - 작업트리: `git diff --name-only`
4. 변경 파일 목록 표시:
   ```
   📌 티켓: WM-XXXXX (브랜치: feature/WM-XXXXX)
   📁 변경 파일 (5개):
     - app/Mail/Models/IndexDAO.php
     - app/Mail/Services/Message/ReadService.php
     - ...
   ```

### Step 2 — 영향 엔드포인트 추적

변경 파일에서 Controller까지 역추적 (최대 3단계):

| 파일 역할 | 추적 방향 |
|-----------|-----------|
| Controller | → Routes.php에서 직접 매칭 |
| Service | → Controller 검색 → Routes.php |
| DAO/Model | → Service → Controller → Routes.php |
| Repository | → Service → Controller → Routes.php |
| 기타 (DTO/Entity/Enum/Library) | → 사용처 전체 검색 |

**추적 방법:**
1. 변경 파일의 클래스명 추출
2. `Grep`으로 `new ClassName` 또는 `use Namespace\ClassName` 검색
3. Controller 도달 시 → 모듈별 `Config/Routes.php`에서 라우트 매칭

결과 출력:
```
🔍 영향 엔드포인트 (8개):
  IndexDAO → ReadService → ReadController
    → GET  /api/v2/mail/mailboxes/{id}/messages/{id}
    → GET  /api/v2/mail/auto-complete
  NoticeMailMemberDAO → NoticeMailService → AdminNoticeMailController
    → POST /api/v2/mail/admin/mails/notice
    → GET  /api/v2/mail/admin/mails/notice
```

### Step 3 — TEST_ENDPOINTS.md 생성

`testjob/{TICKET}/` 디렉토리 생성 후 `TEST_ENDPOINTS.md` 자동 생성:

```markdown
# {TICKET} 테스트 엔드포인트 목록 (자동 생성)

| | METHOD | Path | verify | 비고 | 영향 경로 |
|-|--------|------|--------|------|-----------|
| [ ] | GET | auto-complete | - | 자동완성 | IndexDAO→Service→Controller |
| [ ] | POST | representatives | GET representatives | 생성 | DAO→Service→Controller |
```

**verify 자동 추론:**
- `POST /xxx` → `GET /xxx`
- `PUT /xxx` → `GET /xxx`
- `PATCH /xxx/1` → `GET /xxx/1`
- `DELETE /xxx/1` → `GET /xxx` (부모 경로)

**기존 TEST_ENDPOINTS.md가 있으면** 덮어쓰지 않고 병합 제안.

### Step 4 — 스모크 테스트 실행

1. `urltest.http` 탐색 (testjob/ → ../testjob/ → ~/workspace/testjob/)
2. host/token 읽기 + 토큰 유효성 확인
3. 실행할 엔드포인트 목록 확인:
   - GET: 기본 자동 실행
   - POST/PUT/PATCH/DELETE: 사용자에게 실행 여부 확인

**curl 표준 템플릿:**
```bash
curl -sS -o {output_file} -w "%{http_code}" \
  -X {METHOD} \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  [-d '${BODY_JSON}'] \
  "${URL}"
```

**Write→Verify 패턴 (POST/PUT/PATCH/DELETE):**
```
1. GET {verify_path} → verify_before_{name}.json
2. {METHOD} {path} {body} → 상태코드 확인
3. GET {verify_path} → verify_after_{name}.json
4. diff → 변경 분석
```

### Step 5 — 결과 요약

콘솔 출력:
```
=== WM-XXXXX workcheck 결과 ===

변경 파일: 5개
영향 엔드포인트: 8개

GET 결과:
  ✓ auto-complete          200  62K
  ✓ me/settings/mail       200  3.0K
  ✓ representatives        200  414B

Write→Verify 결과:
  ✓ POST representatives   201  → before/after +1 항목
  ✗ DELETE representatives/1  404  → 대상 없음

미테스트:
  ⊘ POST sendMail — body 미제공

→ testjob/WM-XXXXX/results/SMOKE_TEST_REPORT.md 저장 완료
```

`testjob/{TICKET}/results/SMOKE_TEST_REPORT.md` 생성/갱신.

### Step 6 — Master 비교 (자동)

스모크 테스트에서 호출한 GET 엔드포인트를 `{HOST}/master/{path}` 패턴으로도 호출하여 비교:

```
Feature: curl ${HOST}/api/v2/mail/{path}          → feature.json
Master:  curl ${HOST}/master/api/v2/mail/{path}   → master.json
diff feature.json master.json
```

- **서버 전환 없이 즉시 비교**
- mail/member 서버 모두 `/master/` 지원
- master URL 실패 시 이 단계 스킵 (에러 안내)

결과 저장:
```
testjob/{TICKET}/results/
├── feature/           ← Step 5 스모크 응답 (= feature 응답)
├── master/            ← master 응답
└── DIFF_REPORT.md     ← feature vs master 비교
```

콘솔 추가 출력:
```
🔀 Feature vs Master 비교:
  auto-complete        DIFF  → Google 계정 3개 제외됨
  representatives      동일
  secure-settings      동일

→ testjob/WM-XXXXX/results/DIFF_REPORT.md 저장 완료
```

## 규칙

- JWT/API 키를 채팅·PR에 절대 노출하지 않음
- 응답에 민감정보 있으면 마스킹
- 토큰 만료(401/403) 시 사용자에게 갱신 요청
- POST/PUT/PATCH/DELETE는 사용자 확인 후에만 실행
- DELETE 실행 전 추가 경고
- body 필요한데 없으면 미테스트 항목으로 분류
