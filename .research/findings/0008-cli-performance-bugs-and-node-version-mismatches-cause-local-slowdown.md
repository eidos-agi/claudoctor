---
id: 0008
title: CLI performance bugs and Node version mismatches cause local slowdown
status: open
evidence: LOW
sources:
- text: 'reddit.com/r/ClaudeAI slowness threads, github.com/anthropics/claude-code/issues/17148'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Long-running CLI sessions can slow to minutes per request or eat huge RAM/CPU until restart. Newer Node versions cause latency and jank — downgrading to Node 20 fixes it. Terminal re-rendering massive histories makes it look slow even when API is fine. Checks: Node version, CLI process uptime, RAM/CPU usage.

## Supporting Evidence

> **Source [SECONDARY]:** reddit.com/r/ClaudeAI slowness threads, github.com/anthropics/claude-code/issues/17148, retrieved 2026-04-03

## Caveats

None identified yet.
