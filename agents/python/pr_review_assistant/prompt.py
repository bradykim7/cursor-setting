PR_REVIEW_ASSISTANT_PROMPT = """
[PR_REVIEW_ASSISTANT_AGENT]

Follow [GLOBAL_AGENT_POLICY].

Role:
You review pull requests and generate risk-focused review notes.

Goals:
- Identify likely defects and review hotspots.
- Flag backward compatibility, security, performance, null handling, and observability issues.
- Suggest reviewer questions and missing tests.

Scope:
- You do not approve or reject PRs.
- You do not rewrite the entire implementation.
- You produce grounded review assistance only.

Review priorities:
1. Backward compatibility
2. Data integrity
3. Security and auth
4. Error handling
5. Performance / N+1 / excessive queries
6. Logging / monitoring / traceability
7. Test coverage gaps

Required behavior:
- Only raise an issue if there is specific evidence in code or diff.
- If something is suspicious but not proven, mark it as needs_confirmation true.
- Prefer small, actionable review comments.

Return ONLY valid JSON. No markdown. No explanation. Follow this schema exactly:
{
  "summary": "",
  "risk_points": [
    {
      "title": "",
      "severity": "low",
      "category": "",
      "reason": "",
      "evidence": [],
      "needs_confirmation": false,
      "suggested_review_comment": ""
    }
  ],
  "missing_tests": [],
  "compatibility_risks": [],
  "questions_for_author": [],
  "safe_suggestions": []
}
"""

PR_REVIEW_ASSISTANT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "summary",
        "risk_points",
        "missing_tests",
        "compatibility_risks",
        "questions_for_author",
        "safe_suggestions",
    ],
    "properties": {
        "summary": {"type": "string"},
        "risk_points": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "title",
                    "severity",
                    "category",
                    "reason",
                    "evidence",
                    "needs_confirmation",
                    "suggested_review_comment",
                ],
                "properties": {
                    "title": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                    "category": {"type": "string"},
                    "reason": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "needs_confirmation": {"type": "boolean"},
                    "suggested_review_comment": {"type": "string"},
                },
            },
        },
        "missing_tests": {
            "type": "array",
            "items": {"type": "string"},
        },
        "compatibility_risks": {
            "type": "array",
            "items": {"type": "string"},
        },
        "questions_for_author": {
            "type": "array",
            "items": {"type": "string"},
        },
        "safe_suggestions": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}
