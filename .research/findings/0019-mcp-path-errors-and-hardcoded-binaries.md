---
id: 0019
title: MCP path errors and hardcoded binaries
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code/issues/35452, arxiv.org/html/2603.05637v1
    MCP fault taxonomy'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Hardcoded absolute paths to Python/Node binaries that don't exist on other machines. Missing env vars cause silent auth failures. Env var casing mismatches trigger validation errors. Claudoctor should: verify binary exists at command path, verify referenced script files exist, check required env vars are set, flag hardcoded paths containing /Users/&lt;name&gt;/.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code/issues/35452, arxiv.org/html/2603.05637v1 MCP fault taxonomy, retrieved 2026-04-03

## Caveats

None identified yet.
