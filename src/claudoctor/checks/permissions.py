"""Permissions checks — allowedTools, dangerous flags."""

from __future__ import annotations

import json
import os

from claudoctor.engine import Check
from claudoctor.models import Finding

# Patterns that are too broad for global scope
DANGEROUS_PATTERNS = [
    "Bash(*)",
    "Bash",
    "Write(*)",
    "Write",
    "Edit(*)",
    "Edit",
]


class PermissionsChecks(Check):
    section = "Permissions"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_wildcard_tools())
        findings.append(self._check_skip_permissions())
        return findings

    def _check_wildcard_tools(self) -> Finding:
        path = os.path.expanduser("~/.claude/settings.json")
        if not os.path.exists(path):
            return self.passed("PERMS-001", "No global settings (no wildcard risk)")

        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return self.passed("PERMS-001", "Could not read global settings")

        allowed = data.get("allowedTools", [])
        if not allowed:
            return self.passed("PERMS-001", "No allowedTools in global settings")

        dangerous = [t for t in allowed if t in DANGEROUS_PATTERNS]
        if dangerous:
            return self.error(
                "PERMS-001",
                f"Overly broad allowedTools in global scope: {', '.join(dangerous)}",
                detail="Every project inherits these — one prompt injection away from destructive commands",
                fix_description="Move broad permissions to project-level settings, use specific patterns",
            )

        return self.passed(
            "PERMS-001",
            "Global allowedTools look reasonable",
            value=f"{len(allowed)} tools",
        )

    def _check_skip_permissions(self) -> Finding:
        # Check shell history for --dangerously-skip-permissions
        history_files = [
            os.path.expanduser("~/.zsh_history"),
            os.path.expanduser("~/.bash_history"),
        ]

        for hist in history_files:
            if os.path.exists(hist):
                try:
                    with open(hist, errors="replace") as f:
                        # Read last 1000 lines only
                        lines = f.readlines()[-1000:]
                    skip_count = sum(
                        1 for line in lines
                        if "dangerously-skip-permissions" in line
                    )
                    if skip_count > 5:
                        return self.warn(
                            "PERMS-002",
                            f"--dangerously-skip-permissions used {skip_count} times in recent history",
                            detail="If you're using this routinely, configure allowedTools instead",
                            fix_description="Set up proper allowedTools in project settings",
                        )
                except (OSError, UnicodeDecodeError):
                    pass

        # Check aliases
        shell_configs = [
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.bash_aliases"),
        ]
        for config in shell_configs:
            if os.path.exists(config):
                try:
                    with open(config) as f:
                        content = f.read()
                    if "dangerously-skip-permissions" in content:
                        return self.error(
                            "PERMS-002",
                            f"--dangerously-skip-permissions found in {config}",
                            detail="This flag should never be aliased or defaulted",
                        )
                except OSError:
                    pass

        return self.passed("PERMS-002", "No routine use of --dangerously-skip-permissions")
