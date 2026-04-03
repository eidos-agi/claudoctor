---
id: 0018
title: MCP .mcp.json location and schema errors cause silent ignoring
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #4976, #5037, #13281'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Servers defined in settings.json or .claude.json instead of .mcp.json are silently ignored. Manual edits to .mcp.json sometimes aren't recognized until restart. Config in wrong location shows "No servers configured" despite having config. Claudoctor should: check for MCP config in wrong files, validate .mcp.json schema, detect stale config after manual edits.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #4976, #5037, #13281, retrieved 2026-04-03

## Caveats

None identified yet.
