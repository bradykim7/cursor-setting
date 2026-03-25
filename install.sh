#!/bin/bash
set -e

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== Claude Code Dotfiles Installer ==="
echo ""

# Step 1: Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "[!] Claude Code가 설치되어 있지 않습니다."
    echo ""

    if command -v npm &> /dev/null; then
        echo "[*] npm으로 Claude Code를 설치합니다..."
        npm install -g @anthropic-ai/claude-code
        echo "[✓] Claude Code 설치 완료"
    else
        echo "[✗] npm이 설치되어 있지 않습니다."
        echo "    다음 중 하나를 실행해주세요:"
        echo ""
        echo "    # npm 사용"
        echo "    npm install -g @anthropic-ai/claude-code"
        echo ""
        echo "    # 또는 직접 설치 후 다시 실행"
        echo "    # https://docs.anthropic.com/en/docs/claude-code"
        exit 1
    fi
fi

echo "[✓] Claude Code: $(claude --version 2>/dev/null || echo 'installed')"
echo ""

# Step 2: Ensure ~/.claude/ directory exists
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "[*] ~/.claude/ 디렉토리가 없습니다. 생성합니다..."
    mkdir -p "$CLAUDE_DIR"
    echo "[✓] ~/.claude/ 생성 완료"
fi

# Step 3: Backup & Symlink - commands/
echo "[*] commands/ 설정 중..."
if [ -d "$CLAUDE_DIR/commands" ] && [ ! -L "$CLAUDE_DIR/commands" ]; then
    echo "    기존 commands/ 백업 → commands.bak/"
    mv "$CLAUDE_DIR/commands" "$CLAUDE_DIR/commands.bak"
elif [ -L "$CLAUDE_DIR/commands" ]; then
    rm "$CLAUDE_DIR/commands"
fi
ln -s "$DOTFILES_DIR/commands" "$CLAUDE_DIR/commands"
echo "[✓] commands/ → $DOTFILES_DIR/commands"

# Step 4: Backup & Symlink - agents/
echo "[*] agents/ 설정 중..."
if [ -d "$CLAUDE_DIR/agents" ] && [ ! -L "$CLAUDE_DIR/agents" ]; then
    echo "    기존 agents/ 백업 → agents.bak/"
    mv "$CLAUDE_DIR/agents" "$CLAUDE_DIR/agents.bak"
elif [ -L "$CLAUDE_DIR/agents" ]; then
    rm "$CLAUDE_DIR/agents"
fi
ln -s "$DOTFILES_DIR/agents" "$CLAUDE_DIR/agents"
echo "[✓] agents/ → $DOTFILES_DIR/agents"

# Step 5: Backup & Symlink - settings.json
echo "[*] settings.json 설정 중..."
if [ -f "$CLAUDE_DIR/settings.json" ] && [ ! -L "$CLAUDE_DIR/settings.json" ]; then
    echo "    기존 settings.json 백업 → settings.json.bak"
    mv "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.bak"
elif [ -L "$CLAUDE_DIR/settings.json" ]; then
    rm "$CLAUDE_DIR/settings.json"
fi
ln -s "$DOTFILES_DIR/settings.json" "$CLAUDE_DIR/settings.json"
echo "[✓] settings.json → $DOTFILES_DIR/settings.json"

echo ""
echo "=== 설치 완료! ==="
echo ""
echo "Symlinks:"
ls -la "$CLAUDE_DIR/commands" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/settings.json"
echo ""
echo "사용 가능한 커맨드:"
echo "  /commit-mailplug    - 팀 컨벤션 커밋 메시지 추천"
echo "  /commit-suggest     - 일반 커밋 메시지 추천"
echo "  /pr-description     - PR 설명 자동 생성"
echo "  /affected-endpoints - 영향받는 엔드포인트 추적"
