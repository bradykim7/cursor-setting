# Claude Code 작업 워크플로우

## 전체 커맨드 목록

### 메타 커맨드 (플로우 한번에 실행)

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| **`/workcheck`** | 영향 분석 + 스모크 테스트 한번에 | `/workcheck` |
| **`/workfinish`** | 커밋 추천 + PR 설명 한번에 | `/workfinish` |

### 계획 라이프사이클 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/create-plan` | 구조적 구현 계획 수립 (조사→설계→계획서) | `/create-plan 검색 필터 추가` |
| `/implement-plan` | 계획서 Phase별 구현 + 자동/수동 검증 | `/implement-plan .plans/2026-04-08-desc.md` |
| `/iterate-plan` | 기존 계획서 피드백 반영 수정 | `/iterate-plan .plans/파일.md Phase 2 분리` |
| `/validate-plan` | 구현 결과 전체 검증 + 리포트 | `/validate-plan` |

### 리서치 & 디버깅 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/research` | 코드베이스 구조적 탐색 & 리서치 문서 | `/research 인증 플로우 분석` |
| `/debug` | 구조적 디버깅 (병렬 조사) | `/debug 500 에러 발생` |

### 세션 관리 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/handoff` | 세션 인수인계 문서 작성 | `/handoff` |
| `/resume-handoff` | 핸드오프에서 작업 재개 | `/resume-handoff .handoffs/2026-04-08_14-30-00_desc.md` |

### 테스트 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/affected-endpoints` | 영향 엔드포인트 추적 (읽기 전용) | `/affected-endpoints` |
| `/test-affected` | 영향 추적 + 자동 스모크 테스트 | `/test-affected WM-XXXXX` |
| `/smoke-test` | 수동 스모크 테스트 | `/smoke-test GET /api/v2/mail/...` |
| `/branch-diff` | 브랜치 간 응답 비교 | `/branch-diff WM-XXXXX` |

### 커밋 & PR 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/commit-mailplug` | 팀 컨벤션 커밋 메시지 추천 | `/commit-mailplug` |
| `/pr-description` | PR 설명 자동 생성 | `/pr-description` |
| `/commit-suggest` | 일반 커밋 메시지 추천 | `/commit-suggest` |

### Claude Code 사용 통계 커맨드

| 커맨드 | 용도 | 입력 예시 |
|--------|------|-----------|
| `/claude-usage-collect` | 본인 사용 데이터 수집 → 공유 zip 생성 | `/claude-usage-collect` |
| `/claude-usage-analyze` | 본인 사용 분석 → 개인 리포트 | `/claude-usage-analyze 14d` |
| `/claude-usage-report` | 팀원 JSON 수합 → 8섹션 팀 리포트 | `/claude-usage-report ./team-data 212482160` |

**플로우**: 팀원들이 `collect` 실행 → zip 수합 → 팀장이 `report`로 통합 분석. 개인은 `analyze`로 스스로 점검.

---

## 빠른 사용법 (메타 커맨드)

```
git checkout -b feature/WM-XXXXX
# 코드 작업...

/workcheck              ← 영향 분석 + 스모크 테스트
/workfinish             ← 커밋 + PR 설명 생성
```

이것만으로 전체 플로우가 완료됩니다. 세부 제어가 필요하면 아래 개별 커맨드를 사용하세요.

---

## 개발 워크플로우 (NEW)

### 계획 → 구현 → 검증 → 인수인계 (Full Lifecycle)

```
/create-plan 기능 설명        ← 1. 조사 → 설계 → 계획서 작성
/iterate-plan 피드백          ← 2. 계획 수정 (필요시 반복)
/implement-plan               ← 3. Phase별 구현 + 자동 검증
/validate-plan                ← 4. 구현 결과 전체 검증
/debug 에러 설명              ←    문제 발생 시 병렬 조사
/workcheck                    ← 5. 영향 분석 + 스모크 테스트
/workfinish                   ← 6. 커밋 + PR 생성
/handoff                      ← 7. 세션 종료 시 인수인계
/resume-handoff               ←    다음 세션에서 이어서
```

### 코드베이스 이해

```
/research 주제                ← 코드베이스 탐색 & 문서화
```

### 에이전트 자동 호출 흐름 (예시)

```
사용자: /create-plan 메일 검색 필터 추가

Claude (Opus):
  ├─ spawn codebase-locator (Sonnet)       ← 관련 파일 찾기
  ├─ spawn codebase-analyzer (Sonnet)      ← 기존 구현 분석
  ├─ spawn codebase-pattern-finder (Sonnet) ← 유사 패턴 검색
  ├─ spawn docs-locator (Sonnet)           ← 과거 관련 문서 탐색
  └─ 종합하여 구현 계획서 작성
```

### 프로젝트 초기화

```bash
# 새 프로젝트에서 Claude Code 초기화
./install.sh init /path/to/project

# 생성되는 것:
#   CLAUDE.md       ← 프로젝트별 AI 지침 (TODO 항목 편집)
#   .handoffs/      ← 핸드오프 문서 저장소
#   .plans/         ← 구현 계획서 저장소
#   .research/      ← 리서치 문서 저장소
```

---

## 자동 서브에이전트 (NEW — humanlayer 영감)

커맨드와 달리, 에이전트는 **사용자가 직접 호출하지 않습니다.** Claude가 작업 중 필요할 때 자동으로 spawns 합니다.

### 에이전트 목록

| 에이전트 | 용도 | 자동 호출 시점 |
|----------|------|---------------|
| `codebase-analyzer` | 코드 구현 상세 분석 (데이터 흐름, 로직) | `/create-plan`, `/research`, `/debug` |
| `codebase-locator` | 파일/컴포넌트 위치 탐색 (Super Grep) | `/create-plan`, `/research`, `/implement-plan`, `/debug` |
| `codebase-pattern-finder` | 유사 구현/패턴 찾기 + 코드 예시 | `/create-plan`, `/research`, `/implement-plan` |
| `docs-locator` | 과거 문서 탐색 (.plans/.research/.handoffs/) | `/create-plan`, `/research`, `/resume-handoff`, `/debug` |
| `docs-analyzer` | 과거 문서 인사이트 추출 (의사결정, 제약) | `/resume-handoff`, `/iterate-plan` |
| `web-search-researcher` | 웹 검색으로 최신 정보 조사 | 외부 API/라이브러리 정보 필요할 때 |
| `architecture-review` | 아키텍처 제안 검토 & 리스크 분석 | 설계 문서 리뷰 시 |
| `endpoint-analysis` | API 엔드포인트 동작/계약 분석 | `/validate-plan`, 엔드포인트 분석 시 |
| `pr-review-assistant` | PR 리스크 포커스 리뷰 | `/validate-plan`, PR 리뷰 시 |
| `consistency-check` | 데이터 스냅샷 비교 & 불일치 탐지 | 데이터 정합성 확인 시 |
| `document-summarizer` | 문서 요약 & 구조화 | 미팅 노트/설계 문서 정리 시 |
| `pr-description-generator` | PR 설명 자동 생성 | PR 생성 시 |

### 커맨드 vs 에이전트 차이

```
커맨드 (commands/)          에이전트 (agents/)
──────────────────          ──────────────────
사용자가 직접 호출           Claude가 자동 호출
/create-plan 으로 실행      Claude가 필요할 때 spawn
전체 워크플로우 정의         단일 전문 작업 수행
Opus 모델 사용              Sonnet 모델 사용 (빠르고 저렴)
```

### 실제 동작 예시

```
사용자: /create-plan 메일 검색 필터 추가

Claude (Opus):
  ├─ spawn codebase-locator (Sonnet)    ← 관련 파일 찾기
  ├─ spawn codebase-analyzer (Sonnet)   ← 기존 구현 분석
  ├─ spawn codebase-pattern-finder (Sonnet) ← 유사 패턴 탐색
  └─ 종합하여 구현 계획서 작성
```

---

## 상세 워크플로우 (기존 커맨드)

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
1. Feature — `{host}/api/v2/mail/{path}` 호출
2. Master — `{host}/master/api/v2/mail/{path}` 호출 (**서버 전환 불필요**)
3. JSON diff 비교 → `DIFF_REPORT.md` 생성

> `/workcheck`에도 master 비교가 포함되어 있으므로, workcheck만 실행해도 됩니다.

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
~/.claude-dotfiles/          ← git repo (cursor-setting)
├── commands/                ← 커스텀 커맨드 (20개)
│   ├── create-plan.md         ← 구조적 계획 수립
│   ├── implement-plan.md      ← 계획서 Phase별 구현
│   ├── iterate-plan.md        ← 기존 계획서 수정
│   ├── validate-plan.md       ← 구현 결과 검증
│   ├── research.md            ← 코드베이스 리서치
│   ├── debug.md               ← 구조적 디버깅
│   ├── handoff.md             ← 세션 인수인계
│   ├── resume-handoff.md      ← 핸드오프 재개
│   ├── workcheck.md
│   ├── workfinish.md
│   ├── affected-endpoints.md
│   ├── smoke-test.md
│   ├── branch-diff.md
│   ├── commit-mailplug.md
│   ├── pr-description.md
│   ├── commit-suggest.md
│   ├── test-affected.md
│   ├── claude-usage-collect.md   ← 본인 사용 데이터 수집
│   ├── claude-usage-analyze.md   ← 개인 사용 분석 리포트
│   └── claude-usage-report.md    ← 팀 사용 집계 리포트
├── agents/claude-code/      ← 자동 서브에이전트 (12개)
│   ├── codebase-analyzer.md       ← 코드 구현 분석
│   ├── codebase-locator.md        ← 파일/컴포넌트 위치 탐색
│   ├── codebase-pattern-finder.md ← 코드 패턴/예시 탐색
│   ├── docs-locator.md            ← 과거 문서 탐색 (지식 검색)
│   ├── docs-analyzer.md           ← 과거 문서 인사이트 추출
│   ├── web-search-researcher.md   ← 웹 검색 리서치
│   ├── architecture-review.md
│   ├── consistency-check.md
│   ├── document-summarizer.md
│   ├── endpoint-analysis.md
│   ├── pr-description-generator.md
│   └── pr-review-assistant.md
├── templates/               ← NEW: 프로젝트 템플릿
│   └── CLAUDE.md.template
├── docs/                    ← NEW: 참고 문서
│   └── approach-a-submodule.md
├── settings.json            ← 글로벌 설정
├── install.sh               ← symlink 설치 + 프로젝트 init
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
