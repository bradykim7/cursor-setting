---
description: 팀 컨벤션에 맞는 PR 설명 자동 생성 (티켓 ID 자동 감지, git diff 기반)
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git rev-parse:*)
argument-hint: [티켓 ID 또는 추가 컨텍스트]
---

# Mailplug PR 설명 생성

현재 브랜치의 변경 사항을 분석하여 팀 컨벤션에 맞는 PR 설명을 생성합니다.

## 분석 절차

### 1단계: 브랜치에서 티켓 ID 감지
- `git branch --show-current` 실행
- 브랜치명에서 티켓 ID 추출 (패턴: `WM-\d+`, `LA-\d+`, `LS-\d+`)
- `$ARGUMENTS`가 제공되면 티켓 ID 또는 추가 컨텍스트로 활용
- 티켓 ID를 찾을 수 없으면 사용자에게 입력 요청

### 2단계: 베이스 브랜치와의 차이 분석
- `git merge-base master HEAD`로 분기 지점 확인
- `git log master...HEAD --oneline`으로 브랜치 내 모든 커밋 확인
- `git diff master...HEAD --stat`으로 변경 파일 목록 확인
- `git diff master...HEAD`으로 전체 변경 내용 분석

### 3단계: 변경 사항 분류
변경된 파일들을 모듈/영역별로 그룹핑:
- `app/` — 앱 공통 (엔티티, 라이브러리, 모델 등)
- `app/Mail/` — 메일 모듈
- `app/Contact/` — 주소록/조직도 모듈
- `app/Auth/` — 인증 모듈
- `app/Board/` — 게시판 모듈
- `app/User/` — 사용자 설정 모듈
- `app/Capacity/` — 용량 관리
- `app/Notify/` — 알림 모듈
- `app/admin/` — 관리자 모듈
- `member/` — 멤버 관리 (gw-member)
- `organization/` — 조직 관리 (gw-member)
- `admin/` — 관리자 (gw-member)
- 기타

### 4단계: PR 설명 생성

아래 템플릿에 맞춰 생성:

```markdown
# PR: {TICKET-ID} — {한줄 요약}

## Jira
- https://jira.example.com/browse/{TICKET-ID}

## 요약
- {변경 목적과 핵심 내용을 2~5개 bullet으로 요약}

## 변경 사항

### 1) {변경 그룹 제목}
- **파일**: `{파일 경로}`
  - {변경 내용 설명}

### 2) {변경 그룹 제목}
- **파일**: `{파일 경로}`
  - {변경 내용 설명}

## 영향 범위 / 주의사항
- {side-effect, 의존성, 주의 사항 등}

## 테스트 플랜
- [ ] {테스트 항목 1}
- [ ] {테스트 항목 2}
- [ ] {테스트 항목 3}
```

## 작성 규칙

### 요약
- 변경의 **목적(왜)**과 **핵심 내용(무엇)**을 간결하게
- 2~5개 bullet point
- "~했습니다" 체

### 변경 사항
- 모듈/영역별로 그룹핑 (파일 하나하나 나열하지 않음)
- 파일 경로는 backtick으로 감싸기
- 변경 내용은 **코드가 아닌 비즈니스 관점**에서 설명
- 테이블 형식도 가능 (파일이 많은 경우):
  ```markdown
  | 파일 | 내용 |
  |------|------|
  | `path/to/file.php` | 변경 설명 |
  ```

### 영향 범위 / 주의사항
- 기존 기능에 미치는 영향
- 의존성이나 migration 필요 여부
- 생략 가능한 경우에도 최소 1개 이상 기재

### 테스트 플랜
- checkbox (`- [ ]`) 형식
- 사용자가 직접 수행할 수 있는 구체적인 검증 항목
- 정상 케이스 + 예외 케이스 모두 포함

## 주의
- 이 커맨드는 **읽기 전용**입니다 (커밋, 푸시, 파일 쓰기 없음)
- 생성된 내용은 콘솔에 출력되며, 사용자가 직접 복사하여 사용합니다
