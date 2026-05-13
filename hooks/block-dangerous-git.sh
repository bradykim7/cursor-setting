#!/usr/bin/env bash
# PreToolUse: Bash — block destructive commands before Claude runs them.
# Refined from skills/misc/git-guardrails-claude-code: allows normal git push
# (needed for /workfinish), but blocks force-push to main/master, hard resets,
# and other irrecoverable operations.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[ -z "$COMMAND" ] && exit 0

block() {
  echo "BLOCKED: $1" >&2
  echo "Command was: $COMMAND" >&2
  exit 2
}

# Force push to main/master (either order of --force and target)
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push.*(--force|--force-with-lease|[[:space:]]-f([[:space:]]|$)).*(main|master)([[:space:]]|$)'; then
  block "git push --force to main/master is irrecoverable."
fi
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push.*(main|master)([[:space:]]|$).*(--force|--force-with-lease|[[:space:]]-f([[:space:]]|$))'; then
  block "git push --force to main/master is irrecoverable."
fi

# Hard reset — discards uncommitted work silently
if echo "$COMMAND" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard'; then
  block "git reset --hard discards uncommitted work. Use 'git stash' or run via shell directly if intentional."
fi

# git clean -f / -fd / -fdx — permanently removes untracked files
if echo "$COMMAND" | grep -qE 'git[[:space:]]+clean[[:space:]]+(-[a-zA-Z]*f|--force)'; then
  block "git clean -f permanently removes untracked files."
fi

# Force-delete main/master local branch
if echo "$COMMAND" | grep -qE 'git[[:space:]]+branch[[:space:]]+-D[[:space:]]+(main|master)([[:space:]]|$)'; then
  block "Refuse to force-delete main/master branch."
fi

# git checkout . / git restore . — discards every uncommitted change
if echo "$COMMAND" | grep -qE 'git[[:space:]]+(checkout|restore)[[:space:]]+\.([[:space:]]|$)'; then
  block "git checkout . / git restore . discards all uncommitted changes."
fi

# rm -rf on root or home
if echo "$COMMAND" | grep -qE 'rm[[:space:]]+(-[rRf]+|--recursive|--force).*[[:space:]](/|~)([[:space:]]|/?\*|$)'; then
  block "rm -rf on root or home directory."
fi

exit 0
