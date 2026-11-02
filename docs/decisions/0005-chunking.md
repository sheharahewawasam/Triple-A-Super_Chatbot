# 0005 — Header- and layout-aware parent/child chunking

**Status:** Accepted (`947ea11`, `3267923`, `55973e2`, `6634f9d`)

## Context
Trust deeds are long legal documents organised by numbered clauses and schedules.
Fixed-size chunks split clauses in half. Time-based chunking (`c0b5091`) was tried and
dropped.

## Decision
- `chunking/header_chunking.py` splits the text into sections at headings. Parents are
  up to about 1500 characters. Only the leaves (children) are embedded, and the parent
  text goes to the model as context.
- `chunking/layout_chunking.py` chunks using layout blocks from OCR (PaddleOCR
  PP-StructureV3).
- `chunking/toc_filter.py` drops table-of-contents chunks **conservatively**. It never
  drops a chunk containing a date, ACN/ABN or currency amount, and a trailing number
  counts as a page number only on short, title-like lines.
- If every leaf under a parent is filtered out, the parent is indexed as its own leaf,
  so it can't be left with nothing pointing to it.
- `chunking/extraction.py` (pdfplumber, which keeps tables) is shared by `ingest.py`
  and the upload path.

## Consequences
- The previous TOC filter silently deleted 18% of the corpus (`55973e2`). Any change
  here needs an `eval_retrieval.py` run and a before/after vector count.
- Ingestion stores real source filenames, so citations name the actual document
  (`80a34de`).
