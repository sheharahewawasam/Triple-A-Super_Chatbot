# 0001 — Run all models locally

**Status:** Accepted (12 May 2026, `cd9987e`)

## Context
The MVP used OpenAI for embeddings and generation and Cloudflare Vectorize for
retrieval. The documents are confidential client trust deeds.

## Options
1. Hosted APIs (OpenAI or similar): best quality and speed, but every document and
   question leaves our infrastructure, and each call costs money.
2. Local models via Ollama for everything.
3. Local models, with embedding and reranking run in-process through
   `sentence-transformers` and Ollama used only for generation.

## Decision
Option 3. `BAAI/bge-base-en-v1.5` embeddings and the `BAAI/bge-reranker-base`
cross-encoder run in-process, loaded once in `rag_api/resources.py`. Answers come from
Ollama.

The reasoning was not written down at the time. The team's understanding is that it was
data confidentiality and cost. The final motive/client requirement is still
awaiting team confirmation in [the handover register](../handover-status.md).

Evidence recovered on 1 November 2026: section 9 of the proposal compares local
control/no per-call API charges with OpenAI's external processing/privacy concerns
and continuous API costs. These were documented tradeoffs, but do not independently
confirm the final decision motive or a client-imposed requirement. See
[scope and delivery](../scope-and-delivery.md).

## Consequences
- About 4 GB of RAM at startup, a first-run download from Hugging Face, and 20–35 s per
  answer on CPU.
- Answer quality is limited by a small model (see [0004](0004-answer-model.md)).
- The vector store (Pinecone) is still a hosted service, but it stores chunk text as
  metadata, so document text does leave the host. Bear that in mind if confidentiality
  was the reason for this decision.
