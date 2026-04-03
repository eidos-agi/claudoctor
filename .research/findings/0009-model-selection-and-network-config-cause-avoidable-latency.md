---
id: 0009
title: Model selection and network config cause avoidable latency
status: open
evidence: LOW
sources:
- text: 'syntora.io, reddit.com/r/ClaudeAI, news.ycombinator.com, claudefa.st performance
    guide'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Using heavy models (Sonnet/1M-context) for trivial edits increases latency needlessly. Default timeouts with no compression or tuned retries make transient slowness permanent. Bad proxies or Node HTTP stack issues create big gaps between request and first token. Checks: model config for task, timeout/retry/compression settings, proxy detection.

## Supporting Evidence

> **Source [SECONDARY]:** syntora.io, reddit.com/r/ClaudeAI, news.ycombinator.com, claudefa.st performance guide, retrieved 2026-04-03

## Caveats

None identified yet.
