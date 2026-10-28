# Known issues, tech debt and next steps

## 1. This repository is behind the old repository

This copy was assembled from different points in the old repository's history, and
several fixes made later are not in it. Comparing files with the old repo shows:

| Area in this repo | Matches old commit | Missing from this repo |
| --- | --- | --- |
| `rag_api/views.py` | `a52c198` (23 Sep, sign-in added) | Everything after it in that file, listed below |
| `ocr_solution.py` | old `main` (before 22 Sep) | The OCR rewrite and the import fix |
| `config/settings.py`, `deploy/*.sh`, `deploy/nginx-chatbot.conf` | latest (`feature/account-based-access`) | Nothing |

Fixes that exist in the old repo but **not here**, most important first:

1. **The chat rate limit does nothing** (`462cee2`). `ChatbotRateThrottle` subclasses
   `AnonRateThrottle`, which never throttles authenticated requests, and sign-in makes
   every request authenticated. 14 rapid requests produced no 429. Fix: subclass
   `UserRateThrottle`. See [views.py:28](../mvp_demo/rag_api/views.py#L28).
2. **Citation links return 404** (`7c39817`). The front end links to `../<file>.pdf`,
   and Django has no route for that ([index.html:482](../mvp_demo/index.html#L482)). The
   old repo added `rag_api/sources.py` and `/api/source/`, which serve a PDF only
   against a signed, expiring grant tied to the asking advisor, so a filename cannot be
   used to fetch another fund's deed. Bring back that design. Do not replace it with a
   plain filename route. In the same commit: each answer was rendered twice in the
   bubble.
3. **Uploads are off by default** (`7655e3b`). `DOCUMENT_UPLOADS_ENABLED` defaults to
   `false` here. It was turned off while the advisor's identity came from the request
   body. Sign-in now supplies the identity, so the old repo turned the default back on.
4. **OCR cannot be imported** (`a68e328`). `ocr_solution.py` imports `chonkie`, `ollama`
   and `langchain_text_splitters` at module level but never uses them. Without those
   packages, ingestion silently falls back to pdfplumber. It also builds a
   `SemanticChunker` and then throws its output away.
5. **The OCR rewrite and the `OCR_ENABLED` flag are missing** (`c3d288f`, `0efdf4a`,
   `714f23d`, `4bcdec8`). These add PaddleOCR with a confidence check and a vision-model
   fallback, make OCR run only when the text layer is thin, read the model names from
   environment variables (`OLLAMA_VLM_MODEL`, `OLLAMA_CLEANUP_MODEL`), and add a flag to
   turn OCR off on the VM (see [ADR 0006](decisions/0006-ocr.md)).
6. **Date filter validation is loose** (`c3d288f`). An input like `2024-13-45` silently
   becomes a number no document matches, when it should return a 400. A reversed date
   range is not rejected on the server.
7. **Tests**: the old branch had more tests in `rag_api/tests.py` (33 at its last run)
   than this copy has (25).
8. **Evaluation tools left out**: `eval_retrieval.py`, `evaluation_cases.py`,
   `Grader.py`, `chunk_structure_metrics.py`, `ocr_test.py` and its fixtures. See
   [evaluation.md](evaluation.md).

**Suggested next step:** port items 1–6 from old branch `feature/account-based-access`
before doing anything else. `weihom-layout-aware-chunking` also has OCR logging added
after that (`967d1d4`).

## 2. Known limitations (unfixed in either repo)

- **Answers about "this fund" get mixed up when several funds are in scope**
  (`55973e2`). `qwen3:1.7b` sometimes takes a value from one fund's document and
  attributes it to another. Questions that name the fund are reliable.
- **BM25 is not refitted when documents are uploaded.** Terms that appear only in
  uploads carry no IDF weight until `ingest.py` is re-run in full (`72e824d`).
- **Documents loaded by the bulk script cannot be deleted from the UI.** They have no
  `Document` row recording their Pinecone IDs. Only uploads can be deleted.
- **Most document dates are unknown.** Every row of the original ingest table carried a
  copied placeholder, "21 January 2012". Only dates stated in filenames were kept, the
  rest are `None`, and that is why the date filter is optional. Someone with the PDFs
  open needs to fill them in (`dddcc5d`).
- **Retrieval recall was 8/10** on the hand-checked facts. The remaining misses are
  ranking problems, not missing content.
- **Speed**: 20–35 s per uncached answer on a CPU host, and 90–230 s on the smallest VM
  tried. OCR takes 20–40 minutes for a 57-page deed (see
  [evaluation.md](evaluation.md)).
- **Memory**: the app needs about 4 GB of RAM at startup and cannot start without a
  valid Pinecone key.
- **OCR replaces the whole document.** When it triggers, it re-reads every page, so a
  mostly clean PDF swaps good extracted text for OCR output. Scoping OCR to the thin
  pages is the right fix and has not been done (`a68e328`).
- The cleanup-model default `qwen3.8` is probably a typo for `qwen3:8b` (`714f23d`).
- `Grader.py` copied and pasted the RAG logic from `views.py`, so it drifts out of
  date. Refactor the pipeline into a function both can import.

## 3. Tech debt

- `views.py` has two copies of the context-building block (around lines 325 and 499).
- The ~1500-character cap on each chunk and `num_ctx=8192` are tuned together. Change
  them together.
- `users.py` still exists alongside the database-backed `Advisor` and `Fund` models.
- Every account is created with the placeholder password `admin`.
- The OCI deployment files (Terraform, `mvp_demo/chatbot.service` on the old branches)
  were not carried over. EC2 is the only documented deployment.

## 4. Ideas not yet started

- Stream answers once the model is fast enough to justify it (see
  [tried-and-abandoned.md](tried-and-abandoned.md)).
- Run OCR only on thin pages.
- Refit BM25 incrementally, or store the corpus so it can be refitted.
- Use a larger model, or a hosted one if the client accepts it, to fix the
  multi-fund attribution problem.
- Add HSTS once the hostname is final.
