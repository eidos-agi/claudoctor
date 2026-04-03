---
id: "ADR-001"
type: "decision"
title: "CLI-first: pip install is the product, MCP/skill is future-if-earned"
status: "accepted"
date: "2026-04-03"
relates_to: ["GOAL-001", "GOAL-004"]
source_research_id: "8a9ac5e0-83c1-4759-bcd2-7825b3ff456d"
---

## Context

claudoctor could ship as CLI, MCP server, Claude Code skill, or all three. The temptation is to build the in-session experience first because it has richer context (live MCP connections, token usage, conversation history).

## Decision

CLI is the primary product. `pip install claudoctor && claudoctor` — done.

MCP server and Claude Code skill are future enhancements, only if adoption demands them.

## Rationale

1. **Zero friction** — no config needed to diagnose your config
2. **Runs anywhere** — CI, pre-commit, cron, other people's machines. Not trapped inside a session
3. **Different audience** — cc-health-check is npm; pip install reaches Python users (huge Claude Code segment)
4. **Runtime checks still work from CLI** — can spawn MCP servers to test them, check processes, measure disk without being inside Claude Code
5. **Trust** — a diagnostic tool requiring MCP server install before it can tell you your MCP servers are broken is a bad joke

## Consequences

- Ship CLI first, make it the best
- No MCP server code in v1
- No skill code in v1
- All checks must work from outside a Claude Code session
- In-session enhancements are a separate milestone, gated on adoption
