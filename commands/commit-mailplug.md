---
description: 팀 컨벤션에 맞는 커밋 메시지 추천 (티켓 ID 자동 감지)
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
argument-hint: [티켓 ID 또는 추가 컨텍스트]
---

# Mailplug 커밋 메시지 추천

스테이징된 파일과 git 히스토리를 분석하여 팀 컨벤션에 맞는 커밋 메시지를 추천합니다.

## 커밋 메시지 포맷

```
type(TICKET-ID): 한국어 설명
```

**예시:**
```
feat(WM-XXXXX): AuditLog, domain, host 정보추가
fix(LA-4014): fromSystemKeywordToLang 활용
refactor(WM-XXXXX): 쿼리 최적화 및 whereNotDeleted 헬퍼 추가
hotfix(WM-XXXXX): url 결정 규칙 entity로 이동
```

## 분석 절차

### 1단계: 브랜치에서 티켓 ID 감지
- `git branch --show-current` 실행
- 브랜치명에서 티켓 ID 추출 (패턴: `WM-\d+` 또는 `LA-\d+`)
- `$ARGUMENTS`가 제공되면 티켓 ID 또는 추가 컨텍스트로 활용
- 티켓 ID를 찾을 수 없으면 사용자에게 입력 요청

### 2단계: 스테이징 상태 확인
- `git status`로 스테이징된 파일 확인
- 스테이징된 파일이 없으면 사용자에게 안내

### 3단계: 변경 내용 분석
- `git diff --staged`로 변경 내용 분석
- 변경의 성격과 범위 파악

### 4단계: 최근 히스토리 참고
- `git log --oneline -10`으로 최근 커밋 스타일 확인

### 5단계: 커밋 타입 결정

변경 내용에 따라 적절한 타입을 선택:

| 타입 | 설명 | 사용 시점 |
|------|------|-----------|
| `feat` | 새로운 기능 | 새 기능 추가, 기존 기능 확장 |
| `fix` | 버그 수정 | 버그 및 오류 수정 |
| `hotfix` | 긴급 수정 | 프로덕션 긴급 버그 수정 |
| `refactor` | 리팩토링 | 동작 변경 없는 코드 구조 개선 |
| `docs` | 문서 변경 | 문서만 변경 |
| `style` | 코드 스타일 | 포맷팅, 세미콜론 등 (로직 변경 없음) |
| `perf` | 성능 개선 | 성능 향상을 위한 변경 |
| `test` | 테스트 | 테스트 추가 또는 수정 |
| `build` | 빌드 | 빌드 시스템 또는 의존성 변경 |
| `ci` | CI/CD | CI/CD 설정 변경 |
| `chore` | 기타 | 유지보수, 잡무 |

### 6단계: 추천 메시지 생성

## 출력 포맷

```
📌 감지된 티켓: LA-3843 (브랜치: feature/LA-3843)

변경 파일:
- app/Libraries/Profile/enum/ImagePath.php
- app/Libraries/Profile/ProfileService.php

✨ 추천 커밋 메시지:
feat(LA-3843): 프로필 이미지 경로 처리 로직 개선

📝 대안:
1. refactor(LA-3843): 프로필 이미지 호스트 경로 수정
2. fix(LA-3843): 프로필 이미지 경로 오류 수정

커밋하시겠습니까? 번호를 선택하거나 수정 요청해주세요.
```

## 규칙

- 설명은 한국어로 작성
- 제목은 50자 이내 권장 (최대 72자)
- "~추가", "~수정", "~삭제", "~개선" 등 명사형 종결
- 불필요한 조사나 문장 종결어미 생략
- 변경 내용의 "무엇"과 "왜"에 집중
