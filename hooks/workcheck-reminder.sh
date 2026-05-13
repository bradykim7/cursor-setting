#!/usr/bin/env bash
# PreToolUse: Bash — before `git commit`, warn if smoke test report is missing
# for the current ticket. Non-blocking (exit 0); stderr surfaces to Claude/user
# so the operator can choose to proceed or run /workcheck first.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[ -z "$COMMAND" ] && exit 0

# Match actual `git commit` invocations only (not `git commit --help` etc. — those still fine)
# Exclude amend with no file changes and status/log/show.
if ! echo "$COMMAND" | grep -qE '(^|[[:space:]]|;|&&|\|\|)git[[:space:]]+commit([[:space:]]|$)'; then
  exit 0
fi

branch=$(git symbolic-ref --short HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0

ticket=$(echo "$branch" | grep -oE '[A-Z]+-[0-9]+' | head -1)
[ -z "$ticket" ] && exit 0

testjob_dir="$HOME/workspace/testjob/$ticket"
smoke="$testjob_dir/results/SMOKE_TEST_REPORT.md"

if [ ! -f "$smoke" ]; then
  cat >&2 <<EOF
[reminder] $ticket: 스모크 테스트 리포트 없음.
  expected: $smoke
  '/workcheck' 를 먼저 돌리면 영향 분석 + 스모크가 자동 실행됩니다.
  의도된 경우라면 무시하고 commit 진행하세요.
EOF
fi

exit 0
