# What we tried that didn't work (or that we dropped)

Each entry covers what was tried, why it was dropped, and the old commit to read
first. When a reason was not written down at the time, the entry says so.

## Hosting and stack

**Cloudflare Workers + Vectorize + OpenAI API** (Apr 2026, `864bc9a`, branch
`openAI-api`). This was the first MVP: a Worker (`cloudflare_demo/`) with Vectorize for
retrieval and OpenAI for embeddings and generation. Replaced by a fully local stack in
`cd9987e` (12 May). The commit gives no reason. The team's understanding was that
client documents should not leave infrastructure we control, and that per-call API
costs were a concern. *Team: please confirm.*

**Amazon S3 Vectors, then Amazon OpenSearch Service** (30 Apr – 22 May, `bbd59c7`,
`d08bc2e`). Both were built and run side by side, along with Pinecone (`3b2ab77`).
On 22 May only Pinecone was kept (`43e9719`). The reason is not recorded. *Team:
please fill in.*

**ChromaDB** (May–Aug). Local vector store from the "fully local" migration. Replaced
by Pinecone and removed from requirements in `bc9d428`, because it was unused and
pulled in `onnxruntime`. A 38 MB `chroma.sqlite3` was committed to git for a while.

**Oracle Cloud (OCI)** (Jun–Sep, branch `OCI_VM_deployment`, `4338568`). Terraform for
a VCN and compute instance, with cloud-init that installs Ollama. Lessons learned:
`VM.Standard.E2.4` is a paid shape whose service limit drops to zero when the free
trial ends, and OCI reports that as a misleading `404 NotAuthorizedOrNotFound`. The
first push failed because ~240 MB of Terraform provider binaries and credentials were
committed. The project then moved to EC2 (see [ADR 0007](decisions/0007-hosting-ec2.md)).

## Models

**Ollama for embeddings** (Apr). Replaced by `sentence-transformers` running
`BAAI/bge-base-en-v1.5` in-process, which avoids an HTTP round trip for every chunk
(`cd9987e`).

**Qwen3 as a reranker** (Apr–May). It needed 30–40 sequential LLM calls per query.
Replaced by a cross-encoder: `ms-marco-MiniLM-L6-v2` first, now
`BAAI/bge-reranker-base`, which scores everything in one batched call (`cd9987e`).

**`qwen3` 8B for answers.** Too slow on CPU: 3.5 tokens/s, and it never finished
within the 120 s timeout (`e3af36c`). Replaced by `qwen3:1.7b`.

**Thinking turned off** (`e3af36c`, reversed in `18e6cba`). It was disabled because one
benchmark on one question showed 21 s against 3 s. Across four questions the real cost
was about twice the time (3–7 s), and with thinking off the model failed compound
questions: 0/5 correct with it off, 5/5 with it on. **Lesson: don't tune on one
question.** It is now on by default, and `OLLAMA_THINK=false` turns it off.

**HyDE (hypothetical document embeddings)** (`2dc4431`, May). Added with reranking and
keyword search, and no longer in the pipeline. *Team: why was it dropped?*

## Product and UX

**Streaming answers** (`c221666`, removed in `19da90f`). The answer streamed as
newline-delimited JSON. It worked, but it needed a second code path in the view, a
second Ollama call shape and a stream reader in the browser, all to hide a wait the
model makes unavoidable anyway. Replaced by a "Let me think about the answer" message
with an animated ellipsis (`5a07740`). Worth bringing back if generation gets faster.

**Mandatory date range** (`9792f13`, made optional in `a27fa8a` / `dddcc5d`). Every
document had the same placeholder date, so most ranges returned nothing.

**User/fund selection UI** (PR #3 `Mark-UserFunds`, merged and reverted the same day,
`e8424fa`). The revert also touched the committed `chroma.sqlite3` and `.pyc` files.
The feature came back in a later merge. *Team: confirm why it was reverted.*

**Delete-document JSON list** (branch `Mark-DeleteDocs`, `cb1d872`, untested, never
merged). Superseded by the `Document` model, which stores Pinecone IDs (`72e824d`).

**Bubble UI** (branch `Shehara-Bubble-UI`). Only a README change is left on it.
Shehara confirmed on 1 November 2026 that Bubble UI was **not shipped**. It must
not be included in delivered-feature claims. The reason it was not shipped is
not yet recorded.

## Ingestion and chunking

**pypdf.** Replaced by pdfplumber, which handles tables better (`2dc4431`).

**Aggressive TOC filter** (fixed in `55973e2`). Any chunk under 400 characters with a
line ending in digits was dropped as a table of contents. In legal text that includes
clause numbers, ACNs, dates and dollar amounts. The filter deleted 18% of the corpus
and 23% of the SIS Act, including whole deed schedules. Fixing it raised the index
from 1,970 to 4,107 vectors, and recall went from 5/10 to 7/10. **Lesson: run
`eval_retrieval.py` after any chunking change. Unit tests did not catch this.**

**Time-based chunking** (`c0b5091`, "needs checking"). Did not survive. Superseded by
header and layout chunking.

**`chunking.py` module.** Lost a name collision with main's `chunking/` package during
the 23 Sep merge (`dddcc5d`). The package was kept.

**OCR ensemble (PaddleOCR + `SemanticChunker` + LLM text alignment)**. Commented out.
Its output was thrown away anyway (`a68e328`).

**OCR on the client VM** (`4bcdec8`). PP-StructureV3 crashes in paddlepaddle 3.3.1's
oneDNN kernel. The vision fallback (`qwen3-vl:2b`) needs about 5.4 GB resident, and the
kernel killed Ollama for running out of memory on the 7.8 GB host. OCR is a
local-only feature for now.

**LLM cleanup pass on OCR output.** Took minutes per chunk on CPU, for tidier text that
retrieval does not need. Disabled with `cleanup=False` (`0efdf4a`).
