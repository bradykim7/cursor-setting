# Agent 1: Document Summarizer

내부 문서를 구조화된 운영 요약으로 정규화하는 에이전트입니다.

## 설치

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

## 실행

```bash
# 데모 (내장 샘플 문서)
python agent.py --demo

# 파일 입력
python agent.py --file ./meeting_notes.md --type-hint meeting_notes

# 텍스트 직접 입력
python agent.py --text "회의록 내용..." --type-hint meeting_notes

# 결과를 파일로 저장
python agent.py --demo --output result.json
```

## 출력 스키마

```json
{
  "document_type": "string",
  "summary": "string",
  "key_points": ["string"],
  "decisions": ["string"],
  "risks": ["string"],
  "open_questions": ["string"],
  "next_actions": [
    { "action": "string", "owner": "string", "due_date": "string" }
  ],
  "source_gaps": ["string"]
}
```

## 필드 설명

| 필드 | 설명 |
|------|------|
| `document_type` | 감지된 문서 유형 |
| `summary` | 핵심 요약 (1-3문장) |
| `key_points` | 주요 내용 목록 |
| `decisions` | 확정된 결정 사항 (제안 제외) |
| `risks` | 식별된 리스크 |
| `open_questions` | 미결 사항 |
| `next_actions` | 후속 액션 (담당자 + 기한 포함) |
| `source_gaps` | 문서에서 불명확하거나 누락된 정보 |
