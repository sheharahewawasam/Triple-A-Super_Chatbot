# 0004 — qwen3:1.7b with thinking on

**Status:** Accepted (`e3af36c`, `18e6cba`)

## Context
Answers are generated on CPU. Measured with the roughly 1,900-token context the app
sends:

| Model | Thinking | Time |
| --- | --- | --- |
| qwen3 8B | on | never finished (3.5 tok/s, 120 s timeout) |
| qwen3:1.7b | on | 21 s |
| qwen3:1.7b | off | 2.8 s |

Thinking was turned off on the strength of that one question. Across four questions it
costs only 3–7 s more. On compound questions, quality with thinking off was 0/5
correct, against 5/5 with it on.

## Decision
`qwen3:1.7b` with thinking on. The model, URL, timeout and thinking setting come from
environment variables (`OLLAMA_MODEL`, `OLLAMA_THINK`, …). Hard-coded values had
already let the app and cloud-init drift onto different models twice.

## Consequences
- When several funds are in scope, the model sometimes attributes one fund's value to
  another ([known-issues.md](../known-issues.md)).
- `strip_think_tags()` stays in place as a fallback for older Ollama builds.
- A larger or hosted model is the most likely way to improve quality.
