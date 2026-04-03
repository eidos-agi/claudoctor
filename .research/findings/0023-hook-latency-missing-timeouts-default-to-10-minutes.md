---
id: '0023'
title: Hook latency — missing timeouts default to 10 minutes
status: open
evidence: LOW
sources:
- text: 'code.claude.com/docs/en/hooks-guide, code.claude.com/docs/en/hooks, github.com/anthropics/claude-code/issues/2803'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Every hook should have explicit timeout — default is 10 minutes, so a broken hook blocks that long. PostToolUse hooks on broad matchers (Edit:*) must be under 200ms. Test runners on PostToolUse add 60s per edit — should move to PreToolUse on git commit instead. Claudoctor should: check for missing timeout in hook config, flag PostToolUse hooks with broad matchers, detect heavy operations (test suites) on per-edit hooks.

## Supporting Evidence

> **Source [SECONDARY]:** code.claude.com/docs/en/hooks-guide, code.claude.com/docs/en/hooks, github.com/anthropics/claude-code/issues/2803, retrieved 2026-04-03

## Caveats

None identified yet.
