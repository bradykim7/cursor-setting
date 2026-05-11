# Obsidian Vault 온보딩 가이드

> Obsidian을 처음 쓰는 사람도 따라할 수 있는 단계별 가이드입니다.
> 이 가이드를 마치면 **회사 지식 + 개발 지식이 분리 저장되는 vault**가 만들어지고, **Claude Code로 그 vault를 다룰 수 있습니다**.

---

## 이 가이드가 만들어주는 것

- 폴더 구조가 잡힌 Obsidian vault (`~/Documents/MyVault` 등)
- 7가지 노트 템플릿 (데일리·미팅·ADR·기술 지식·트러블슈팅·용어집·주간 회고)
- Claude Code 연동 (vault 안에서 `claude` 실행 → 노트 자동 생성·검색·정리)
- 3가지 슬래시 커맨드 (`/daily`, `/weekly`, `/triage`)

---

## 사전 조건

- macOS / Linux / Windows (이 가이드는 macOS 기준)
- Obsidian 앱 설치: https://obsidian.md/download
- Claude Code 설치 + agcoco 글로벌 설치 완료
  - 미완료면 [메인 README](../README.md) 의 Quick Start 먼저 진행

---

## Step 1 — Vault 생성 (1분)

터미널에서:

```bash
cd ~/agcoco    # agcoco 레포 위치
./install.sh obsidian-init ~/Documents/MyVault
```

> `MyVault` 자리에 원하는 이름. 회사용·개인용 분리하려면 두 번 실행해서 `~/Documents/Work-Vault` `~/Documents/Personal-Vault` 처럼 만드는 것도 가능.

**확인 포인트**:
```bash
ls ~/Documents/MyVault
# 00-Inbox  10-Daily  20-Company  30-Development  40-Projects  90-Archive
# CLAUDE.md  _attachments  _templates
```

위 폴더들이 보이면 성공.

---

## Step 2 — Obsidian 앱에서 Vault 열기 (1분)

1. Obsidian 앱 실행
2. 시작 화면에서 **"Open folder as vault"** 클릭
3. 방금 만든 `~/Documents/MyVault` 선택
4. 신뢰 작성자 다이얼로그 → **"Trust author and enable plugins"**

**확인 포인트**:
- 좌측 파일 트리에 `00-Inbox`, `10-Daily`, ... 폴더가 보임
- 폴더 클릭 시 비어있거나 `.gitkeep` 만 있음

---

## Step 3 — 코어 플러그인 설정 확인 (2분)

`obsidian-init` 가 자동 설정하지만 한 번 확인:

### Templates 플러그인
- **Settings (⌘,) → Templates**
- "Template folder location" 이 **`_templates`** 인지 확인

### Daily Notes 플러그인
- **Settings → Daily notes**
- "New file location": `10-Daily`
- "Template file location": `_templates/daily-note`
- "Date format": `YYYY-MM-DD`

설정 미일치 시 직접 수정.

---

## Step 4 — 첫 데일리 노트 만들기 (1분)

Obsidian 안에서:

1. **Cmd+P** (Command Palette) 열기
2. `Daily notes: Open today's daily note` 검색 후 실행

`10-Daily/2026-04-27.md` (오늘 날짜) 가 자동 생성됩니다.

**확인 포인트**:
- 파일 상단에 frontmatter (`---`로 둘러싸인 YAML) 가 있음
- "오늘 할 일", "진행 중", "미팅" 등 섹션이 보임

---

## Step 5 — 첫 회사 노트 만들기 (3분)

오늘 미팅이 있다고 가정하고 회사 미팅 노트를 만들어봅니다.

1. `20-Company/meetings/` 폴더 우클릭 → **New note**
2. 파일명: `2026-04-27-결제-스펙-리뷰` (날짜-주제 컨벤션)
3. 빈 노트가 열리면 **Cmd+P → "Templates: Insert template"**
4. `meeting-note` 선택

템플릿이 삽입되면:
- 참석자, 안건, 결정 사항 채우기
- 액션 아이템에 `- [ ]` 체크박스 사용

**확인 포인트**:
- 노트 상단 frontmatter에 `type: meeting`, `tags: [meeting, company]` 표시
- 좌측 파일 트리에서 `20-Company/meetings/2026-04-27-결제-스펙-리뷰.md` 확인

---

## Step 6 — 첫 개발 지식 노트 만들기 (3분)

회사와 무관한 일반 기술 지식을 정리합니다.

1. `30-Development/patterns/` 우클릭 → New note
2. 파일명: `idempotency-key-design` (kebab-case)
3. **Templates: Insert template** → `tech-knowledge`
4. "Idempotency Key 설계" 같은 일반 지식 정리

**핵심 차이점** (회사 vs 개발 지식):

| 회사 노트 (`20-Company/`) | 개발 노트 (`30-Development/`) |
|---|---|
| "우리 결제 서비스의 환불 처리" | "결제 시스템 설계 시 멱등성 보장" |
| 구체적 시스템·결정·사람 | 일반화된 패턴·교훈 |
| 외부 공유 불가 | 블로그·면접에 활용 가능 |
| 회사 떠나면 폐기 | 평생 가져갈 자산 |

같은 인시던트라도 두 노트로 나눠서 적습니다 (사내 컨텍스트 + 일반화 교훈).

---

## Step 7 — Claude Code 연동 (2분)

이제 진짜 강력해지는 단계입니다.

```bash
cd ~/Documents/MyVault
claude
```

Claude Code가 vault 루트의 `CLAUDE.md` 를 자동 인식해서 컨벤션을 따릅니다.

### 시도해볼 만한 것들

```
나: "어제 미팅에서 결정한 환불 정책을 ADR로 정리해줘"
→ Claude가 어제 미팅 노트 읽고, 20-Company/decisions/ 에 ADR 작성

나: "최근 1주 데일리 노트에서 30-Development/learning/ 으로 옮길만한 학습 항목 찾아줘"
→ Claude가 데일리 노트들 훑고, 일반화 가능한 학습 항목 추출

나: "idempotency 관련 노트 다 찾아서 인덱스 만들어줘"
→ Claude가 vault 검색, MOC (Map of Contents) 노트 생성

나: "00-Inbox/ 노트들을 적절한 폴더로 분류해줘"
→ Claude가 각 노트 분석 후 이동 제안 (실제로 옮기는 건 사용자 확인 후)
```

### 슬래시 커맨드 사용

vault 안에서 Claude Code를 실행하면 다음 커맨드가 추가로 활성화됩니다:

| 커맨드 | 동작 |
|--------|------|
| `/daily` | 오늘 데일리 노트 생성 (어제 미완료 태스크 인계) |
| `/weekly` | 이번 주 주간 회고 생성 (월~금 데일리 분석) |
| `/triage` | `00-Inbox/` 분류 제안 |

---

## Step 8 — 동기화 설정 (선택, 5분)

vault 내용을 다른 기기에서도 보고 싶다면:

### 옵션 A: Git + Obsidian Git 플러그인 (개발자 추천)

**Step A-1. Remote 연결**
```bash
cd ~/Documents/MyVault
git remote add origin git@github.com:사용자명/my-vault.git    # private 레포 권장
git add . && git commit -m "Initial vault"
git branch --show-current
# 예시 출력: main 또는 master
git push -u origin "$(git branch --show-current)"
```

> 회사 지식이 들어간다면 반드시 **private 레포** 사용. 회사 GitHub 계정 말고 개인 계정에.

**Step A-2. Obsidian Git 플러그인 활성화**

이 vault는 `obsidian-init` 시점에 플러그인 **설정 파일**이 미리 깔려 있습니다. Obsidian 앱에서 한 번만 활성화하면 됩니다.

1. Obsidian → **Settings (⌘,) → Community plugins**
2. 처음이면 **"Turn on community plugins"** 클릭 (Restricted mode 해제)
3. **Browse** → 검색창에 `Obsidian Git` → **Install** → **Enable**
4. 활성화하면 vault에 미리 깔린 설정 (`.obsidian/plugins/obsidian-git/data.json`) 이 자동 적용됨

**미리 적용된 기본 설정**:
| 항목 | 값 | 의미 |
|------|----|----|
| 자동 커밋 주기 | 10분 | 변경 있을 때만 커밋 |
| 자동 푸쉬 주기 | 10분 | 커밋과 별개 인터벌 |
| 부팅 시 pull | ON | 다른 기기에서 만든 변경 가져옴 |
| Push 전 pull | ON | 충돌 방지 |
| 충돌 처리 | merge | rebase 대신 merge |
| 커밋 메시지 | `vault: YYYY-MM-DD HH:mm:ss` | 자동 |

값 변경하려면 Settings → Obsidian Git 에서 직접 수정. 또는 `.obsidian/plugins/obsidian-git/data.json` 직접 편집 후 Obsidian 재시작.

**Step A-3. 동작 확인**

- Obsidian 우하단 상태표시줄에 `Obsidian Git` 아이콘과 브랜치 이름 표시되면 정상
- 노트 하나 만들고 10분 기다리거나, **Cmd+P → "Obsidian Git: Create backup"** 으로 즉시 커밋·푸쉬 테스트

### 옵션 B: Obsidian Sync (가장 매끄러움, 유료)
- Settings → Sync → 구독 (~$10/월)
- E2E 암호화, 모바일 동기화 가장 안정적

### 옵션 C: iCloud / Dropbox (무료, 충돌 가능)
- vault 폴더를 iCloud Drive 안에 두면 자동 동기화
- 단점: 모바일에서 편집 충돌 발생 빈도 있음

---

## Step 9 — 일주일 사용해보기

처음부터 완벽한 구조를 잡으려 하지 말고:

### Day 1-3: 무조건 `00-Inbox/` 에만 던지기
- 분류 고민 금지
- 떠오르는 모든 메모를 inbox에 빠르게 캡처

### Day 4-7: 매일 아침 데일리 노트로 시작
- `Cmd+P → Open today's daily note`
- 어제 inbox에 던진 것 중 정리할 것 결정

### 주말: 첫 분류
- `claude` 실행 → `/triage` 사용
- inbox 비우기 (Inbox Zero)
- `weekly-review` 템플릿으로 주간 회고

이 사이클이 몸에 익을 때까지 컨벤션 수정 자제. **사용해보고 진짜 불편한 부분만** 수정.

---

## 트러블슈팅

### "Templates: Insert template" 가 빈 목록을 보여줌
- Settings → Templates → Template folder location 이 `_templates` 인지 확인
- 슬래시 없이, 절대경로 아닌 vault 루트 기준 상대경로

### `cd vault && claude` 했는데 CLAUDE.md를 못 읽는 것 같음
- vault 루트에 `CLAUDE.md` 가 실제로 있는지 확인 (`ls ~/Documents/MyVault/CLAUDE.md`)
- Claude Code가 vault를 작업 디렉토리로 인식해야 함 (다른 폴더에서 실행하면 안 됨)

### `/daily` 커맨드가 안 보임
- vault의 `.claude/commands/` 디렉토리가 있는지 확인 (`ls -la ~/Documents/MyVault/.claude/`)
- 없으면 `obsidian-init` 가 hidden 파일을 못 복사한 것 — 수동 복사:
  ```bash
  cp -a ~/agcoco/templates/obsidian/vault/.claude ~/Documents/MyVault/
  ```

### Obsidian이 노트 변경을 인식 못함
- Claude가 외부에서 파일을 수정한 직후 Obsidian에 즉시 반영 안 될 수 있음
- 해당 노트 탭 닫았다 다시 열거나, Obsidian 우상단 새로고침

### 회사 정보가 vault에 들어갔는데 보안이 걱정됨
- 가장 강한 분리: **vault 두 개로 나누기** (`Work-Vault`, `Personal-Vault`)
- 약한 분리: 한 vault + `20-Company/` 만 별도 백업/암호화
- Obsidian Sync는 E2E 암호화 — 회사 정보 동기화 시 다른 동기화보다 안전

---

## 다음 단계

- [메인 README](../templates/obsidian/README.md) — vault 구조 상세
- [Vault CLAUDE.md](../templates/obsidian/vault/CLAUDE.md) — Claude Code 컨벤션
- 권장 커뮤니티 플러그인: **Templater, Dataview, Periodic Notes, Obsidian Git, QuickAdd**
  - Settings → Community plugins → Browse 에서 검색 후 설치

---

## FAQ

**Q. 이미 Obsidian vault가 있어요. 이걸로 덮어쓰면 안 되나요?**
A. `obsidian-init` 는 기존 vault를 보호합니다 (덮어쓰기 거부). 기존 vault에 적용하려면:
   ```bash
   # 안전하게: 새 vault 만들고 노트 수동 이동
   ./install.sh obsidian-init ~/Documents/MyVault-New
   # 그 후 기존 vault의 노트들을 적절한 폴더로 이동
   ```

**Q. 폴더 구조 (20-Company / 30-Development) 가 마음에 안 들어요.**
A. 바꿀 수는 있지만 `CLAUDE.md` 만 수정하면 끝나지 않습니다. 최소한 아래를 함께 맞춰야 합니다:
   - vault 루트의 `CLAUDE.md` — Claude Code 규칙
   - `.obsidian/daily-notes.json` — 데일리 노트 폴더
   - `.obsidian/app.json` — 새 노트 기본 생성 위치 (`00-Inbox/`)
   - `.claude/commands/` 아래 커맨드 문서 — `/daily`, `/weekly`, `/triage` 가 참조하는 경로

   특히 `10-Daily/` 나 `00-Inbox/` 를 바꾸면 위 설정이 어긋나기 쉬우니, 처음 1-2주는 기본 구조로 써보고 불편이 확인된 뒤 바꾸는 것을 권장합니다.

**Q. 모바일에서도 쓰고 싶어요.**
A. Obsidian 모바일 앱 + 동기화 (Step 8) 조합. Claude Code는 모바일 미지원이지만, 노트 읽기/편집은 가능.

**Q. 첨부 이미지가 너무 많아져서 vault 크기가 커요.**
A. `_attachments/` 만 git LFS로 관리하거나, Obsidian Sync로 vault 동기화 + 큰 첨부는 별도 클라우드.

**Q. AI가 회사 정보를 학습하면 어쩌죠?**
A. 이런 정책 문구는 바뀔 수 있으니 사용 전 Anthropic의 최신 공식 정책을 직접 확인하세요. 문서 정책과 별개로, 민감 정보·자격 증명·토큰은 vault에 넣지 말고 별도 비밀 관리 도구를 쓰는 쪽이 안전합니다.
