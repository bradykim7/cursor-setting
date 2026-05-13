#!/usr/bin/env bash
# Stop hook — after Claude finishes responding, remind it to consider saving
# significant learnings to the Obsidian vault.
# stdout is appended to Claude's context; Claude decides whether to act.

VAULT="~/Obsidian"

# Only fire if vault exists (guards against machines without the vault)
[ -d "$VAULT" ] || exit 0

echo "[obsidian] If this session introduced new knowledge, architecture decisions, or tool learnings worth keeping, proactively offer to save a note to $VAULT/30-Development/ (or 20-Company/ if company-specific). Use kebab-case filename + frontmatter. Skip for trivial tasks."
