---
id: "GUARD-001"
type: "guardrail"
title: "Never modify user files without explicit consent"
status: "active"
date: "2026-04-03"
---

Claudoctor is read-only by default. Auto-fix must be opt-in (--fix flag). Never write to CLAUDE.md, settings.json, permissions, or any user file unless the user explicitly asks. Diagnostic tools that silently modify state destroy trust.
