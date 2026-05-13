#!/usr/bin/env bash
# SessionStart — when current branch matches a JIRA-style ticket pattern,
# surface related artifacts (.plans/, .handoffs/, .research/, testjob/<ticket>/).
# stdout is appended to Claude's session context; stderr is shown to the user.

if ! git rev-parse --git-dir > /dev/null 2>&1; then
  exit 0
fi

branch=$(git symbolic-ref --short HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0

ticket=$(echo "$branch" | grep -oE '[A-Z]+-[0-9]+' | head -1)
[ -z "$ticket" ] && exit 0

found=()

for dir in .plans .handoffs .research; do
  if [ -d "$dir" ]; then
    matches=$(find "$dir" -maxdepth 2 -name "*${ticket}*" -type f 2>/dev/null | head -3)
    if [ -n "$matches" ]; then
      while IFS= read -r f; do
        found+=("$f")
      done <<< "$matches"
    fi
  fi
done

testjob_dir="$HOME/workspace/testjob/$ticket"
if [ -d "$testjob_dir" ]; then
  status=""
  [ -f "$testjob_dir/results/SMOKE_TEST_REPORT.md" ] && status="${status} smoke✓"
  [ -f "$testjob_dir/results/DIFF_REPORT.md" ] && status="${status} diff✓"
  [ -z "$status" ] && status=" (no reports yet)"
  found+=("testjob/$ticket:$status")
fi

if [ ${#found[@]} -gt 0 ]; then
  echo "## Existing artifacts for ticket $ticket (branch: $branch)"
  echo ""
  for item in "${found[@]}"; do
    echo "- $item"
  done
fi

exit 0
