---
type: weekly
week: {{date:gggg-[W]ww}}
date: {{date:YYYY-MM-DD}}
tags:
  - weekly
  - review
---

# 주간 회고 — {{date:gggg-[W]ww}}

> 파일명 권장: `weekly-YYYY-Www.md` (예: `weekly-2026-W17.md`)
> 매주 금요일 오후 또는 일요일 저녁에 작성 권장.

## 이번 주 한 일

### 출시·완료한 것
- 

### 진행 중
- 

### 막힌 것 / 멈춘 것
- 

## 배운 것 (Lessons)

> 다음 주에도 기억해야 할 것. 일반화 가능하면 `30-Development/learning/` 으로 별도 노트.

- 

## 미해결 / 이월

- [ ] 

## 다음 주 우선순위

1. 
2. 
3. 

## 관련 데일리 노트

```dataview
LIST
FROM "10-Daily"
WHERE date >= date(this.date) - dur(7 days) AND date <= date(this.date)
SORT date ASC
```

> Dataview 플러그인이 있으면 자동으로 이번 주 데일리 노트가 나열됨.
