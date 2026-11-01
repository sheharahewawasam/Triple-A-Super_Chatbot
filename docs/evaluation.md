# Evaluation and benchmarks

## Post-port verification — 1 November 2026

[GitHub retrieval run 41273655594](https://github.com/sheharahewawasam/Triple-A-Super_Chatbot/actions/runs/41273655594)
passed after the two repository secret names were verified. It ran
`python eval_retrieval.py --verbose --require 8` against the authorised live index.
Recall@5 (facts reaching model context) was **8/10**; recall@60 (facts present in
candidates) was **8/10**. The two misses were Sample's trustee and Ausis's members;
their expected facts were not in the top-60 candidates for the tested phrasing.

This confirms the ten-case retrieval baseline after porting. It does not measure
generated-answer correctness, prove complete corpus coverage, or establish the
root cause of the candidate misses. No index re-ingestion was performed.

## Available tools

The following evaluation tools are present in this repository after the handover
port. The improved existing grader was retained rather than replaced with its older version:

| Script (old repo, `mvp_demo/`) | What it measures | Notes |
| --- | --- | --- |
| `eval_retrieval.py` | Retrieval recall: does the chunk holding the answer reach the model? | 10 questions whose answers were read by hand from the PDFs. Needs live Pinecone and the BGE models, so it is a script, not a Django test. **Run it before and after any chunking, ingestion or retrieval change.** |
| `evaluation_cases.py` + `validate_evaluation_dataset.py` | Question/ground-truth dataset by fund, category and clause | Used by the grader |
| `Grader.py` | Answer quality: an Ollama judge scores correctness, groundedness and relevance from 0 to 10, and records response time | Copies the RAG logic from `views.py`, so re-copy it before each run. Results are in `currentVersionEval.txt` |
| `chunk_structure_metrics.py` | Chunk-structure statistics per document | Results were written to `output.txt` |
| `ocr_test.py` + `testing/` fixtures | OCR accuracy against `.png`/`.json` ground-truth pairs | Needs PaddleOCR |

The 25-question set the client supplied is `RAG Questions.pdf`, run against the
TestData funds with the `TestAdvisor` account (migration `0003`). It is not in git.

## Results recorded so far

**Retrieval recall@5 (10 hand-checked facts)**

| When | Change | Recall |
| --- | --- | --- |
| before `55973e2` | aggressive TOC filter, 1,970 vectors | 5/10 |
| `55973e2` | TOC filter fixed, 4,107 vectors | 7/10 |
| `dddcc5d` | after the chunking-package merge | 8/10 |

**Latency (chat endpoint, CPU only)**

| Setup | Time |
| --- | --- |
| qwen3 8B, thinking on | never finished (3.5 tok/s, timed out at 120 s) |
| qwen3:1.7b, thinking on, one simple question | 21 s |
| qwen3:1.7b, thinking off, same question | 2.8 s (with a severe quality loss, see below) |
| full pipeline, uncached, dev machine | 21–35 s |
| smallest VM | 90–230 s |

**Thinking on vs off** (`18e6cba`): on the compound deed-date question, 0/5 runs were
correct with thinking off and 5/5 with it on. With thinking on, four phrasings of the
question each gave the date correctly and cited `deed.pdf`.

**Grader sample** (`currentVersionEval.txt`, Summers Family Super Fund): correctness
scores of 9/10 and 10/10 on the deed-date and pension-commencement questions.

**OCR ingestion time** (`PDF_ingestion_measure.md`, 27 Sep 2026)

| PDF | Pages | Time |
| --- | --- | --- |
| Trust_Deed_Sample_Superannuation_Fund.pdf | 57 | 2,510 s (~42 min) |
| deed.pdf | 12 | 1,178 s (~20 min) |

**How much OCR is needed** (`a68e328`): of the 32 deployed documents, 7 were flagged for
OCR. Only 3 extract no text at all, 2 of those are test fixtures, and the only real
client document with no text layer is the Powell trust deed (4 pages).

## Rules of thumb we learned

- Test on several questions, including compound ones. A single question misled us once
  (see [tried-and-abandoned.md](tried-and-abandoned.md)).
- Count vectors before and after re-ingesting. A large drop means the filters are
  deleting content.
- When access scoping changes, test the answer cache as well as the filter. The cache
  once served answers across advisers (`55973e2`).
