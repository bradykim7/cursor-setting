# cursor-setting

Claude Code 커스텀 커맨드, 에이전트, 설정을 관리하는 dotfiles 레포입니다.

## Quick Start

```bash
git clone <repo-url> ~/cursor-setting
cd ~/cursor-setting
./install.sh
```

## What's Included

### Commands (20개)

| Category | Commands |
|----------|----------|
| **Plan Lifecycle** | `/create-plan`, `/implement-plan`, `/iterate-plan`, `/validate-plan` |
| **Research & Debug** | `/research`, `/debug` |
| **Session** | `/handoff`, `/resume-handoff` |
| **Test** | `/workcheck`, `/affected-endpoints`, `/smoke-test`, `/branch-diff`, `/test-affected` |
| **Commit & PR** | `/workfinish`, `/commit-mailplug`, `/commit-suggest`, `/pr-description` |
| **Claude Usage** | `/claude-usage-collect`, `/claude-usage-analyze`, `/claude-usage-report` |

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

### Skills (22개)

Ported from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Skills auto-fire when your phrasing matches their `description` field — no slash command needed.

| Category | Skill | Triggers when you say… |
|----------|-------|------------------------|
| **engineering** | `setup-matt-pocock-skills` | "set up the engineering skills for this repo" — run first in any new project |
| | `grill-with-docs` | "stress-test this plan against our domain model" |
| | `to-prd` | "turn this conversation into a PRD" |
| | `to-issues` | "break this plan into issues" |
| | `triage` | "triage these incoming issues" |
| | `tdd` | "let's TDD this", "red-green-refactor" |
| | `diagnose` | "diagnose this bug", "this is broken/throwing/failing" |
| | `improve-codebase-architecture` | "find refactoring opportunities", "improve architecture" |
| | `prototype` | "let me prototype this", "try a few UI variations" |
| | `zoom-out` | "zoom out", "give me the bigger picture" |
| **productivity** | `grill-me` | "grill me on this plan", "interview me" |
| | `caveman` | (terse output mode) |
| | `write-a-skill` | "create a new skill" |
| **misc** | `git-guardrails-claude-code` | "block dangerous git commands", "add git safety hooks" |
| | `setup-pre-commit` | "set up pre-commit hooks", "add Husky + lint-staged" |
| | `migrate-to-shoehorn` | "replace `as` with shoehorn in tests" |
| | `scaffold-exercises` | "scaffold an exercise structure" |
| **personal** | `edit-article` | "edit/revise this article" |
| | `obsidian-vault` | "find/create a note in Obsidian" |
| **in-progress** | `writing-fragments` | "ideate", "fragments", "raw material" |
| | `writing-shape` | "shape these notes into an article" |
| | `writing-beats` | "assemble this as a narrative" |

**Commands vs Agents vs Skills:**
- **Commands** (`/foo`) — you invoke explicitly. Full workflows.
- **Agents** — Claude spawns them automatically inside commands. Specialized single tasks.
- **Skills** — auto-fire from your phrasing. Trigger via `description` matching.

## Project Init

```bash
./install.sh init /path/to/project
```

Creates `CLAUDE.md` + `.handoffs/` + `.plans/` + `.research/` in the target project.

## Obsidian Vault Init

회사 지식 + 개발 지식 축적용 Obsidian vault를 부트스트랩합니다.

```bash
./install.sh obsidian-init ~/Documents/MyVault
```

Creates a vault with:
- 폴더 구조 (`20-Company/` 회사 지식, `30-Development/` 개발 지식 분리)
- 7가지 노트 템플릿 (데일리·미팅·ADR·기술 지식·트러블슈팅·용어집·주간 회고)
- Claude Code 연동 (`CLAUDE.md` + `.claude/commands/` 슬래시 커맨드 3종)
- Obsidian 코어 플러그인 자동 설정

→ [Obsidian Onboarding Guide](docs/obsidian-onboarding.md) 따라하기 (10분)

## Docs

- [Onboarding Guide](docs/onboarding.md) — 처음 사용자를 위한 소개
- [Obsidian Onboarding](docs/obsidian-onboarding.md) — Obsidian vault 단계별 셋업
- [Workflow Reference](WORKFLOW.md) — 전체 커맨드 & 워크플로우 상세
- [Submodule Approach](docs/approach-a-submodule.md) — 팀 공유 시 대안 구조

## Inspired by

- [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) `.claude/` structure
