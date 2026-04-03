---
id: "GUARD-003"
type: "guardrail"
title: "No secrets or telemetry"
status: "active"
date: "2026-04-03"
---

Claudoctor reads local config files to diagnose them. It must never transmit, log, or store their contents externally. No phone-home, no analytics, no telemetry. Everything stays local.
