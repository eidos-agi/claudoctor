---
id: TASK-0008
title: 'Decide: Python CLI vs Node CLI vs shell script'
status: Done
created: '2026-04-03'
priority: high
milestone: MS-0001
tags:
  - research
  - design
visionlog_goal_id: GOAL-004
updated: '2026-04-03'
---
Claude Code users have Node (it's an npm package). They may or may not have Python. Shell scripts are universal but limited. Research the trade-offs and decide on the implementation language. Consider: target audience, dependencies, distribution (PyPI vs npm vs homebrew).

Decision: Python CLI. `pip install claudoctor`. Rationale: cc-health-check already owns npm, Python reaches a different audience, pip is natural for the eidos-agi ecosystem (resume-resume, apple-a-day, claude-session-commons all on PyPI). Recorded as ADR-001.
