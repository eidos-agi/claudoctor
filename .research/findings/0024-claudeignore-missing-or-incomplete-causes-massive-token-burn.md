---
id: '0024'
title: .claudeignore missing or incomplete causes massive token burn
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #79, #187'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Missing .claudeignore entirely causes massive token burn scanning node_modules, .venv, dist (#79, #187). Lock files (package-lock.json) eat thousands of tokens. Deny Read rules are incomplete — .claudeignore is the only reliable exclusion since Bash grep bypasses deny rules. Minimum .claudeignore should cover: node_modules/, dist/, .next/, build/, __pycache__/, *.lock. Claudoctor should: check .claudeignore exists, verify key exclusions present, estimate token savings.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #79, #187, retrieved 2026-04-03

## Caveats

None identified yet.
