# 서브 에이전트 (한국어)

Claude Code 가 `Agent` 도구로 호출하는 전문 에이전트. [`agents/claude-code/`](../agents/claude-code/) 의 각 `.md` 는 이름·설명·모델·시스템 프롬프트를 포함한 독립 정의 파일.

사용자가 직접 부르는 것이 아니라, 작업이 해당 에이전트의 `description` 과 매치되면 Claude 가 선택합니다 — description 이 곧 라우터.

> English: [agents.md](./agents.md)

## 목록

### 코드베이스 탐색
| 에이전트 | 모델 | 언제 |
|----------|------|------|
| [`codebase-locator`](../agents/claude-code/codebase-locator.md) | sonnet | "이 코드 어디 있어?" — Super Grep/Glob |
| [`codebase-analyzer`](../agents/claude-code/codebase-analyzer.md) | sonnet | "이 로직 어떻게 동작해?" — 데이터 흐름·로직 분석 |
| [`codebase-pattern-finder`](../agents/claude-code/codebase-pattern-finder.md) | sonnet | "비슷한 패턴 있어?" — 구체 코드 포함 유사 구현 탐색 |

### 리뷰 & 분석
| 에이전트 | 모델 | 언제 |
|----------|------|------|
| [`architecture-review`](../agents/claude-code/architecture-review.md) | opus | 아키텍처 제안 검토 — 확장성·복원력·보안 경계·장애 격리 |
| [`pr-review-assistant`](../agents/claude-code/pr-review-assistant.md) | sonnet | 리스크 중심 PR 리뷰 — 하위호환·보안·성능·null·관측성 |
| [`endpoint-analysis`](../agents/claude-code/endpoint-analysis.md) | sonnet | API 엔드포인트 분석 — 동작·계약·검증·테스트 케이스 |
| [`consistency-check`](../agents/claude-code/consistency-check.md) | haiku | 두 데이터 스냅샷 비교, 심각도 분류 |

### 문서 & 리서치
| 에이전트 | 모델 | 언제 |
|----------|------|------|
| [`docs-locator`](../agents/claude-code/docs-locator.md) | sonnet | 과거 핸드오프 / 계획 / 리서치 문서 찾기 |
| [`docs-analyzer`](../agents/claude-code/docs-analyzer.md) | sonnet | 과거 문서에서 고가치 인사이트 추출 |
| [`document-summarizer`](../agents/claude-code/document-summarizer.md) | haiku | 결정 / 리스크 / 다음 액션 / 미해결 질문으로 정규화 |
| [`web-search-researcher`](../agents/claude-code/web-search-researcher.md) | sonnet | 최신 문서·베스트 프랙티스·비교 자료 웹 검색 |

### PR 생성
| 에이전트 | 모델 | 언제 |
|----------|------|------|
| [`pr-description-generator`](../agents/claude-code/pr-description-generator.md) | haiku | git 변경 + 커밋 + 연결 티켓으로 PR 설명 작성 |

## 모델 선택 기준

- **`opus`** — 멀티스텝 추론, 리스크 분석, 횡단 리뷰.
- **`sonnet`** — 일반 탐색·분석·작성 작업.
- **`haiku`** — 경계가 명확한 구조적 작업 (요약·비교·포맷). 빠르고 저렴.

새 에이전트를 만들 때는 평가 통과 가능한 가장 저렴한 등급을 선택하세요.

## 규칙

- 파일명 = frontmatter `name:` 필드 (kebab-case).
- `description:` 은 Claude 가 라우팅 시 보는 유일한 텍스트 — 일반 산문이 아닌 "Use this agent when…" 라우팅 카피로 작성.
- description 에 예시 입력 2–3 개 포함 → Claude 가 패턴 매칭을 안정적으로 수행.

## 새 에이전트 추가

1. `your-agent.md` 를 [`agents/claude-code/`](../agents/claude-code/) 에 frontmatter 와 함께 작성:
   ```yaml
   ---
   name: your-agent
   description: Use this agent when … Examples: "...", "...", "..."
   model: sonnet
   tools: Read, Grep, Glob, Bash
   ---
   ```
2. 시스템 프롬프트 본문 작성. 에이전트 하나당 한 가지 일에 집중.
3. `./install.sh` 재실행 → `~/.claude/agents/claude-code/` 로 심링크.
