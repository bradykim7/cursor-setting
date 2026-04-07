"""
Document Summarizer Agent - 평가 케이스
----------------------------------------
10개의 다양한 문서 유형으로 에이전트 품질을 검증합니다.
"""

EVAL_CASES = [
    # 1. 주간 보고서 - 정상 케이스
    {
        "id": "eval_001",
        "description": "주간 보고서 - 정보 완전",
        "input": {
            "document_type_hint": "weekly_report",
            "document_text": """
## 주간 보고 2026-W14

완료: API 마이그레이션 (PR #1234), Redis 버그 수정
결정: v1 API 종료일 2026-06-30 확정
리스크: 레거시 클라이언트 12개 미마이그레이션
다음 주: 레거시 클라이언트 정리 (박개발, 4/10)
""",
        },
        "expect": {
            "document_type": "weekly_report",
            "has_decisions": True,
            "has_next_actions": True,
            "next_actions_have_owner": True,
        },
    },

    # 2. 회의록 - 결정 사항 불명확
    {
        "id": "eval_002",
        "description": "회의록 - 결정 vs 제안 혼재",
        "input": {
            "document_type_hint": "meeting_notes",
            "document_text": """
## 미팅 메모

- 정합성 점검을 매일 돌리면 어떨까 얘기 나왔음
- 혹시 주 1회로 줄이는 건? → 아직 결정 못함
- 인프라팀에서 배치 스케줄 잡아줄 수 있다고 했음
""",
        },
        "expect": {
            "open_questions_not_empty": True,
            "source_gaps_not_empty": True,
        },
    },

    # 3. 인시던트 노트
    {
        "id": "eval_003",
        "description": "인시던트 노트",
        "input": {
            "document_type_hint": "incident_note",
            "document_text": """
인시던트 #892
발생: 2026-04-03 14:22 KST
원인: Redis TTL 설정값이 0으로 배포됨 → 세션 전체 만료
영향: 로그인 불가 약 40분
조치: TTL 값 복구 배포 완료 (14:58)
재발 방지: 배포 전 TTL 검증 스텝 추가 예정 (담당자 미정)
""",
        },
        "expect": {
            "document_type": "incident_note",
            "has_risks": True,
        },
    },

    # 4. 설계 문서 - 소유자 불명
    {
        "id": "eval_004",
        "description": "설계 문서 - 소유자 정보 없음",
        "input": {
            "document_type_hint": "design_doc",
            "document_text": """
## 정합성 점검 플랫폼 설계

목적: MariaDB와 SQLite 데이터 정합성을 주기적으로 비교
방식: 스냅샷 비교, 배치 실행
미결: 불일치 발견 시 자동 수정할지 수동 검토할지 결정 필요
""",
        },
        "expect": {
            "source_gaps_not_empty": True,
            "open_questions_not_empty": True,
        },
    },

    # 5. 빈 문서 엣지 케이스
    {
        "id": "eval_005",
        "description": "엣지 케이스 - 내용 거의 없는 문서",
        "input": {
            "document_type_hint": "unknown",
            "document_text": "TBD",
        },
        "expect": {
            "source_gaps_not_empty": True,
        },
    },

    # 6. 요구사항 초안
    {
        "id": "eval_006",
        "description": "요구사항 초안",
        "input": {
            "document_type_hint": "requirement_draft",
            "document_text": """
## 자동완성 API v3 요구사항 초안

- types 파라미터에 group 타입 추가
- 결과 최대 50개 → 100개로 변경
- 하위 호환성 유지 필수
- 예상 출시: 2026 Q3
- 검토자: 미정
""",
        },
        "expect": {
            "has_risks": True,
        },
    },

    # 7. 영어 문서
    {
        "id": "eval_007",
        "description": "영어 문서 처리",
        "input": {
            "document_type_hint": "meeting_notes",
            "document_text": """
## Team Sync - Apr 7

Done: Deployed hotfix for null pointer in mail parser
Decided: Freeze releases from Apr 20 to Apr 30 for QA
Risk: 3 PRs still in review that need to land before freeze
Owner for freeze plan: TBD
""",
        },
        "expect": {
            "has_decisions": True,
            "has_risks": True,
        },
    },

    # 8. 월간 보고서
    {
        "id": "eval_008",
        "description": "월간 보고서 - 항목 다수",
        "input": {
            "document_type_hint": "monthly_report",
            "document_text": """
## 2026년 3월 월간 보고

완료: API v2 출시, 인프라 마이그레이션 1단계
미완료: 모니터링 대시보드 고도화 (4월로 이월)
결정: SLA 목표 99.9% → 99.5%로 현실화
리스크: 레거시 DB 마이그레이션 지연 시 6월 목표 달성 불투명
다음달 목표: 정합성 점검 자동화, v1 종료 공지
""",
        },
        "expect": {
            "has_decisions": True,
            "has_risks": True,
            "has_next_actions": True,
        },
    },

    # 9. 중복 정보가 많은 문서
    {
        "id": "eval_009",
        "description": "중복 정보 제거 검증",
        "input": {
            "document_type_hint": "meeting_notes",
            "document_text": """
## 회의록

- Redis TTL 버그 수정 완료됨
- Redis TTL 문제가 해결됐다고 함
- TTL 이슈는 이번에 수정됐음
- 다음 배포는 4월 15일
- 4월 15일에 다음 배포 예정
- 배포는 15일에 함
""",
        },
        "expect": {
            "summary_concise": True,
        },
    },

    # 10. 미결 사항만 있는 문서
    {
        "id": "eval_010",
        "description": "결정 없이 미결 사항만 있는 문서",
        "input": {
            "document_type_hint": "meeting_notes",
            "document_text": """
## 킥오프 미팅

- 정합성 점검 주기를 어떻게 할지 논의 중
- 자동 수정 vs 수동 검토 방식 선택 필요
- 담당자 배정 아직 안됨
- 예산 승인 여부 미확인
""",
        },
        "expect": {
            "decisions_empty": True,
            "open_questions_not_empty": True,
            "source_gaps_not_empty": True,
        },
    },
]
