# 0009 — One JSON response, no streaming

**Status:** Accepted (`c221666` added streaming, `19da90f` removed it)

## Context
Answers take 20–230 s depending on the host. Streaming the answer as newline-delimited
JSON (citations, then tokens, then a terminator) was built and worked.

## Decision
Remove it. It needed a second code path in the view, a second Ollama call shape and a
stream reader in the browser, while total time stayed the same. Instead, the UI shows
"Let me think about the answer" with an animated ellipsis (`5a07740`), and blocks a new
send until the reply arrives.

## Consequences
- A single response path is easier to test and to cache.
- Reconsider if a faster model makes the wait short enough that streaming matters, or
  if the wait becomes the main complaint. The removed implementation in `c221666` is a
  working starting point. It handles reasoning arriving separately in
  `message.thinking`.
