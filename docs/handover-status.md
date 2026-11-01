# Handover task register

Updated 1 November 2026. Joint coordination: Fred and Shehara.
Do not substitute code preparation for account-side completion or live evidence.

| Item | Status and evidence / next action |
|---|---|
| 3. Old repo visibility | Completed: FIT-4002-CHATBOT changed to PRIVATE and verified through GitHub on 1 November 2026. Not deleted or archived; files/history preserved. Previously fetched copies cannot be recalled. |
| 4. Adviser passwords | New installs now create unusable seed passwords. Existing databases are unchanged; rotate each account on every deployment and record completion privately. |
| 5. Chat throttling | Restored `UserRateThrottle` and original regression check. |
| 6. Citations / duplicate answers | Restored signed grants, route, source module and one-time frontend rendering. |
| 7. Upload defaults | Restored default enabled; deployment flag remains supported. |
| 8. OCR imports | Removed Chonkie; lazy Ollama imports for optional inference paths. |
| 9. OCR rewrite and logging | Restored confidence/VLM behaviour, model environment variables, OCR_ENABLED, page-path logs and elapsed-time logs; no native OCR benchmark run claimed. |
| 10. Dates | Restored actual calendar-date and reversed-range checks. |
| 11. Tests | Restored original 33 tests, plus focused handover checks; see verification below. |
| 12. Evaluation tools | Restored missing evaluation cases, OCR script and 22 fixture files (11 image/annotation pairs). Existing retrieval/chunk metrics and improved grader retained rather than overwritten with older regressions. |
| 13. Recall | Completed 1 November 2026: both secret names verified, then live GitHub evaluation passed with recall@5=8/10 and recall@60=8/10. Sample trustee and Ausis members facts are absent from the top-60 candidates. [Run evidence](https://github.com/sheharahewawasam/Triple-A-Super_Chatbot/actions/runs/41273655594). This measures retrieval, not generated-answer accuracy. |
| 14. Pinecone choice | Hybrid search/filter support documented; reason S3 Vectors/OpenSearch lost still needs team confirmation. |
| 15. Local models | Proposal documents privacy/cost tradeoffs; final motivation/client requirement still needs confirmation. |
| 16. HyDE / UI / Bubble | Shehara confirmed on 1 November 2026 that Bubble UI was not shipped. HyDE removal and the user/fund UI revert still need decision evidence. |
| 17. OCI → EC2 | Trial/shape limitation documented historically; actual decision owner/reason pending confirmation. |
| 18. People and account owners | Client/project owner recovered as Champ Mendis from Project_26.pdf. Supervisor and AWS/DuckDNS/Pinecone owners pending. |
| 19. Scope/delivery | Source-backed summary and implementation mapping in scope-and-delivery.md. Client acceptance not asserted. |
| 20. Infrastructure identifiers | Instance ID/region and actual Pinecone index/plan need owner confirmation; code defaults are not production evidence. |
| 21. Document dates | Three sample dates checked against source deed text and applied; remaining originals require review. Existing filename-derived dates marked for confirmation. Index metadata not changed. |
| 22. PDF backup | Procedure in backup-and-restore.md; destination, execution and next-team restore/access test still pending. |
| 23. Review / commit | Implementation/docs reviewed and committed in fba9e37, pushed to handover/fit-4002-chatbot; this follow-up records verified account and CI outcomes. |
| 24. PR | [Draft PR #1](https://github.com/sheharahewawasam/Triple-A-Super_Chatbot/pull/1), handover/fit-4002-chatbot → main. Keep unmerged while security and team evidence remain incomplete. |

## Verification

All 37 Django tests passed (33 restored plus four focused checks), using RAG_OFFLINE=1 and the
pinned Django 6.0.4 / DRF 3.17.1 in an isolated Python 3.14 environment. Focused
checks also cover invalid dates, seed-password defaults and import-light OCR.
The PR's Python 3.12 unit-test job passed on fba9e37. After the repository secrets
were saved and verified, the live retrieval rerun passed on 1 November 2026 with
8/10 at both top-5 context and top-60 candidates. The ten-case sample does not
establish general answer accuracy, OCR quality, production configuration or backup.

## Human review record

Fred and Shehara: record the exact commit, reviewer/date, findings, requested
changes and disposition for auth/fund grants, citation grants, upload ownership,
OCR fallback/resource use, dates, cache invalidation, deletion/ingestion failure
handling, deployment isolation and confidential-data handling. Review remains
pending until actual feedback is recorded. AI-assisted checks are not human approval.

Previously reported partial-upsert cleanup, file-deletion error handling,
interrupted ingestion recovery and slow live responses are not fixed by this port.
