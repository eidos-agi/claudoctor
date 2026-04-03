---
id: '0011'
title: Dangerous permissions — god mode tools and skipped confirmations
status: open
evidence: LOW
sources:
- text: 'institute.sfeir.com best practices, eesel.ai settings guide, shipyard.build
    cheat sheet'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Three permission anti-patterns: (1) allowedTools set to broad patterns like Bash(*) or Write globally so every project is one prompt from destruction, (2) no env separation — same permissive settings for CI/review and local dev, (3) using --dangerously-skip-permissions as a default instead of one-off. Checks: detect wildcard allowedTools in global scope, flag skip-permissions in shell history/aliases, compare global vs project permission strictness.

## Supporting Evidence

> **Source [SECONDARY]:** institute.sfeir.com best practices, eesel.ai settings guide, shipyard.build cheat sheet, retrieved 2026-04-03

## Caveats

None identified yet.
