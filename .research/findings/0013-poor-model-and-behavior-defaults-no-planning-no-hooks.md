---
id: '0013'
title: 'Poor model and behavior defaults — no planning, no hooks'
status: open
evidence: LOW
sources:
- text: 'builder.io best practices, institute.sfeir.com best practices, shipyard.build
    cheat sheet'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Three behavior anti-patterns: (1) defaulting to heaviest model and 1M context for everything including trivial edits, (2) planning tools off or never configured so Claude jumps straight into editing, (3) no hooks for tests/linters/checks before or after edits. Checks: detect model override in settings, check for hooks config existence, flag absence of planning mode awareness.

## Supporting Evidence

> **Source [SECONDARY]:** builder.io best practices, institute.sfeir.com best practices, shipyard.build cheat sheet, retrieved 2026-04-03

## Caveats

None identified yet.
