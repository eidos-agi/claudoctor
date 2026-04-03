---
id: TASK-0006
title: Research permissions.allow patterns — what approval fatigue looks like
status: Done
created: '2026-04-03'
priority: medium
milestone: MS-0001
tags:
  - research
visionlog_goal_id: GOAL-002
updated: '2026-04-03'
---
Survey common permission configurations. What tools do power users auto-allow? What's the cost of not having permissions.allow set up? Quantify: how many extra approvals per session for a bare config vs a tuned one?

Completed via findings F11, F15. Wildcard allowedTools (Bash(*), Write) in global scope is the main anti-pattern. --dangerously-skip-permissions used as default. Good baseline: three-tier settings hierarchy with tighter project scope. See findings 0011, 0015.
