---
id: '0005'
title: Skills misconfiguration causes repeated context waste
status: open
evidence: LOW
sources:
- text: 'reddit.com/r/ClaudeAI context problem thread, wmedia.es setup guide'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Stuffing all context into one CLAUDE.md instead of modular skills hits attention limits. Missing .claude/skills/ means skill-based loading never triggers. Broken import chains or exceeded nesting depth cause docs to silently not load. Checks: skills dir exists, oversized CLAUDE.md detection, import path validation.

## Supporting Evidence

> **Source [SECONDARY]:** reddit.com/r/ClaudeAI context problem thread, wmedia.es setup guide, retrieved 2026-04-03

## Caveats

None identified yet.
