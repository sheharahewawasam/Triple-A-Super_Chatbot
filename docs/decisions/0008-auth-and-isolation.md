# 0008 — Django sessions, with fund scope derived on the server

**Status:** Accepted (`72e824d`, `a52c198`, `55973e2`)

## Context
Advisers started with a dropdown, and `{"user": "John"}` in the request body was the
entire identity check. Worse, the fund list also came from the request body, so a
signed-in adviser could read any fund's deeds by naming it.

## Decision
- `Advisor` and `Fund` are database models (they replaced a hard-coded dictionary) and
  `Advisor` is linked to `django.contrib.auth.User`. Login uses sessions with CSRF.
  Cookies are HttpOnly and SameSite=Lax, and Secure once TLS is on.
- DRF requires authentication by default. Only the endpoints in `auth.py` allow
  anonymous access.
- `permitted_funds()` intersects the requested funds with the advisor's grant, so a
  request can narrow the scope but never widen it. `build_access_filter()` builds the
  Pinecone filter "fund in grant OR owner = me".
- The cache key includes the asker and their fund scope.
- Rate limits: 10 chat requests a minute per user (must use `UserRateThrottle`; see
  [known-issues.md](../known-issues.md)), plus a separate login throttle.

## Consequences
- Accounts are created in migration `0006` with the placeholder password `admin`.
- Migrations `0003`/`0004` exist because two branches each added advisors (TestAdvisor
  for the TestData funds, and two advisers from main), and they were reconciled in the
  23 Sep merge.
- Tests in `rag_api/tests.py` enforce isolation. Keep them passing.
