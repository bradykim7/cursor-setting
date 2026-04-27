# CLAUDE.md — Vault Guidelines

이 파일은 **Claude Code가 이 vault에서 작업할 때 따를 컨벤션**을 정의합니다.
vault 루트에서 `claude` 실행 시 자동으로 이 파일이 로드됩니다.

## Vault 목적

- **20-Company/** 회사 지식 축적 (떠나면 폐기/인계)
- **30-Development/** 일반 개발 지식 (평생 자산)
- **10-Daily/** 일일 작업 로그 — 두 영역의 임시 저수지
- **00-Inbox/** 분류 전 빠른 캡처

## 폴더 컨벤션

```
00-Inbox/          분류 전 모든 것 — 주 1회 비우기
10-Daily/          YYYY-MM-DD.md 데일리 노트
20-Company/        회사 컨텍스트 (사내 시스템·결정·사람)
  meetings/        YYYY-MM-DD-주제.md
  decisions/       ADR-NNNN-제목.md
  glossary/        용어.md (aliases 활용)
  people/          이름.md
30-Development/    회사 무관 지식
  patterns/        kebab-case-제목.md
  troubleshooting/ kebab-case-증상.md (일반화된 교훈)
  snippets/        언어-목적.md
  learning/        출처-주제.md
40-Projects/       진행 중 프로젝트 (완료 시 90-Archive로)
90-Archive/        보관
_attachments/      이미지·PDF 자동 저장 (Obsidian 설정)
_templates/        Templates 코어 플러그인용
```

## 노트 작성 규칙

### 파일명
- **소문자 + 하이픈** (kebab-case): `idempotency-key-design.md`
- 날짜 prefix가 의미 있을 때만 사용: `2026-04-27-결제-스펙-리뷰.md`
- 한글 OK, 공백 대신 하이픈 권장

### Frontmatter
모든 노트는 frontmatter로 시작:

```yaml
---
type: tech-knowledge | meeting | decision | troubleshooting | glossary | daily | weekly
date: YYYY-MM-DD
tags:
  - 영역태그
  - 토픽태그
---
```

### 위키링크
- 형식: `[[파일명]]` 또는 `[[파일명|표시 이름]]`
- 새 노트 만들 때 다른 노트에서 참조될 만하면 적극적으로 링크
- glossary 항목은 첫 등장 시 반드시 위키링크

### 태그 컨벤션
- `#status/draft`, `#status/in-progress`, `#status/done`
- `#area/backend`, `#area/frontend`, `#area/infra`
- `#topic/{이름}` 자유 토픽
- `#company/{팀이름}` 20-Company 하위에서만

## Claude Code 작업 가이드

### 새 노트 만들 때
1. 적절한 폴더 결정 (애매하면 `00-Inbox/`)
2. 파일명을 kebab-case로
3. type에 맞는 템플릿 적용 (`_templates/` 참고)
4. frontmatter 채우기
5. 관련 노트가 있으면 위키링크로 연결

### 분리 원칙 (중요)
회사 정보와 일반 지식은 **반드시 분리**:

- 사내 시스템명·고유 결정·사람 → `20-Company/`
- 일반화된 교훈·기술 패턴 → `30-Development/`
- 같은 인시던트는 두 노트로 나눠 작성 (사내 컨텍스트 + 일반화 교훈)

이유: vault를 외부 공유하거나 회사 떠날 때 `20-Company/` 만 분리/삭제하면 됨.

### 데일리 노트 자동화
- `/daily` 커맨드: 오늘 데일리 노트 생성 (어제의 미완료 태스크 가져옴)
- `/weekly` 커맨드: 이번 주 주간 회고 생성
- `/triage` 커맨드: `00-Inbox/` 노트들 적절한 폴더로 분류 제안

### 검색 우선순위
사용자가 무언가 물어보면:
1. `30-Development/` 우선 검색 (재사용 가능한 지식)
2. `10-Daily/` 최근 7일 (현재 컨텍스트)
3. `20-Company/` (회사 관련 질문일 때만)
4. `00-Inbox/` (마지막 — 분류 전이라 노이즈 많음)

## 금지사항

- ❌ 자격 증명·API 키·토큰 vault에 저장 (별도 비밀 관리 도구 사용)
- ❌ `20-Company/` 내용을 외부 노출 가능한 곳에 복사
- ❌ `_templates/` 직접 수정 — 템플릿 변경은 별도 PR로 논의
- ❌ 파일명에 공백 사용 (위키링크 깨짐)

## 업데이트 정책

이 파일을 수정할 때는:
- 변경 이유를 commit 메시지에 명시
- vault 사용자(본인)가 1주 이상 컨벤션 따라본 후 수정 권장 (조기 최적화 방지)
