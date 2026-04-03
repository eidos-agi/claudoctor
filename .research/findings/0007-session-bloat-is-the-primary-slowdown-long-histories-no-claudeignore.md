---
id: '0007'
title: 'Session bloat is the primary slowdown — long histories, no .claudeignore'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code/issues/10881, claudefa.st performance guide,
    institute.sfeir.com troubleshooting'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Long sessions send huge token payloads increasing latency. IDE plugins shipping all open tabs is self-DOS via tokens. Missing .claudeignore lets node_modules/build artifacts inflate scanning. Checks: session age/turn count, .claudeignore existence and coverage, IDE integration settings.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code/issues/10881, claudefa.st performance guide, institute.sfeir.com troubleshooting, retrieved 2026-04-03

## Caveats

None identified yet.
