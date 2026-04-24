#!/bin/bash
set -e

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# ─────────────────────────────────────────────
# 서브커맨드 분기
# ─────────────────────────────────────────────
SUBCMD="${1:-install}"

case "$SUBCMD" in
    init)
        # ─────────────────────────────────────
        # init: 프로젝트 레포에 CLAUDE.md 생성
        # ─────────────────────────────────────
        TARGET_DIR="${2:-.}"
        # 틸드(~)를 $HOME으로 확장 (변수 안의 틸드는 쉘이 자동 확장하지 않음)
        TARGET_DIR="${TARGET_DIR/#\~/$HOME}"
        TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
        CLAUDE_MD="$TARGET_DIR/CLAUDE.md"

        echo "=== Claude Code Per-Repo Init ==="
        echo "대상: $TARGET_DIR"
        echo ""

        if [ -f "$CLAUDE_MD" ]; then
            echo "[!] CLAUDE.md가 이미 존재합니다: $CLAUDE_MD"
            echo "    덮어쓰려면 삭제 후 다시 실행하세요."
            exit 1
        fi

        # 프로젝트 정보 자동 감지
        PROJECT_NAME=$(basename "$TARGET_DIR")
        GIT_REMOTE=$(cd "$TARGET_DIR" && git remote get-url origin 2>/dev/null || echo "N/A")

        # 언어/타입 감지
        if [ -f "$TARGET_DIR/composer.json" ]; then
            LANG="PHP"; TYPE="PHP Project"
        elif [ -f "$TARGET_DIR/package.json" ]; then
            LANG="TypeScript/JavaScript"; TYPE="Node.js Project"
        elif [ -f "$TARGET_DIR/pom.xml" ] || [ -f "$TARGET_DIR/build.gradle" ]; then
            LANG="Java"; TYPE="Java Project"
        elif [ -f "$TARGET_DIR/requirements.txt" ] || [ -f "$TARGET_DIR/pyproject.toml" ]; then
            LANG="Python"; TYPE="Python Project"
        elif [ -f "$TARGET_DIR/go.mod" ]; then
            LANG="Go"; TYPE="Go Project"
        elif [ -f "$TARGET_DIR/Cargo.toml" ]; then
            LANG="Rust"; TYPE="Rust Project"
        else
            LANG="Unknown"; TYPE="Project"
        fi

        # 디렉토리 구조 (1레벨)
        DIR_TREE=$(cd "$TARGET_DIR" && ls -d */ 2>/dev/null | head -10 | sed 's/^/├── /' || echo "├── (empty)")

        # 템플릿으로 CLAUDE.md 생성
        cat > "$CLAUDE_MD" << CLAUDEEOF
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

- **Project**: $PROJECT_NAME
- **Type**: $TYPE
- **Language**: $LANG
- **Remote**: $GIT_REMOTE

## Directory Structure

\`\`\`
$DIR_TREE
\`\`\`

## Development Commands

### Build
\`\`\`bash
# TODO: 빌드 명령 추가
\`\`\`

### Test
\`\`\`bash
# TODO: 테스트 명령 추가
\`\`\`

### Lint
\`\`\`bash
# TODO: 린트 명령 추가
\`\`\`

### Run (Dev)
\`\`\`bash
# TODO: 개발 서버 실행 명령 추가
\`\`\`

## Technical Guidelines

- TODO: 코드 스타일 가이드 추가
- TODO: 프로젝트 컨벤션 추가

## Important Notes

- TODO: 프로젝트 특이사항 추가
CLAUDEEOF

        # .handoffs, .plans, .research 디렉토리 생성
        mkdir -p "$TARGET_DIR/.handoffs" "$TARGET_DIR/.plans" "$TARGET_DIR/.research"

        # .gitignore에 추가 (이미 없으면)
        GITIGNORE="$TARGET_DIR/.gitignore"
        if [ -f "$GITIGNORE" ]; then
            for PATTERN in ".handoffs/" ".plans/" ".research/"; do
                if ! grep -qF "$PATTERN" "$GITIGNORE" 2>/dev/null; then
                    echo "$PATTERN" >> "$GITIGNORE"
                fi
            done
        fi

        echo "[✓] CLAUDE.md 생성 완료: $CLAUDE_MD"
        echo "[✓] 작업 디렉토리 생성: .handoffs/ .plans/ .research/"
        echo ""
        echo "다음 단계:"
        echo "  1. CLAUDE.md의 TODO 항목을 프로젝트에 맞게 수정"
        echo "  2. 필요시 .gitignore에 .handoffs/ .plans/ .research/ 추가 여부 확인"
        exit 0
        ;;

    install|"")
        # 아래 기존 install 로직으로 계속
        ;;

    help|--help|-h)
        echo "사용법: ./install.sh [command] [options]"
        echo ""
        echo "Commands:"
        echo "  install          글로벌 설치 (기본값) — ~/.claude/에 symlink 생성"
        echo "  init [path]      프로젝트 초기화 — CLAUDE.md + 작업 디렉토리 생성"
        echo "  help             이 도움말 표시"
        echo ""
        echo "Examples:"
        echo "  ./install.sh                    # 글로벌 설치"
        echo "  ./install.sh init .             # 현재 디렉토리에 프로젝트 초기화"
        echo "  ./install.sh init ~/my-project  # 특정 프로젝트에 초기화"
        exit 0
        ;;

    *)
        echo "[✗] 알 수 없는 명령: $SUBCMD"
        echo "    ./install.sh help 로 사용법을 확인하세요."
        exit 1
        ;;
esac

# ─────────────────────────────────────────────
# install: 글로벌 설치 (기존 로직)
# ─────────────────────────────────────────────

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

# Step 4: Backup & Symlink - agents/claude-code/ → ~/.claude/agents/
echo "[*] agents/ 설정 중..."
if [ -d "$CLAUDE_DIR/agents" ] && [ ! -L "$CLAUDE_DIR/agents" ]; then
    echo "    기존 agents/ 백업 → agents.bak/"
    mv "$CLAUDE_DIR/agents" "$CLAUDE_DIR/agents.bak"
elif [ -L "$CLAUDE_DIR/agents" ]; then
    rm "$CLAUDE_DIR/agents"
fi
ln -s "$DOTFILES_DIR/agents/claude-code" "$CLAUDE_DIR/agents"
echo "[✓] agents/ → $DOTFILES_DIR/agents/claude-code"

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

# Step 6: urltest.http 설정 안내
if [ ! -f "$DOTFILES_DIR/urltest.http" ]; then
    echo "[!] urltest.http가 없습니다. 템플릿에서 복사 후 토큰을 설정해주세요:"
    echo "    cp $DOTFILES_DIR/urltest.http.example $DOTFILES_DIR/urltest.http"
    echo "    vi $DOTFILES_DIR/urltest.http"
    echo ""
else
    echo "[✓] urltest.http 존재 확인"
fi

echo ""
echo "=== 설치 완료! ==="
echo ""
echo "Symlinks:"
ls -la "$CLAUDE_DIR/commands" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/settings.json"
echo ""
echo "사용 가능한 커맨드:"
echo ""
echo "  === 워크플로우 (메타) ==="
echo "  /workcheck          - 작업 중간 점검 (영향 분석 + 스모크 + master 비교)"
echo "  /workfinish         - 작업 마무리 (커밋 + PR 설명)"
echo ""
echo "  === 계획 라이프사이클 ==="
echo "  /create-plan        - 구조적 구현 계획 수립"
echo "  /implement-plan     - 계획서 Phase별 구현"
echo "  /iterate-plan       - 기존 계획서 수정"
echo "  /validate-plan      - 구현 결과 검증"
echo ""
echo "  === 리서치 & 디버깅 ==="
echo "  /research           - 코드베이스 구조적 탐색"
echo "  /debug              - 구조적 디버깅 (병렬 조사)"
echo ""
echo "  === 세션 관리 ==="
echo "  /handoff            - 세션 인수인계 문서 작성"
echo "  /resume-handoff     - 핸드오프에서 작업 재개"
echo ""
echo "  === 테스트 ==="
echo "  /affected-endpoints - 영향받는 엔드포인트 추적"
echo "  /smoke-test         - 스모크 테스트"
echo "  /branch-diff        - 브랜치 간 응답 비교"
echo "  /test-affected      - 영향 추적 + 자동 스모크"
echo ""
echo "  === 커밋 & PR ==="
echo "  /commit-mailplug    - 팀 컨벤션 커밋 메시지 추천"
echo "  /commit-suggest     - 일반 커밋 메시지 추천"
echo "  /pr-description     - PR 설명 자동 생성"
echo ""
echo "  === Claude Code 사용 통계 ==="
echo "  /claude-usage-collect  - 본인 사용 데이터 수집 → 공유 zip 생성 (팀원 배포용)"
echo "  /claude-usage-analyze  - 본인 사용 분석 → 개인 리포트 생성"
echo "  /claude-usage-report   - 팀원 JSON 수합 → 8섹션 팀 리포트 (+Confluence 옵션)"
echo ""
echo "프로젝트 초기화: ./install.sh init /path/to/project"
echo "토큰 설정:      $DOTFILES_DIR/urltest.http"
echo "워크플로우:     $DOTFILES_DIR/WORKFLOW.md"
