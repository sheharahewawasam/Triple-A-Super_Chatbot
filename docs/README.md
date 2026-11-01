# Handover documentation

This repository is a cleaned-up copy of the team's working repository,
<https://github.com/sheharahewawasam/FIT-4002-CHATBOT>, which holds about 140 commits
across 18 branches from April to October 2026. The original history was not carried over; subsequent handover commits are recorded here. These
documents record what that history would have told you: what was tried, what was
decided, and why.

Historical commit hashes (for example `55973e2`) refer to the old repository.
Handover commits, including `fba9e37`, refer to this repository. Many of its commit messages are detailed write-ups and are
worth reading in full when you touch the area they describe.

| Document | Read it when |
| --- | --- |
| [known-issues.md](known-issues.md) | Current port status, remaining limitations and tech debt |
| [decisions/](decisions/) | You want to change a core part of the design (vector store, models, chunking, OCR, auth, hosting) |
| [tried-and-abandoned.md](tried-and-abandoned.md) | You have an idea and want to know whether we already tried it |
| [evaluation.md](evaluation.md) | You change chunking, ingestion, retrieval or the prompt and need to measure the effect |
| [history.md](history.md) | You want the timeline, or need to find the old branch where something was done |
| [security-and-data.md](security-and-data.md) | You deploy, handle client documents, or manage credentials |
| [project-context.md](project-context.md) | You need the project's scope, people and constraints |

Setup and deployment steps are in the top-level [README](../README.md) and
[deploy/README.md](../deploy/README.md), and are not repeated here.

## Current handover work

- [Task register and verification](handover-status.md)
- [Original scope and implementation mapping](scope-and-delivery.md)
- [Source backup and restore procedure](backup-and-restore.md)
- [Document-date verification register](document-date-register.json)
