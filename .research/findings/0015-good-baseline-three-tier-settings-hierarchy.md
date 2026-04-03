---
id: '0015'
title: 'Good baseline — three-tier settings hierarchy'
status: open
evidence: LOW
sources:
- text: 'dev.to settings guide, eesel.ai blog, code.claude.com/docs/en/settings (primary)'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Community consensus baseline: User scope (~/.claude/settings.json) gets fast default model, sensible prefs, no wildcards in allowedTools. Project scope (.claude/settings.json) gets tight allowedTools per environment, test/lint commands, package manager. Local scope (.claude/settings.local.json) gets machine-specific paths, extra permissive tools not in git, secrets via env/MCP. Claudoctor should score against this baseline and suggest what's missing.

## Supporting Evidence

> **Source [SECONDARY]:** dev.to settings guide, eesel.ai blog, code.claude.com/docs/en/settings (primary), retrieved 2026-04-03

## Caveats

None identified yet.
