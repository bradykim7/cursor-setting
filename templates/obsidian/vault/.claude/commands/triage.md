---
description: 00-Inbox/ 노트 분류 — 적절한 폴더로 이동 제안
allowed-tools: Read, Write, Glob, Grep, Bash(mv:*), Bash(ls:*)
argument-hint: [없음]
---

# /triage — Inbox 분류

`00-Inbox/` 의 노트들을 읽고 적절한 폴더로 이동을 제안합니다.

## 프로세스

### Step 1: Inbox 노트 목록 수집

```bash
ls 00-Inbox/*.md 2>/dev/null
```

빈 inbox면 "Inbox 비어있음" 출력 후 종료.

### Step 2: 각 노트 분석

노트별로 다음 정보 추출:
- **frontmatter `type`** (있으면 분류 힌트)
- **태그**
- **첫 1-3 문단의 키워드**

### Step 3: 분류 결정

각 노트마다 가장 적합한 목적지 추천:

| 신호 | 추천 폴더 |
|------|----------|
| 회사 시스템명·고유명사 | `20-Company/` 하위 |
| ADR 형식·"결정"·"trade-off" | `20-Company/decisions/` |
| 미팅·참석자 | `20-Company/meetings/` |
| 일반 기술 용어·패턴 이름 | `30-Development/patterns/` |
| 증상→원인→해결 구조 | `30-Development/troubleshooting/` 또는 `20-Company/troubleshooting/` |
| 코드 스니펫 위주 | `30-Development/snippets/` |
| 책·아티클 인용 | `30-Development/learning/` |
| 진행 중 프로젝트명 | `40-Projects/` |
| 회사 vs 일반 모호 | 사용자에게 질문 |

### Step 4: 제안 출력

각 노트에 대해 한 줄 제안:

```
00-Inbox/회의-결제-스펙.md
  → 20-Company/meetings/2026-04-27-결제-스펙-리뷰.md
  근거: "참석자" 섹션 + 회사 시스템명 등장
  파일명도 컨벤션(YYYY-MM-DD-주제)에 맞게 변경 제안

00-Inbox/idempotency.md
  → 30-Development/patterns/idempotency-key-design.md
  근거: 일반 기술 개념, 회사 컨텍스트 없음
```

### Step 5: 일괄 실행 옵션

사용자 확인 후:
- "전부 적용" / "선택 적용" / "취소" 선택
- 선택 시 인덱스로 지정 (예: 1, 3, 5)

이동 시:
- 파일명 컨벤션 적용 (kebab-case)
- frontmatter에 `type` 누락이면 추가 제안
- 백업: 이동 전 git status 확인 (커밋 안 된 변경 있으면 경고)

### Step 6: 사후 점검

이동 완료 후:
- 깨진 위키링크 검사 (`Grep -r "[[원래파일명]]"`)
- 깨진 링크 있으면 자동 업데이트 제안

## 출력 예시

```
Inbox 5개 노트 분석 완료:

[1] 회의-결제-스펙.md → 20-Company/meetings/2026-04-27-결제-스펙-리뷰.md
[2] idempotency.md → 30-Development/patterns/idempotency-key-design.md
[3] 메모.md → 사용자 확인 필요 (제목이 모호)
[4] 책-DDIA-3장.md → 30-Development/learning/ddia-ch03-storage.md
[5] TODO.md → 10-Daily/{오늘}.md 의 "오늘 할 일" 섹션으로 병합

진행: [a]ll / [s]elect / [c]ancel?
```
