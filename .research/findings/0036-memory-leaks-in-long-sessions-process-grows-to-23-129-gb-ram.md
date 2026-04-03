---
id: '0036'
title: 'Memory leaks in long sessions — process grows to 23-129 GB RAM'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #18859, #11377, #4953'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Long-running Claude Code sessions can grow to 23-129 GB RAM (#18859, #11377, #4953). Streaming API response buffers not released when generator terminated early (fixed in recent versions). SessionEnd hooks killed after 1.5s regardless of timeout setting (now configurable via CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS). Claudoctor should: check current Claude Code process RSS, warn on high memory usage, detect long-running sessions, verify Claude Code version for known leak fixes.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #18859, #11377, #4953, retrieved 2026-04-03

## Caveats

None identified yet.
