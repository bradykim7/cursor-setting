---
description: 본인 Claude Code 사용 분석 — ccusage 기반 모델 라우팅/세션 위생/ROI 리포트
allowed-tools: Bash(npx:*), Bash(ccusage:*), Bash(mkdir:*), Bash(ls:*), Bash(whoami:*), Bash(date:*), Bash(jq:*), Bash(test:*), Read, Write, Glob, Grep
argument-hint: [기간 생략 가능, 예: 14d / 30d / 2026-04-10:2026-04-24]
---

# Claude Usage Analyze (본인 사용 분석)

로컬 `~/.claude/projects/` 데이터를 `ccusage`로 집계하고, 모델 라우팅 효율 · 세션 위생 · ROI를 분석한 개인 리포트를 생성합니다.

**Personal Claude Code usage analysis — routing efficiency, session hygiene, ROI.**

출력: `.research/claude-usage-{YYYY-MM-DD}.md`

---

## 사전 조건 / Prerequisites

- `npx` + `jq` 설치
- `~/.claude/projects/` 존재 (Claude Code 1회 이상 사용)
- 프로젝트 루트에 `.research/` 있으면 거기에, 없으면 `~/Desktop/`

---

## 실행 흐름 / Flow

### Step 1: 인자 파싱

- 없음 → 전체 기간
- `14d` / `30d` / `90d` → 오늘부터 N일 전까지
- `YYYY-MM-DD:YYYY-MM-DD` → 명시 범위

### Step 2: 데이터 수집

```bash
npx ccusage@latest daily   --json > /tmp/cu-daily.json
npx ccusage@latest session --json > /tmp/cu-session.json
npx ccusage@latest monthly --json > /tmp/cu-monthly.json
```

필요 시 `--since` / `--until` 플래그로 기간 필터.

### Step 3: 지표 계산

#### 3-1. 활동 지표 / Activity

- Total tokens (in / out / cache_read / cache_creation)
- Sessions 수
- Active days (메시지 1개 이상 있는 날)
- Tokens/session = total / sessions
- 일별 토큰 분포 (최대/평균/중앙값)
- Peak day (토큰 최대)

#### 3-2. 모델 라우팅 / Model Routing

jq로 모델별 토큰 집계:

```jq
[.daily[] | .modelBreakdowns[]?] | group_by(.modelName) |
  map({model: .[0].modelName, tokens: (map(.inputTokens + .outputTokens) | add)})
```

평가 기준:
- **Haiku < 2%** → 라우팅 비효율 플래그
- **Opus > 90%** → Opus 편중 플래그
- **Sonnet 80%+ 급증** → rate limit 회피 의심

#### 3-3. 세션 위생 / Session Hygiene

- 최장 세션 duration
- **5d+ 세션** → 🚩 idle 의심
- **24h+ 세션** → 🟡 확인 권장
- 세션당 평균 토큰 (< 20k = 얕은 사용, > 300k = 헤비)

#### 3-4. 비용 / Cost

공개 API 가격 (per 1M):
| 모델 | Input | Output |
|---|---|---|
| Opus (4.6/4.7) | $15 | $75 |
| Sonnet 4.6 | $3 | $15 |
| Haiku 4.5 | $1 | $5 |

- API 환산 총액
- Max 5× ($100/월) 대비 ROI = API환산 / $100
- `$/M tokens` (개인 단가)

### Step 4: 인사이트 도출

평가 규칙 (자동 플래그):

| 관찰 | 플래그 |
|------|-------|
| Haiku < 2% | 🔴 라우팅 개선 필요 |
| Opus > 95% | 🟡 모델 다변화 여지 |
| 최장 세션 5d+ | 🔴 세션 위생 점검 |
| 세션당 < 20k | 🟡 세션 깊이 얕음 |
| ROI < 1.0 | 🟡 Pro 다운그레이드 고려 |
| ROI > 5.0 | 🟢 Max 5× 매우 효율적 |
| Active day 비율 < 30% | 🟡 사용 정착 미흡 |

### Step 5: 리포트 생성

파일명: `.research/claude-usage-{YYYY-MM-DD}.md` (`.research/`가 없으면 `~/Desktop/`)

템플릿:

```markdown
---
date: {ISO}
user: {whoami}
period: {start} ~ {end}
type: claude-usage-personal
---

# Claude Code 사용 분석 — {whoami}

## 요약 / Summary

| 지표 | 값 |
|---|---|
| Total tokens | {total} |
| Sessions | {n} |
| Active days | {active}/{total_days} |
| Tokens/session | {avg} |
| API 환산 | ${cost} |
| Max 5× ROI | {roi}× |

## 모델 라우팅 / Model Routing

| 모델 | 비중 | Input | Output |
|---|---|---|---|
| Opus 4.7 | {%} | ... | ... |
| Opus 4.6 | ... | ... | ... |
| Sonnet 4.6 | ... | ... | ... |
| Haiku 4.5 | ... | ... | ... |

**플래그**: {🔴/🟡/🟢 자동 판정}

## 세션 위생 / Session Hygiene

- 최장 세션: {duration} — {판정}
- 평균 세션: {avg}
- 🚩 의심 세션: {5d+ 목록}

## 일별 추이 / Daily Trend

{피크일 ~5개 + 최근 7일 bar}

## 인사이트 / Insights

1. {자동 생성 인사이트 1}
2. {자동 생성 인사이트 2}
3. {자동 생성 인사이트 3}

## 권장 조치 / Recommended Actions

- [ ] {플래그 기반 action 1}
- [ ] {플래그 기반 action 2}

## Raw Data

- daily.json / session.json / monthly.json 위치
- 재실행 명령: `/claude-usage-analyze {args}`
```

### Step 6: 콘솔 요약

```
[✓] 리포트 생성: .research/claude-usage-2026-04-24.md

핵심 수치:
  Total: 13.4M tokens / 62 sessions / 12 active days
  ROI: 9.3× (Max 5× 대비 매우 효율)

🔴 발견된 이슈:
  - Haiku 1.8% → 경량 작업 라우팅 개선 여지
🟡 주의:
  - 최장 세션 2d 19h → 종료 습관 확인
🟢 강점:
  - ROI 9.3× / Active day 비율 86%

다음 단계:
  - 팀 집계 참여: /claude-usage-collect
  - 리포트 공유: .research/claude-usage-2026-04-24.md
```

---

## 규칙 / Rules

- **개인 데이터만 분석** — 타인의 데이터 건드리지 않음
- **비판 없음** — 수치 기반 관찰만, 평가는 절제된 톤
- **재현 가능성** — 모든 수치의 계산 근거를 리포트에 포함
- **캐시 활용** — 같은 날 2번째 실행은 이전 JSON 재사용 가능 (TTL 1h)

---

## 실패 처리

| 상황 | 대응 |
|------|------|
| ccusage 실패 | 에러 출력 + `npx ccusage@latest doctor` 안내 |
| 데이터 없음 | "사용 이력 부족 — 최소 하루 이상 필요" 안내 |
| jq 없음 | 설치 안내 (`brew install jq`) |
| `.research/` 없음 | `~/Desktop/`로 fallback + 안내 |
