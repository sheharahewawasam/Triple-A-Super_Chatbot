# Handover task register

Updated 1 November 2026. Joint coordination: Fred and Shehara.
Do not substitute code preparation for account-side completion or live evidence.

| Item | Status and evidence / next action |
|---|---|
| 1. OpenAI and Cloudflare revocation | Owner action pending. Historical credential-shaped values confirmed without displaying them. Revocation cannot be inferred from source deletion. |
| 2. Pinecone key | No candidate in the limited configuration-blob scan. Full history/account review and rotation if exposed remain pending. Never use a historical leaked key for testing. |
| 3. Old repo visibility | Owner sign-in required. Prefer private, optionally archive afterward; archive alone leaves history public. Do not delete. |
| 4. Adviser passwords | New installs now create unusable seed passwords. Existing databases are unchanged; rotate each account on every deployment and record completion privately. |
| 5. Chat throttling | Restored `UserRateThrottle` and original regression check. |
| 6. Citations / duplicate answers | Restored signed grants, route, source module and one-time frontend rendering. |
| 7. Upload defaults | Restored default enabled; deployment flag remains supported. |
| 8. OCR imports | Removed Chonkie; lazy Ollama imports for optional inference paths. |
| 9. OCR rewrite and logging | Restored confidence/VLM behaviour, model environment variables, OCR_ENABLED, page-path logs and elapsed-time logs; no native OCR benchmark run claimed. |
| 10. Dates | Restored actual calendar-date and reversed-range checks. |
| 11. Tests | Restored original 33 tests, plus focused handover checks; see verification below. |
| 12. Evaluation tools | Restored missing evaluation cases, OCR script and 22 fixture files (11 image/annotation pairs). Existing retrieval/chunk metrics and improved grader retained rather than overwritten with older regressions. |
| 13. Recall | Live rerun blocked on authorised Pinecone credentials, intended populated index and local BGE dependencies/models. Historical baseline is 8/10, not a newly measured result. |
| 14. Pinecone choice | Hybrid search/filter support documented; reason S3 Vectors/OpenSearch lost still needs team confirmation. |
| 15. Local models | Proposal documents privacy/cost tradeoffs; final motivation/client requirement still needs confirmation. |
| 16. HyDE / UI / Bubble | Historical implementation notes retained; motives and merge outcome need team evidence. |
| 17. OCI → EC2 | Trial/shape limitation documented historically; actual decision owner/reason pending confirmation. |
| 18. People and account owners | Client/project owner recovered as Champ Mendis from Project_26.pdf. Supervisor and AWS/DuckDNS/Pinecone owners pending. |
| 19. Scope/delivery | Source-backed summary and implementation mapping in scope-and-delivery.md. Client acceptance not asserted. |
| 20. Infrastructure identifiers | Instance ID/region and actual Pinecone index/plan need owner confirmation; code defaults are not production evidence. |
| 21. Document dates | Three sample dates checked against source deed text and applied; remaining originals require review. Existing filename-derived dates marked for confirmation. Index metadata not changed. |
| 22. PDF backup | Procedure in backup-and-restore.md; destination, execution and next-team restore/access test still pending. |
| 23. Review / commit | Changes reviewed locally; final commit identifier is supplied by Git history/PR rather than predicted here. |
| 24. PR | Target is handover/fit-4002-chatbot → main. Keep unmerged while security and team evidence remain incomplete. |

## Verification

All 37 Django tests passed (33 restored plus four focused checks), using RAG_OFFLINE=1 and the
pinned Django 6.0.4 / DRF 3.17.1 in an isolated Python 3.14 environment. Focused
checks also cover invalid dates, seed-password defaults and import-light OCR.
CI uses Python 3.12; its result must be checked separately. Offline checks do not
validate live Pinecone recall, OCR quality, production configuration or backup.

## Human review record

Fred and Shehara: record the exact commit, reviewer/date, findings, requested
changes and disposition for auth/fund grants, citation grants, upload ownership,
OCR fallback/resource use, dates, cache invalidation, deletion/ingestion failure
handling, deployment isolation and confidential-data handling. Review remains
pending until actual feedback is recorded. AI-assisted checks are not human approval.

Previously reported partial-upsert cleanup, file-deletion error handling,
interrupted ingestion recovery and slow live responses are not fixed by this port.
