"""
Architecture Review Agent - 평가 케이스 10개
"""

EVAL_CASES = [
    # 1. 단일 장애점(SPOF) 감지
    {
        "id": "eval_001",
        "description": "단일 서버 배포에서 SPOF 감지",
        "input": {
            "system_name": "consistency-check-platform",
            "architecture_text": """
모든 컴포넌트(API, Checker, Redis, PostgreSQL)를
단일 서버에 Docker Compose로 배포.
""",
            "constraints": ["운영 트래픽 영향 없어야 함"],
        },
        "expect": {
            "has_spof_risk": True,
            "risk_severity_high_or_medium": True,
        },
    },

    # 2. 트레이드오프 명시 검증
    {
        "id": "eval_002",
        "description": "Redis 캐시 사용의 트레이드오프 명시",
        "input": {
            "system_name": "snapshot-cache",
            "architecture_text": """
스냅샷을 Redis에 TTL 1시간으로 캐싱.
만료 전 비교 수행 필수.
""",
            "constraints": ["읽기 중심 설계"],
        },
        "expect": {
            "tradeoffs_not_empty": True,
            "tradeoff_has_gain_and_cost": True,
        },
    },

    # 3. 실패 전파 리스크
    {
        "id": "eval_003",
        "description": "점검 서비스 실패가 운영에 전파되는 리스크",
        "input": {
            "system_name": "checker",
            "architecture_text": """
Consistency Checker가 MariaDB 운영 DB에
직접 쿼리를 실행해 스냅샷 수집.
""",
            "constraints": ["서비스 오류가 운영으로 전파되면 안 됨"],
        },
        "expect": {
            "has_failure_propagation_risk": True,
            "recommended_changes_not_empty": True,
        },
    },

    # 4. 보안 경계 누락
    {
        "id": "eval_004",
        "description": "내부 API에 인증 없음",
        "input": {
            "system_name": "api-server",
            "architecture_text": """
관리자용 점검 결과 API.
현재 인증 없이 내부 네트워크에서만 접근 가능하도록 설정.
""",
            "constraints": ["내부 관리자만 조회"],
        },
        "expect": {
            "has_security_risk": True,
            "open_questions_not_empty": True,
        },
    },

    # 5. 확장성 리스크
    {
        "id": "eval_005",
        "description": "단일 프로세스 배치의 확장성 한계",
        "input": {
            "system_name": "batch-checker",
            "architecture_text": """
매일 새벽 2시에 단일 Python 프로세스가
1,000개 서버의 SQLite 파일을 순차적으로 비교.
""",
            "traffic_assumptions": ["메일 서버 1,000대", "배치 완료 목표: 2시간 이내"],
        },
        "expect": {
            "has_scalability_risk": True,
            "recommended_changes_not_empty": True,
        },
    },

    # 6. 데이터 일관성 - 스냅샷 시점 차이
    {
        "id": "eval_006",
        "description": "두 스냅샷 수집 시점 차이로 인한 false positive",
        "input": {
            "system_name": "snapshot-collector",
            "architecture_text": """
MariaDB 스냅샷을 먼저 수집하고,
SQLite 스냅샷을 이후 수집.
두 수집 사이 간격은 최대 10분.
""",
            "constraints": ["스냅샷 비교 정확도 중요"],
        },
        "expect": {
            "has_consistency_risk": True,
        },
    },

    # 7. 모니터링/관찰가능성 누락
    {
        "id": "eval_007",
        "description": "배치 실패 감지 및 알림 부재",
        "input": {
            "system_name": "scheduler",
            "architecture_text": """
cron으로 배치 실행.
실패 시 로그 파일에만 기록.
알림이나 모니터링 대시보드 없음.
""",
            "constraints": ["운영팀이 장애를 빠르게 인지해야 함"],
        },
        "expect": {
            "has_observability_risk": True,
            "recommended_changes_not_empty": True,
        },
    },

    # 8. 롤백 복잡도
    {
        "id": "eval_008",
        "description": "DB 스키마 변경 포함 배포의 롤백 복잡도",
        "input": {
            "system_name": "result-db",
            "architecture_text": """
Result DB(PostgreSQL) 스키마 변경이 배포에 포함.
마이그레이션은 배포 시 자동 실행.
롤백 절차 미정의.
""",
            "constraints": ["배포 실패 시 빠른 롤백 필요"],
        },
        "expect": {
            "has_deployment_risk": True,
            "open_questions_not_empty": True,
        },
    },

    # 9. 강점 + 리스크 균형 — 잘 설계된 케이스
    {
        "id": "eval_009",
        "description": "잘 설계된 아키텍처 - 강점도 명시해야 함",
        "input": {
            "system_name": "well-designed-checker",
            "architecture_text": """
- read replica만 사용해 운영 DB 영향 없음
- Checker는 별도 서버에서 실행 — 장애 격리
- 결과 DB는 운영 DB와 완전히 분리
- 배치 실패 시 Slack 알림
- 자동 수정 없이 감지만 수행
""",
            "constraints": ["운영 트래픽 영향 없어야 함", "읽기 중심 설계"],
        },
        "expect": {
            "strengths_not_empty": True,
            "risk_severity_no_high": True,
        },
    },

    # 10. 제약 조건 미충족 감지
    {
        "id": "eval_010",
        "description": "명시된 제약 조건을 충족하지 못하는 설계 감지",
        "input": {
            "system_name": "constraint-violation",
            "architecture_text": """
Snapshot Collector가 MariaDB 운영 primary에
직접 SELECT 쿼리 실행.
초당 최대 100 queries 예상.
""",
            "constraints": [
                "운영 DB 직접 접근 제한 — 읽기 전용 replica만 허용",
                "운영 트래픽 영향 없어야 함",
            ],
        },
        "expect": {
            "risk_points_not_empty": True,
            "evidence_mentions_constraint": True,
        },
    },
]
