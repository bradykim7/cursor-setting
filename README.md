# agcoco

> **agcoco** = **Ag**ent-**Co**ding-**Co**nfig — pronounced "AG-co-co".
> Personal dotfiles repo for AI agent-assisted coding.

Manages custom slash commands, sub-agents, skills, and per-tool symlinks for any CLI that follows the `AGENTS.md` convention (Claude Code, Codex, and easily extensible to Gemini / Cursor / Aider / Continue via `tools/<name>.sh`).

> Korean / 한국어: [README.kr.md](./README.kr.md)

## Architecture

![agcoco architecture](./architecture.png)

## Quick Start

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

**Add any other tool** — Gemini, Cursor agent, Aider, Continue, etc:

```bash
cp tools/_template.sh tools/<your-tool>.sh
$EDITOR tools/<your-tool>.sh    # fill in 4 vars: TOOL_NAME, TOOL_CMD, TOOL_DIR, TOOL_SYMLINKS
./install.sh                    # auto-detected from the next run on
```

`_template.sh` has commented-out example definitions for Gemini, Cursor, Aider, and Continue. See `tools/README.md` for the convention details. Tools whose CLI isn't installed are listed under the "skipped tools" section and skipped silently.

## Layer 04 — Core

![The agent loop](./docs/images/agcoco-04-core.png)

## Layer 05 — Commands

![Twenty-one workflows behind a slash](./docs/images/agcoco-05-commands.png)

## Layer 06 — Agents

![Twelve specialists on Sonnet](./docs/images/agcoco-06-agents.png)

## Layer 07 — Skills

![Twenty-two habits, autoloaded](./docs/images/agcoco-07-skills.png)

Ported from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Skills auto-fire when your phrasing matches their `description` field — no slash command needed.

## Layer 08 — Plugins

![Six marketplace bundles](./docs/images/agcoco-08-plugins.png)

Install bundles via the plugin marketplace:

```bash
/plugin marketplace add mskim/Agcoco
/plugin install engineering-skills@agcoco
/plugin install workflow@agcoco
```

## Layer 09 — Memory

![Markdown on disk is the memory](./docs/images/agcoco-09-memory.png)

### Project Init

```bash
./install.sh init /path/to/project
```

Creates `CLAUDE.md` + `.handoffs/` + `.plans/` + `.research/` in the target project.

### Obsidian Vault Init

Bootstraps an Obsidian vault for accumulating company knowledge + development knowledge.

```bash
./install.sh obsidian-init ~/Documents/MyVault
```

Creates a vault with:
- Folder structure (`20-Company/` for company knowledge, `30-Development/` for general dev knowledge — kept separate)
- 7 note templates (daily, meeting, ADR, tech knowledge, troubleshooting, glossary, weekly review)
- Claude Code integration (`CLAUDE.md` + `.claude/commands/` with 3 slash commands)
- Auto-configured Obsidian core plugins

→ Follow the [Obsidian Onboarding Guide](docs/obsidian-onboarding.md) (10 minutes)

## Layer 10 — Output

![What lands in your repo](./docs/images/agcoco-10-output.png)

## Layer 11 — Hooks

![Four guardrails the agent can't dodge](./docs/images/agcoco-11-hooks.png)

## Docs

### Component reference
- [Slash Commands](docs/commands.en.md) ([KR](docs/commands.kr.md)) — 21 commands grouped by category
- [Sub-agents](docs/agents.en.md) ([KR](docs/agents.kr.md)) — 12 specialized agents Claude spawns
- [Hooks](docs/hooks.en.md) ([KR](docs/hooks.kr.md)) — 4 lifecycle hook scripts
- [Scripts](docs/scripts.en.md) ([KR](docs/scripts.kr.md)) — Standalone shell helpers
- [Plugins](docs/plugins.en.md) ([KR](docs/plugins.kr.md)) — 6 plugin marketplace bundles

### Guides
- [Onboarding Guide](docs/onboarding.md) — Intro for first-time users
- [Obsidian Onboarding](docs/obsidian-onboarding.md) — Step-by-step Obsidian vault setup
- [Workflow Reference](WORKFLOW.md) — Full command & workflow reference
- [Submodule Approach](docs/approach-a-submodule.md) — Alternative structure for team sharing

## Inspired by

- [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) `.claude/` structure
