"""Process checks — orphans, memory usage, session health."""

from __future__ import annotations

import subprocess

from claudoctor.engine import Check
from claudoctor.models import Finding


class ProcessChecks(Check):
    section = "Processes"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_orphaned_processes())
        findings.append(self._check_claude_memory())
        return findings

    def _check_orphaned_processes(self) -> Finding:
        try:
            # Find claude-related processes
            result = subprocess.run(
                ["ps", "aux"], capture_output=True, text=True, timeout=5,
            )
            lines = result.stdout.split("\n")
            claude_procs = []
            for line in lines:
                if any(term in line.lower() for term in ["claude", "mcp-server", "mcp_server"]):
                    if "grep" not in line and "claudoctor" not in line:
                        claude_procs.append(line.strip())

            if len(claude_procs) > 20:
                return self.warn(
                    "PROC-001",
                    f"Found {len(claude_procs)} Claude-related processes",
                    detail="May include orphaned MCP servers or subagents from crashed sessions\n"
                           + "\n".join(claude_procs[:10]),
                    fix_description="Review and kill orphaned processes",
                )

            return self.passed(
                "PROC-001",
                f"Claude-related processes",
                value=f"{len(claude_procs)} found",
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return self.passed("PROC-001", "Could not check processes")

    def _check_claude_memory(self) -> Finding:
        try:
            # Get RSS of claude processes
            result = subprocess.run(
                ["ps", "-eo", "rss,comm"],
                capture_output=True, text=True, timeout=5,
            )
            total_rss_kb = 0
            for line in result.stdout.split("\n"):
                if "claude" in line.lower() and "claudoctor" not in line.lower():
                    parts = line.strip().split()
                    if parts and parts[0].isdigit():
                        total_rss_kb += int(parts[0])

            if total_rss_kb == 0:
                return self.passed("PROC-002", "No Claude Code processes running")

            total_mb = total_rss_kb / 1024
            total_gb = total_mb / 1024

            if total_gb > 2:
                return self.warn(
                    "PROC-002",
                    f"Claude Code processes using {total_gb:.1f} GB RAM",
                    detail="Memory leaks in long sessions can grow to 23+ GB",
                    fix_description="Restart Claude Code to reclaim memory",
                )

            return self.passed(
                "PROC-002",
                f"Claude Code memory usage OK",
                value=f"{total_mb:.0f} MB",
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return self.passed("PROC-002", "Could not check process memory")
