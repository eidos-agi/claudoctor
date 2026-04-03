---
id: '0034'
title: MEMORY.md truncates at 200 lines — stale entries accumulate silently
status: open
evidence: LOW
sources:
- text: 'code.claude.com/docs/en/memory, zenvanriel.com AutoDream guide'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

MEMORY.md truncates at 200 lines / 25 KB — anything beyond is silently ignored. Stale entries accumulate: old debugging notes, relative timestamps ("yesterday"), contradictory facts. No deduplication or freshness check. Fix options: AutoDream (memory consolidation sub-agent) or manual pruning, move detail to separate files keeping index lean. Claudoctor should: count MEMORY.md lines, warn on approaching 200, detect stale/relative timestamps, flag potential duplicates.

## Supporting Evidence

> **Source [SECONDARY]:** code.claude.com/docs/en/memory, zenvanriel.com AutoDream guide, retrieved 2026-04-03

## Caveats

None identified yet.
