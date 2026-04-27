---
description: 오늘 데일리 노트 생성 — 어제 미완료 태스크 자동 인계
allowed-tools: Read, Write, Glob, Bash(date:*), Bash(ls:*)
argument-hint: [날짜 또는 생략]
---

# /daily — 데일리 노트 생성

오늘(또는 지정 날짜) 데일리 노트를 `10-Daily/` 에 생성합니다.

## 프로세스

### Step 1: 날짜 결정

```bash
# 인자 없으면 오늘
TARGET_DATE="${1:-$(date +%Y-%m-%d)}"
```

### Step 2: 기존 파일 확인

`10-Daily/{TARGET_DATE}.md` 가 이미 있으면:
- 사용자에게 이어서 편집할지, 새로 만들지 물어보기
- 새로 만들면 백업 후 진행

### Step 3: 어제 노트에서 미완료 태스크 추출

```bash
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d)
```

`10-Daily/{YESTERDAY}.md` 가 있으면 미완료 체크박스(`- [ ]`)만 추출:
- "## 오늘 할 일" 섹션과 "## 진행 중" 섹션의 미완료 항목
- "## 내일 할 일" 섹션 항목 (있으면 우선 인계)

### Step 4: 템플릿 적용

`_templates/daily-note.md` 의 frontmatter + 구조를 따르되:
- `{{date:YYYY-MM-DD}}` → 실제 날짜
- `{{date:YYYY-MM-DD-1}}` → 어제 날짜
- `## 오늘 할 일` 섹션에 어제 미완료 태스크 인계
- `## 메모 / 캡처` 비워두기

### Step 5: 작성 후 알림

- 파일 경로 출력
- 인계된 태스크 개수 알림
- "어제 노트 미완료 N개 인계 — 오늘 우선순위 다시 검토 권장"

## 출력 예시

```
✓ 10-Daily/2026-04-27.md 생성 완료
  - 어제 미완료 태스크 3개 인계
  - 어제의 "내일 할 일" 항목 2개 추가
  
다음: 오늘 우선순위를 데일리 노트에서 정리하세요.
```
