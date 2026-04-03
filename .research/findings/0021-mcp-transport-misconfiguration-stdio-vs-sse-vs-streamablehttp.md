---
id: '0021'
title: MCP transport misconfiguration — stdio vs SSE vs StreamableHTTP
status: open
evidence: LOW
sources:
- text: 'mcpcat.io/guides/comparing-stdio-sse-streamablehttp/'
  tier: SECONDARY
created: '2026-04-03'
---

## Claim

Using type: "sse" when server only supports stdio (or vice versa) causes connection refused. SSE is deprecated in favor of StreamableHTTP. Claude Desktop only supports stdio natively. Claudoctor should: validate transport type matches server capability, flag deprecated SSE transport, suggest Supergateway for bridging.

## Supporting Evidence

> **Source [SECONDARY]:** mcpcat.io/guides/comparing-stdio-sse-streamablehttp/, retrieved 2026-04-03

## Caveats

None identified yet.
