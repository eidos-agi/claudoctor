---
id: '0006'
title: Cloud provider flags are a silent failure trap
status: open
evidence: LOW
sources:
- text: mintlify.com Claude Code troubleshooting mirror
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Setting CLAUDE_CODE_USE_BEDROCK or CLAUDE_CODE_USE_VERTEX without valid credentials causes opaque errors. apiKeyHelper scripts that aren't executable or print extra stdout fail silently. Checks: detect cloud env vars and verify matching credentials, check apiKeyHelper executability.

## Supporting Evidence

> **Source [SECONDARY]:** mintlify.com Claude Code troubleshooting mirror, retrieved 2026-04-03

## Caveats

None identified yet.
