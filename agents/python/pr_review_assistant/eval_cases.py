"""
PR Review Assistant Agent - 평가 케이스 10개
"""

EVAL_CASES = [
    # 1. limit 기본값 변경 - 하위 호환성
    {
        "id": "eval_001",
        "description": "limit 기본값 변경으로 인한 하위 호환성 리스크 감지",
        "input": {
            "pr_title": "feat: limit 기본값 20 -> 50 변경",
            "diff": """\
-        $limit = min((int) $request->input('limit', 20), 100);
+        $limit = min((int) $request->input('limit', 50), 100);
""",
        },
        "expect": {
            "compatibility_risks_not_empty": True,
            "has_high_or_medium_risk": True,
        },
    },

    # 2. N+1 쿼리
    {
        "id": "eval_002",
        "description": "N+1 쿼리 패턴 감지",
        "input": {
            "diff": """\
+        $mails = Mail::where('user_id', $userId)->get();
+        foreach ($mails as $mail) {
+            $mail->sender;
+            $mail->attachments;
+        }
""",
        },
        "expect": {
            "has_performance_risk": True,
            "risk_points_not_empty": True,
        },
    },

    # 3. 인증 누락
    {
        "id": "eval_003",
        "description": "인증 미들웨어 누락 감지",
        "input": {
            "diff": """\
+    Route::get('/api/v2/admin/users', [AdminController::class, 'index']);
""",
            "context": {
                "routes/api.php": """\
Route::middleware('auth')->group(function () {
    Route::get('/api/v2/mail', [MailController::class, 'index']);
});
// 신규 라우트는 middleware 밖에 추가됨
Route::get('/api/v2/admin/users', [AdminController::class, 'index']);
""",
            },
        },
        "expect": {
            "has_security_risk": True,
            "risk_severity_high": True,
        },
    },

    # 4. SQL 인젝션 가능성
    {
        "id": "eval_004",
        "description": "Raw SQL에서 미검증 입력 사용",
        "input": {
            "diff": """\
+        $results = DB::select("SELECT * FROM accounts WHERE email = '{$email}'");
""",
        },
        "expect": {
            "has_security_risk": True,
            "risk_severity_high": True,
        },
    },

    # 5. 에러 핸들링 누락
    {
        "id": "eval_005",
        "description": "외부 API 호출에 try-catch 없음",
        "input": {
            "diff": """\
+        $response = Http::post('https://external-api.example.com/notify', [
+            'user_id' => $userId,
+            'event'   => 'mail_sent',
+        ]);
+        $result = $response->json();
""",
        },
        "expect": {
            "risk_points_not_empty": True,
            "missing_tests_not_empty": True,
        },
    },

    # 6. 로깅 누락
    {
        "id": "eval_006",
        "description": "중요한 상태 변경에 로그 없음",
        "input": {
            "diff": """\
+    public function deleteAccount(int $accountId): void
+    {
+        Account::destroy($accountId);
+        Cache::forget("account:{$accountId}");
+    }
""",
        },
        "expect": {
            "risk_points_not_empty": True,
        },
    },

    # 7. Null 처리 누락
    {
        "id": "eval_007",
        "description": "nullable 필드에 대한 null 체크 없음",
        "input": {
            "diff": """\
+        $quota = $account->settings->quota;
+        if ($quota > 0) {
+            $this->enforceQuota($quota);
+        }
""",
            "context": {
                "Account.php": """\
class Account extends Model
{
    // settings 관계는 nullable - 설정이 없는 계정 존재
    public function settings(): HasOne
    {
        return $this->hasOne(AccountSettings::class);
    }
}
""",
            },
        },
        "expect": {
            "risk_points_not_empty": True,
            "needs_confirmation_present": True,
        },
    },

    # 8. 테스트 커버리지 - 분기 누락
    {
        "id": "eval_008",
        "description": "새 분기에 대한 테스트 케이스 누락",
        "input": {
            "diff": """\
+        if (in_array('alias', $types)) {
+            $results = array_merge($results, $this->searchAliases($query));
+        }
""",
            "context": {
                "AutoCompleteServiceTest.php": """\
class AutoCompleteServiceTest extends TestCase
{
    public function test_search_contacts() { ... }
    public function test_search_groups() { ... }
    // alias 테스트 없음
}
""",
            },
        },
        "expect": {
            "missing_tests_not_empty": True,
        },
    },

    # 9. 안전한 변경 - 리스크 없음
    {
        "id": "eval_009",
        "description": "안전한 변경 - 불필요한 리스크 보고 안 함",
        "input": {
            "diff": """\
-        // TODO: fix this later
+        // Fixed: use strict comparison
-        if ($count == 0) {
+        if ($count === 0) {
""",
        },
        "expect": {
            "no_high_risk": True,
            "safe_suggestions_or_empty_risk": True,
        },
    },

    # 10. 복합 케이스
    {
        "id": "eval_010",
        "description": "복합 케이스 - 다중 리스크 동시 감지",
        "input": {
            "pr_title": "refactor: 계정 삭제 로직 개선",
            "diff": """\
+    public function destroy(Request $request, int $id): JsonResponse
+    {
+        $account = Account::find($id);
+        $account->delete();
+        DB::table('sessions')->where('account_id', $id)->delete();
+        return response()->json(['deleted' => true]);
+    }
""",
        },
        "expect": {
            "risk_points_count_gte": 2,
            "questions_for_author_not_empty": True,
        },
    },
]
