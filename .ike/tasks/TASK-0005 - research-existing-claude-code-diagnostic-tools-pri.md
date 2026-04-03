---
id: TASK-0005
title: Research existing Claude Code diagnostic tools / prior art
status: Done
created: '2026-04-03'
priority: high
milestone: MS-0001
tags:
  - research
updated: '2026-04-03'
---
Search GitHub, npm, PyPI for any existing Claude Code diagnostic or health-check tools. Also check: does Claude Code have a built-in /doctor command? What do similar tools do for other AI coding assistants (Cursor, Copilot, Aider)?

Completed via findings F26-F32, F37. Built-in /doctor exists (installation only). Three competitors: cc-health-check (20 checks, npm), Waza /health (6-layer skill, 648 stars), second-brain-health-check (45 checks, opinionated). Flutter doctor is gold standard. claudoctor beats all by being comprehensive + runtime + CLI-first. See findings 0026-0032, 0037.
