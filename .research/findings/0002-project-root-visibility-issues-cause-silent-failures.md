---
id: '0002'
title: 'Project root & visibility issues cause silent failures'
status: open
evidence: LOW
sources:
- text: 'wmedia.es, heyuan110.com, institute.sfeir.com troubleshooting guides'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Starting Claude Code from wrong directory means it won't see repo or CLAUDE.md. Nested projects with no clear root cause scope confusion. Read-only files cause edits to silently fail. Checks needed: cwd vs git root mismatch, CLAUDE.md not in cwd, file permission issues.

## Supporting Evidence

> **Source [SECONDARY]:** wmedia.es, heyuan110.com, institute.sfeir.com troubleshooting guides, retrieved 2026-04-03

## Caveats

None identified yet.
