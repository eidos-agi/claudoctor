---
title: "The definitive diagnostic tool for Claude Code"
type: "vision"
date: "2026-04-03"
---

claudoctor is not a niche tool. It is the best diagnostic tool for Claude Code — period.

## Core idea

claudoctor runs everywhere Claude Code runs — inside sessions as a skill/MCP server, outside as a CLI, in CI as a check. Same engine, adapts to its environment. When running inside Claude Code it's smarter: it can see active MCP connections, conversation context, live process state, session history. When running outside it still catches everything static analysis can find. It doesn't force you to choose.

## What "best" means

It does everything the competition does, plus everything they don't:

| Capability | cc-health-check | Waza /health | second-brain | claudoctor |
|------------|:-:|:-:|:-:|:-:|
| Static config linting | 20 checks | qualitative | 45 checks | all of them |
| Runtime MCP probing | no | no | no | yes — ping servers, detect zombies, measure latency |
| Hook execution tracing | no | no | no | yes — verify hooks run, measure timing |
| Security (CVEs, permissions) | no | no | partial | yes — .mcp.json RCE, god-mode permissions, secrets |
| Disk/process hygiene | no | no | no | yes — ~/.claude size, orphaned processes, log rotation |
| CLAUDE.md quality | length only | word count | length only | contradictions, outdated rules, attention dilution |
| Context budget analysis | no | token estimate | traffic light | precise — MCP tools + CLAUDE.md + skills + memory |
| MEMORY.md health | no | no | no | truncation risk, stale entries, duplicates |
| Methodology-agnostic | yes | yes | no (Second Brain) | yes — works for any workflow |
| Runs inside Claude Code | no | yes (only) | yes (MCP) | yes — skill + MCP, with richer diagnostics |
| Runs outside Claude Code | yes | no | yes | yes — standalone CLI |
| CI integration | yes | no | no | yes — exit codes, JSON output |
| Score + verbose + auto-fix | score only | no score | score | all three, flutter doctor style |

## The model

flutter doctor. Categorized sections with pass/warn/fail. Verbose mode with sub-checks. Actionable fix commands. Summary score. Works for beginners and power users.

## Environment-aware diagnostics

When running inside Claude Code (as skill or MCP server):
- Can probe live MCP server connections, not just config files
- Can read conversation history for behavioral analysis
- Can check active process memory/CPU in real time
- Can see which tools are actually being called vs just configured
- Can offer to fix issues directly in the session

When running outside (CLI):
- Full static analysis: config, permissions, disk, security, CLAUDE.md quality
- CI-friendly: exit codes, JSON output, badge generation
- No Claude Code session required

Same check catalog. Richer results when it has more context.

## Distribution

- `pip install claudoctor` — standalone CLI
- MCP server — runs inside any Claude Code session
- Claude Code skill — `/doctor` with full session awareness
- CI action — GitHub Actions, pre-commit hook
