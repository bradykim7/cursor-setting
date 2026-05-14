---
name: obsidian-vault
description: Search, create, and manage notes in the Obsidian vault. Use when user wants to find, create, or organize notes — or when significant knowledge, architecture decisions, or new tool learnings should be saved.
---

# Obsidian Vault

## Vault location

`${OBSIDIAN_VAULT:-$HOME/Obsidian}` — set `OBSIDIAN_VAULT` env var in your shell to override the default.

## Folder structure

| Folder | What goes here |
|--------|---------------|
| `00-Inbox/` | Quick captures — unclassified, clear weekly |
| `10-Daily/` | Daily logs (`YYYY-MM-DD.md`) |
| `20-Company/` | Company-specific: meetings, decisions, people, glossary |
| `30-Development/` | General tech knowledge (patterns, troubleshooting, snippets, learning) |
| `40-Projects/` | Active projects — move to `90-Archive/` when done |
| `90-Archive/` | Completed/inactive |
| `_templates/` | Note templates (don't edit directly) |
| `_attachments/` | Images, PDFs (auto-managed by Obsidian) |

**Key rule — separate company vs general knowledge:**
- Company-specific context → `20-Company/`
- Generalizable lessons/patterns → `30-Development/`
- Same incident? Write two notes (one each).

## Naming conventions

- **kebab-case**: `claude-code-plugin-marketplace.md`
- Lowercase, hyphens instead of spaces
- Date prefix only when meaningful: `2026-05-13-architecture-decision.md`
- Korean OK, prefer hyphens over spaces

## Frontmatter (required on every note)

```yaml
---
type: tech-knowledge | meeting | decision | troubleshooting | glossary | daily | weekly
date: YYYY-MM-DD
tags:
  - area/tag
  - topic/tag
---
```

## Wikilinks

- Use `[[note-name]]` or `[[note-name|display text]]`
- Link to related notes at the bottom of each note
- First mention of a glossary term → always wikilink

## Workflows

### Search for notes

```bash
VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian}"

# By filename
find "$VAULT" -name "*.md" | grep -i "keyword"

# By content
grep -rl "keyword" "$VAULT" --include="*.md"
```

### Create a new note

1. Pick the right folder (when in doubt → `00-Inbox/`)
2. kebab-case filename
3. Apply the matching template from `_templates/`
4. Fill in frontmatter
5. Wikilink to related notes at the bottom

### Decide where a note goes

```
Is it specific to current company/team?
  Yes → 20-Company/{meetings|decisions|glossary|people}/
  No  → Is it a generalizable pattern/lesson?
          Yes → 30-Development/{patterns|troubleshooting|snippets|learning}/
          No  → 00-Inbox/ (classify later)
```
