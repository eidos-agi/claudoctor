---
id: '0017'
title: 'MCP server crashes, hangs, and zombie processes'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code/issues/15945, modelcontextprotocol.io/docs/tools/debugging,
    mcpevals.io debugging guide'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

MCP servers crash after init (bad deps, uncaught exceptions), hang indefinitely (no timeout), or write to stdout corrupting stdio protocol. One reported case: 16-hour hang spawning 70+ zombie processes (Issue #15945). Tools silently fail or session freezes. Claudoctor should: ping each server with startup timeout, check for zombie MCP processes, verify servers log to stderr not stdout.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code/issues/15945, modelcontextprotocol.io/docs/tools/debugging, mcpevals.io debugging guide, retrieved 2026-04-03

## Caveats

None identified yet.
