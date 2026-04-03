---
id: '0020'
title: MCP security — malicious .mcp.json enables RCE and token exfiltration
status: open
evidence: LOW
sources:
- text: 'research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Malicious .mcp.json in cloned repos can achieve RCE and API token exfiltration (CVE-2025-59536, CVE-2026-21852). Project-scoped .mcp.json in untrusted repos is a real attack vector. Claudoctor should: warn on project-scoped .mcp.json in repos not owned by user, flag servers requesting broad filesystem access, detect suspicious command patterns.

## Supporting Evidence

> **Source [SECONDARY]:** research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/, retrieved 2026-04-03

## Caveats

None identified yet.
