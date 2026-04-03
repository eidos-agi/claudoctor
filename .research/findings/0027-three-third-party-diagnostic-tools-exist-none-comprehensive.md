---
id: '0027'
title: 'Three third-party diagnostic tools exist — none comprehensive'
status: open
evidence: LOW
sources:
- text: 'libraries.io/npm/cc-health-check, github.com/tw93/claude-health, github.com/demon0998/claude-code-health-check,
    pypi.org/project/claude-usage-monitor'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Existing tools: (1) cc-health-check (npm) — 20 checks, 0-100 score, JSON output, CI exit codes, (2) claude-health (tw93) — Claude Code skill (/health), six-layer framework, two parallel diagnostic agents, (3) claude-code-health-check (demon0998) — 45 checks, 2-second scan. Also claude-usage-monitor (PyPI) for token tracking only. None are comprehensive flutter-doctor-style tools — they focus on config linting, not full environment validation. No AI coding assistant (Cursor, Copilot, Aider, Continue) has a doctor command at all.

## Supporting Evidence

> **Source [SECONDARY]:** libraries.io/npm/cc-health-check, github.com/tw93/claude-health, github.com/demon0998/claude-code-health-check, pypi.org/project/claude-usage-monitor, retrieved 2026-04-03

## Caveats

None identified yet.
