---
id: TASK-0007
title: Define severity model and output format
status: Done
created: '2026-04-03'
priority: medium
milestone: MS-0001
tags:
  - research
  - design
visionlog_goal_id: GOAL-001
updated: '2026-04-03'
---
Decide on severity levels (info/warn/error? low/medium/high/critical?), output format (plain text, JSON, markdown?), and report structure. Look at how eslint, shellcheck, hadolint structure their output for inspiration.

Completed via findings F28 and Check Catalog DOC-0001. Flutter doctor model: 3-state (pass/warn/fail), categorized sections, verbose mode, actionable fix commands, summary score. 12 sections, 60+ checks defined. See DOC-0001.
