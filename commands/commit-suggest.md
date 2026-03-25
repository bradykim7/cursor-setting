---
description: Analyze staged files and git history to recommend a commit message
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [optional context]
---

# Commit Message Recommendation

Analyze the currently staged files and recent git history to recommend an appropriate commit message following best practices.

## Instructions

1. **Check Repository Status**
   - Run `git status` to see staged files
   - If no files are staged, inform the user and suggest staging files first

2. **Analyze Staged Changes**
   - Run `git diff --staged` to review what will be committed
   - Identify the scope and nature of changes (features, fixes, refactoring, etc.)

3. **Review Recent History**
   - Run `git log --oneline -10` to see recent commit patterns
   - Check the project's commit message style and conventions

4. **Determine Commit Type**
   Based on the changes, categorize using conventional commit types:
   - `feat:` - New features or functionality
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes only
   - `style:` - Code style/formatting (no logic changes)
   - `refactor:` - Code restructuring without changing behavior
   - `perf:` - Performance improvements
   - `test:` - Adding or updating tests
   - `build:` - Build system or dependency changes
   - `ci:` - CI/CD configuration changes
   - `chore:` - Routine tasks, maintenance

5. **Generate Recommendations**
   Provide 3-5 commit message options:
   - **Primary recommendation**: Most accurate based on changes
   - **Alternative options**: Different perspectives or scopes
   - Each message should:
     - Start with type and optional scope: `type(scope): description`
     - Use imperative mood: "add" not "added" or "adds"
     - Be concise but descriptive (50-72 chars for subject)
     - Include body if changes need explanation
	 - Generate English version and also Korean version

6. **Additional Context**
   - If `$ARGUMENTS` provided, incorporate that context into recommendations
   - Highlight breaking changes if detected
   - Suggest adding co-authors if multiple contributors in recent commits

## Example Output Format

```
Based on your staged changes, here are my commit message recommendations:

✨ Primary Recommendation:
feat(auth): add OAuth2 login with Google provider

📝 Alternative Options:
1. feat(user): implement social authentication for login
2. feat: add Google OAuth2 integration to authentication system
3. feat(auth): enable third-party login via OAuth2

💡 Details:
- Detected changes in: src/auth/, config/oauth.ts
- Type: New feature (OAuth implementation)
- Scope: Authentication system
- Recent commits follow conventional commits style

Would you like me to:
- Create the commit with one of these messages?
- Add a detailed commit body?
- Modify any of these suggestions?
```

## Notes

- Follow the project's existing commit conventions
- Keep subject lines under 72 characters
- Use present tense, imperative mood
- Focus on "what" and "why", not "how"
