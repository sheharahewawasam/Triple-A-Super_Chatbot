# Project context

Reviewed 1 November 2026. Current implementation: `handover/fit-4002-chatbot`;
[draft PR #1](https://github.com/sheharahewawasam/Triple-A-Super_Chatbot/pull/1)
targets `main`. Refer to [handover status](handover-status.md) for remaining work.

## Purpose and current system

A FIT4002 Monash project for Triple A Super: an adviser chatbot for fund documents,
including trust deeds, amendments, ATO forms and legislation. Django serves the
HTML interface and API. SQLite stores accounts, fund grants and uploaded-document
records. Pinecone stores searchable vectors and chunk text. BGE embeddings and
reranking run in-process; Ollama generates answers.

Authenticated advisers can retrieve granted funds' documents OR their own uploads.
The shared General fund is visible only where granted. Fund selections narrow the
fund clause; an empty selection uses all granted funds. This does not remove the
owner-upload clause. Signed citation links serve PDFs through the application.

## Constraints and evidence

- Confidential PDFs, logs and environment files require restricted storage outside
  source control. The proposal discusses privacy and cost tradeoffs for local
  models; the final motivation and any client-imposed requirement remain unconfirmed.
- Local inference is not fully local storage: Pinecone holds chunk text/metadata.
- CPU/memory constraints influenced the small answer model and batched reranking.
  Historical hardware figures are not a verified current VM inventory.
- Compound questions motivated keeping model thinking enabled in the recorded
  experiments; these small experiments do not establish general answer accuracy.

## People and ownership

`Project_26.pdf`, pages 1–2, names client/project owner **Champ Mendis**, Triple A
Super Pty Ltd, **Champake.Mendis@tripleasuper.com.au**. This is the project contact,
not confirmation of cloud-account ownership.

The proposal authors are Mark Shim, Shehara Hewawasam, Yiyou (Fred) Xu, Weihom Tan
and Jun Ng. Historical contribution areas are in [history.md](history.md).
Fred and Shehara jointly coordinate the handover documentation.

Still needed from the team: unit supervisor/teaching contact, each client's
decision responsibilities, and the AWS billing/access owner, DuckDNS owner and
Pinecone owner with the process for next-team access. Do not put credentials here.

## Scope and delivery

[Scope and delivery](scope-and-delivery.md) summarises the original brief/proposal
and maps it to the current implementation. It distinguishes implemented features
from client acceptance and unverified integrations. Bubble UI was not shipped,
confirmed by Shehara on 1 November 2026; the delivered UI is HTML/Django.

## Infrastructure and maintenance

The documented deployment targets Amazon Linux 2023 with nginx, Gunicorn,
systemd, Ollama, DuckDNS and Let's Encrypt. The public HTTPS sign-in page and
authenticated dashboard were observed on 1 November 2026. Installed service units,
certificate renewal, network controls and scheduled jobs were not inspected.

The team still needs to record the EC2 instance ID, region, current shape,
billing owner, actual Pinecone index name/plan and backup owner/location.
The configured secrets were sufficient for the successful 8/10 live retrieval
evaluation; this does not disclose or independently inventory the account plan.
Use [deployment instructions](../deploy/README.md) and the
[backup/restore procedure](backup-and-restore.md) for operational handover.
