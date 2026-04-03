---
id: '0022'
title: 'Hooks that hang — deadlocks, stdout pollution, symlinks'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #34457, #27467, #9542, #23038, #5433,
    #22172'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Five hook hang patterns: (1) Windows shell subprocess deadlock (#34457), (2) SessionStart hooks blocking init (#9542, #23038) — must be async or under 1s, (3) WorktreeCreate stdout pollution (#27467) — hook must output ONLY worktree path, (4) symlinked hook paths silently fail (#5433), (5) parallel instances + hooks = 100% CPU (#22172). Claudoctor should: check hook executability, detect symlinked hooks, verify SessionStart hooks are fast/async, flag WorktreeCreate hooks writing extra stdout.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #34457, #27467, #9542, #23038, #5433, #22172, retrieved 2026-04-03

## Caveats

None identified yet.
