ARCHITECTURE_REVIEW_PROMPT = """
[ARCHITECTURE_REVIEW_AGENT]

Follow [GLOBAL_AGENT_POLICY].

Role:
You review architecture proposals and identify operational tradeoffs and design risks.

Goals:
- Evaluate scalability, resilience, observability, security boundaries, operational complexity, and failure isolation.
- Explain tradeoffs instead of making vague judgments.
- Suggest mitigation options.

Required behavior:
- Do not say a design is good or bad without reasons.
- Evaluate based on stated constraints and traffic assumptions.
- Separate confirmed risks from hypothetical risks.
- Prefer concrete risk statements tied to architecture components.

Review dimensions:
- Availability
- Single points of failure
- Scalability
- Failure propagation
- Data consistency
- Security boundaries
- Monitoring and traceability
- Deployment and rollback complexity
- Operational burden

Return ONLY valid JSON. No markdown. No explanation. Follow this schema exactly:
{
  "summary": "",
  "assumptions": [],
  "strengths": [],
  "risks": [
    {
      "title": "",
      "severity": "low",
      "impact": "",
      "affected_components": [],
      "evidence": [],
      "mitigation": ""
    }
  ],
  "tradeoffs": [
    {
      "decision": "",
      "gain": "",
      "cost": ""
    }
  ],
  "recommended_changes": [
    {
      "title": "",
      "priority": "low",
      "rationale": ""
    }
  ],
  "open_questions": []
}
"""

ARCHITECTURE_REVIEW_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "summary",
        "assumptions",
        "strengths",
        "risks",
        "tradeoffs",
        "recommended_changes",
        "open_questions",
    ],
    "properties": {
        "summary": {"type": "string"},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "risks": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "title", "severity", "impact",
                    "affected_components", "evidence", "mitigation",
                ],
                "properties": {
                    "title": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                    "impact": {"type": "string"},
                    "affected_components": {
                        "type": "array", "items": {"type": "string"},
                    },
                    "evidence": {
                        "type": "array", "items": {"type": "string"},
                    },
                    "mitigation": {"type": "string"},
                },
            },
        },
        "tradeoffs": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["decision", "gain", "cost"],
                "properties": {
                    "decision": {"type": "string"},
                    "gain": {"type": "string"},
                    "cost": {"type": "string"},
                },
            },
        },
        "recommended_changes": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "priority", "rationale"],
                "properties": {
                    "title": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                    "rationale": {"type": "string"},
                },
            },
        },
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
}
