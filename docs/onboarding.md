# cursor-setting 온보딩 가이드

> Claude Code를 처음 사용하는 사람을 위한 소개 문서입니다.

---

## cursor-setting이란?

Claude Code에서 사용하는 **커스텀 커맨드, 에이전트, 설정**을 모아둔 dotfiles 레포입니다.
한 번 설치하면 어떤 프로젝트에서든 `/커맨드이름`으로 바로 사용할 수 있습니다.

---

## 동작 원리

### 전체 구조

```
cursor-setting/              ← 이 레포 (한 곳에 clone)
├── commands/*.md            ← 슬래시 커맨드 정의 (17개)
├── agents/claude-code/*.md  ← AI 서브에이전트 정의 (12개)
└── settings.json            ← 글로벌 설정

        │  install.sh (symlink 생성)
        ▼

~/.claude/                   ← Claude Code가 읽는 글로벌 설정 디렉토리
├── commands/ → cursor-setting/commands/
├── agents/  → cursor-setting/agents/claude-code/
└── settings.json → cursor-setting/settings.json
```

`install.sh`가 **symlink**를 생성하므로, cursor-setting에서 파일을 수정하면 즉시 반영됩니다.

### 커맨드 (commands/)

```
commands/
├── create-plan.md       ← /create-plan 으로 호출됨
├── implement-plan.md    ← /implement-plan 으로 호출됨
├── handoff.md           ← /handoff 로 호출됨
└── ...
```

- **파일명 = 커맨드 이름**: `handoff.md` → `/handoff`
- **트리거 방법**: Claude Code 채팅에서 `/커맨드이름` 입력
- **동작 방식**: `.md` 파일 안의 지시문을 Claude가 읽고 그대로 수행
- **구조**:
  ```markdown
  ---
  description: 커맨드 설명 (자동완성에 표시됨)
  allowed-tools: 이 커맨드가 사용할 수 있는 도구 목록
  argument-hint: [파라미터 힌트]
  ---

  # 커맨드 제목

  Claude에게 주는 지시문...
  (Step 1, Step 2, ... 형태로 워크플로우 정의)
  ```

### 에이전트 (agents/)

```
agents/claude-code/
├── codebase-analyzer.md       ← 코드 구현 분석
├── codebase-locator.md        ← 파일 위치 탐색
├── docs-locator.md            ← 과거 문서 검색
└── ...
```

- **역할**: 특정 전문 분야에 특화된 AI 서브에이전트
- **트리거 방법**: Claude가 작업 중 필요할 때 **자동으로** spawn
- **사용자가 직접 호출하지 않음** — 커맨드가 내부적으로 호출
- **Sonnet 모델 사용** — 메인 Opus보다 빠르고 저렴

### settings.json

```json
{
  "model": "opus"
}
```

- Claude Code의 글로벌 동작 설정 (기본 모델, 권한 등)

### CLAUDE.md (프로젝트별)

```
my-project/
├── CLAUDE.md    ← 이 프로젝트 전용 AI 지침
├── .handoffs/   ← 세션 인수인계 문서
├── .plans/      ← 구현 계획서
├── .research/   ← 리서치 문서
├── src/
└── ...
```

- **위치**: 각 프로젝트 루트
- **역할**: "이 프로젝트는 Java/Spring이고, 빌드는 `./gradlew build`, 테스트는 ..."
- **생성 방법**: `./install.sh init /path/to/project`
- Claude Code가 해당 프로젝트에서 실행될 때 **자동으로** 읽음

---

## 설치 방법

### 1. 레포 클론

```bash
git clone <cursor-setting-repo-url> ~/cursor-setting
```

### 2. 글로벌 설치

```bash
cd ~/cursor-setting
./install.sh
```

이것만으로 `~/.claude/`에 symlink가 생성되고, 모든 커맨드를 사용할 수 있습니다.

### 3. (선택) 프로젝트별 초기화

```bash
./install.sh init ~/my-project
```

프로젝트에 `CLAUDE.md` + 작업 디렉토리(`.handoffs/`, `.plans/`, `.research/`)가 생성됩니다.
`CLAUDE.md`의 TODO 항목을 프로젝트에 맞게 편집하세요.

---

## 커맨드 카테고리

### 계획 라이프사이클

| 커맨드 | 언제 쓰나 |
|--------|----------|
| `/create-plan` | 새 기능 구현 전 계획을 체계적으로 세울 때 |
| `/implement-plan` | 계획서를 Phase별로 구현할 때 |
| `/iterate-plan` | 피드백으로 기존 계획서를 수정할 때 |
| `/validate-plan` | 구현 완료 후 계획대로 됐는지 검증할 때 |

### 리서치 & 디버깅

| 커맨드 | 언제 쓰나 |
|--------|----------|
| `/research` | 코드베이스를 파악하고 문서로 남기고 싶을 때 |
| `/debug` | 에러가 발생해서 원인을 찾아야 할 때 |

### 세션 관리

| 커맨드 | 언제 쓰나 |
|--------|----------|
| `/handoff` | 오늘 작업을 중단하고 내일 이어가야 할 때 |
| `/resume-handoff` | 이전 세션의 핸드오프에서 작업을 재개할 때 |

### 테스트 & 검증

| 커맨드 | 언제 쓰나 |
|--------|----------|
| `/workcheck` | 코드 수정 후 영향 분석 + 스모크 테스트 한번에 |
| `/affected-endpoints` | 변경한 코드가 어떤 API에 영향 주는지 확인 |
| `/smoke-test` | 특정 엔드포인트 수동 테스트 |
| `/branch-diff` | master 대비 API 응답 차이 비교 |
| `/test-affected` | 영향 엔드포인트 추적 + 자동 스모크 |

### 커밋 & PR

| 커맨드 | 언제 쓰나 |
|--------|----------|
| `/workfinish` | 커밋 메시지 추천 + PR 설명 한번에 |
| `/commit-mailplug` | 팀 컨벤션에 맞는 커밋 메시지 추천 |
| `/commit-suggest` | 일반 커밋 메시지 추천 |
| `/pr-description` | PR 설명 자동 생성 |

---

## 에이전트 — 자동으로 동작하는 전문가들

커맨드를 실행하면 Claude가 **자동으로** 서브에이전트를 호출합니다.
사용자가 직접 부르지 않아도, 뒤에서 병렬로 작업합니다.

### 코드 탐색 에이전트

| 에이전트 | 하는 일 | 호출하는 커맨드 |
|----------|--------|---------------|
| `codebase-locator` | 파일 위치 찾기 (Super Grep) | create-plan, research, implement-plan, debug |
| `codebase-analyzer` | 코드 구현 상세 분석 | create-plan, research, debug |
| `codebase-pattern-finder` | 유사 패턴/예시 탐색 | create-plan, research, implement-plan |

### 지식 관리 에이전트

| 에이전트 | 하는 일 | 호출하는 커맨드 |
|----------|--------|---------------|
| `docs-locator` | 과거 계획서/리서치/핸드오프 검색 | create-plan, research, resume-handoff, debug |
| `docs-analyzer` | 과거 문서에서 인사이트 추출 | resume-handoff, iterate-plan |

### 리뷰 & 분석 에이전트

| 에이전트 | 하는 일 |
|----------|--------|
| `web-search-researcher` | 웹에서 최신 정보 검색 |
| `architecture-review` | 아키텍처 리스크 분석 |
| `endpoint-analysis` | API 엔드포인트 계약 분석 |
| `pr-review-assistant` | PR 리스크 리뷰 |
| `consistency-check` | 데이터 정합성 비교 |
| `document-summarizer` | 문서 요약 & 구조화 |
| `pr-description-generator` | PR 설명 자동 생성 |

### 동작 예시

```
사용자: /create-plan 메일 검색 필터 추가

Claude (Opus):
  ├─ spawn codebase-locator (Sonnet)       ← 관련 파일 찾기
  ├─ spawn codebase-analyzer (Sonnet)      ← 기존 구현 분석
  ├─ spawn codebase-pattern-finder (Sonnet) ← 유사 패턴 검색
  ├─ spawn docs-locator (Sonnet)           ← 과거 관련 문서 탐색
  └─ 종합하여 구현 계획서 작성
```

---

## 예시: 실제 작업 흐름

### 시나리오: 새 기능 구현 (Full Lifecycle)

```
── Day 1 오전 ──

/research 결제 모듈 구조 분석          ← 코드베이스 파악
/create-plan 결제 수단 추가 기능       ← 구현 계획 수립
/iterate-plan Phase 2 분리 필요        ← 피드백으로 계획 수정

── Day 1 오후 ──

/implement-plan                        ← Phase 1 구현
/debug 결제 API 500 에러              ← 문제 발생 시 조사
/handoff                              ← 퇴근 전 인수인계 문서 작성

── Day 2 오전 ──

/resume-handoff                       ← 어제 컨텍스트 복원
/implement-plan                       ← Phase 2 이어서 구현
/validate-plan                        ← 구현 결과 전체 검증
/workcheck                            ← 영향 분석 + 스모크 테스트
/workfinish                           ← 커밋 + PR 설명 생성
```

### 시나리오: 빠른 버그 수정

```
/debug 로그인 실패 에러               ← 원인 조사
# 수정 작업...
/workfinish                           ← 커밋 + PR
```

---

## 커맨드 커스터마이징

새 커맨드를 추가하고 싶다면:

1. `commands/` 디렉토리에 `my-command.md` 파일 생성
2. frontmatter(`---`) + 지시문 작성
3. 바로 `/my-command`로 사용 가능 (symlink이므로 즉시 반영)

```markdown
---
description: 내 커맨드 설명
allowed-tools: Read, Grep, Bash(git:*)
---

# My Command

Claude에게 주는 지시문을 여기에 작성...
```

---

## 참고

- 상세 워크플로우: [WORKFLOW.md](../WORKFLOW.md)
- Submodule 방식 전환 참고: [approach-a-submodule.md](approach-a-submodule.md)
