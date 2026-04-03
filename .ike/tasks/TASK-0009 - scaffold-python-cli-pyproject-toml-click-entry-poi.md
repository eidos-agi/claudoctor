---
id: TASK-0009
title: Scaffold Python CLI — pyproject.toml, click, entry point
status: In Progress
created: '2026-04-03'
priority: high
milestone: MS-0002
tags:
  - build
definition-of-done:
  - pyproject.toml with claudoctor entry point
  - click CLI with -v, --json, --fix flags
  - pip install -e . works
  - claudoctor prints version and exits
visionlog_goal_id: GOAL-001
updated: '2026-04-03'
---
Set up the Python package: pyproject.toml, src/claudoctor/, click CLI with `claudoctor` entry point, `claudoctor -v` verbose flag, `--json` output flag, `--fix` flag. Zero external deps beyond click. Follow eidos-agi PyPI patterns (trusted publisher, GitHub Actions).
