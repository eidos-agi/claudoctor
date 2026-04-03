---
id: TASK-0010
title: Build check engine — runner, registry, finding model, output formatter
status: Done
created: '2026-04-03'
priority: high
milestone: MS-0002
tags:
  - build
definition-of-done:
  - Check base class with run() interface
  - Finding dataclass with severity/message/fix
  - CheckRunner discovers and runs all checks
  - Summary output with section icons
  - Verbose output with sub-check detail
  - JSON output mode
visionlog_goal_id: GOAL-001
updated: '2026-04-03'
---
Core engine: Check base class (id, section, run() -> list[Finding]), Finding model (id, severity, message, fix_command, detail), CheckRunner (discovers checks, runs them, collects findings), OutputFormatter (summary, verbose, JSON modes). Flutter doctor style output with pass/warn/fail icons per section.
