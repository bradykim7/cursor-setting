# cursor-setting

Claude Code 커스텀 커맨드, 에이전트, 설정을 관리하는 dotfiles 레포입니다.

## Quick Start

```bash
git clone <repo-url> ~/cursor-setting
cd ~/cursor-setting
./install.sh
```

## What's Included

### Commands (17개)

| Category | Commands |
|----------|----------|
| **Plan Lifecycle** | `/create-plan`, `/implement-plan`, `/iterate-plan`, `/validate-plan` |
| **Research & Debug** | `/research`, `/debug` |
| **Session** | `/handoff`, `/resume-handoff` |
| **Test** | `/workcheck`, `/affected-endpoints`, `/smoke-test`, `/branch-diff`, `/test-affected` |
| **Commit & PR** | `/workfinish`, `/commit-mailplug`, `/commit-suggest`, `/pr-description` |

### Agents (12개)

Commands trigger these automatically — you don't call them directly.

| Agent | Role |
|-------|------|
| `codebase-analyzer` | Code implementation analysis |
| `codebase-locator` | File/component location (Super Grep) |
| `codebase-pattern-finder` | Find similar patterns + code examples |
| `docs-locator` | Search past plans/research/handoffs |
| `docs-analyzer` | Extract insights from past documents |
| `web-search-researcher` | Web search for up-to-date info |
| `architecture-review` | Architecture risk analysis |
| `endpoint-analysis` | API endpoint behavior analysis |
| `pr-review-assistant` | PR risk-focused review |
| `consistency-check` | Data snapshot comparison |
| `document-summarizer` | Document summarization |
| `pr-description-generator` | PR description generation |

## Project Init

```bash
./install.sh init /path/to/project
```

Creates `CLAUDE.md` + `.handoffs/` + `.plans/` + `.research/` in the target project.

## Docs

- [Onboarding Guide](docs/onboarding.md) — 처음 사용자를 위한 소개
- [Workflow Reference](WORKFLOW.md) — 전체 커맨드 & 워크플로우 상세
- [Submodule Approach](docs/approach-a-submodule.md) — 팀 공유 시 대안 구조

## Inspired by

- [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) `.claude/` structure
