# Agent 2: Endpoint Analysis

API 엔드포인트의 요청/응답 구조, 검증 규칙, 에러 케이스,
하위 호환성 리스크, 테스트 케이스를 구조화해서 분석합니다.

## 실행

```bash
# 데모
python agent.py --demo

# 코드 파일 직접 지정
python agent.py \
  --code AutoCompleteController.php AutoCompleteService.php \
  --method GET \
  --path /api/v2/mail/auto-complete \
  --focus "backward_compatibility" "null_handling"

# 스펙 파일 포함
python agent.py \
  --code Controller.php \
  --spec openapi.yaml \
  --method POST \
  --path /api/v2/mail/send \
  --output result.json
```

## 출력 스키마

```json
{
  "endpoint": { "method": "GET", "path": "/api/v2/..." },
  "summary": "string",
  "request_fields": [
    { "name": "", "type": "", "required": false, "default": "", "validation": "", "notes": "" }
  ],
  "response_fields": [
    { "name": "", "type": "", "nullable": false, "notes": "" }
  ],
  "behavior_notes": ["string"],
  "error_cases": [
    { "status_code": 400, "condition": "", "response_body": "" }
  ],
  "dependencies": ["string"],
  "compatibility_risks": ["string"],
  "test_cases": [
    { "title": "", "input": "", "expected": "", "priority": "high" }
  ],
  "documentation_gaps": ["string"]
}
```

## 필드 설명

| 필드 | 설명 |
|------|------|
| `request_fields` | 요청 파라미터별 타입·필수여부·검증규칙 |
| `response_fields` | 응답 필드별 타입·nullable 여부 |
| `behavior_notes` | 코드에서 발견된 동작 특이사항 |
| `error_cases` | HTTP 상태코드별 에러 조건과 응답 |
| `dependencies` | 의존하는 서비스·DB·외부 시스템 |
| `compatibility_risks` | 하위 호환성 위험 항목 |
| `test_cases` | 우선순위별 테스트 케이스 제안 |
| `documentation_gaps` | 코드와 스펙 간 불일치·누락 항목 |
