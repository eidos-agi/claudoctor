---
id: '0025'
title: 'Skills broken — subdirectory format, name collisions, truncated descriptions'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #42158, #34144, #41898'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Four skills problems: (1) subdirectory commands under commands/ not discovered in v2.1.89+ (#42158) — must use .claude/skills/name/SKILL.md, (2) custom CLAUDE_CONFIG_DIR causes "Unknown skill" (#34144), (3) user vs project skill name collisions — project wins (#41898), (4) too many skills truncate descriptions — set SLASH_COMMAND_TOOL_CHAR_BUDGET higher. Claudoctor should: verify skills use correct directory structure, detect name collisions, count total skills and warn on description budget.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #42158, #34144, #41898, retrieved 2026-04-03

## Caveats

None identified yet.
