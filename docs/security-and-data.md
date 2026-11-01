# Security and data handling

## Leaked credentials in the old repository — action required

The old repository was **public** and tracked `mvp_demo/.env` from its first commit
(`864bc9a`). `mvp_demo/.env.template` contained real values as well. Together they
exposed an **OpenAI API key** (`sk-proj…`) and a **Cloudflare API token** (`cfut_…`).
Both were untracked on 14 Sep (`dfbe7d0`), but they remain in history on 17 branches.

- Shehara confirmed on 1 November 2026 that the leaked OpenAI key and Cloudflare
  token were deleted. This is owner-reported completion; provider dashboards were
  not independently inspected. Treat the historical values as compromised.
- Check the Pinecone key in the same way. A key that was ever committed should be
  rotated.
- Make the old repository private or archive it. Deleting files does not remove them
  from git history.
- `cloudflare_demo/.wrangler/` (local Wrangler state, including an account file) was
  also committed.

The current source excludes runtime secrets. Previously tracked audit transcripts
were removed from the current tree in this handover update, but remain in earlier
commits. Restrict access and handle historical data separately; no history was rewritten.

## What must never be committed

The `.gitignore` covers these, and the reasons are below:
- **Fund PDFs**: confidential client documents, about 40–56 MB per set. Keep them
  outside the checkout and pass their path to `ingest.py`.
- **`audit_logs/`**: transcripts of real adviser questions and answers about real
  funds. Some were committed to the old repo by accident and removed in `dddcc5d`.
- **`db.sqlite3`**: a committed development database once shipped to the client VM
  (`bc9d428`).
- **`ocr_output/`, chunk snapshots**: tens of MB that every ingest run regenerates.
- Terraform `tfstate`/`tfvars`/`.terraform/` (for the OCI path).

When merging, a merge stages incoming files whatever `.gitignore` says. Check
`git status` for PDFs and logs before committing (`c3d288f`).

## Where data lives in production

- The **source PDFs** for citation links live on the VM in `/opt/chatbot/documents`,
  outside the checkout so `git pull` cannot touch them. `SOURCE_DOCUMENT_DIRS` in the
  host's `secrets.env` points there. If you rebuild the host without them, citations
  report "not stored on this server", which can look like a bug (`d533a94`).
- **Vectors** are in Pinecone. Bulk-ingested documents have no owner and are shared by
  everyone with access to the fund. Uploads carry `owner=<advisor>`.
- **Accounts** are Django users linked to `Advisor`, and are in SQLite on the host.

## Access model (keep these properties)

- Every endpoint requires authentication by default (DRF). Only the endpoints in
  `rag_api/auth.py` allow anonymous callers.
- A user's fund scope is worked out on the server and never taken from the request.
  `permitted_funds()` intersects what was asked for with what the advisor was granted.
  Asking for a fund the advisor doesn't hold returns nothing, not an error, so funds
  cannot be enumerated (`a52c198`).
- `build_access_filter` must return `None` for an empty scope, never `{}`. An empty
  `{}` filter queries Pinecone with no filter and exposes every document (tested).
- The answer cache key includes the asker and their fund scope (`55973e2`).
- Citation downloads must use the signed per-advisor grant from `7c39817`, not a
  filename route. That fix has been restored; see
  [known-issues.md](known-issues.md).
- The audit log path is keyed by the advisor's primary key, with a containment check.
  It once allowed path traversal (`1f44082`).
- Escape all model output and citation text before it reaches `innerHTML`. Answers
  come from uploaded PDFs, which could contain hostile markup (`1f44082`).

## Deployment security notes

- New seed accounts have unusable passwords until individually provisioned. Rotate shared placeholder passwords on all existing deployments; the source change does not rotate them.
- Set `DJANGO_SECURE_COOKIES=true` only once TLS is in place. Set
  `DJANGO_TRUST_PROXY_PROTO=true` only while gunicorn binds to `127.0.0.1` behind
  nginx.
- certbot's default redirect only matched the certificate's hostname, so
  `http://<ip>/` served the app unencrypted. Port 80 now redirects unconditionally
  (`62a62d0`).
- Exceptions return a reference ID, not `str(e)`, so index names and file paths don't
  leak to the client (`bc9d428`).
- `.gitattributes` forces LF line endings. A CRLF `secrets.env` caused a hard-to-trace
  failure. Scripts committed from Windows lost their executable bit (`063bbc3`).

## Verification on 1 November 2026

A heuristic scan of credential-related blobs in fetched original histories confirmed
OpenAI- and Cloudflare-shaped values without printing them. No Pinecone key
candidate was found in that limited scan; this is not proof that none was ever
committed. Shehara subsequently confirmed deleting the leaked OpenAI key and
Cloudflare token on 1 November 2026. Account-side completion is owner-confirmed,
not independently verified through provider dashboards.
The old repository was made PRIVATE and verified through GitHub on 1 November 2026;
its files and history are preserved. Archiving alone would leave public history
readable. No repository was deleted; previously downloaded copies remain outside
the visibility change's control.
