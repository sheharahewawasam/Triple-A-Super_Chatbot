# Original scope and delivered implementation

Reviewed 1 November 2026 against `feature/account-based-access` at
`b269f317ca5396fedd91843ccaf012b765bddc0b` and this handover branch.
This mapping describes code present in the delivered implementation.

## Sources

- [Project_26.pdf](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/blob/b269f317ca5396fedd91843ccaf012b765bddc0b/Project_26.pdf), pages 1–2.
- [Proposal Document.pdf](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/blob/b269f317ca5396fedd91843ccaf012b765bddc0b/Proposal%20Document.pdf), sections 4.1, 9, 11 and 12.

Project 26 proposes an adviser RAG assistant using S3 documents, chunking,
embeddings, retrieval, generated answers with citations, and logs/analytics. Its
objectives are faster access to policies and updates, reduced manual dependency
and consistent explainable answers. It names Champ Mendis at Triple A Super as
client and project owner (Champake.Mendis@tripleasuper.com.au).

The proposal expands that into S3/MongoDB ingestion, OCR, automated fund/date/type
classification, hybrid search, metadata filters and verifiable references. It
proposes integration with the client's Django API, Apex dashboard and Firecloud
protocols. Sample stories include document questions, balance histories, fund
summaries, suggested questions, updates, TTR questions and deed-date checks.

## Delivery mapping

| Proposed outcome | Implementation evidence / current status |
|---|---|
| Adviser questions with retrieved context | Implemented in Django chat endpoint with BGE embeddings, hybrid Pinecone search, reranking and local Ollama generation; quality/latency remain constrained. |
| Citations and source viewing | Signed, expiring adviser-bound grants and `/api/source/` restored. PDFs must exist on the configured host. |
| Adviser/fund isolation | Session identity, database grants, request-scope intersection, owner checks and regression tests. |
| S3 ingestion / MongoDB mapping | Changed: current bulk ingestion reads local files and uploads use local storage; SQLite and Pinecone replace the proposed MongoDB/vector architecture. No completed S3 connector is established by the delivered path. |
| OCR | Optional PaddleOCR with confidence-based vision fallback; host-dependent and disabled where resources are insufficient. Not a verified integration with the client's existing OCR service. |
| Automatic fund/type/date classification | Partial: supplied metadata and explicit ingestion configuration are used. Three sample deed dates verified; most real-document dates remain unresolved. |
| Date-aware document questions | Validated optional date bounds implemented. Unknown dates are excluded by date filters; complete latest-version detection is not established. |
| Logs and analytics | Local audit records exist; a production analytics dashboard is not established. Transcripts must not be tracked in git. |
| Client Django/Apex/Firecloud integration | Standalone Django API and HTML interface exist; completed integration is not established by the delivered code. |
| Bubble UI | Not shipped, confirmed by Shehara on 1 November 2026. The delivered interface is the HTML/Django application. |
| Fund balances, summaries and updates | Document-grounded questions may retrieve relevant text. No account-balance connector, proactive change monitor or complete dedicated workflow is established. |
| Suggested questions / TTR coverage | No dedicated workflow or coverage evaluation is established by the generic chat interface. |

## Architecture changes

The implementation uses local models, Pinecone and local document storage instead
of the originally proposed storage/integration stack. See [local models](decisions/0001-local-models.md),
[Pinecone](decisions/0002-pinecone.md) and [hosting](decisions/0007-hosting-ec2.md)
for the researched decision evidence. Pinecone stores chunk text outside the host;
local model inference does not mean all data remains on the host.
