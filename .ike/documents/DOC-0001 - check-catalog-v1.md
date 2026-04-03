---
id: DOC-0001
title: Check Catalog v1
created: '2026-04-03'
tags:
  - design
  - catalog
---
# claudoctor Check Catalog v1

Synthesized from 37 research findings. 12 sections, 60+ checks.
Each check: ID, what it detects, severity, static/runtime, auto-fix available.

Severity: ERROR (broken, must fix), WARN (degraded, should fix), INFO (suggestion).

---

## Section 1: Installation [INSTALL]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| INSTALL-001 | Claude Code binary on PATH | ERROR | static | suggest PATH fix |
| INSTALL-002 | Claude Code version (outdated?) | WARN | static | `npm update -g @anthropic-ai/claude-code` |
| INSTALL-003 | Node.js version (known-bad versions cause jank) | WARN | static | suggest nvm use 20 |
| INSTALL-004 | npm global permission issues (EACCES) | ERROR | static | suggest npx or fix permissions |
| INSTALL-005 | Multiple Claude Code installations conflict | ERROR | static | show paths, suggest cleanup |
| INSTALL-006 | Built-in /doctor passes | INFO | runtime | run `claude doctor` and relay results |

Source: F1, F8, F26

---

## Section 2: Authentication [AUTH]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| AUTH-001 | ANTHROPIC_API_KEY exported (not just set) | ERROR | static | suggest `export` in shell profile |
| AUTH-002 | API key actually works (test call) | ERROR | runtime | - |
| AUTH-003 | OAuth token valid (not expired) | WARN | runtime | suggest re-auth |
| AUTH-004 | Cloud provider flags (BEDROCK/VERTEX) have matching credentials | ERROR | static | list missing env vars |
| AUTH-005 | apiKeyHelper script is executable and prints only key to stdout | ERROR | static | `chmod +x` + test stdout |

Source: F1, F6

---

## Section 3: Project Root [PROJECT]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| PROJECT-001 | cwd is a git repo root (not a subdirectory) | WARN | static | suggest correct directory |
| PROJECT-002 | CLAUDE.md exists in project root | WARN | static | suggest `claude init` |
| PROJECT-003 | .claudeignore exists | WARN | static | generate from template |
| PROJECT-004 | .claudeignore covers node_modules/, dist/, build/, .venv/, *.lock | WARN | static | append missing patterns |
| PROJECT-005 | No read-only files in common edit targets (src/, lib/) | WARN | static | flag specific files |
| PROJECT-006 | Nested project detection (multiple CLAUDE.md in tree) | INFO | static | show hierarchy |

Source: F2, F24

---

## Section 4: Settings [SETTINGS]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| SETTINGS-001 | ~/.claude/settings.json exists and is valid JSON | ERROR | static | fix syntax or create |
| SETTINGS-002 | .claude/settings.json exists (project scope) | INFO | static | suggest creation |
| SETTINGS-003 | .claude/settings.local.json in .gitignore | WARN | static | append to .gitignore |
| SETTINGS-004 | No unknown/deprecated keys in settings | WARN | static | list unknown keys |
| SETTINGS-005 | Settings not empty (user has actually configured something) | INFO | static | suggest baseline |
| SETTINGS-006 | No stale experimental overrides (model, limits, disabled tools) | WARN | static | flag overrides older than 30 days |
| SETTINGS-007 | CLAUDE_CONFIG_DIR not shared across personas | WARN | static | flag if set |

Source: F3, F12, F14, F15

---

## Section 5: Permissions [PERMS]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| PERMS-001 | No wildcard allowedTools in global scope (Bash(*), Write) | ERROR | static | suggest scoped patterns |
| PERMS-002 | --dangerously-skip-permissions not in aliases/shell history | WARN | static | flag usage |
| PERMS-003 | Project-level permissions tighter than global | INFO | static | compare and suggest |
| PERMS-004 | Approval fatigue estimate (tools requiring manual approval per session) | INFO | runtime | suggest allowedTools additions |

Source: F6, F11

---

## Section 6: CLAUDE.md Quality [CLAUDEMD]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| CLAUDEMD-001 | Global CLAUDE.md token count (budget: suggest <4K tokens) | WARN | static | show token count, suggest trimming |
| CLAUDEMD-002 | Project CLAUDE.md token count (budget: suggest <8K tokens) | WARN | static | show token count |
| CLAUDEMD-003 | Combined context load (global + project + skills) | WARN | static | show total, breakdown |
| CLAUDEMD-004 | Missing core ops config (build, test, lint, dev server commands) | WARN | static | suggest section |
| CLAUDEMD-005 | Duplicated config (package.json, tsconfig, eslint rules in CLAUDE.md) | WARN | static | flag duplicates |
| CLAUDEMD-006 | Scope confusion (project-specific rules in global CLAUDE.md) | WARN | static | suggest moving to project |
| CLAUDEMD-007 | Content that should be skills (long workflows, policies) | INFO | static | suggest skill extraction |
| CLAUDEMD-008 | Stale/outdated references (old file paths, removed functions) | WARN | runtime | cross-reference with codebase |

Source: F4, F5, F12

---

## Section 7: Skills [SKILLS]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| SKILLS-001 | .claude/skills/ uses correct structure (name/skill.md) | ERROR | static | show expected format |
| SKILLS-002 | No name collisions between user and project skills | WARN | static | list collisions |
| SKILLS-003 | Skill count vs SLASH_COMMAND_TOOL_CHAR_BUDGET | WARN | static | suggest env var increase |
| SKILLS-004 | Broken import paths in skills (@docs/foo.md) | ERROR | static | validate each path |
| SKILLS-005 | Skills total token budget reasonable | INFO | static | estimate total |

Source: F5, F25

---

## Section 8: MCP Servers [MCP]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| MCP-001 | .mcp.json is valid JSON | ERROR | static | fix syntax |
| MCP-002 | MCP config not in wrong file (settings.json, .claude.json) | WARN | static | suggest moving |
| MCP-003 | All server command binaries exist on PATH | ERROR | static | flag missing binaries |
| MCP-004 | All referenced script files exist | ERROR | static | flag missing files |
| MCP-005 | No hardcoded /Users/name/ paths (portability) | WARN | static | flag paths |
| MCP-006 | Required env vars for each server are set | ERROR | static | list missing vars |
| MCP-007 | Server count and estimated token overhead | WARN | static | count × ~5K tokens |
| MCP-008 | Transport type matches server capability | WARN | static | flag mismatches |
| MCP-009 | No deprecated SSE transport (use StreamableHTTP) | INFO | static | suggest upgrade |
| MCP-010 | Each server responds to ping (liveness) | ERROR | runtime | flag dead servers |
| MCP-011 | Server startup time (latency) | WARN | runtime | flag slow servers (>5s) |
| MCP-012 | No zombie MCP processes (PPID=1 orphans) | WARN | runtime | offer to kill |
| MCP-013 | Project .mcp.json security audit (untrusted repos) | ERROR | static | warn on suspicious commands |
| MCP-014 | Unused servers (configured but never called) | INFO | runtime | suggest disabling |

Source: F16-F21

---

## Section 9: Hooks [HOOKS]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| HOOKS-001 | Hook scripts exist and are executable (chmod +x) | ERROR | static | `chmod +x` |
| HOOKS-002 | No symlinked hook paths | WARN | static | flag symlinks |
| HOOKS-003 | Every hook has explicit timeout set | WARN | static | suggest timeout values |
| HOOKS-004 | SessionStart hooks are fast (<1s) or async | WARN | static/runtime | flag slow hooks |
| HOOKS-005 | PostToolUse hooks on broad matchers are fast (<200ms) | WARN | runtime | suggest narrower matchers |
| HOOKS-006 | No test suites on PostToolUse (move to commit hook) | WARN | static | suggest PreToolUse on git commit |
| HOOKS-007 | WorktreeCreate hooks output only path to stdout | WARN | static | flag extra stdout |
| HOOKS-008 | Hook actually executes successfully (dry run) | ERROR | runtime | show error output |

Source: F22, F23

---

## Section 10: Memory [MEMORY]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| MEMORY-001 | Global MEMORY.md line count (<200 lines) | WARN | static | show count, flag if >180 |
| MEMORY-002 | Project MEMORY.md line count (<200 lines) | WARN | static | show count |
| MEMORY-003 | Stale entries (relative timestamps, old dates) | INFO | static | flag candidates |
| MEMORY-004 | Duplicate or contradictory entries | INFO | static | flag candidates |
| MEMORY-005 | Memory files referenced in MEMORY.md actually exist | ERROR | static | flag broken links |
| MEMORY-006 | Orphaned memory files (exist but not in MEMORY.md) | INFO | static | list orphans |

Source: F34

---

## Section 11: Disk & Logs [DISK]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| DISK-001 | Total ~/.claude/ size | INFO | static | show breakdown |
| DISK-002 | projects/ directory size and session count | WARN if >2GB | static | suggest cleanup |
| DISK-003 | resume-summaries/ file count | WARN if >10K | static | suggest pruning old |
| DISK-004 | session-cache/ file count | WARN if >10K | static | suggest pruning old |
| DISK-005 | daemon-stderr.log size (no rotation) | WARN if >100MB | static | suggest truncation |
| DISK-006 | bookmarks/ orphaned files (no matching session) | INFO | static | list orphans |
| DISK-007 | telemetry/ size | INFO | static | show size |
| DISK-008 | Large session JSONL files (>100MB) | ERROR | static | flag specific files |

Source: F33

---

## Section 12: Processes [PROC]

| ID | Check | Severity | Mode | Auto-fix |
|----|-------|----------|------|----------|
| PROC-001 | Orphaned claude/node processes (PPID=1) | WARN | runtime | offer to kill |
| PROC-002 | Current Claude Code process RSS (memory usage) | WARN if >2GB | runtime | suggest restart |
| PROC-003 | Claude Code process uptime (long sessions degrade) | INFO | runtime | suggest restart if >4h |
| PROC-004 | Zombie child processes | WARN | runtime | offer to kill |

Source: F35, F36

---

## Output Design

### Summary (default)
```
claudoctor v0.1.0

[✓] Installation ............. 6/6 passed
[✓] Authentication ........... 5/5 passed
[!] Project Root ............. 4/6 passed (2 warnings)
[✓] Settings ................. 7/7 passed
[✗] Permissions .............. 3/4 passed (1 error)
[!] CLAUDE.md Quality ........ 6/8 passed (2 warnings)
[✓] Skills ................... 5/5 passed
[✗] MCP Servers .............. 11/14 passed (2 errors, 1 warning)
[✓] Hooks .................... 8/8 passed
[!] Memory ................... 5/6 passed (1 warning)
[!] Disk & Logs .............. 6/8 passed (2 warnings)
[✓] Processes ................ 4/4 passed

Score: 82/100 | 2 errors, 6 warnings | Run `claudoctor -v` for details
```

### Verbose (-v)
Expand each section with sub-checks, values found, and fix commands.

### JSON (--json)
Machine-readable output for CI integration. Exit code 1 if any ERROR.

### Fix (--fix)
Apply safe, reversible auto-fixes. Confirm before each change.

---

## Distribution Priority

**CLI first.** `pip install claudoctor && claudoctor` — that's the product.

No MCP server to configure, no skill to install, no dependencies to manage. One command, full diagnostic. This is what ships first and what most users will use.

Future (only if earned):
- MCP server mode — for in-session diagnostics, programmatic access
- Claude Code skill — for conversational fix-it-for-me flow
- These are enhancements, not the core product
