---
description: 오늘 데일리 노트 생성 — 어제 미완료 태스크 자동 인계 + 오늘 세션 활동 취합
allowed-tools: Read, Write, Edit, Glob, Bash(date:*), Bash(ls:*), Bash(find:*), Bash(python3:*)
argument-hint: [날짜 또는 생략]
---

# /daily — 데일리 노트 생성

오늘(또는 지정 날짜) 데일리 노트를 `10-Daily/` 에 생성합니다.

## 프로세스

### Step 1: 날짜 결정

```bash
# 인자 없으면 오늘
TARGET_DATE="${1:-$(date +%Y-%m-%d)}"
```

### Step 2: 기존 파일 확인

`10-Daily/{TARGET_DATE}.md` 가 이미 있으면:
- 사용자에게 이어서 편집할지, 새로 만들지 물어보기
- 새로 만들면 백업 후 진행
- placeholder 미치환 버그(`[[YYYY-MM-DD-1]]` 같은 패턴) 발견 시 어제 날짜로 즉시 수정

### Step 3: 어제 노트에서 미완료 태스크 추출

```bash
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d)
```

`10-Daily/{YESTERDAY}.md` 가 있으면 미완료 체크박스(`- [ ]`)만 추출:
- "## 오늘 할 일" 섹션과 "## 진행 중" 섹션의 미완료 항목
- "## 내일 할 일" 섹션 항목 (있으면 우선 인계)

### Step 4: 템플릿 적용

`_templates/daily-note.md` 의 frontmatter + 구조를 따르되:
- `{{date:YYYY-MM-DD}}` → 실제 날짜
- `{{date:YYYY-MM-DD-1}}` → 어제 날짜 (반드시 실제 날짜 문자열로 치환)
- `## 오늘 할 일` 섹션에 어제 미완료 태스크 인계
- `## 메모 / 캡처` 비워두기

### Step 5: 오늘 세션 활동 자동 취합 (기본 활성화)

`~/.claude/projects/<인코딩-경로>/<세션ID>.jsonl` 들을 날짜로 필터해서 "## 오늘 세션 활동" 섹션을 채운다.

```bash
find ~/.claude/projects/ -maxdepth 2 -name "*.jsonl" \
  -newermt "$TARGET_DATE 00:00" -not -newermt "$TARGET_DATE+1 00:00"
```

**디렉토리 prefix로 자동 분리:**
- `personal/` 또는 비-workspace 경로 → **상세 (Q&A timeline)**
- `workspace/` 하위 → **메타데이터만** (회사 분리 원칙, CLAUDE.md 참조)

#### 형식 가이드 (★ 중요)

**원칙: 추상 요약·메타데이터 표 금지. 사용자가 한 질문과 그에 대한 작업을 시간순으로 raw하게.**

데일리 노트의 본질은 "내가 무슨 질문을 했고 무슨 작업이 일어났는지" 추적이다. 메타데이터 표(시간/횟수/강도)는 정보 손실이 크고 회고에 도움 안 됨. **반드시 질문(Q) ↔ 작업/결정(A) 짝을 유지하라.**

**Personal 세션 형식:**

```markdown
#### `personal/<프로젝트>` (HH:MM–HH:MM)

**1) <의미 단위 제목> [HH:MM]**
- **Q:** "<사용자 질문 원문 가깝게>"
- **A:** <어떤 작업·도구·파일 변경 → 어떤 결정 / 결과>

**2) <다음 의미 단위> [HH:MM–HH:MM]**
- **Q1:** "..."
- **A1:** ...
- **Q2:** "..."
- **A2:** ...
```

- 의미 단위(주제 전환점)로 청크 묶기 — 보통 시간대(시간 점프)가 자연스러운 경계
- 같은 청크 안 여러 Q는 `Q1/Q2/Q3` 로 번호 매김
- 사용자 질문은 **원문에 가깝게** 인용(따옴표). 의역하더라도 핵심 단어 보존
- A는 결정·도구 호출·파일 경로·핵심 결론까지 포함 (`file:line` 패턴 환영)
- 외부 산출물 만들었으면 위키링크로 연결 (`[[learning-note-name]]`)

**Workspace 세션 형식 (회사 분리 원칙):**

```markdown
### Workspace (회사 — 메타데이터만)

> CLAUDE.md 분리 원칙. 상세는 회사 노트/핸드오프에 별도.

| 프로젝트 | 세션 | 활동 시간(KST) | 패턴 |
|---|---|---|---|
| `<proj>` | N | HH:MM–HH:MM (~Nh) | <user msg 수, 주요 도구 종류>, <한 줄 패턴> |
```

- 프로젝트명·세션수·활동 시간·도구 사용 패턴까지만
- 사용자 질문 원문·시스템 이름·티켓 ID·의사결정 상세 **절대 X**
- 의문 들면 빼는 쪽으로

#### 데이터 추출 — 권장 Python 스니펫

```python
import json
events = []
with open(jsonl_path) as f:
    for line in f:
        d = json.loads(line)
        ts = d.get("timestamp","")[:19]
        msg = d.get("message", {})
        if d.get("type") == "user" and msg.get("role") == "user":
            content = msg.get("content","")
            if isinstance(content, list):
                txt = next((c["text"] for c in content if c.get("type")=="text"), "")
            else:
                txt = str(content)
            if txt and not txt.startswith("<"):  # slash command/tool_result 제외
                events.append((ts, "U", txt))
        elif d.get("type") == "assistant":
            txts = [c["text"] for c in msg.get("content",[])
                    if c.get("type")=="text" and c.get("text","").strip()]
            if txts:
                events.append((ts, "A", "\n".join(txts)))
```

`<command-message>`/`<local-command-*>`/`<system-reminder>` 등 `<`로 시작하는 user 메시지는 실제 질문이 아니므로 제외.

### Step 6: 작성 후 알림

- 파일 경로 출력
- 인계된 태스크 개수 알림
- 취합한 personal 세션 수 / workspace 세션 수
- "어제 노트 미완료 N개 인계, 오늘 세션 M개 취합 — 우선순위 검토 권장"

## 출력 예시

```
✓ 10-Daily/2026-04-29.md 생성 완료
  - 어제 미완료 태스크 3개 인계
  - 어제의 "내일 할 일" 항목 2개 추가
  - 오늘 세션 취합: personal 2 / workspace 4
  
다음: 오늘 우선순위를 데일리 노트에서 정리하세요.
```

## 안티패턴 (하지 말 것)

- ❌ 세션 활동을 메타데이터 표(시간/횟수/강도)로만 요약 — 정보 손실
- ❌ "코드 수정·검증 사이클" 같은 추상어로 personal 세션 압축 — Q&A 원문 그대로 살릴 것
- ❌ workspace 세션의 사용자 질문 본문·시스템 이름·티켓 노출 — 분리 원칙 위반
- ❌ 어제 노트 없을 때 본문을 비워둔 채 "인계할 게 없어요"로 종료 — 오늘 세션 취합으로라도 채울 것
- ❌ `[[YYYY-MM-DD-1]]` 같은 placeholder 미치환 그대로 두기
