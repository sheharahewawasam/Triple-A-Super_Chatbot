# Project context

> Parts of this page can't be recovered from the code or the commit history. Sections
> marked **TODO** need someone from the team to fill them in.

## What it is

A FIT4002 (Monash) industry project for Triple A Super: a chatbot that answers
financial advisers' questions about self-managed super fund documents (trust deeds,
deeds of amendment, ATO forms) and the SIS Act, citing the document each answer came
from. Each adviser sees only the funds assigned to them, plus a shared "General" fund
that holds legislation.

## Constraints that shaped the design

- **Confidential client documents.** This is why the models run locally and why fund
  PDFs and audit logs stay out of git. *TODO: confirm this was a client requirement
  and record who set it.*
- **Isolation between advisers.** Promised to the client and enforced by
  `permitted_funds()` and `build_access_filter()`, with tests.
- **Cheap CPU-only hosting.** This drove the choice of a 1.7B model, a cross-encoder
  reranker instead of LLM reranking, and OCR as a local-only feature.
- **Questions advisers actually ask are compound** (for example "what is the deed
  date, and has it been updated since?"). This is why model thinking stays on.

## People

Verified from `Project_26.pdf` (pages 1–2): client and project owner **Champ Mendis**,
Triple A Super Pty Ltd, **Champake.Mendis@tripleasuper.com.au**. This identifies the
project contact, not ownership of any cloud account.

The proposal names Mark Shim, Shehara Hewawasam, Yiyou (Fred) Xu, Weihom Tan and
Jun Ng as its authors. Their present account-access responsibilities and the unit
supervisor still need confirmation.

**TODO**:
- Client contacts at Triple A Super and what each person decides
- Unit supervisor and teaching team
- Team members (see [history.md](history.md#contributors) for each person's areas)
- Who owns the AWS account, the DuckDNS domain `triple-a-chatbot.duckdns.org` and the
  Pinecone account, and who to ask for access

## Original scope and status

See [scope-and-delivery.md](scope-and-delivery.md) for a source-backed comparison of
the initial S3/MongoDB/Apex proposal with the standalone Django/Pinecone delivery.
Implementation is distinguished from client acceptance and unverified integrations.

**TODO**: summarise `Project_26.pdf` and `Proposal Document.pdf`, which are in the old
repo root (first commit). Note which requirements were delivered, partly delivered or
dropped, and any decisions the client made in meetings.

## Accounts and renewals

- The TLS certificate for `triple-a-chatbot.duckdns.org` was issued on 23 Sep 2026 and
  renews automatically through the certbot timer. DuckDNS is refreshed by a systemd
  timer, because Amazon Linux 2023 has no cron.
- **TODO**: EC2 instance ID and region, billing owner, Pinecone plan and index name.
