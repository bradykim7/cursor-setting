# Claude Code 작업 워크플로우

## 전체 커맨드 목록

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/affected-endpoints` | 영향 엔드포인트 추적 (읽기 전용) | `/affected-endpoints` |
| `/test-affected` | 영향 추적 + 자동 스모크 테스트 | `/test-affected WM-XXXXX` |
| `/smoke-test` | 수동 스모크 테스트 | `/smoke-test GET /api/v2/mail/...` |
| `/branch-diff` | 브랜치 간 응답 비교 | `/branch-diff WM-XXXXX` |
| `/commit-mailplug` | 팀 컨벤션 커밋 메시지 추천 | `/commit-mailplug` |
| `/pr-description` | PR 설명 자동 생성 | `/pr-description` |
| `/commit-suggest` | 일반 커밋 메시지 추천 | `/commit-suggest` |

---

## 티켓 작업 워크플로우

### 1단계: 브랜치 생성 & 코드 작업

```bash
git checkout -b feature/WM-XXXXX
# 코드 수정 작업...
```

### 2단계: 영향 분석

변경한 코드가 어떤 API 엔드포인트에 영향을 주는지 확인:

```
/affected-endpoints
```

출력 예시:
```
IndexDAO → ReadService → ReadController
  → GET /api/v2/mail/mailboxes/{id}/messages/{id}
NoticeMailMemberDAO → NoticeMailService → AdminNoticeMailController
  → POST /api/v2/mail/admin/mails/notice
```

### 3단계: 자동 스모크 테스트

영향 엔드포인트를 자동으로 추적하고 스모크 테스트까지 실행:

```
/test-affected
```

수행 내용:
1. 변경 파일 → 영향 엔드포인트 자동 추적
2. `testjob/WM-XXXXX/TEST_ENDPOINTS.md` 자동 생성
3. GET 엔드포인트 스모크 호출
4. POST/PUT/DELETE는 **Write→Verify** 패턴으로 검증
5. `testjob/WM-XXXXX/results/SMOKE_TEST_REPORT.md` 생성

### 4단계: (선택) 수동 스모크 테스트

특정 엔드포인트만 추가 테스트:

```
# 단일 엔드포인트
/smoke-test GET /api/v2/mail/admin/mails/approvalfilters

# POST + Write→Verify
/smoke-test POST /api/v2/mail/admin/mails/representatives {"name":"test"}

# 티켓 일괄 테스트
/smoke-test WM-XXXXX
```

### 5단계: (선택) 브랜치 비교

master 대비 응답 차이가 있는지 확인:

```
/branch-diff WM-XXXXX
```

수행 내용:
1. Run1 — 현재 브랜치에서 모든 GET 엔드포인트 호출
2. 서버 브랜치 전환 대기
3. Run2 — master에서 동일 엔드포인트 호출
4. JSON diff 비교 → `DIFF_REPORT.md` 생성

### 6단계: 커밋

```
/commit-mailplug
```

출력 예시:
```
📌 감지된 티켓: WM-XXXXX

✨ 추천: feat(WM-XXXXX): 자동완성에서 Google 계정 제외 처리

📝 대안:
1. fix(WM-XXXXX): 자동완성 Google 계정 필터링 추가
2. refactor(WM-XXXXX): 자동완성 쿼리에 account_type 조건 추가
```

### 7단계: PR 생성

```
/pr-description
```

출력 예시:
```markdown
# PR: WM-XXXXX — 자동완성에서 Google 계정 제외

## Jira
- https://jira.example.com/browse/WM-XXXXX

## 요약
- ...

## 변경 사항
- ...

## 테스트 플랜
- [ ] ...
```

---

## Write→Verify 패턴

POST/PUT/PATCH/DELETE 실행 시 자동으로 GET 검증을 수행:

```
1. GET /representatives       → before.json 저장
2. POST /representatives {..} → 201 확인
3. GET /representatives       → after.json 저장
4. diff before.json after.json
   → "id:5 항목이 새로 추가됨 ✓"
```

### verify 자동 추론 규칙

| Write 메서드 | verify GET 경로 |
|-------------|----------------|
| `POST /xxx` | `GET /xxx` |
| `PUT /xxx` | `GET /xxx` |
| `PATCH /xxx/1` | `GET /xxx/1` |
| `DELETE /xxx/1` | `GET /xxx` (부모 경로) |

TEST_ENDPOINTS.md에서 verify 컬럼으로 직접 지정 가능:

```markdown
| | METHOD | Path | verify | 비고 |
|-|--------|------|--------|------|
| [ ] | POST | representatives | GET representatives | 생성 후 재조회 |
| [ ] | DELETE | representatives/1 | GET representatives | 삭제 후 재조회 |
```

---

## testjob 디렉토리 구조

```
~/workspace/testjob/
├── urltest.http                    ← host·token (공용, git 제외)
├── TESTING_RULE.md                 ← 스모크 테스트 규칙
├── BRANCH_DIFF_TEST_RULE.md        ← 브랜치 비교 규칙
└── {TICKET}/                       ← 티켓별 디렉토리
    ├── TEST_ENDPOINTS.md           ← 테스트 대상 엔드포인트
    └── results/
        ├── run1_{desc}/            ← 브랜치 비교 run1 응답
        ├── run2_{desc}/            ← 브랜치 비교 run2 응답
        ├── {method}_{name}.json    ← 스모크 응답
        ├── verify_before_{name}.json
        ├── verify_after_{name}.json
        ├── SMOKE_TEST_REPORT.md    ← 스모크 결과
        └── DIFF_REPORT.md          ← 브랜치 비교 결과
```

---

## 환경 설정

### dotfiles 구조

```
~/.claude-dotfiles/          ← git repo
├── commands/                ← 커스텀 커맨드 (7개)
├── agents/                  ← 에이전트 설정
├── settings.json            ← 글로벌 설정
├── install.sh               ← symlink 설치 스크립트
├── WORKFLOW.md              ← 이 문서
└── .gitignore
```

### 새 환경 설정 (dev server 등)

```bash
git clone git@github.com:{repo}/claude-dotfiles.git ~/.claude-dotfiles
cd ~/.claude-dotfiles
./install.sh
```

### 커맨드 추가/수정 후 동기화

```bash
cd ~/.claude-dotfiles
git add -A && git commit -m "update commands" && git push

# dev server에서:
cd ~/.claude-dotfiles && git pull
```
