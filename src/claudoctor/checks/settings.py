"""Settings checks — JSON validity, hierarchy, stale overrides."""

from __future__ import annotations

import json
import os

from claudoctor.engine import Check
from claudoctor.models import Finding


class SettingsChecks(Check):
    section = "Settings"

    def run(self) -> list[Finding]:
        findings = []
        findings.append(self._check_global_settings())
        findings.append(self._check_project_settings())
        findings.append(self._check_local_gitignore())
        findings.append(self._check_config_dir())
        return findings

    def _check_global_settings(self) -> Finding:
        path = os.path.expanduser("~/.claude/settings.json")
        if not os.path.exists(path):
            return self.passed("SETTINGS-001", "No global settings.json (using defaults)")

        try:
            with open(path) as f:
                content = f.read()
            if not content.strip():
                return self.warn(
                    "SETTINGS-005",
                    "Global settings.json exists but is empty",
                    detail="You're running on pure defaults — consider configuring allowedTools, model preferences",
                )
            json.loads(content)
            return self.passed("SETTINGS-001", "Global settings.json is valid JSON", value=path)
        except json.JSONDecodeError as e:
            return self.error(
                "SETTINGS-001",
                f"Global settings.json has invalid JSON: {e}",
                detail=f"File: {path}",
                fix_description="Fix JSON syntax (trailing commas, missing quotes, etc.)",
            )

    def _check_project_settings(self) -> Finding:
        path = ".claude/settings.json"
        if not os.path.exists(path):
            return self.passed(
                "SETTINGS-002",
                "No project settings.json (using global + defaults)",
            )

        try:
            with open(path) as f:
                data = json.load(f)
            return self.passed(
                "SETTINGS-002",
                "Project settings.json found and valid",
                value=f"{len(data)} keys",
            )
        except json.JSONDecodeError as e:
            return self.error(
                "SETTINGS-002",
                f"Project settings.json has invalid JSON: {e}",
            )

    def _check_local_gitignore(self) -> Finding:
        local_settings = ".claude/settings.local.json"
        if not os.path.exists(local_settings):
            return self.passed("SETTINGS-003", "No settings.local.json (nothing to gitignore)")

        # Check if it's in .gitignore
        gitignore_path = ".gitignore"
        if os.path.exists(gitignore_path):
            with open(gitignore_path) as f:
                content = f.read()
            if "settings.local" in content or ".claude/settings.local" in content:
                return self.passed("SETTINGS-003", "settings.local.json is gitignored")

        return self.warn(
            "SETTINGS-003",
            "settings.local.json exists but may not be gitignored",
            detail="Local settings may contain machine-specific paths or secrets",
            fix_command="echo '.claude/settings.local.json' >> .gitignore",
            fix_description="Add settings.local.json to .gitignore",
        )

    def _check_config_dir(self) -> Finding:
        config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
        if not config_dir:
            return self.passed("SETTINGS-007", "No custom CLAUDE_CONFIG_DIR")

        return self.warn(
            "SETTINGS-007",
            f"Custom CLAUDE_CONFIG_DIR set: {config_dir}",
            detail="Ensure this isn't shared across different personas (work/personal/prod/dev)",
        )
