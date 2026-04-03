---
id: TASK-0003
title: Research MCP server health detection — how to probe if a server is alive
status: Done
created: '2026-04-03'
priority: high
milestone: MS-0001
tags:
  - research
visionlog_goal_id: GOAL-002
updated: '2026-04-03'
---
MCP servers defined in .mcp.json may be dead, misconfigured, or unreachable. Research how to detect: process not running, socket not listening, server returning errors, stale config pointing to moved binaries. Look at how Claude Code itself discovers MCP failures.

Completed via findings F16-F21. MCP probing: spawn server with timeout, check binary exists, validate env vars, detect zombies (PPID=1), flag deprecated SSE transport, security audit for .mcp.json RCE (CVE-2025-59536). See findings 0016-0021.
