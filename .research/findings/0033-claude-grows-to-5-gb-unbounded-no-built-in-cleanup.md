---
id: '0033'
title: '~/.claude grows to 5+ GB unbounded — no built-in cleanup'
status: open
evidence: LOW
sources:
- text: 'github.com/anthropics/claude-code issues #24207, #21179, #22365, #11963'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

~/.claude can reach 5.6 GB / 160K+ files with no cleanup mechanism. Breakdown: projects/ 3.7 GB (98K session dirs), resume-summaries/ 531 MB (73K files), session-cache/ 501 MB (66K files), daemon-stderr.log 155 MB (single file, no rotation), debug/ 153 MB, telemetry/ 152 MB, file-history/ 100 MB, bookmarks/ 83 MB (21K files), todos/ 25 MB (6.5K files). When disk fills, cascade failure destroys settings/auth (#24207). Verbose command output creates multi-GB session JSONL (#21179, #22365). No built-in cleanup — proposed `claude cleanup` command (#11963) not shipped. Claudoctor should: measure total ~/.claude size, per-directory breakdown, flag files older than N days, warn on disk pressure.

## Supporting Evidence

> **Source [SECONDARY]:** github.com/anthropics/claude-code issues #24207, #21179, #22365, #11963, retrieved 2026-04-03

## Caveats

None identified yet.
