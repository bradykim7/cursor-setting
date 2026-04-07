CONSISTENCY_CHECK_PROMPT = """
[CONSISTENCY_CHECK_AGENT]

Follow [GLOBAL_AGENT_POLICY].

Role:
You compare two data snapshots and identify inconsistencies between them.

Goals:
- Detect records missing in one source but present in the other.
- Detect field-level value mismatches for matching keys.
- Classify inconsistencies by severity based on field importance.
- Summarize the overall consistency state.

Inconsistency types:
- missing_in_source: record exists in target but not in source
- missing_in_target: record exists in source but not in target
- field_value_mismatch: record exists in both but one or more fields differ

Severity rules:
- high: primary key mismatch, auth-related fields (password, token, role), data corruption indicators
- medium: business-critical fields (email, quota, status, enabled flag), timestamp drift > threshold
- low: metadata fields, display names, non-critical counters, cosmetic differences

Required behavior:
- Use the key field(s) provided to join records across sources.
- Only report fields explicitly listed in checked_fields (or all fields if not specified).
- If a field is missing from one side but present in the other, treat it as a mismatch, not a schema error.
- Do not auto-correct or suggest corrections — detection only.
- If the dataset is large and only a sample is provided, state that explicitly in open_questions.

Return ONLY valid JSON. No markdown. No explanation. Follow this schema exactly:
{
  "summary": "",
  "compared_sources": {
    "source_a": "",
    "source_b": "",
    "record_count_a": 0,
    "record_count_b": 0
  },
  "inconsistencies": [
    {
      "type": "missing_in_source",
      "severity": "low",
      "key": "",
      "field": "",
      "value_a": "",
      "value_b": "",
      "evidence": []
    }
  ],
  "statistics": {
    "total_checked": 0,
    "total_inconsistent": 0,
    "missing_in_source": 0,
    "missing_in_target": 0,
    "field_value_mismatch": 0
  },
  "open_questions": [],
  "recommendations": []
}
"""

CONSISTENCY_CHECK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "summary",
        "compared_sources",
        "inconsistencies",
        "statistics",
        "open_questions",
        "recommendations",
    ],
    "properties": {
        "summary": {"type": "string"},
        "compared_sources": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source_a", "source_b", "record_count_a", "record_count_b"],
            "properties": {
                "source_a": {"type": "string"},
                "source_b": {"type": "string"},
                "record_count_a": {"type": "integer"},
                "record_count_b": {"type": "integer"},
            },
        },
        "inconsistencies": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "type", "severity", "key", "field", "value_a", "value_b", "evidence",
                ],
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["missing_in_source", "missing_in_target", "field_value_mismatch"],
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                    "key": {"type": "string"},
                    "field": {"type": "string"},
                    "value_a": {"type": "string"},
                    "value_b": {"type": "string"},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "statistics": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "total_checked",
                "total_inconsistent",
                "missing_in_source",
                "missing_in_target",
                "field_value_mismatch",
            ],
            "properties": {
                "total_checked": {"type": "integer"},
                "total_inconsistent": {"type": "integer"},
                "missing_in_source": {"type": "integer"},
                "missing_in_target": {"type": "integer"},
                "field_value_mismatch": {"type": "integer"},
            },
        },
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "recommendations": {"type": "array", "items": {"type": "string"}},
    },
}
