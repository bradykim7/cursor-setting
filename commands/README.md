# Commands

Slash commands for Claude Code. Each `.md` file is invoked as `/<filename>`.

Linked into `~/.claude/commands/` by `install.sh`. Routing rules — when each command auto-fires from natural phrasing — live in [`AGENTS.md`](../AGENTS.md#intent-routing--natural-phrasing--action).

> 한국어: [README.kr.md](./README.kr.md)

## Inventory

### Planning lifecycle
| Command | Purpose |
|---------|---------|
| [`/create-plan`](./create-plan.md) | Build a structured implementation plan — research → design → phased plan |
| [`/iterate-plan`](./iterate-plan.md) | Update an existing plan with feedback (research-driven) |
| [`/implement-plan`](./implement-plan.md) | Implement plan phase-by-phase with auto-verification gates |
| [`/validate-plan`](./validate-plan.md) | Verify implementation against the plan's success criteria |

### Research, debug, understanding
| Command | Purpose |
|---------|---------|
| [`/research`](./research.md) | Parallel codebase exploration → research doc |
| [`/debug`](./debug.md) | Broad parallel investigation (logs + git + files) when cause is unknown |

### Test
| Command | Purpose |
|---------|---------|
| [`/affected-endpoints`](./affected-endpoints.md) | Trace HTTP endpoints affected by a code change |
| [`/branch-diff`](./branch-diff.md) | Compare API responses across branches via URL patterns |
| [`/smoke-test`](./smoke-test.md) | Run curl-based smoke tests (Write→Verify supported) |
| [`/test-affected`](./test-affected.md) | Affected-endpoints + smoke test in one pass |

### Commit & PR
| Command | Purpose |
|---------|---------|
| [`/commit-suggest`](./commit-suggest.md) | Recommend a commit message from staged files + history |
| [`/commit-mailplug`](./commit-mailplug.md) | Team-convention commit (ticket ID auto-detected) |
| [`/pr-description`](./pr-description.md) | Generate PR description from diff + commits |
| [`/workfinish`](./workfinish.md) | Commit-suggest + PR description in one run — "wrap up" |
| [`/workcheck`](./workcheck.md) | Mid-work check-in — affected-endpoints + smoke test |

### Session
| Command | Purpose |
|---------|---------|
| [`/handoff`](./handoff.md) | Preserve session context so a future session can resume |
| [`/resume-handoff`](./resume-handoff.md) | Restore context from a handoff doc and continue |

### Claude usage
| Command | Purpose |
|---------|---------|
| [`/claude-usage-collect`](./claude-usage-collect.md) | Extract your own ccusage data into a shareable bundle |
| [`/claude-usage-analyze`](./claude-usage-analyze.md) | Personal ROI / model-routing / session-hygiene report |
| [`/claude-usage-report`](./claude-usage-report.md) | Team-wide report from collected bundles (8 sections; optional Confluence publish) |

### Jira
| Command | Purpose |
|---------|---------|
| [`/jira-daily`](./jira-daily.md) | Analyze today's assigned Jira issues — macOS notification + plan doc |

## Conventions

- Filename = command name (no leading slash).
- Frontmatter `description:` is what's shown above.
- Korean and English commands are both supported; routing matches phrasing in either language.

## Adding a new command

1. Drop `your-command.md` in this directory with frontmatter:
   ```yaml
   ---
   description: One-line summary shown in /help and this README
   ---
   ```
2. Re-run `./install.sh` from the repo root to symlink it into `~/.claude/commands/`.
3. If it should auto-fire from natural phrasing, add a routing entry in [`AGENTS.md`](../AGENTS.md#intent-routing--natural-phrasing--action).
