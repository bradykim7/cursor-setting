#!/usr/bin/env bash
# PreToolUse: Bash — block destructive commands before Claude runs them.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[ -z "$COMMAND" ] && exit 0

block() {
  echo "BLOCKED: $1" >&2
  echo "Command was: $COMMAND" >&2
  exit 2
}

# ─── GIT: commit & push (always require human) ───────────────────────────────

if echo "$COMMAND" | grep -qE 'git[[:space:]]+commit([[:space:]]|$)'; then
  block "git commit is reserved for the user. Stage changes and let the user commit manually."
fi

if echo "$COMMAND" | grep -qE 'git[[:space:]]+push([[:space:]]|$)'; then
  block "git push is reserved for the user. Run manually when ready."
fi

# ─── GIT: force push ──────────────────────────────────────────────────────────

# Force push to main/master
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push.*(--force|--force-with-lease|[[:space:]]-f([[:space:]]|$)).*(main|master)([[:space:]]|$)'; then
  block "git push --force to main/master is irrecoverable."
fi
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push.*(main|master)([[:space:]]|$).*(--force|--force-with-lease|[[:space:]]-f([[:space:]]|$))'; then
  block "git push --force to main/master is irrecoverable."
fi

# Delete remote branch
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push[[:space:]]+.*--delete'; then
  block "git push --delete removes a remote branch permanently. Run manually if intentional."
fi
if echo "$COMMAND" | grep -qE 'git[[:space:]]+push[[:space:]]+.*:[[:space:]]*[a-zA-Z]'; then
  block "git push origin :branch deletes a remote branch. Run manually if intentional."
fi

# ─── GIT: history rewrite ────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE 'git[[:space:]]+(filter-branch|filter-repo)'; then
  block "git filter-branch/filter-repo rewrites history and is hard to recover from."
fi

if echo "$COMMAND" | grep -qE 'git[[:space:]]+rebase.*(main|master)'; then
  block "git rebase onto main/master rewrites commit history. Run manually if intentional."
fi

# Amend a pushed commit
if echo "$COMMAND" | grep -qE 'git[[:space:]]+commit[[:space:]]+.*--amend'; then
  block "git commit --amend on a pushed commit causes divergence. Run manually if intentional."
fi

# ─── GIT: discard changes ────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard'; then
  block "git reset --hard discards uncommitted work. Use 'git stash' or run manually if intentional."
fi

if echo "$COMMAND" | grep -qE 'git[[:space:]]+clean[[:space:]]+(-[a-zA-Z]*f|--force)'; then
  block "git clean -f permanently removes untracked files."
fi

if echo "$COMMAND" | grep -qE 'git[[:space:]]+(checkout|restore)[[:space:]]+\.([[:space:]]|$)'; then
  block "git checkout . / git restore . discards all uncommitted changes."
fi

# ─── GIT: branch deletion ────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE 'git[[:space:]]+branch[[:space:]]+-D[[:space:]]+(main|master)([[:space:]]|$)'; then
  block "Refuse to force-delete main/master branch."
fi

# ─── FILE SYSTEM: rm ─────────────────────────────────────────────────────────

# rm -rf on root or home
if echo "$COMMAND" | grep -qE 'rm[[:space:]]+(-[rRf]+|--recursive|--force).*[[:space:]](/|~)([[:space:]]|/?\*|$)'; then
  block "rm -rf on root or home directory."
fi

# rm -rf . (current directory)
if echo "$COMMAND" | grep -qE 'rm[[:space:]]+(-[rRf]+|--recursive)[[:space:]]+\.([[:space:]]|$)'; then
  block "rm -rf . deletes the entire current directory."
fi

# sudo rm anything
if echo "$COMMAND" | grep -qE 'sudo[[:space:]]+rm'; then
  block "sudo rm is too dangerous to run autonomously. Run manually if intentional."
fi

# ─── FILE SYSTEM: overwrite via redirect ─────────────────────────────────────

# Overwriting known critical files with > redirect
if echo "$COMMAND" | grep -qE '>[[:space:]]*(CLAUDE\.md|AGENTS\.md|settings\.json|\.env|package\.json|composer\.json)'; then
  block "Redirecting output to a critical config file could destroy it. Use Edit tool instead."
fi

# ─── PERMISSIONS ─────────────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE 'chmod[[:space:]]+(-[rR][[:space:]]+)?777'; then
  block "chmod 777 makes files world-writable. Too permissive to run autonomously."
fi

# ─── REMOTE CODE EXECUTION ───────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE '(curl|wget)[[:space:]].*\|[[:space:]]*(bash|sh|zsh|python|ruby|node)'; then
  block "Piping remote content directly to a shell is a code injection risk."
fi

# ─── DATABASE ────────────────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qiE '(DROP[[:space:]]+(DATABASE|TABLE|SCHEMA)|TRUNCATE[[:space:]]+TABLE)'; then
  block "Destructive SQL (DROP/TRUNCATE) blocked. Run manually if intentional."
fi

# ─── PROCESS KILLING ─────────────────────────────────────────────────────────

if echo "$COMMAND" | grep -qE '(pkill|killall)[[:space:]]+(-9[[:space:]]|-KILL[[:space:]])?[a-zA-Z]'; then
  block "Broad process kill (pkill/killall) blocked. Run manually if intentional."
fi

exit 0
