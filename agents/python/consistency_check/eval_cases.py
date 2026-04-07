"""
Consistency Check Agent - 평가 케이스 10개
------------------------------------------
다양한 불일치 유형과 엣지 케이스로 에이전트 품질을 검증합니다.
"""

EVAL_CASES = [
    # 1. 완전히 일치하는 데이터
    {
        "id": "eval_001",
        "description": "완전 일치 - 불일치 없음",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120, "status": "active"},
                {"account_id": "acct_002", "email": "bob@example.com",   "quota_mb": 2048, "status": "active"},
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120, "status": "active"},
                {"account_id": "acct_002", "email": "bob@example.com",   "quota_mb": 2048, "status": "active"},
            ],
        },
        "expect": {
            "inconsistencies_empty": True,
            "total_inconsistent": 0,
        },
    },

    # 2. target에 레코드 누락
    {
        "id": "eval_002",
        "description": "missing_in_target 감지",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "status": "active"},
                {"account_id": "acct_002", "email": "bob@example.com",   "status": "active"},
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "status": "active"},
                # acct_002 누락
            ],
        },
        "expect": {
            "has_missing_in_target": True,
            "missing_in_target_count": 1,
        },
    },

    # 3. source에 레코드 누락
    {
        "id": "eval_003",
        "description": "missing_in_source 감지",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "status": "active"},
                # acct_002 누락
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "status": "active"},
                {"account_id": "acct_002", "email": "bob@example.com",   "status": "active"},
            ],
        },
        "expect": {
            "has_missing_in_source": True,
            "missing_in_source_count": 1,
        },
    },

    # 4. 필드 값 불일치 - quota_mb (medium)
    {
        "id": "eval_004",
        "description": "field_value_mismatch - quota_mb (medium severity)",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120, "status": "active"},
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 1024, "status": "active"},
            ],
        },
        "expect": {
            "has_field_value_mismatch": True,
            "mismatch_field": "quota_mb",
            "severity_medium_or_high": True,
        },
    },

    # 5. 상태 불일치 - status + enabled (medium)
    {
        "id": "eval_005",
        "description": "field_value_mismatch - status 및 enabled 동시 불일치",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_003", "email": "carol@example.com", "status": "suspended", "enabled": False},
            ],
            "records_b": [
                {"account_id": "acct_003", "email": "carol@example.com", "status": "active",    "enabled": True},
            ],
        },
        "expect": {
            "has_field_value_mismatch": True,
            "inconsistencies_count_gte": 2,
        },
    },

    # 6. 이메일 불일치 (high)
    {
        "id": "eval_006",
        "description": "field_value_mismatch - email (high severity)",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_007", "email": "original@example.com", "status": "active"},
            ],
            "records_b": [
                {"account_id": "acct_007", "email": "changed@example.com",  "status": "active"},
            ],
        },
        "expect": {
            "has_field_value_mismatch": True,
            "has_high_severity": True,
        },
    },

    # 7. 복합 케이스 - 누락 + 값 불일치 혼합
    {
        "id": "eval_007",
        "description": "복합 케이스 - missing + mismatch 동시 발생",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120},
                {"account_id": "acct_002", "email": "bob@example.com",   "quota_mb": 2048},
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 9999},  # mismatch
                # acct_002 누락
                {"account_id": "acct_003", "email": "new@example.com",   "quota_mb": 1024},  # source에 없음
            ],
        },
        "expect": {
            "has_missing_in_source": True,
            "has_missing_in_target": True,
            "has_field_value_mismatch": True,
            "inconsistencies_count_gte": 3,
        },
    },

    # 8. 빈 소스 A
    {
        "id": "eval_008",
        "description": "엣지 케이스 - 소스 A가 비어 있음",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "status": "active"},
            ],
        },
        "expect": {
            "has_missing_in_source": True,
            "open_questions_not_empty": True,
        },
    },

    # 9. 대용량 암시 - 샘플만 제공
    {
        "id": "eval_009",
        "description": "샘플 데이터 - 전체 데이터셋 일부만 제공",
        "input": {
            "source_a_name": "MariaDB (1000건 중 5건 샘플)",
            "source_b_name": "SQLite (1000건 중 5건 샘플)",
            "key_field": "account_id",
            "records_a": [
                {"account_id": f"acct_{i:03d}", "email": f"user{i}@example.com", "quota_mb": 2048}
                for i in range(1, 6)
            ],
            "records_b": [
                {"account_id": f"acct_{i:03d}", "email": f"user{i}@example.com", "quota_mb": 2048}
                for i in range(1, 6)
            ],
        },
        "expect": {
            "open_questions_not_empty": True,
        },
    },

    # 10. 필드 존재 불일치 (한쪽에만 필드 있음)
    {
        "id": "eval_010",
        "description": "한쪽에만 필드가 존재하는 경우",
        "input": {
            "source_a_name": "MariaDB",
            "source_b_name": "SQLite",
            "key_field": "account_id",
            "records_a": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120, "extra_field": "value"},
            ],
            "records_b": [
                {"account_id": "acct_001", "email": "alice@example.com", "quota_mb": 5120},
                # extra_field 없음
            ],
        },
        "expect": {
            "has_field_value_mismatch": True,
        },
    },
]
