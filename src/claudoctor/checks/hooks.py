"""Hooks checks — executability, timeouts, latency, dry-run."""

from __future__ import annotations

import json
import os
import stat

from claudoctor.engine import Check
from claudoctor.models import Finding

BROAD_MATCHERS = ["Edit:*", "Edit", "Write:*", "Write", "Bash:*", "Bash"]


class HooksChecks(Check):
    section = "Hooks"

    def run(self) -> list[Finding]:
        findings = []
        hooks = self._load_hooks()

        if hooks is None:
            findings.append(self.passed("HOOKS-000", "No hooks configured"))
            return findings

        for hook_config in hooks:
            findings.extend(self._check_hook(hook_config))

        if not findings:
            findings.append(self.passed("HOOKS-000", "No hooks to check"))

        return findings

    def _load_hooks(self) -> list[dict] | None:
        paths = [
            ".claude/settings.json",
            ".claude/settings.local.json",
            os.path.expanduser("~/.claude/settings.json"),
        ]

        all_hooks = []
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        data = json.load(f)
                    hooks = data.get("hooks", {})
                    for event_name, hook_list in hooks.items():
                        if isinstance(hook_list, list):
                            for hook in hook_list:
                                hook["_event"] = event_name
                                hook["_source"] = path
                                all_hooks.append(hook)
                except (json.JSONDecodeError, OSError, AttributeError):
                    pass

        return all_hooks if all_hooks else None

    def _check_hook(self, hook: dict) -> list[Finding]:
        findings = []
        event = hook.get("_event", "unknown")
        command = hook.get("command", "")
        timeout = hook.get("timeout")
        matcher = hook.get("matcher", "")

        hook_label = f"[{event}] {command[:40]}"

        # Check command script exists and is executable
        if command:
            script_path = command.split()[0]
            if os.path.exists(script_path):
                mode = os.stat(script_path).st_mode
                if not (mode & stat.S_IXUSR):
                    findings.append(self.error(
                        "HOOKS-001",
                        f"{hook_label} — script not executable",
                        fix_command=f"chmod +x {script_path}",
                    ))

                # Check for symlinks
                if os.path.islink(script_path):
                    findings.append(self.warn(
                        "HOOKS-002",
                        f"{hook_label} — uses symlinked script",
                        detail="Symlinked hook paths can silently fail",
                        fix_description="Use real paths instead of symlinks",
                    ))

        # Check timeout
        if timeout is None:
            findings.append(self.warn(
                "HOOKS-003",
                f"{hook_label} — no explicit timeout (default: 10 minutes)",
                fix_description="Add \"timeout\": <ms> to prevent hung hooks from blocking",
            ))

        # SessionStart hooks should be fast
        if event == "SessionStart":
            if not hook.get("async", False):
                findings.append(self.warn(
                    "HOOKS-004",
                    f"{hook_label} — SessionStart hook is synchronous",
                    detail="Slow SessionStart hooks block Claude Code init",
                    fix_description="Set \"async\": true or keep under 1 second",
                ))

        # PostToolUse with broad matchers
        if event == "PostToolUse" and matcher in BROAD_MATCHERS:
            findings.append(self.warn(
                "HOOKS-005",
                f"{hook_label} — PostToolUse with broad matcher '{matcher}'",
                detail="This hook fires on every edit — keep under 200ms or narrow the matcher",
                fix_description="Use specific matchers like 'Edit:*.py' instead of 'Edit:*'",
            ))

        return findings
