# Delegation Failure Patterns

## model_not_supported (most common)

```
Error code: 400 - {'error': {'message': 'Model <name> is not supported on /v1/chat/completions.', ...}}
```

**Cause:** The subagent's default model (or the session's current model, e.g. `gemini-flash-lite-latest`, `mimo-v2.5-pro`, any non-standard provider model) isn't available on the `/v1/chat/completions` endpoint. The delegate_task system inherits or selects a model the completions API rejects.

**Resolution:** Fall back to inline execution using `web_search` + `web_extract` tools directly (preferred — faster, more reliable for moderate research). If those are missing, use terminal-based `~/.local/bin/kagi search` and `~/.local/bin/kagi summarize`.

**Prevention:** None — this is an infrastructure issue. Always be prepared for delegation to fail.

## rate_limit / timeout

Delegation can also fail silently with max_iterations or timeout errors. Same fallback applies.

## Empty Subagent Results (self-reported success, no data returned)

**What happened:** Subagent ran for ~300 seconds, made 17 API calls, and returned a summary saying *"I have extremely thorough data now from all major sources. Let me save the comprehensive findings to a file."* — but never actually saved the file. The parent session got an empty result after burning significant tokens.

**Root cause:** The subagent decided to save to a file (side effect) instead of returning data through the summary. It either ran out of context/tokens before completing the write, or the write failed silently.

**Prevention:**
1. **Specify output format explicitly in the goal.** Add: *"Print all findings to stdout as your final response. Do not save to files."* This forces data back through the return channel.
2. **Keep subagent tasks short and focused.** 17 API calls is too many for one delegation — split into 2-3 parallel searches and merge results in the parent.
3. **Verify before trusting.** After any subagent claims it saved something, check the file exists before telling the user.

**Key lesson:** Subagent summaries are self-reports. Never trust "saved successfully" without verification.

## Key lesson

**Don't trust delegation to succeed.** The subagent infrastructure is fragile. Always budget time for inline fallback when delegating research tasks. The inline path uses terminal-based Kagi CLI calls which are reliable.
