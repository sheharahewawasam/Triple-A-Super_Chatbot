# Known issues, tech debt and next steps

## 1. Port status (1 November 2026)

The handover branch now restores authenticated chat throttling, signed citation
grants and source serving, single answer rendering, enabled-by-default uploads,
strict date validation, the 33 original regression tests, the OCR confidence/VLM
rewrite and environment flags, and OCR page/timing logs. Unused Chonkie imports
were removed; Ollama is imported only on paths that invoke it.

Evaluation cases, OCR checks and fixtures are restored. Existing retrieval,
chunk-structure and improved grader scripts are retained. The live recall rerun
passed on 1 November 2026 with recall@5=8/10 and recall@60=8/10; see
[the evaluation record](evaluation.md).
See [handover-status.md](handover-status.md) for incomplete security and team work.

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
- **Post-port retrieval recall is 8/10** on ten hand-checked facts (1 November 2026).
  Sample trustee and Ausis members facts are not in the top-60 candidates. This
  localises the observed misses to candidate retrieval; it does not establish
  whether extraction, chunking, index content or query matching is the root cause.
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
- New installations create unusable passwords pending explicit provisioning. Existing deployments still require password rotation.
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
