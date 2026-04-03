---
id: '0026'
title: 'Claude Code has built-in /doctor — but it only checks installation'
status: open
evidence: LOW
sources:
- text: 'code.claude.com/docs/en/troubleshooting, github.com/anthropics/claude-code
    issues #19354, #20303'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Claude Code ships `claude doctor` (CLI) and `/doctor` (slash command). It checks: installation type/version, executable path, auto-update permissions, multiple installation conflicts, PATH config, search functionality. But it's narrow — installation health only, not environment/workflow health. Known bugs: hangs on Enter, 100% CPU, incorrect PATH suggestions (#19354, #20303). Claudoctor must complement, not replace, the built-in command.

## Supporting Evidence

> **Source [SECONDARY]:** code.claude.com/docs/en/troubleshooting, github.com/anthropics/claude-code issues #19354, #20303, retrieved 2026-04-03

## Caveats

None identified yet.
