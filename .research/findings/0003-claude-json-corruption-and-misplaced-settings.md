---
id: '0003'
title: ~/.claude.json corruption and misplaced settings
status: open
evidence: LOW
sources:
- text: 'code.claude.com/docs/en/settings (primary), claudelog.com/troubleshooting'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Users put global settings into editor settings.json instead of ~/.claude.json (ignored or schema errors). Hand-edited JSON gets corrupted silently. Stale experimental config persists for weeks. Checks: validate JSON syntax, detect unknown keys, flag stale overrides.

## Supporting Evidence

> **Source [SECONDARY]:** code.claude.com/docs/en/settings (primary), claudelog.com/troubleshooting, retrieved 2026-04-03

## Caveats

None identified yet.
