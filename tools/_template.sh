# Template for adding a new AI CLI / agent tool.
#
# How to add a tool:
#   1. Copy this file: `cp tools/_template.sh tools/<your-tool>.sh`
#   2. Fill in TOOL_NAME / TOOL_CMD / TOOL_DIR / TOOL_SYMLINKS
#   3. Re-run `./install.sh` — the loop will pick it up automatically.
#
# Files prefixed with `_` (underscore) are skipped by the install loop.
# That's why this template stays inert until you rename it.

TOOL_NAME=""              # 사람이 읽는 이름 (e.g., "Gemini CLI")
TOOL_CMD=""               # 감지에 쓸 바이너리 이름 — `command -v <TOOL_CMD>` 로 확인
TOOL_DIR=""               # config 디렉토리 (e.g., "$HOME/.gemini")

# 각 항목: "<target relative to TOOL_DIR>=<source relative to DOTFILES_DIR>"
# Source 파일이 cursor-setting/ 안에 존재해야 함 — 없으면 그 entry는 스킵됨.
# Target 경로는 nested 가능 (e.g., "plugins/my-plugin/config.json").
TOOL_SYMLINKS=(
    # "AGENTS.md=AGENTS.md"
    # "skills=skills"
)

# ─────────────────────────────────────────────
# 알려진 툴 예시 (참고용 — 직접 검증 후 사용하세요)
# ─────────────────────────────────────────────
#
# Gemini CLI (https://github.com/google-gemini/gemini-cli)
#   TOOL_NAME="Gemini CLI"
#   TOOL_CMD="gemini"
#   TOOL_DIR="$HOME/.gemini"
#   TOOL_SYMLINKS=("GEMINI.md=AGENTS.md")
#
# Cursor agent CLI (https://cursor.sh)
#   TOOL_NAME="Cursor agent"
#   TOOL_CMD="cursor-agent"
#   TOOL_DIR="$HOME/.cursor"
#   TOOL_SYMLINKS=("AGENTS.md=AGENTS.md")
#
# Aider (https://aider.chat)
#   TOOL_NAME="Aider"
#   TOOL_CMD="aider"
#   TOOL_DIR="$HOME/.aider"
#   TOOL_SYMLINKS=("CONVENTIONS.md=AGENTS.md")
#
# Continue (https://continue.dev)
#   TOOL_NAME="Continue"
#   TOOL_CMD="continue"
#   TOOL_DIR="$HOME/.continue"
#   TOOL_SYMLINKS=("AGENTS.md=AGENTS.md")
