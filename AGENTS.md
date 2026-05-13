# Global Agent Memory

Canonical agent context shared by every CLI that follows the `AGENTS.md` convention. `install.sh` symlinks this file to:

- `~/.claude/CLAUDE.md` — Claude Code (loaded every session)
- `~/.codex/AGENTS.md` — Codex CLI (when installed)
- `CLAUDE.md` (sibling in this repo) → symlink to `AGENTS.md` so local Claude Code sessions in `agcoco/` also see it

Keep it tight — it's always in context.

## Repo structure

| Directory | Purpose |
|-----------|---------|
| `commands/` | Slash command markdown files → symlinked to `~/.claude/commands/` |
| `skills/` | Skill SKILL.md files → symlinked to `~/.claude/skills/` |
| `hooks/` | PreToolUse/SessionStart hook scripts → symlinked to `~/.claude/hooks/` |
| `plugins/` | Claude Code plugin marketplace structure |
| `agents/` | Agent definition files |
| `tools/` | Install script tool registry |

## Setup & plugin install

```bash
# 개인 설치 (심링크 방식)
./install.sh

# 플러그인 마켓플레이스로 설치
/plugin marketplace add mskim/Agcoco
/plugin install engineering-skills@agcoco
/plugin install workflow@agcoco
```

## Routing: command vs agent vs skill

| Type | Who invokes | When |
|------|-------------|------|
| **Command** (`/foo`) | User explicitly | Full workflow with multiple steps |
| **Agent** | Claude auto-spawns inside a command | Specialized single task (codebase search, doc analysis) |
| **Skill** | Auto-fires from user phrasing | When user's words match the skill's `description` field |

**Default precedence**: if user invokes a command, run it. Otherwise check if a skill should auto-fire. Use agents only for delegation inside commands.

## Skill trigger map (auto-fire on these phrases)

| User says… | Fires |
|------------|-------|
| "grill me" / "interview me on this plan" | `grill-me` |
| "zoom out" / "bigger picture" / "context for this" | `zoom-out` |
| "diagnose this" / "this is broken/throwing" / "perf regression" | `diagnose` |
| "let's TDD" / "red-green-refactor" | `tdd` |
| "prototype this" / "try a few UI variations" | `prototype` |
| "find refactoring opportunities" / "improve architecture" | `improve-codebase-architecture` |
| "turn this conversation into a PRD" | `to-prd` |
| "break this plan into issues" | `to-issues` |
| "triage these issues" | `triage` |
| "set up pre-commit hooks" / "Husky + lint-staged" | `setup-pre-commit` |
| "block dangerous git commands" | `git-guardrails-claude-code` |

## Overlap rules (use this, not that)

- **`/debug` vs `diagnose`** — `/debug` for broad parallel investigation when the bug is unknown. `diagnose` (skill) for hard-to-reproduce bugs needing strict reproduce → minimize → instrument loop. If user names the symptom but not cause, lean `/debug`. If they say "diagnose this", lean `diagnose`.
- **`/handoff` (command) only** — there is no `handoff` skill (deleted as duplicate). Always use `/handoff` and pair with `/resume-handoff`.
- **`/create-plan` vs `grill-with-docs` + `to-prd` + `to-issues`** — `/create-plan` is one-shot and faster. The skill chain is incremental and produces persistent artifacts (PRDs + issues). Pick by user signal: ad-hoc planning → command; formal scoping → skill chain.

## Per-repo behavior

- **In `agcoco/`**: read `WORKFLOW.md` upfront before suggesting workflow changes — it's the source of truth for commands/agents/skills inventory.
- **In a fresh project (no `AGENTS.md`/`CLAUDE.md` with `## Agent skills` block)**: suggest running `setup-matt-pocock-skills` skill first to bootstrap context for `tdd`, `triage`, `to-prd`, `to-issues`, `diagnose`, etc.

## Anti-patterns to avoid

- Don't spawn agents for trivial work (single file read, simple grep) — call the tool directly.
- Don't invoke a skill the user didn't trigger. Skills fire on user phrasing, not your interpretation.
- Don't paraphrase command flows; if `/workcheck` exists for a flow, suggest the command, don't reimplement it manually.

## Behavioral guidelines

**Tradeoff:** These bias toward caution over speed. Use judgment for trivial tasks.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```
