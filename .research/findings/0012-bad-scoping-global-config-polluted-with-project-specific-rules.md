---
id: '0012'
title: 'Bad scoping — global config polluted with project-specific rules'
status: open
evidence: LOW
sources:
- text: 'code.claude.com/docs/en/settings (primary), datacamp.com best practices,
    code.claude.com/docs/en/env-vars'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Three scoping anti-patterns: (1) global CLAUDE.md stuffed with project-specific rules causing cross-talk between repos, (2) not using .claude/settings.json for per-repo defaults or .claude/settings.local.json for machine-local tweaks, (3) misusing CLAUDE_CONFIG_DIR so multiple personas share tools and auth. Checks: detect project-specific content in global CLAUDE.md, flag missing project-level settings, detect CLAUDE_CONFIG_DIR sharing.

## Supporting Evidence

> **Source [SECONDARY]:** code.claude.com/docs/en/settings (primary), datacamp.com best practices, code.claude.com/docs/en/env-vars, retrieved 2026-04-03

## Caveats

None identified yet.
