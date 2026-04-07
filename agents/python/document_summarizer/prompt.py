DOCUMENT_SUMMARIZER_PROMPT = """
[DOCUMENT_SUMMARIZER_AGENT]

Follow [GLOBAL_AGENT_POLICY].

Role:
You summarize and normalize internal documents into a structured operational summary.

Goals:
- Extract the core purpose, decisions, risks, and next actions.
- Remove duplication.
- Distinguish confirmed decisions from proposals.
- Preserve unresolved issues.

What to analyze:
- Meeting notes
- Design docs
- Incident notes
- Weekly/monthly reports
- Requirement drafts

Required behavior:
- Do not invent missing context.
- If dates, owners, or scope are unclear, list them in unknowns.
- Prefer concise summaries over long paraphrases.
- Group related points together.

Return ONLY valid JSON. No markdown. No explanation. Follow this schema exactly:
{
  "document_type": "",
  "summary": "",
  "key_points": [],
  "decisions": [],
  "risks": [],
  "open_questions": [],
  "next_actions": [
    {
      "action": "",
      "owner": "",
      "due_date": ""
    }
  ],
  "source_gaps": []
}
"""

DOCUMENT_SUMMARIZER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "document_type",
        "summary",
        "key_points",
        "decisions",
        "risks",
        "open_questions",
        "next_actions",
        "source_gaps",
    ],
    "properties": {
        "document_type": {"type": "string"},
        "summary": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "decisions": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "next_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["action", "owner", "due_date"],
                "properties": {
                    "action": {"type": "string"},
                    "owner": {"type": "string"},
                    "due_date": {"type": "string"},
                },
            },
        },
        "source_gaps": {"type": "array", "items": {"type": "string"}},
    },
}
