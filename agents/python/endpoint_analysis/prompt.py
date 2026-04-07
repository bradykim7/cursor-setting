ENDPOINT_ANALYSIS_PROMPT = """
[ENDPOINT_ANALYSIS_AGENT]

Follow [GLOBAL_AGENT_POLICY].

Role:
You analyze an endpoint and describe behavior, contracts, and change impact.

Goals:
- Explain request and response structure.
- Identify validation rules, defaults, and error cases.
- Detect documentation gaps and compatibility risks.
- Suggest meaningful test cases.

Required behavior:
- Compare code behavior and documentation when both are available.
- If behavior depends on flags, roles, or account types, list those conditions explicitly.
- Distinguish guaranteed behavior from inferred behavior.
- Prefer operationally useful summaries.

Return ONLY valid JSON. No markdown. No explanation. Follow this schema exactly:
{
  "endpoint": {
    "method": "",
    "path": ""
  },
  "summary": "",
  "request_fields": [
    {
      "name": "",
      "type": "",
      "required": false,
      "default": "",
      "validation": "",
      "notes": ""
    }
  ],
  "response_fields": [
    {
      "name": "",
      "type": "",
      "nullable": false,
      "notes": ""
    }
  ],
  "behavior_notes": [],
  "error_cases": [
    {
      "status_code": 0,
      "condition": "",
      "response_body": ""
    }
  ],
  "dependencies": [],
  "compatibility_risks": [],
  "test_cases": [
    {
      "title": "",
      "input": "",
      "expected": "",
      "priority": "low"
    }
  ],
  "documentation_gaps": []
}
"""

ENDPOINT_ANALYSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "endpoint",
        "summary",
        "request_fields",
        "response_fields",
        "behavior_notes",
        "error_cases",
        "dependencies",
        "compatibility_risks",
        "test_cases",
        "documentation_gaps",
    ],
    "properties": {
        "endpoint": {
            "type": "object",
            "additionalProperties": False,
            "required": ["method", "path"],
            "properties": {
                "method": {"type": "string"},
                "path": {"type": "string"},
            },
        },
        "summary": {"type": "string"},
        "request_fields": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "type", "required", "default", "validation", "notes"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "required": {"type": "boolean"},
                    "default": {"type": "string"},
                    "validation": {"type": "string"},
                    "notes": {"type": "string"},
                },
            },
        },
        "response_fields": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "type", "nullable", "notes"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "nullable": {"type": "boolean"},
                    "notes": {"type": "string"},
                },
            },
        },
        "behavior_notes": {"type": "array", "items": {"type": "string"}},
        "error_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["status_code", "condition", "response_body"],
                "properties": {
                    "status_code": {"type": "integer"},
                    "condition": {"type": "string"},
                    "response_body": {"type": "string"},
                },
            },
        },
        "dependencies": {"type": "array", "items": {"type": "string"}},
        "compatibility_risks": {"type": "array", "items": {"type": "string"}},
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "input", "expected", "priority"],
                "properties": {
                    "title": {"type": "string"},
                    "input": {"type": "string"},
                    "expected": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
            },
        },
        "documentation_gaps": {"type": "array", "items": {"type": "string"}},
    },
}
