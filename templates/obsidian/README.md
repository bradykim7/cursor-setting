# Obsidian Vault Bootstrap

회사 지식 + 개발 지식을 축적하기 위한 Obsidian vault 스타터입니다.

이 디렉토리는 **vault 자체가 아닙니다**. 새 vault를 만들 때 부트스트랩하는 템플릿입니다.

## Quick Start

```bash
# vault 새로 생성
./install.sh obsidian-init ~/Documents/MyVault

# Obsidian 앱에서 "Open folder as vault"로 ~/Documents/MyVault 선택
```

이후 vault는 **별도 git 레포**로 관리하는 것을 권장합니다 (이 dotfiles 레포에 vault 컨텐츠를 섞지 않음).

## Vault 구조

```
MyVault/
├── 00-Inbox/          # 빠른 캡처 — 분류 전 임시 보관
├── 10-Daily/          # 데일리 노트 (YYYY-MM-DD.md)
├── 20-Company/        # 회사 지식 (회사 떠나면 가져갈 수 없음)
│   ├── meetings/      # 미팅 노트
│   ├── decisions/     # 의사결정 로그 (ADR 스타일)
│   ├── glossary/      # 회사 용어집
│   ├── people/        # 팀원·이해관계자 정보
│   └── troubleshooting/ # 사내 인시던트/장애 기록
├── 30-Development/    # 개발 지식 (회사 무관, 평생 자산)
│   ├── patterns/      # 패턴·아키텍처 메모
│   ├── troubleshooting/ # 트러블슈팅 로그 (증상→원인→해결→예방)
│   ├── snippets/      # 코드 스니펫
│   └── learning/      # 학습 요약 (책·아티클·강의)
├── 40-Projects/       # 진행 중인 프로젝트 노트
├── 90-Archive/        # 아카이브
├── _attachments/      # 이미지·PDF 등 첨부 (Obsidian 자동 저장 폴더)
└── _templates/        # Obsidian 템플릿 (Templates 코어 플러그인용)
```

## 핵심 분리 원칙

**20-Company vs 30-Development**

| 기준 | 20-Company | 30-Development |
|------|-----------|----------------|
| 회사 떠날 때 | 폐기 / 인계 | 들고 감 |
| 내용 | 사내 시스템·결정·사람 | 일반 기술·패턴·교훈 |
| 예시 | "우리 결제 서비스의 환불 플로우" | "결제 시스템 설계 시 고려사항" |
| 민감도 | 비밀유지 가능 | 외부 공유 가능 (블로그·면접) |

같은 인시던트라도 두 곳에 나눠서 적습니다:
- `20-Company/troubleshooting/2026-04-결제-환불-실패.md` (사내 컨텍스트)
- `30-Development/troubleshooting/idempotency-key-conflict.md` (일반화된 교훈)

## 제공되는 템플릿 (`_templates/`)

| 템플릿 | 용도 |
|--------|------|
| `daily-note.md` | 일일 작업 로그 |
| `meeting-note.md` | 미팅 노트 (참석자·결정·액션) |
| `decision-log.md` | 의사결정 ADR (배경·결정·결과) |
| `tech-knowledge.md` | 기술 지식 엔트리 (개념·패턴·교훈) |
| `troubleshooting.md` | 트러블슈팅 로그 (증상·원인·해결·예방) |
| `company-glossary.md` | 회사 용어 한 항목 |
| `weekly-review.md` | 주간 회고 |

Obsidian → Settings → Templates → Template folder location → `_templates` 설정 후 사용.

## Tagging 컨벤션

- `#status/draft`, `#status/in-progress`, `#status/done`
- `#area/backend`, `#area/frontend`, `#area/infra`, `#area/product`
- `#topic/{이름}` — 자유 토픽 (예: `#topic/auth`, `#topic/payment`)
- `#company/{팀이름}` — 20-Company 하위에서만

## 권장 워크플로우

1. **캡처**: 모든 새 노트는 일단 `00-Inbox/`에 던짐
2. **데일리**: 매일 아침 daily-note 생성 → 그날 작업·미팅 링크
3. **분류**: 주 1회 `00-Inbox/` 비우기 → 적절한 폴더로 이동
4. **회고**: 주 1회 weekly-review 작성 → 흩어진 메모를 지식으로 연결

## Sync 옵션 (선택)

vault 동기화 방법 — 이 레포는 동기화에 관여하지 않습니다:

- **Obsidian Sync** ($) — 가장 매끄러움, E2E 암호화
- **iCloud / Dropbox** — 무료, 충돌 가능성 있음
- **Git** — 버전 관리 좋음, 모바일 셋업 번거로움 (Working Copy 등)

회사 지식이 들어간다면 **개인 git 레포 (private)** + Obsidian Git 플러그인 조합을 추천합니다.
