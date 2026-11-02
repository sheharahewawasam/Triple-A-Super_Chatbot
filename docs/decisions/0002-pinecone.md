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

Research on 2 November 2026: `3b2ab77` introduced Pinecone for testing;
`f47ab7f` modified both Pinecone and OpenSearch; `43e9719` then removed the
separate S3/OpenSearch ingestion and view implementations and consolidated the
application around Pinecone (1,231 deleted lines, 175 added). This establishes
consolidation and a working hybrid/filter API as the technical basis retained.
Reducing parallel backend maintenance is an inference from that change, not a
recorded team explanation. No comparative cost or recall benchmark was found
in these commits, so superiority on those measures is not claimed.

Pinecone documents combined sparse/dense retrieval in its
[hybrid-search explanation](https://www.pinecone.io/blog/sparse-dense/).
AWS also documents [OpenSearch hybrid search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-configure-neural-search.html)
and [S3 vector indexes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-indexes.html).
These product references explain capabilities, not why this team rejected an
alternative. OpenSearch must not be described as lacking hybrid search.

## Consequences
- Normal application startup requires authorised Pinecone access and its configured
  index. `RAG_OFFLINE=1` deliberately skips these resources for unit tests only.
- Access control relies on exact-match metadata filters (`fund_name`, `owner`). A
  document ingested with a `fund_name` that no advisor holds can't be reached by
  anyone. This happened with the TestData funds (`c221666`).
- ChromaDB was removed from the requirements (`bc9d428`).

## Research sources

Repository history reviewed on 2 November 2026:

- [Original commit `3b2ab77`](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/commit/3b2ab77cb66c61bfe5a2b458b11ef28f71f41ad6)
- [Original commit `f47ab7f`](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/commit/f47ab7fad0ecc579e9fae15916aba4c4f9adc56b)
- [Original commit `43e9719`](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/commit/43e97193d4cddf380527fdcd5671f9d04c20ba61)
