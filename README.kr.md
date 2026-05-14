# agcoco (한국어)

> **agcoco** = **Ag**ent-**Co**ding-**Co**nfig — "AG-co-co" 라고 읽습니다.
> AI 에이전트 코딩을 위한 개인 dotfiles 레포 (Claude Code, Codex 등 멀티툴 지원).

`AGENTS.md` 컨벤션을 따르는 모든 CLI (Claude Code, Codex, 그리고 `tools/<name>.sh` 로 손쉽게 확장 가능한 Gemini / Cursor / Aider / Continue) 를 위한 커스텀 슬래시 커맨드, 서브 에이전트, 스킬, tool-별 심링크를 관리하는 dotfiles 저장소.

> English: [README.md](./README.md)

## 아키텍처

![agcoco architecture](./architecture.png)

## 빠른 시작

```bash
git clone <repo-url> ~/agcoco
cd ~/agcoco
./install.sh
```

## Layer 01 — Input

![One config, many CLIs](./docs/images/agcoco-01-input.png)

## Layer 02 — Router

![Three ways to fire the loop](./docs/images/agcoco-02-router.png)

## Layer 03 — Integration

![One source, symlinked everywhere](./docs/images/agcoco-03-integration.png)

**다른 도구 추가** — Gemini, Cursor agent, Aider, Continue 등:

```bash
cp tools/_template.sh tools/<your-tool>.sh
$EDITOR tools/<your-tool>.sh    # 4개 변수 입력: TOOL_NAME, TOOL_CMD, TOOL_DIR, TOOL_SYMLINKS
./install.sh                    # 다음 실행부터 자동 감지
```

`_template.sh` 에 Gemini, Cursor, Aider, Continue 예제 정의가 주석 처리되어 있음. 컨벤션 상세는 `tools/README.md` 참조. CLI 가 설치되지 않은 도구는 "건너뛴 툴" 에 표시되고 조용히 스킵.

## Layer 04 — Core

![The agent loop](./docs/images/agcoco-04-core.png)

## Layer 05 — Commands

![Twenty-one workflows behind a slash](./docs/images/agcoco-05-commands.png)

## Layer 06 — Agents

![Twelve specialists on Sonnet](./docs/images/agcoco-06-agents.png)

## Layer 07 — Skills

![Twenty-two habits, autoloaded](./docs/images/agcoco-07-skills.png)

[mattpocock/skills](https://github.com/mattpocock/skills) (MIT) 에서 포팅. 사용자 문구가 스킬의 `description` 필드와 매치되면 자동 발화 — 슬래시 커맨드 불필요.

## Layer 08 — Plugins

![Six marketplace bundles](./docs/images/agcoco-08-plugins.png)

플러그인 마켓플레이스로 묶음 설치:

```bash
/plugin marketplace add mskim/Agcoco
/plugin install engineering-skills@agcoco
/plugin install workflow@agcoco
```

## Layer 09 — Memory

![Markdown on disk is the memory](./docs/images/agcoco-09-memory.png)

### 프로젝트 초기화

```bash
./install.sh init /path/to/project
```

대상 프로젝트에 `CLAUDE.md` + `.handoffs/` + `.plans/` + `.research/` 생성.

### Obsidian 볼트 초기화

회사 지식 + 개발 지식 축적용 Obsidian 볼트를 부트스트랩.

```bash
./install.sh obsidian-init ~/Documents/MyVault
```

생성 항목:
- 폴더 구조 (`20-Company/` 회사 지식, `30-Development/` 개발 지식 분리)
- 7가지 노트 템플릿 (데일리·미팅·ADR·기술 지식·트러블슈팅·용어집·주간 회고)
- Claude Code 연동 (`CLAUDE.md` + `.claude/commands/` 슬래시 커맨드 3종)
- Obsidian 코어 플러그인 자동 설정

→ [Obsidian Onboarding Guide](docs/obsidian-onboarding.md) 따라하기 (10분)

## Layer 10 — Output

![What lands in your repo](./docs/images/agcoco-10-output.png)

## Layer 11 — Hooks

![Four guardrails the agent can't dodge](./docs/images/agcoco-11-hooks.png)

## 문서

### 컴포넌트 레퍼런스
- [슬래시 커맨드](docs/commands.kr.md) ([EN](docs/commands.en.md)) — 카테고리별 21개 커맨드
- [서브 에이전트](docs/agents.kr.md) ([EN](docs/agents.en.md)) — Claude 가 spawn 하는 12개 전문 에이전트
- [Hooks](docs/hooks.kr.md) ([EN](docs/hooks.en.md)) — 4개 라이프사이클 hook 스크립트
- [Scripts](docs/scripts.kr.md) ([EN](docs/scripts.en.md)) — 독립 실행 셸 헬퍼
- [Plugins](docs/plugins.kr.md) ([EN](docs/plugins.en.md)) — 6개 플러그인 마켓플레이스 번들

### 가이드
- [Onboarding Guide](docs/onboarding.md) — 처음 사용자를 위한 소개
- [Obsidian Onboarding](docs/obsidian-onboarding.md) — Obsidian 볼트 단계별 셋업
- [Workflow Reference](WORKFLOW.md) — 전체 커맨드 & 워크플로우 상세
- [Submodule Approach](docs/approach-a-submodule.md) — 팀 공유 시 대안 구조

## 영감받은 곳

- [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) `.claude/` 구조
