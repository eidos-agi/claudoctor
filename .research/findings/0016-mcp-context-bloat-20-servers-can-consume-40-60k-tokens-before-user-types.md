---
id: '0016'
title: 'MCP context bloat — 20+ servers can consume 40-60K tokens before user types'
status: open
evidence: LOW
sources:
- text: 'medium.com/@joe.njenga (46.9% reduction), ai.gopubby.com (82% context eaten),
    scottspence.com MCP optimization'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Every connected MCP server injects full tool schemas into every message. 20+ servers can consume 40K-60K+ tokens before the user types anything. Tool Search (deferred loading) reduced bloat by ~47% but users must opt in. Claudoctor should: count connected servers, estimate schema token overhead, flag unused servers, recommend deferred loading.

## Supporting Evidence

> **Source [SECONDARY]:** medium.com/@joe.njenga (46.9% reduction), ai.gopubby.com (82% context eaten), scottspence.com MCP optimization, retrieved 2026-04-03

## Caveats

None identified yet.
