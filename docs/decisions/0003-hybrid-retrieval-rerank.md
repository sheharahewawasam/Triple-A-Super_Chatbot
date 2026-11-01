# 0003 — Hybrid dense + BM25 retrieval with a cross-encoder reranker

**Status:** Accepted (`2dc4431`, `cd9987e`, `dc80bea`)

## Context
Advisers ask about exact identifiers (clause numbers, ACNs, dates, dollar amounts),
which dense embeddings match poorly.

## Decision
- Query Pinecone with a dense BGE embedding plus a BM25 sparse vector (the fitted
  encoder is in `bm25_encoder.json`), taking the top 40–60 results.
- Rerank them with a cross-encoder in a single batched forward pass and keep the top 5.
- An earlier version reranked with qwen3 in 30–40 sequential LLM calls, which was far
  too slow.
- When a question has no fitted BM25 term, omit the sparse vector and use
  dense-only retrieval. Passing empty sparse indices would make Pinecone reject it (`dddcc5d`).

## Consequences
- BM25 must be refitted on the whole corpus with `ingest.py`. Uploads reuse the fitted
  encoder, so terms that appear only in uploads get no IDF weight (`72e824d`).
- Each chunk is capped at about 1500 characters to fit `num_ctx=8192`.
