# Source PDF backup and restore

Status: procedure prepared; no VM access, backup destination or restore test was
provided for this handover update. No backup completion is claimed.

Joint coordination: Fred and Shehara. Name the client-approved storage owner and
next-team access group before copying confidential documents.

## Backup procedure

1. On the authorised VM, inventory `/opt/chatbot/documents` and the configured
   `SOURCE_DOCUMENT_DIRS`. Include uploaded PDFs under `MEDIA_ROOT` separately;
   copying the source directory alone does not preserve uploads.
2. Record SHA-256 checksums, file count, timestamp, running commit and path mapping
   in a manifest kept with the backup. Avoid printing document contents.
3. Take a consistent SQLite backup using the SQLite backup API, and preserve the
   fitted BM25 encoder, index/schema configuration and an inventory of Pinecone
   document IDs. The application database is not the vector index.
4. Encrypt the backup and store it in client-approved restricted storage with
   access for the next team. Keep credentials/recovery keys separately; never
   commit PDFs, environment files, manifests containing sensitive names, or keys.
5. Record the storage location, accountable owner, access group, retention policy
   and backup date in the private handover record. Confirm the next team's access.
6. Restore a copy in a disposable environment. Verify checksums and counts, configure
   source paths, and open sample authorised citation links. Record who tested it,
   when, and the result. Treat the backup as unverified until this passes.

## Document-date verification

Use [document-date-register.json](document-date-register.json). Verify the operative
or execution date in each original and record the page/section; do not use file
modification times, tax years or repeated template dates as deed dates. Leave an
unknown date null. Amendments and consolidated deeds may have distinct dates.
Changing `ingest.py` does not update existing Pinecone metadata: perform an
authorised re-ingestion or controlled metadata update and rerun retrieval checks.

Three source texts were checked during this update: Sample Schedule 3 has
`09/10/2020` (interpreted as 9 October 2020 in the Australian date convention);
Summers execution schedule explicitly gives `21 January 2012`; Ausis schedule
gives `27 May 2022`. These are sample deed dates, not a review of every client PDF.
