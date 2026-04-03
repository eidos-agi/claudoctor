---
id: '0014'
title: 'Messy settings.json — empty, invalid, or mixed concerns'
status: open
evidence: LOW
sources:
- text: 'reddit.com/r/ClaudeAI settings.json thread, github.com/anthropics/claude-code/issues/26167'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Four settings.json anti-patterns: (1) blank file assumed configured but actually running pure defaults, (2) hand-edited invalid JSON (trailing commas, wrong types) causing silent key ignoring, (3) mixing auth, MCP config, and preferences in settings.json instead of separating state into ~/.claude.json, (4) no awareness of the settings hierarchy (user > project > local). Checks: validate JSON syntax, detect empty-but-present, flag auth/state mixed into settings, check hierarchy completeness.

## Supporting Evidence

> **Source [SECONDARY]:** reddit.com/r/ClaudeAI settings.json thread, github.com/anthropics/claude-code/issues/26167, retrieved 2026-04-03

## Caveats

None identified yet.
