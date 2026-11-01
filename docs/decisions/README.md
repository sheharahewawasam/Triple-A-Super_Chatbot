# Architecture decision records

One file per significant decision: the context, the options considered, what we chose,
and what follows from it. Commit hashes refer to the old repository. To change a
decision, add a new record that supersedes the old one instead of editing history.

| # | Decision | Status |
| --- | --- | --- |
| [0001](0001-local-models.md) | Run all models locally (Ollama + sentence-transformers) | Accepted |
| [0002](0002-pinecone.md) | Pinecone as the only vector store | Accepted |
| [0003](0003-hybrid-retrieval-rerank.md) | Hybrid dense + BM25 retrieval with a cross-encoder reranker | Accepted |
| [0004](0004-answer-model.md) | qwen3:1.7b with thinking on | Accepted |
| [0005](0005-chunking.md) | Header- and layout-aware parent/child chunking | Accepted |
| [0006](0006-ocr.md) | OCR as a fallback, local-only for now | Accepted |
| [0007](0007-hosting-ec2.md) | Single EC2 VM with nginx, gunicorn, systemd, DuckDNS and Let's Encrypt | Accepted |
| [0008](0008-auth-and-isolation.md) | Django sessions, with fund scope derived on the server | Accepted |
| [0009](0009-no-streaming.md) | One JSON response, no streaming | Accepted |
