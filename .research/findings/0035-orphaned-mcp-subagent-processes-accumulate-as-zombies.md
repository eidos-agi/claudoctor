---
id: '0035'
title: Orphaned MCP/subagent processes accumulate as zombies
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #33947, #33979'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

MCP servers and subagents not killed on session end accumulate as PPID=1 orphans on macOS (#33947). Feature request for built-in session manager (#33979) not shipped. `ps aux | grep claude` shows dozens of zombie processes. Claudoctor should: detect orphaned claude/MCP processes with PPID=1, count zombie processes, recommend cleanup, check for orphaned bookmark files with no matching active session.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #33947, #33979, retrieved 2026-04-03

## Caveats

None identified yet.
