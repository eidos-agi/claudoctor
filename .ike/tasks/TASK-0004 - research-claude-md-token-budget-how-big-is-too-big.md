---
id: TASK-0004
title: Research CLAUDE.md token budget — how big is too big?
status: Done
created: '2026-04-03'
priority: medium
milestone: MS-0001
tags:
  - research
visionlog_goal_id: GOAL-002
updated: '2026-04-03'
---
CLAUDE.md content is injected into every conversation context. Research: what's the actual token overhead? At what size does it degrade response quality? How does global + project CLAUDE.md stack? What's a reasonable budget recommendation?

Completed via findings F4, F7, F16. Token budgets: CLAUDE.md global <4K, project <8K suggested. MCP servers ~5K tokens each for tool schemas. 20+ servers = 40-60K tokens consumed before user types. Combined context load (CLAUDE.md + skills + MCP) should be tracked. See findings 0004, 0007, 0016.
