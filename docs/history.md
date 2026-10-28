# Project history

A summary of the old repository, <https://github.com/sheharahewawasam/FIT-4002-CHATBOT>.
Keep that repository archived (read-only) and do not delete it. It is the only record
of this history, but it also contains leaked credentials (see
[security-and-data.md](security-and-data.md)).

## Timeline (2026)

| Date | Milestone | Old commits |
| --- | --- | --- |
| 12 Apr | MVP uploaded: Cloudflare Worker + Vectorize + OpenAI, plus a Django demo | `864bc9a` |
| 26 Apr | Answer and embedding models moved to local Ollama | `6a35d6a` |
| 30 Apr – 4 May | S3 Vectors and OpenSearch tried. Reranking, HyDE and keyword search added. pypdf replaced by pdfplumber | `bbd59c7`, `2dc4431`, `d08bc2e` |
| 5 May – 4 Jun | PaddleOCR pipeline developed (merged in PR #2) | `ab202fc` … `5ff9fdb` |
| 12 May | Fully local stack: BGE embeddings, cross-encoder reranker, answer cache, front end served by Django (PR #1) | `cd9987e` |
| 22 May | Pinecone chosen as the only vector store | `43e9719` |
| 15 Jun | First VM deployment (OCI) running qwen3:1.7b | `ea819dd` |
| 10–16 Aug | User/fund UI (reverted, then re-merged), RAG metrics grader, header-based chunking, real filenames in citations, audit log | `e8424fa`, `0d4920a`, `947ea11`, `80a34de`, `b770a2f` |
| 21–29 Aug | Rate limiting (10/min), session timeout, send lock, cache made private to each user | `2b9d169`, `a531d5d`, `e0e797b` |
| 3 Sep | OCI Terraform. Database-backed advisors and funds. Per-user upload and ingestion | `4338568`, `72e824d` |
| 7 Sep | Path traversal and XSS fixed. First tests | `1f44082` |
| 9 Sep | Deployment hardening, model and thinking tuning, TOC filter fix (+2,137 vectors), cache scoped to each asker | `bc9d428`, `18e6cba`, `55973e2` |
| 14–16 Sep | Leaked `.env` untracked. Streaming added, then removed | `dfbe7d0`, `c221666`, `19da90f` |
| 23 Sep | Big merge of main into the feature branch. Sign-in and authorisation. TLS live on `triple-a-chatbot.duckdns.org` (EC2) | `dddcc5d`, `a52c198`, `62a62d0` |
| 25–28 Sep | Rate-limit fix, signed citation links, uploads re-enabled | `462cee2`, `7c39817`, `7655e3b` |
| 27 Sep – 3 Oct | Layout-aware chunking, VLM fallback for OCR, OCR made local-only | `6634f9d`, `c3d288f`, `4bcdec8` |
| 20 Oct | OCR logging. Last commit in the old repo | `967d1d4` |

## Branch map

`main` stopped moving on 22 September. The newest work is on the two branches below,
**which were never merged back into `main`**.

| Branch | State | Contents |
| --- | --- | --- |
| `feature/account-based-access` | 50 commits ahead of main | Auth, security fixes, deployment, citation grants, OCR integration. **The most complete version of the app** |
| `weihom-layout-aware-chunking` | 57 ahead; contains the branch above plus `ocr-testing` | Layout chunking, OCR/VLM work, OCR logging (latest, 20 Oct) |
| `ocr-testing` | merged into the branch above | PaddleOCR, confidence scoring, VLM prompts |
| `OCI_VM_deployment` | abandoned | First OCI deployment |
| `openAI-api` | abandoned | Original OpenAI/Cloudflare version |
| `Mark-DeleteDocs` | abandoned, untested | Delete documents via a JSON list |
| `Mark-ResponseTime` | 1 commit | Response times in RAG metrics (also on main as `38bce94`) |
| `Jun_edits`, `Shehara-Bubble-UI` | stale | Small edits only |
| `Mark-AuditLog`, `Mark-Rag-Metrics`, `Mark-UserFunds`, `Mark-docs`, `weihom`, `Shehara-ollama_debugged` | merged | — |

This repository's `views.py` matches `a52c198` and its `ocr_solution.py` matches old
`main`, so it is behind `feature/account-based-access`. See
[known-issues.md](known-issues.md).

## Contributors

Mark, weihom05, JunHaoN, yxuu0194, Skygeneral133, fx7165, sheharahewawasam. Areas each
person worked on, from the commit log:
- **Mark**: local Ollama move, retrieval pipeline (reranking, HyDE, BM25), user/fund UI, RAG metrics grader, audit log
- **weihom05**: vector store trials (S3, OpenSearch, Pinecone), header and layout chunking, rate limiting, session timeout, prompt changes
- **yxuu0194**: OCR (PaddleOCR, confidence, VLM), ATO form testing, test cases
- **JunHaoN**: deployment (OCI, EC2, TLS), security, auth, merges, uploads
- **sheharahewawasam**: MVP, fully local stack migration, repo admin
