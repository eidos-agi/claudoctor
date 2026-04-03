---
id: 0028
title: 'Flutter doctor is the gold standard — categorized, 3-state, verbose, actionable'
status: open
evidence: LOW
sources:
- text: 'codecademy.com flutter doctor article, docs.npmjs.com/cli/v11/commands/npm-doctor,
    codeepsilon.com flutter doctor overview'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Flutter doctor pattern: categorized sections (SDK, toolchain, IDE, devices, network), three-state icons (pass/warn/fail), verbose mode (-v) with sub-checks, actionable fix commands per failure, one-line summary at top. Brew doctor is warnings-only. npm doctor uses table format (check/value/recommendation). cc-health-check adds score (0-100) + JSON + fix commands. Claudoctor should model after flutter doctor -v: sections, severity icons, verbose mode, fix commands, summary score.

## Supporting Evidence

> **Source [SECONDARY]:** codecademy.com flutter doctor article, docs.npmjs.com/cli/v11/commands/npm-doctor, codeepsilon.com flutter doctor overview, retrieved 2026-04-03

## Caveats

None identified yet.
