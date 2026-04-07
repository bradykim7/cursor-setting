"""
Endpoint Analysis Agent - 평가 케이스 10개
"""

EVAL_CASES = [
    # 1. 코드 + 스펙 모두 있음 - 차이 감지
    {
        "id": "eval_001",
        "description": "코드와 스펙 불일치 감지 (alias 타입)",
        "input": {
            "method": "GET",
            "path": "/api/v2/mail/auto-complete",
            "has_code": True,
            "has_spec": True,
        },
        "expect": {
            "documentation_gaps_not_empty": True,
            "compatibility_risks_not_empty": True,
        },
    },

    # 2. 코드만 있고 스펙 없음
    {
        "id": "eval_002",
        "description": "코드만 있을 때 스펙 부재를 documentation_gaps에 기록",
        "input": {
            "method": "POST",
            "path": "/api/v2/mail/send",
            "has_code": True,
            "has_spec": False,
            "code": """
public function send(Request $request): JsonResponse {
    $to = $request->input('to');
    $subject = $request->input('subject', '(no subject)');
    $body = $request->input('body');
    if (!$to) return response()->json(['error' => 'to is required'], 422);
    $this->mailService->dispatch($to, $subject, $body);
    return response()->json(['status' => 'queued']);
}
""",
        },
        "expect": {
            "documentation_gaps_not_empty": True,
            "request_fields_not_empty": True,
        },
    },

    # 3. 스펙만 있고 코드 없음
    {
        "id": "eval_003",
        "description": "스펙만 있을 때 inferred behavior 명시",
        "input": {
            "method": "GET",
            "path": "/api/v2/accounts",
            "has_code": False,
            "has_spec": True,
            "spec": """
/api/v2/accounts:
  get:
    parameters:
      - name: page
        in: query
        schema:
          type: integer
          default: 1
      - name: per_page
        in: query
        schema:
          type: integer
          default: 20
          maximum: 100
""",
        },
        "expect": {
            "behavior_notes_not_empty": True,
        },
    },

    # 4. 에러 케이스 추출
    {
        "id": "eval_004",
        "description": "다양한 에러 케이스 추출",
        "input": {
            "method": "POST",
            "path": "/api/v1/auth/login",
            "code": """
public function login(Request $request): JsonResponse {
    $email = $request->input('email');
    $password = $request->input('password');
    if (!$email || !$password) {
        return response()->json(['error' => 'Missing credentials'], 400);
    }
    $user = User::where('email', $email)->first();
    if (!$user || !Hash::check($password, $user->password)) {
        return response()->json(['error' => 'Invalid credentials'], 401);
    }
    if ($user->is_locked) {
        return response()->json(['error' => 'Account locked'], 403);
    }
    return response()->json(['token' => $user->createToken()]);
}
""",
        },
        "expect": {
            "error_cases_count_gte": 3,
        },
    },

    # 5. 하위 호환성 리스크
    {
        "id": "eval_005",
        "description": "필드 타입 변경으로 인한 호환성 리스크",
        "input": {
            "method": "GET",
            "path": "/api/v2/mail/folders",
            "code": """
// v1: folder_id was string
// v2: folder_id is now integer
return response()->json([
    'folders' => $folders->map(fn($f) => [
        'folder_id' => (int) $f->id,  // changed from string
        'name' => $f->name,
        'count' => $f->mail_count,
    ])
]);
""",
        },
        "expect": {
            "compatibility_risks_not_empty": True,
        },
    },

    # 6. 권한/롤 분기
    {
        "id": "eval_006",
        "description": "권한에 따른 동작 분기 감지",
        "input": {
            "method": "GET",
            "path": "/api/v2/admin/users",
            "code": """
public function index(Request $request): JsonResponse {
    if (!$request->user()->isAdmin()) {
        return response()->json(['error' => 'Forbidden'], 403);
    }
    $users = User::paginate(50);
    return response()->json($users);
}
""",
        },
        "expect": {
            "behavior_notes_not_empty": True,
            "error_cases_not_empty": True,
        },
    },

    # 7. N+1 위험이 있는 엔드포인트
    {
        "id": "eval_007",
        "description": "N+1 쿼리 위험 감지",
        "input": {
            "method": "GET",
            "path": "/api/v2/mail/list",
            "code": """
public function list(): JsonResponse {
    $mails = Mail::where('user_id', auth()->id())->get();
    return response()->json($mails->map(fn($mail) => [
        'id' => $mail->id,
        'subject' => $mail->subject,
        'sender' => $mail->sender->email,  // N+1 here
        'attachments' => $mail->attachments->count(),  // N+1 here
    ]));
}
""",
        },
        "expect": {
            "behavior_notes_not_empty": True,
        },
    },

    # 8. 페이지네이션 경계값
    {
        "id": "eval_008",
        "description": "페이지네이션 경계값 테스트케이스 생성",
        "input": {
            "method": "GET",
            "path": "/api/v2/contacts",
            "code": """
$page = max(1, (int) $request->input('page', 1));
$perPage = min(max(1, (int) $request->input('per_page', 20)), 100);
$contacts = Contact::paginate($perPage, ['*'], 'page', $page);
""",
        },
        "expect": {
            "test_cases_not_empty": True,
            "test_cases_have_high_priority": True,
        },
    },

    # 9. 완전히 비어있는 입력
    {
        "id": "eval_009",
        "description": "엣지 케이스 - 코드/스펙 없이 경로만",
        "input": {
            "method": "DELETE",
            "path": "/api/v2/mail/{id}",
            "code": None,
            "spec": None,
        },
        "expect": {
            "documentation_gaps_not_empty": True,
            "summary_not_empty": True,
        },
    },

    # 10. 복잡한 필터 파라미터
    {
        "id": "eval_010",
        "description": "복수 필터 파라미터의 검증 규칙 추출",
        "input": {
            "method": "GET",
            "path": "/api/v2/mail/search",
            "code": """
$query = $request->input('q');
$from = $request->input('from');
$to = $request->input('to');
$dateFrom = $request->input('date_from');
$dateTo = $request->input('date_to');
$hasAttachment = filter_var($request->input('has_attachment', false), FILTER_VALIDATE_BOOLEAN);
$folder = $request->input('folder', 'inbox');

if ($dateFrom && $dateTo && strtotime($dateFrom) > strtotime($dateTo)) {
    return response()->json(['error' => 'date_from must be before date_to'], 422);
}
""",
        },
        "expect": {
            "request_fields_not_empty": True,
            "error_cases_not_empty": True,
        },
    },
]
