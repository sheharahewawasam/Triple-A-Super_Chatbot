# 0002 — Pinecone as the only vector store

**Status:** Accepted (22 May 2026, `43e9719`)

## Context
Between April and May the team tried Cloudflare Vectorize, ChromaDB, Amazon S3
Vectors, Amazon OpenSearch Service and Pinecone, several of them side by side
(`bbd59c7`, `d08bc2e`, `3b2ab77`).

## Decision
Keep Pinecone only. It supports hybrid search (dense and sparse vectors in one query)
and metadata filters, which [0003](0003-hybrid-retrieval-rerank.md) and the per-fund
access filter both need.

*Team: record why S3 Vectors and OpenSearch lost (cost, setup effort, missing sparse
vectors?).*

## Consequences
- The app cannot start without a valid `PINECONE_API_KEY`.
- Access control relies on exact-match metadata filters (`fund_name`, `owner`). A
  document ingested with a `fund_name` that no advisor holds can't be reached by
  anyone. This happened with the TestData funds (`c221666`).
- ChromaDB was removed from the requirements (`bc9d428`).
